from datetime import datetime
import streamlit as st
import style
from core import get_data, ensure_structure, compute_points
from utils import active_items, calc_continuous_days, registered_item_count, img_to_html

style.apply()
data = ensure_structure(get_data())

st.markdown("<h2 style='text-align:center'>📊 射精ダッシュボード</h2>", unsafe_allow_html=True)

items = active_items(data)
total_counts = sum(sum(v.get("counts", {}).values()) for v in items.values())
streak = calc_continuous_days(data["history"])

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("💋 累計敗北回数", total_counts)
with col2:
    st.metric("🌸 登録弱点数", registered_item_count(data))
with col3:
    st.metric("🔥 連続敗北日数", f"{streak} 日")

st.divider()

st.markdown("<h3>🏆 敗北ランキング Top 5</h3>", unsafe_allow_html=True)

ranking = compute_points(data)
sorted_rank = sorted(ranking.items(), key=lambda x: -x[1]["points"])

tier_icon = {"SS": "👑", "S": "🥇", "A": "🥈", "B": "🥉", "C": "💜", "D": "🖤"}

for rank, (name, info) in enumerate(sorted_rank[:5], 1):
    t = info["tier"]
    icon = tier_icon.get(t, "")
    item = next((v for v in data["items"].values() if v["name"] == name), {})
    thumb = img_to_html(
        item.get("img", ""),
        style="width:56px;height:56px;object-fit:cover;border-radius:8px;flex-shrink:0;"
    )
    img_block = f"<div>{thumb}</div>" if thumb else f"<span style='font-size:1.6em;min-width:2em;text-align:center;'>{icon}</span>"
    st.markdown(
        f"<div class='ero-card' style='display:flex;align-items:center;gap:1em;text-align:left;padding:0.6em 1em;'>"
        f"{img_block}"
        f"<span style='flex:1;font-size:1.1em;color:#ffe0f0;font-weight:600;'>#{rank}　{name}</span>"
        f"<span class='tier-{t}' style='margin-right:0.5em;font-size:1.3em;'>{t}</span>"
        f"<span style='color:#ff80ab;font-weight:700;'>{info['points']} 敗北</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.divider()

st.markdown("<h3>📅 月別 敗北回数</h3>", unsafe_allow_html=True)

month_map = {}
for v in items.values():
    for m, c in v.get("counts", {}).items():
        month_map[m] = month_map.get(m, 0) + c

for m, c in sorted(month_map.items(), reverse=True):
    bar_len = min(c * 4, 200)
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:1em;margin:0.3em 0;'>"
        f"<span style='color:#ff80ab;min-width:7em;font-weight:600;'>{m}</span>"
        f"<div style='height:18px;width:{bar_len}px;background:linear-gradient(90deg,#c2185b,#ff4081);border-radius:9px;'></div>"
        f"<span style='color:#ffe0f0;font-weight:700;'>{c} 回</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.divider()

# ===== 時間帯別 & 曜日別分析 =====
time_labels = ["深夜\n(0-4時)", "朝\n(5-10時)", "昼\n(11-16時)", "夜\n(17-23時)"]
time_keys   = ["深夜", "朝", "昼", "夜"]
time_counts = {k: 0 for k in time_keys}
weekday_labels = ["月", "火", "水", "木", "金", "土", "日"]
weekday_counts = {d: 0 for d in weekday_labels}

for h in data["history"]:
    try:
        dt = datetime.strptime(h["time"], "%Y-%m-%d %H:%M:%S")
        hr = dt.hour
        if hr < 5:
            time_counts["深夜"] += 1
        elif hr < 11:
            time_counts["朝"] += 1
        elif hr < 17:
            time_counts["昼"] += 1
        else:
            time_counts["夜"] += 1
        weekday_counts[weekday_labels[dt.weekday()]] += 1
    except Exception:
        pass

time_total = sum(time_counts.values()) or 1
weekday_total = sum(weekday_counts.values()) or 1

peak_time = max(time_counts, key=time_counts.get) if time_total > 1 else None
peak_day  = max(weekday_counts, key=weekday_counts.get) if weekday_total > 1 else None

time_comments = {
    "深夜": "深夜の衝動が一番強いのね……ふふ。",
    "朝":   "朝から溜まってるなんて、かわいい子。",
    "昼":   "昼間っから……我慢できないのね。",
    "夜":   "夜になると弱くなるのね。わかりやすい。",
}

st.markdown("<h3>⏰ 時間帯別 敗北パターン</h3>", unsafe_allow_html=True)

time_icons = {"深夜": "🌙", "朝": "🌅", "昼": "☀️", "夜": "🌆"}
max_time_c = max(time_counts.values()) or 1
time_row = ""
for k in time_keys:
    c = time_counts[k]
    pct = round(c / time_total * 100)
    bar_w = int(c / max_time_c * 140)
    is_peak = (k == peak_time)
    highlight = "background:rgba(194,24,91,0.2);border:1px solid #ff4081;" if is_peak else "background:rgba(30,0,20,0.4);border:1px solid rgba(194,24,91,0.2);"
    peak_mark = " 👑" if is_peak else ""
    time_row += (
        f"<div style='flex:1;{highlight}border-radius:10px;padding:0.6em;text-align:center;'>"
        f"<div style='font-size:1.4em;'>{time_icons[k]}</div>"
        f"<div style='color:#ffb6d9;font-size:0.78em;white-space:pre-line;'>{k}{peak_mark}</div>"
        f"<div style='color:#fff;font-size:1.2em;font-weight:900;'>{c}</div>"
        f"<div style='color:#804060;font-size:0.72em;'>{pct}%</div>"
        f"</div>"
    )
st.markdown(
    f"<div style='display:flex;gap:0.5em;margin-bottom:0.8em;'>{time_row}</div>",
    unsafe_allow_html=True,
)
if peak_time:
    st.markdown(
        f"<div style='color:#ffb6d9;font-style:italic;font-size:0.9em;text-align:center;"
        f"background:rgba(194,24,91,0.1);border-radius:8px;padding:0.5em;margin-bottom:0.8em;'>"
        f"💬 {time_comments[peak_time]}</div>",
        unsafe_allow_html=True,
    )

st.divider()
st.markdown("<h3>📆 曜日別 危険度</h3>", unsafe_allow_html=True)

max_day_c = max(weekday_counts.values()) or 1
day_row = ""
for d in weekday_labels:
    c = weekday_counts[d]
    pct = round(c / weekday_total * 100)
    bar_h = int(c / max_day_c * 70) + 10
    is_peak = (d == peak_day)
    color = "#ff4081" if is_peak else "#c2185b"
    border = "border:2px solid #ff4081;" if is_peak else "border:1px solid rgba(194,24,91,0.3);"
    peak_mark = "👑" if is_peak else ""
    day_row += (
        f"<div style='flex:1;text-align:center;'>"
        f"<div style='height:{bar_h}px;background:linear-gradient(180deg,{color},{color}88);"
        f"border-radius:4px 4px 0 0;{border}border-bottom:none;'></div>"
        f"<div style='background:rgba(30,0,20,0.6);{border}border-top:none;"
        f"border-radius:0 0 4px 4px;padding:2px 0;'>"
        f"<div style='color:#ff80ab;font-size:0.78em;font-weight:700;'>{d}{peak_mark}</div>"
        f"<div style='color:#ffe0f0;font-size:0.75em;'>{c}回</div>"
        f"</div></div>"
    )
st.markdown(
    f"<div style='display:flex;gap:4px;align-items:flex-end;margin-bottom:0.8em;'>{day_row}</div>",
    unsafe_allow_html=True,
)
if peak_day:
    st.markdown(
        f"<div style='color:#ffb6d9;font-style:italic;font-size:0.9em;text-align:center;"
        f"background:rgba(194,24,91,0.1);border-radius:8px;padding:0.5em;'>"
        f"💬 {peak_day}曜日が一番危険な日ね。自分でもわかってるでしょ？</div>",
        unsafe_allow_html=True,
    )
