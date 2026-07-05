import streamlit as st
from core import get_data, ensure_structure
from storage import save_data
from utils import undo_count_from_history

data = ensure_structure(get_data())

st.title("📜 History")

# =====================
# 全履歴表示
# =====================
st.subheader("全履歴")

for i, h in enumerate(reversed(data["history"])):
    st.write(f"{h['time']} | {h['name']} ({h['tab']})")

st.divider()

# =====================
# 履歴削除
# =====================
st.subheader("履歴削除")

if data["history"]:
    index_map = list(range(len(data["history"])))

    sel = st.selectbox(
        "削除対象",
        index_map,
        format_func=lambda i: f"{data['history'][i]['time']} | {data['history'][i]['name']}"
    )

    if st.button("削除"):
        entry = data["history"][sel]
        undo_count_from_history(data, entry)
        data["history"].pop(sel)
        save_data(data)
        st.rerun()