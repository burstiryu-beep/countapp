from datetime import date, datetime, timedelta, timezone
import hashlib
import re

JST = timezone(timedelta(hours=9))

from storage import load_data, save_data
from utils import active_items, make_key, tier


DEFAULT_CATEGORIES = [
    {"id": "gravure", "name": "グラビア", "icon": "📸"},
    {"id": "cosplay", "name": "コスプレ", "icon": "🎭"},
    {"id": "swimsuit", "name": "水着", "icon": "👙"},
    {"id": "uniform", "name": "制服", "icon": "🎀"},
    {"id": "idol", "name": "アイドル", "icon": "✨"},
    {"id": "oneesan", "name": "お姉さん・OL", "icon": "💼"},
    {"id": "jk", "name": "学生系", "icon": "📚"},
    {"id": "married", "name": "人妻・熟女", "icon": "🍷"},
    {"id": "other", "name": "その他", "icon": "💋"},
]


def get_data():
    return load_data()


def _slug_category_id(name):
    raw = re.sub(r"\s+", "_", (name or "").strip())
    raw = re.sub(r"[^\w\-ぁ-んァ-ン一-龥]", "", raw, flags=re.UNICODE)
    base = (raw[:28] or "cat").lower()
    suffix = hashlib.md5(name.encode("utf-8")).hexdigest()[:5]
    return f"{base}_{suffix}"


def ensure_structure(data):
    data.setdefault("items", {})
    data.setdefault("history", [])
    data.setdefault("tabs", [{"id": "all", "name": "全体"}])
    data.setdefault("categories", [])

    tab_ids = {t.get("id") for t in data["tabs"] if isinstance(t, dict)}
    if "all" not in tab_ids:
        data["tabs"].insert(0, {"id": "all", "name": "全体"})

    # 既定カテゴリを不足分だけ足す（ユーザー追加分は残す）
    existing_ids = {
        c.get("id") for c in data["categories"]
        if isinstance(c, dict) and c.get("id")
    }
    for cat in DEFAULT_CATEGORIES:
        if cat["id"] not in existing_ids:
            data["categories"].append(dict(cat))
            existing_ids.add(cat["id"])

    # 壊れたエントリを除去
    data["categories"] = [
        c for c in data["categories"]
        if isinstance(c, dict) and c.get("id") and c.get("name")
    ]

    valid_ids = {c["id"] for c in data["categories"]}
    for v in data["items"].values():
        if not isinstance(v.get("counts"), dict):
            v["counts"] = {}
        if not isinstance(v.get("img"), str):
            v["img"] = ""
        if not v.get("tab"):
            v["tab"] = "all"
        if not isinstance(v.get("weak_tags"), list):
            v["weak_tags"] = []
        if not isinstance(v.get("mirror_note"), str):
            v["mirror_note"] = ""
        cats = v.get("categories")
        if not isinstance(cats, list):
            cats = []
        v["categories"] = [c for c in cats if c in valid_ids]
    return data


def list_categories(data):
    ensure_structure(data)
    return list(data.get("categories") or [])


def category_map(data):
    return {c["id"]: c for c in list_categories(data)}


def category_labels(data, cat_ids):
    cmap = category_map(data)
    out = []
    for cid in cat_ids or []:
        c = cmap.get(cid)
        if c:
            out.append(f"{c.get('icon', '🏷')} {c['name']}")
    return out


def add_category(data, name, icon="🏷"):
    """ユーザー定義カテゴリを追加。戻り値は新id or None。"""
    name = (name or "").strip()
    if not name:
        return None
    ensure_structure(data)
    for c in data["categories"]:
        if c.get("name") == name:
            return c.get("id")
    cid = _slug_category_id(name)
    # 万一衝突したらハッシュを伸ばす
    existing = {c["id"] for c in data["categories"]}
    while cid in existing:
        cid = _slug_category_id(name + cid)
    data["categories"].append({"id": cid, "name": name, "icon": (icon or "🏷")[:2]})
    return cid


def delete_category(data, cat_id):
    """カテゴリ定義を消し、各アイテムからも外す。"""
    ensure_structure(data)
    data["categories"] = [c for c in data["categories"] if c.get("id") != cat_id]
    for v in data["items"].values():
        cats = v.get("categories") or []
        if cat_id in cats:
            v["categories"] = [c for c in cats if c != cat_id]
    return True


def category_defeat_stats(data, month=None):
    """
    カテゴリ別敗北回数。
    アイテムが複数カテゴリを持つ場合はそれぞれに加算（属性ごとの弱さ可視化用）。
    戻り値: [{"id","name","icon","count","item_n","pct"}, ...] 降順
    + uncategorized 件数
    """
    ensure_structure(data)
    cmap = category_map(data)
    tallies = {cid: {"count": 0, "item_n": 0} for cid in cmap}
    uncategorized = 0
    uncat_items = 0
    total_item_defeats = 0

    for v in active_items(data).values():
        counts = v.get("counts") or {}
        if month and month != "all":
            total = int(counts.get(month, 0) or 0)
        else:
            total = int(sum(counts.values()))
        if total <= 0:
            continue
        total_item_defeats += total
        cats = [c for c in (v.get("categories") or []) if c in cmap]
        if not cats:
            uncategorized += total
            uncat_items += 1
            continue
        for cid in cats:
            tallies[cid]["count"] += total
            tallies[cid]["item_n"] += 1

    rows = []
    for cid, c in cmap.items():
        n = tallies[cid]["count"]
        rows.append({
            "id": cid,
            "name": c.get("name", cid),
            "icon": c.get("icon", "🏷"),
            "count": n,
            "item_n": tallies[cid]["item_n"],
            "pct": 0,
        })
    rows.sort(key=lambda r: (-r["count"], r["name"]))

    # 割合は「カテゴリ付き敗北の合計」ではなく、実アイテム敗北合計に対する比率
    # （複数カテゴリ加算があるので合計100%超もあり得る → その場合はカテゴリ合計で正規化）
    cat_sum = sum(r["count"] for r in rows) or 1
    for r in rows:
        r["pct"] = round(r["count"] / cat_sum * 100) if cat_sum else 0

    return {
        "rows": rows,
        "uncategorized": uncategorized,
        "uncategorized_items": uncat_items,
        "total_item_defeats": total_item_defeats,
        "peak": rows[0] if rows and rows[0]["count"] > 0 else None,
    }


def category_tease(peak_name, peak_count, total):
    import random
    if not peak_name or not peak_count:
        return "まだカテゴリ負けの偏りが見えないわ……属性をつけてから、ボコボコにされなさい。"
    base = total or peak_count
    pct = round(peak_count / base * 100) if base else 0
    lines = [
        f"いちばんボコボコにされてるの、「{peak_name}」ね。……{peak_count}回。ちんぽ、正直すぎるわ❤️",
        f"「{peak_name}」に{peak_count}回敗北。属性だけで負け癖、バレバレよ。ふふ。",
        f"グラフ見ただけでビンビンでしょ。「{peak_name}」に弱いの、自分でも分かってるわね。",
        f"「{peak_name}」特化の敗北射精……属性シェア約{pct}%。かわいい属性マゾ。",
        f"また「{peak_name}」に負けに行く気満々ね。偏りを見て興奮してる顔、想像できるわ。",
    ]
    return random.choice(lines)


def render_category_defeat_html(stats, title="🏷 カテゴリ別 敗北マップ"):
    """カテゴリ敗北の横棒ビジュアル HTML。"""
    rows = stats.get("rows") or []
    peaked = stats.get("peak")
    uncat = int(stats.get("uncategorized") or 0)
    total = int(stats.get("total_item_defeats") or 0)
    max_c = max((r["count"] for r in rows), default=0) or 1

    bars = ""
    for i, r in enumerate(rows):
        if r["count"] <= 0 and i > 8:
            continue
        w = int(r["count"] / max_c * 100)
        is_peak = peaked and r["id"] == peaked.get("id") and r["count"] > 0
        border = "border:1px solid #ff4081;" if is_peak else "border:1px solid rgba(194,24,91,0.25);"
        crown = " 👑" if is_peak else ""
        glow = "box-shadow:0 0 12px rgba(255,64,129,0.35);" if is_peak else ""
        bars += (
            f"<div style='margin:0.45em 0;{glow}'>"
            f"<div style='display:flex;justify-content:space-between;align-items:baseline;"
            f"margin-bottom:0.2em;'>"
            f"<span style='color:#ffe0f0;font-weight:700;font-size:0.92em;'>"
            f"{r.get('icon','🏷')} {r['name']}{crown}</span>"
            f"<span style='color:#ff80ab;font-weight:800;font-size:0.9em;'>"
            f"{r['count']} 敗北 · {r['pct']}%</span>"
            f"</div>"
            f"<div style='height:14px;background:rgba(30,0,20,0.7);border-radius:8px;{border}"
            f"overflow:hidden;'>"
            f"<div style='height:100%;width:{w}%;background:linear-gradient(90deg,#c2185b,#ff4081);"
            f"border-radius:8px;'></div>"
            f"</div>"
            f"<div style='color:#804060;font-size:0.72em;margin-top:0.15em;'>"
            f"登録 {r['item_n']} 体がこの属性</div>"
            f"</div>"
        )

    tease = ""
    if peaked and peaked.get("count", 0) > 0:
        tease_txt = category_tease(
            peaked.get("name"),
            peaked.get("count"),
            sum(r["count"] for r in rows) or total,
        )
        tease = (
            f"<div style='color:#ffb6d9;font-style:italic;font-size:0.9em;text-align:center;"
            f"background:rgba(194,24,91,0.15);border:1px solid rgba(255,64,129,0.35);"
            f"border-radius:10px;padding:0.65em 0.8em;margin-top:0.85em;'>"
            f"💬 {tease_txt}</div>"
        )

    uncat_html = ""
    if uncat > 0:
        uncat_html = (
            f"<div style='color:#ff80ab;font-size:0.8em;text-align:center;margin-top:0.7em;'>"
            f"⚠ 未分類の敗北が {uncat} 回あるわ。管理画面で属性つけて……偏り、直視しなさい❤️"
            f"</div>"
        )
    elif total == 0:
        uncat_html = (
            "<div style='color:#804060;font-size:0.85em;text-align:center;margin-top:0.5em;'>"
            "まだ敗北記録がないわ。属性をつけてから、ボコボコにされに行きなさい。"
            "</div>"
        )
    elif all(r["count"] == 0 for r in rows):
        uncat_html = (
            "<div style='color:#ff80ab;font-size:0.85em;text-align:center;margin-top:0.5em;'>"
            "記録はあるのに属性が空よ。管理でカテゴリ付けしたら、弱点マップが疼きはじめるわ。"
            "</div>"
        )

    return (
        f"<div style='background:rgba(15,0,10,0.65);border:1px solid rgba(194,24,91,0.35);"
        f"border-radius:14px;padding:1em 1.1em;margin:0.4em 0 1em;'>"
        f"<div style='color:#ff80ab;font-size:0.95em;font-weight:800;text-align:center;"
        f"letter-spacing:0.06em;margin-bottom:0.75em;'>{title}</div>"
        f"{bars}{tease}{uncat_html}</div>"
    )


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
            "points": 0,
            "weak_tags": [],
            "mirror_note": "",
            "categories": [],
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
