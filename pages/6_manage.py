import streamlit as st
import style
from core import get_data, ensure_structure
from storage import save_data, IMG_DIR
from utils import delete_item, make_key, rename_item

style.apply()
data = ensure_structure(get_data())

st.markdown("<h2 style='text-align:center'>⚙️ 管理</h2>", unsafe_allow_html=True)

item_names = list({v["name"] for v in data["items"].values()})

# ===== 弱点追加 =====
st.markdown("<h3>➕ 弱点を追加</h3>", unsafe_allow_html=True)

with st.form("add"):
    name = st.text_input("弱点名")
    img = st.file_uploader("画像（任意）")
    ok = st.form_submit_button("追加する")

    if ok and name.strip():
        key = make_key(name.strip(), "all")
        if key in data["items"]:
            st.error("同じ名前の弱点が既にあります")
        else:
            data["items"][key] = {
                "name": name.strip(), "tab": "all",
                "counts": {}, "img": "", "points": 0
            }
            if img:
                path = IMG_DIR / img.name
                path.write_bytes(img.read())
                data["items"][key]["img"] = str(path)
            save_data(data)
            st.success("追加しました！")
            st.rerun()

st.divider()

# ===== 弱点名変更 =====
st.markdown("<h3>✏️ 弱点名を変更</h3>", unsafe_allow_html=True)

if item_names:
    sel_rename = st.selectbox("変更対象", sorted(item_names), key="rename_sel")
    new_name = st.text_input("新しい名前", key="rename_input")

    if st.button("名前を変更", key="rename_btn"):
        if not new_name.strip():
            st.error("名前を入力してください")
        elif new_name.strip() == sel_rename:
            st.warning("同じ名前です")
        else:
            item_key = next((k for k, v in data["items"].items() if v["name"] == sel_rename), None)
            if item_key and rename_item(data, sel_rename, data["items"][item_key]["tab"], new_name.strip()):
                save_data(data)
                st.success("変更しました")
                st.rerun()
            else:
                st.error("その名前は既に使われています")
else:
    st.caption("登録されている弱点がありません")

st.divider()

# ===== 弱点削除 =====
st.markdown("<h3>🗑 弱点を削除</h3>", unsafe_allow_html=True)

if item_names:
    sel_del = st.selectbox("削除対象", sorted(item_names), key="del_sel")
    if st.button("削除する", key="del_btn"):
        item_key = next((k for k, v in data["items"].items() if v["name"] == sel_del), None)
        if item_key:
            delete_item(data, sel_del, data["items"][item_key]["tab"])
            save_data(data)
            st.success("削除しました")
            st.rerun()
else:
    st.caption("登録されている弱点がありません")
