from storage import load_data, save_data
from utils import month, now, make_key, tier, calc_continuous_days


def get_data():
    return load_data()


def ensure_structure(data):
    data.setdefault("items", {})
    data.setdefault("history", [])
    data.setdefault("tabs", [{"id": "all", "name": "全体"}])
    return data


def aggregate(data, tab_id):
    result = {}

    for k, v in data["items"].items():
        if tab_id != "all" and v.get("tab") != tab_id:
            continue
        name = v["name"]
        result[name] = result.get(name, 0) + sum(v.get("counts", {}).values())

    return result


def count_item(data, name, tab):
    key = make_key(name, tab)

    if key not in data["items"]:
        data["items"][key] = {
            "name": name,
            "tab": tab,
            "counts": {},
            "img": "",
            "points": 0
        }

    m = month()
    data["items"][key]["counts"][m] = data["items"][key]["counts"].get(m, 0) + 1

    data["history"].append({
        "name": name,
        "tab": tab,
        "time": now()
    })

    save_data(data)


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


def compute_points(data):
    points = {}

    for k, v in data["items"].items():
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