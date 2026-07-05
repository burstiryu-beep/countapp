from datetime import date, datetime

from storage import load_data, save_data
from utils import make_key, tier


def get_data():
    return load_data()


def ensure_structure(data):
    data.setdefault("items", {})
    data.setdefault("history", [])
    data.setdefault("tabs", [{"id": "all", "name": "全体"}])
    return data


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


def aggregate(data, tab_id):
    result = {}

    for k, v in active_items(data).items():
        if tab_id != "all" and v.get("tab") != tab_id:
            continue
        name = v["name"]
        result[name] = result.get(name, 0) + sum(v.get("counts", {}).values())

    return result


def count_item(data, name, tab, count_date=None):
    if count_date is None:
        count_date = date.today()
    elif isinstance(count_date, str):
        count_date = datetime.strptime(count_date, "%Y-%m-%d").date()

    key = make_key(name, tab)

    if key not in data["items"]:
        data["items"][key] = {
            "name": name,
            "tab": tab,
            "counts": {},
            "img": "",
            "points": 0
        }

    m = count_date.strftime("%Y-%m")
    data["items"][key]["counts"][m] = data["items"][key]["counts"].get(m, 0) + 1

    time_str = datetime.combine(
        count_date,
        datetime.now().time()
    ).strftime("%Y-%m-%d %H:%M:%S")

    data["history"].append({
        "name": name,
        "tab": tab,
        "time": time_str
    })

    save_data(data)


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


def compute_points(data):
    points = {}

    for v in active_items(data).values():
        name = v["name"]
        total = sum(v.get("counts", {}).values())
        points[name] = points.get(name, 0) + total

    sorted_items = sorted(points.items(), key=lambda x: -x[1])
    n = len(sorted_items)

    result = {}
    for i, (name, p) in enumerate(sorted_items):
        result[name] = {
            "points": p,
            "tier": tier(p, i, n)
        }

    return result
