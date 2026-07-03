import streamlit as st
from core import get_data, ensure_structure, compute_points
from utils import calc_continuous_days

data = ensure_structure(get_data())

st.title("📊 Dashboard")

# =====================
# サマリー
# =====================
total_counts = sum(
    sum(v.get("counts", {}).values())
    for v in data["items"].values()
)

st.metric("総カウント数", total_counts)
st.metric("登録アイテム数", len(data["items"]))
st.metric("連続日数", calc_continuous_days(data["history"]))

st.divider()

# =====================
# トップランキング
# =====================
st.subheader("🏆 Top 5")

ranking = compute_points(data)
sorted_rank = sorted(ranking.items(), key=lambda x: -x[1]["points"])

for name, info in sorted_rank[:5]:
    st.write(f"**{name}** : {info['points']} pt ({info['tier']})")

st.divider()

# =====================
# 月別集計
# =====================
st.subheader("📅 月別カウント")

month_map = {}

for v in data["items"].values():
    for m, c in v.get("counts", {}).items():
        month_map[m] = month_map.get(m, 0) + c

for m, c in sorted(month_map.items(), reverse=True):
    st.write(f"{m}: {c}回")