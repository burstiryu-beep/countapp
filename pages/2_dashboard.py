import streamlit as st
import style
from core import get_data, ensure_structure, compute_points
from utils import active_items, calc_continuous_days, registered_item_count

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
    st.markdown(
        f"<div class='ero-card' style='display:flex;align-items:center;gap:1em;text-align:left;padding:0.6em 1em;'>"
        f"<span style='font-size:1.6em;min-width:2em;text-align:center;'>{icon}</span>"
        f"<span style='flex:1;font-size:1.1em;color:#ffe0f0;font-weight:600;'>{name}</span>"
        f"<span class='tier-{t}' style='margin-right:0.5em;'>{t}</span>"
        f"<span style='color:#ff80ab;font-weight:700;'>{info['points']} 回</span>"
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
