from datetime import date, datetime

import streamlit as st
import style
from core import get_data, ensure_structure
from storage import save_data
from utils import change_history_date, undo_count_from_history

style.apply()
data = ensure_structure(get_data())

st.markdown("<h2 style='text-align:center'>📜 射精履歴</h2>", unsafe_allow_html=True)

st.markdown("<h3>全記録</h3>", unsafe_allow_html=True)

for h in reversed(data["history"]):
    st.markdown(
        f"<div style='padding:0.3em 0; border-bottom:1px solid rgba(194,24,91,0.2);'>"
        f"<span style='color:#ff80ab;'>{h['time']}</span>"
        f"　<span style='color:#ffe0f0; font-weight:600;'>{h['name']}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

st.divider()
st.markdown("<h3>📝 履歴編集</h3>", unsafe_allow_html=True)

if data["history"]:
    index_map = list(range(len(data["history"])))

    def history_label(i):
        h = data["history"][i]
        return f"{h['time']} | {h['name']}"

    sel = st.selectbox("対象を選択", index_map, format_func=history_label, key="edit_sel")

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
        if st.button("📅 日付を変更", key="change_date_btn"):
            if new_date == current_date:
                st.info("同じ日付です")
            elif change_history_date(data, sel, new_date):
                save_data(data)
                st.success("日付を変更しました")
                st.rerun()
            else:
                st.error("変更に失敗しました")
    with col2:
        if st.button("🗑 この記録を削除", key="delete_btn"):
            undo_count_from_history(data, entry)
            data["history"].pop(sel)
            save_data(data)
            st.success("削除しました")
            st.rerun()
else:
    st.markdown("<p style='color:#804060;'>履歴がありません</p>", unsafe_allow_html=True)
