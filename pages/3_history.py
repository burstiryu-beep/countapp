from datetime import date, datetime

import streamlit as st
from core import get_data, ensure_structure
from storage import save_data
from utils import change_history_date, undo_count_from_history

data = ensure_structure(get_data())

st.title("📜 History")

st.subheader("全履歴")

for h in reversed(data["history"]):
    st.write(f"{h['time']} | {h['name']} ({h['tab']})")

st.divider()

st.subheader("履歴編集")

if data["history"]:
    index_map = list(range(len(data["history"])))

    def history_label(i):
        h = data["history"][i]
        return f"{h['time']} | {h['name']} ({h['tab']})"

    sel = st.selectbox("対象", index_map, format_func=history_label, key="edit_sel")

    entry = data["history"][sel]
    current_date = datetime.strptime(entry["time"][:10], "%Y-%m-%d").date()

    new_date = st.date_input(
        "新しい日付",
        value=current_date,
        max_value=date.today(),
        key="edit_date"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("日付を変更", key="change_date_btn"):
            if new_date == current_date:
                st.info("同じ日付です")
            elif change_history_date(data, sel, new_date):
                save_data(data)
                st.success("日付を変更しました")
                st.rerun()
            else:
                st.error("日付の変更に失敗しました")

    with col2:
        if st.button("削除", key="delete_btn"):
            undo_count_from_history(data, entry)
            data["history"].pop(sel)
            save_data(data)
            st.success("削除しました")
            st.rerun()
else:
    st.caption("履歴がありません")
