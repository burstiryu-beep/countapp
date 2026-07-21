import copy
import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

try:
    from firebase_manager import load_cloud_data, save_cloud_data
except Exception:
    def load_cloud_data():
        return None

    def save_cloud_data(data):
        return False, "Firebase未接続"


def _init_dirs():
    for base in (Path.home() / "countapp_dashboard", APP_DIR / ".data"):
        try:
            base.mkdir(parents=True, exist_ok=True)
            img_dir = base / "images"
            img_dir.mkdir(exist_ok=True)
            return base, img_dir
        except OSError:
            continue

    base = APP_DIR / ".data"
    base.mkdir(parents=True, exist_ok=True)
    img_dir = base / "images"
    img_dir.mkdir(exist_ok=True)
    return base, img_dir


BASE, IMG_DIR = _init_dirs()
DATA_FILE = BASE / "data.json"


def default_data():
    return {
        "tabs": [{"id": "all", "name": "全体"}],
        "items": {},
        "history": []
    }


def _load_local():
    if not DATA_FILE.exists():
        return None
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def _merge_data(cloud, local):
    if not cloud:
        return local
    if not local:
        return cloud

    merged = copy.deepcopy(cloud)
    merged.setdefault("items", {})
    merged.setdefault("history", [])
    merged.setdefault("tabs", [{"id": "all", "name": "全体"}])

    for key, item in local.get("items", {}).items():
        if key not in merged["items"]:
            merged["items"][key] = item
            continue
        cloud_item = merged["items"][key]
        local_counts = item.get("counts") or {}
        cloud_counts = cloud_item.get("counts") or {}
        for month, count in local_counts.items():
            cloud_counts[month] = max(int(cloud_counts.get(month, 0)), int(count))
        cloud_item["counts"] = cloud_counts
        if item.get("img") and not cloud_item.get("img"):
            cloud_item["img"] = item["img"]
        if item.get("name"):
            cloud_item["name"] = item["name"]

    cloud_hist = {(h.get("name"), h.get("time")) for h in merged.get("history", [])}
    for h in local.get("history", []):
        sig = (h.get("name"), h.get("time"))
        if sig not in cloud_hist:
            merged["history"].append(h)

    return merged


def load_data():
    local = _load_local()
    cloud = load_cloud_data()
    return _merge_data(cloud, local) or cloud or local or default_data()


def save_data(data):
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    return save_cloud_data(data)
