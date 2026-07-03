import streamlit as st
from core import get_data, ensure_structure, compute_points

data = ensure_structure(get_data())

st.subheader("🏆 ランキング")

ranking = compute_points(data)
sorted_rank = sorted(ranking.items(), key=lambda x: -x[1]["points"])

for name, info in sorted_rank:
    st.write(f"""
### {name}
- ポイント: {info['points']}
- ティア: **{info['tier']}**
""")