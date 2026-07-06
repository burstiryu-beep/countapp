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
        total = counts.get(month, 0) if (month and month != "all") else sum(counts.values())
        result[name] = result.get(name, 0) + total
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
