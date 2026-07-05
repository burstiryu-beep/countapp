import streamlit as st
from core import get_data, ensure_structure
from storage import save_data, IMG_DIR
from utils import make_key

data = ensure_structure(get_data())

st.subheader("➕ アイテム追加")

with st.form("add"):
    name = st.text_input("弱点名")

    tab_names = {t["id"]: t["name"] for t in data["tabs"]}
    tab_ids = list(tab_names.keys())

    tab = st.selectbox("タブ", tab_ids, format_func=lambda x: tab_names[x])
    img = st.file_uploader("画像")

    ok = st.form_submit_button("追加")

    if ok and name:
        key = make_key(name, tab)

        data["items"][key] = {
            "name": name,
            "tab": tab,
            "counts": {},
            "img": "",
            "points": 0
        }

        if img:
            path = IMG_DIR / img.name
            path.write_bytes(img.read())
            data["items"][key]["img"] = str(path)

        save_data(data)
        st.success("追加完了")
        st.rerun()

st.divider()
st.subheader("🗑 削除")

names = [v["name"] for v in data["items"].values()]
del_name = st.selectbox("削除対象", names)

if st.button("削除"):
    data["items"] = {
        k: v for k, v in data["items"].items()
        if v["name"] != del_name
    }
    save_data(data)
    st.rerun()

st.divider()
st.subheader("🏷 タブ追加")

new_tab = st.text_input("タブ名")

if st.button("追加タブ"):
    if new_tab:
        data["tabs"].append({
            "id": new_tab,
            "name": new_tab
        })
        save_data(data)
        st.rerun()
