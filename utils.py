from datetime import datetime, date, timedelta, timezone
from pathlib import Path

JST = timezone(timedelta(hours=9))


def now():
    return datetime.now(JST).strftime("%Y-%m-%d %H:%M:%S")


def month():
    return datetime.now(JST).strftime("%Y-%m")


def today():
    return datetime.now(JST).strftime("%Y-%m-%d")


def make_key(name, tab):
    return f"{name}@@{tab}"


def all_months(data):
    months = set()
    for v in active_items(data).values():
        months.update(v.get("counts", {}).keys())
    return sorted(months, reverse=True)


def aggregate(data, tab_id, month=None):
    result = {}
    for v in active_items(data).values():
        if tab_id != "all" and v.get("tab") != tab_id:
            continue
        name = v["name"]
        counts = v.get("counts", {})
        if month and month != "all":
            total = counts.get(month, 0)
        else:
            total = sum(counts.values())
        result[name] = total
    return result


def valid_tab_ids(data):
    return {t["id"] for t in data["tabs"]}


def active_items(data):
    tabs = valid_tab_ids(data)
    return {
        k: v for k, v in data["items"].items()
        if v.get("tab") in tabs
    }


def registered_item_count(data):
    return len(active_items(data))


_face_pos_cache: dict = {}


def _face_cache_key(src: str) -> str:
    """巨大な data URI をキャッシュキーにしないための短縮キー。"""
    if not src:
        return ""
    if src.startswith("data:"):
        import hashlib
        return "data:" + hashlib.md5(src.encode("utf-8", errors="ignore")).hexdigest()
    return src


def _load_bgr_image(src: str):
    """ファイルパス / data URI から OpenCV BGR 画像を読む。"""
    import base64
    import numpy as np
    import cv2

    if isinstance(src, str) and src.startswith("data:"):
        try:
            b64 = src.split(",", 1)[1]
            raw = base64.b64decode(b64)
            arr = np.frombuffer(raw, dtype=np.uint8)
            return cv2.imdecode(arr, cv2.IMREAD_COLOR)
        except Exception:
            return None

    p = resolve_img_path(src) if not Path(str(src)).is_file() else Path(str(src))
    if not p:
        return None
    return cv2.imread(str(p))


def detect_face_position(src: str) -> str:
    """顔を検出して CSS object-position を返す。検出失敗時は上部寄り。"""
    cache_key = _face_cache_key(src)
    if cache_key in _face_pos_cache:
        return _face_pos_cache[cache_key]

    # ポートレート想定のデフォルト（中央だと顔が切れやすい）
    default = "center 18%"
    result = default
    try:
        import cv2

        img = _load_bgr_image(src)
        if img is None:
            _face_pos_cache[cache_key] = default
            return default

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)

        min_side = max(24, int(min(w, h) * 0.08))
        faces = []
        for name in (
            "haarcascade_frontalface_default.xml",
            "haarcascade_frontalface_alt2.xml",
            "haarcascade_profileface.xml",
        ):
            cascade = cv2.CascadeClassifier(cv2.data.haarcascades + name)
            if cascade.empty():
                continue
            found = cascade.detectMultiScale(
                gray,
                scaleFactor=1.08,
                minNeighbors=3,
                minSize=(min_side, min_side),
            )
            if len(found):
                faces.extend(found)
                break

        if len(faces):
            fx, fy, fw, fh = max(faces, key=lambda f: f[2] * f[3])
            # 顔の少し上寄りを中心に（額〜目線が映りやすい）
            cx = int((fx + fw / 2) / w * 100)
            cy = int((fy + fh * 0.35) / h * 100)
            cx = max(5, min(95, cx))
            cy = max(5, min(70, cy))
            result = f"{cx}% {cy}%"
    except Exception:
        result = default

    _face_pos_cache[cache_key] = result
    return result


def img_to_html(img_path, style="width:100%;border-radius:12px;margin-bottom:0.6em;", face_detect=True):
    if not img_path:
        return ""

    if img_path.startswith("cloud:"):
        try:
            from firebase_manager import fetch_image
            img_path = fetch_image(img_path)
        except Exception:
            img_path = ""
        if not img_path:
            return ""

    if face_detect and "object-position" not in style:
        pos = detect_face_position(img_path)
        style = style.rstrip(";") + f";object-position:{pos};"

    if img_path.startswith("data:"):
        return f'<img src="{img_path}" style="{style}"/>'

    # ファイルパスの場合（ローカル開発 / 旧形式）
    p = resolve_img_path(img_path)
    if not p:
        return ""
    try:
        import base64
        with open(str(p), "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        ext = str(p).rsplit(".", 1)[-1].lower()
        mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"
        return f'<img src="data:{mime};base64,{b64}" style="{style}"/>'
    except Exception:
        return ""


def resolve_img_path(img_path):
    if not img_path:
        return None

    p = Path(img_path)
    if p.is_file():
        return p

    name = p.name
    for base in (
        Path.cwd(),
        Path.cwd() / "images",
        Path.home() / "countapp_dashboard" / "images",
        Path(__file__).resolve().parent / "images",
        Path(__file__).resolve().parent / ".data" / "images",
    ):
        candidate = base / name if base.name == "images" else base / img_path
        if candidate.is_file():
            return candidate

    return None


def undo_count_from_history(data, entry):
    key = make_key(entry["name"], entry["tab"])
    if key not in data["items"]:
        return

    m = entry["time"][:7]
    counts = data["items"][key]["counts"]
    if m in counts and counts[m] > 0:
        counts[m] -= 1
        if counts[m] == 0:
            del counts[m]


def apply_count_for_date(data, entry, count_date):
    key = make_key(entry["name"], entry["tab"])
    if key not in data["items"]:
        return

    m = count_date.strftime("%Y-%m")
    counts = data["items"][key]["counts"]
    counts[m] = counts.get(m, 0) + 1


def change_history_date(data, index, new_date):
    if index < 0 or index >= len(data["history"]):
        return False

    if isinstance(new_date, str):
        new_date = datetime.strptime(new_date, "%Y-%m-%d").date()

    entry = data["history"][index]
    undo_count_from_history(data, entry)

    old_time = entry["time"]
    old_hms = old_time[11:] if len(old_time) > 10 else datetime.now().strftime("%H:%M:%S")
    entry["time"] = f"{new_date.strftime('%Y-%m-%d')} {old_hms}"

    apply_count_for_date(data, entry, new_date)
    return True


def delete_item(data, name, tab=None):
    keys_to_delete = [
        k for k, v in data["items"].items()
        if v["name"] == name and (tab is None or v.get("tab") == tab)
    ]

    for k in keys_to_delete:
        del data["items"][k]

    data["history"] = [
        h for h in data["history"]
        if not (h["name"] == name and (tab is None or h["tab"] == tab))
    ]


def rename_item(data, old_name, tab, new_name):
    old_key = make_key(old_name, tab)
    if old_key not in data["items"]:
        return False

    new_key = make_key(new_name, tab)
    if new_key in data["items"] and new_key != old_key:
        return False

    item = data["items"].pop(old_key)
    item["name"] = new_name
    data["items"][new_key] = item

    for h in data["history"]:
        if h["name"] == old_name and h["tab"] == tab:
            h["name"] = new_name

    return True


def delete_tab(data, tab_id):
    if tab_id == "all":
        return False

    data["tabs"] = [t for t in data["tabs"] if t["id"] != tab_id]
    data["items"] = {
        k: v for k, v in data["items"].items()
        if v.get("tab") != tab_id
    }
    data["history"] = [h for h in data["history"] if h["tab"] != tab_id]
    return True


def rename_tab_name(data, tab_id, new_name):
    for t in data["tabs"]:
        if t["id"] == tab_id:
            t["name"] = new_name
            return True
    return False


def rename_tab_id(data, old_id, new_id):
    if old_id == "all" or old_id == new_id:
        return False

    if any(t["id"] == new_id for t in data["tabs"]):
        return False

    for t in data["tabs"]:
        if t["id"] == old_id:
            t["id"] = new_id
            break
    else:
        return False

    new_items = {}
    for k, v in data["items"].items():
        if v.get("tab") == old_id:
            v["tab"] = new_id
            new_key = make_key(v["name"], new_id)
            new_items[new_key] = v
        else:
            new_items[k] = v
    data["items"] = new_items

    for h in data["history"]:
        if h["tab"] == old_id:
            h["tab"] = new_id

    return True


def calc_continuous_days(history):
    if not history:
        return 0

    dates = sorted({h["time"][:10] for h in history})
    if not dates:
        return 0

    today_d = date.today()
    count = 0
    current = today_d

    for d in reversed(dates):
        dt = datetime.strptime(d, "%Y-%m-%d").date()
        if dt == current:
            count += 1
            current -= timedelta(days=1)
        elif dt < current:
            break

    return count


def tier(points, rank, n):
    if n == 0:
        return "D"

    if rank == 0:
        return "SS"

    r = rank / n
    if r <= 0.10:
        return "S"
    if r <= 0.30:
        return "A"
    if r <= 0.50:
        return "B"
    if r <= 0.80:
        return "C"
    return "D"
