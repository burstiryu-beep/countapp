from datetime import date

import streamlit as st
from core import get_data, ensure_structure, aggregate, count_item
from utils import make_key, resolve_img_path

data = ensure_structure(get_data())

tab_names = {t["id"]: t["name"] for t in data["tabs"]}
tab_ids = list(tab_names.keys())

current_tab = st.sidebar.selectbox(
    "表示タブ",
    tab_ids,
    format_func=lambda x: tab_names[x]
)

_raw_date = st.sidebar.date_input(
    "カウント日付",
    value=date.today(),
    max_value=date.today(),
    help="前日分などを後から記録するときに変更してください"
)
count_date = _raw_date if isinstance(_raw_date, date) else date.today()

items = aggregate(data, current_tab)
is_all_tab = current_tab == "all"

st.subheader("弱点一覧")

if is_all_tab:
    st.info("「全体」タブでは各月の合計を確認できます。カウントするにはタブを選択してください。")
elif count_date < date.today():
    st.info(f"📅 {count_date.strftime('%Y-%m-%d')} の日付でカウントします")

cols = st.columns(3)

for i, (name, val) in enumerate(items.items()):
    with cols[i % 3]:
        st.markdown(f"### {name}")

        if is_all_tab:
            # 全体タブ：同名アイテムの最初の画像を探す
            item = next(
                (v for v in data["items"].values() if v["name"] == name),
                {}
            )
        else:
            item = data["items"].get(make_key(name, current_tab), {})

        img_path = resolve_img_path(item.get("img", ""))
        if img_path:
            st.image(str(img_path), use_container_width=True)

        st.metric("敗北数", val)

        if not is_all_tab:
            if st.button("カウント", key=f"btn_{name}"):
                try:
                    count_item(data, name, current_tab, count_date)
                    st.rerun()
                except Exception as e:
                    st.error(f"エラー詳細: {type(e).__name__}: {e}")

st.divider()
st.subheader("履歴")

for h in reversed(data["history"][-20:]):
    st.write(f"{h['time']} | {h['name']} ({h['tab']})")
