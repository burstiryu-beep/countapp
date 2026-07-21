from datetime import date, datetime, timedelta, timezone

JST = timezone(timedelta(hours=9))

from storage import load_data, save_data
from utils import active_items, make_key, tier


def get_data():
    return load_data()


def ensure_structure(data):
    data.setdefault("items", {})
    data.setdefault("history", [])
    data.setdefault("tabs", [{"id": "all", "name": "全体"}])

    tab_ids = {t.get("id") for t in data["tabs"] if isinstance(t, dict)}
    if "all" not in tab_ids:
        data["tabs"].insert(0, {"id": "all", "name": "全体"})

    for v in data["items"].values():
        if not isinstance(v.get("counts"), dict):
            v["counts"] = {}
        if not isinstance(v.get("img"), str):
            v["img"] = ""
        if not v.get("tab"):
            v["tab"] = "all"
    return data


def aggregate(data, tab_id, month=None):
    result = {}

    for k, v in active_items(data).items():
        if tab_id != "all" and v.get("tab") != tab_id:
            continue
        name = v["name"]
        counts = v.get("counts", {})
        if month and month != "all":
            total = counts.get(month, 0)
        else:
            total = sum(counts.values())
        result[name] = result.get(name, 0) + total

    return result


def all_months(data):
    months = set()
    for v in active_items(data).values():
        months.update(v.get("counts", {}).keys())
    return sorted(months, reverse=True)


def count_item(data, name, tab, count_date=None):
    if count_date is None or not isinstance(count_date, date):
        count_date = date.today()
    elif isinstance(count_date, str):
        count_date = datetime.strptime(count_date, "%Y-%m-%d").date()
    if isinstance(count_date, datetime):
        count_date = count_date.date()

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
        datetime.now(JST).time()
    ).strftime("%Y-%m-%d %H:%M:%S")

    data["history"].append({
        "name": name,
        "tab": tab,
        "time": time_str
    })

    save_data(data)


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
