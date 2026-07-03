import streamlit as st
from core import get_data, ensure_structure, compute_points

data = ensure_structure(get_data())
ranking = compute_points(data)

st.subheader("🧠 診断書")

selected = st.selectbox(
    "診断する弱点",
    list(ranking.keys()) if ranking else []
)

if selected:
    pts = ranking[selected]["points"]

    st.markdown(f"""
## 【{selected} 診断書】

- 総ポイント: {pts}
- 平均射精時間: {max(8, 40 - pts//2)} 秒
- 即イキ率: {min(95, 40 + pts//2)} %
- 射精後虚無時間: {min(8, 2 + pts//15)} 分

---

### 弱点評価
- カリ：{"★" * min(5, pts//15)}
- 尿道：{"★" * min(5, pts//12)}
- 玉：{"★" * min(5, pts//20)}
- 先走り：{"★" * min(5, pts//10)}

---

### 総合評価
{"S+級オナペ" if pts >= 50 else "A級オナペ"}
""")