import streamlit as st
from core import get_data, ensure_structure
from storage import save_data, IMG_DIR
from utils import (
    delete_item,
    delete_tab,
    make_key,
    rename_item,
    rename_tab_id,
    rename_tab_name,
)

data = ensure_structure(get_data())

tab_names = {t["id"]: t["name"] for t in data["tabs"]}
editable_tabs = [t for t in data["tabs"] if t["id"] != "all"]

st.subheader("➕ アイテム追加")

with st.form("add"):
    name = st.text_input("弱点名")
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
st.subheader("✏️ 弱点名変更")

if data["items"]:
    item_keys = list(data["items"].keys())

    def item_label(key):
        v = data["items"][key]
        return f"{v['name']} ({tab_names.get(v['tab'], v['tab'])})"

    rename_key = st.selectbox("変更対象", item_keys, format_func=item_label, key="rename_sel")
    new_name = st.text_input("新しい名前", key="rename_input")

    if st.button("名前を変更", key="rename_btn"):
        if not new_name.strip():
            st.error("新しい名前を入力してください")
        elif new_name.strip() == data["items"][rename_key]["name"]:
            st.warning("同じ名前です")
        elif rename_item(
            data,
            data["items"][rename_key]["name"],
            data["items"][rename_key]["tab"],
            new_name.strip()
        ):
            save_data(data)
            st.success("名前を変更しました")
            st.rerun()
        else:
            st.error("その名前は既に使われています")
else:
    st.caption("登録アイテムがありません")

st.divider()
st.subheader("🗑 弱点削除")

if data["items"]:
    del_key = st.selectbox("削除対象", item_keys, format_func=item_label, key="del_sel")

    if st.button("削除", key="del_btn"):
        item = data["items"][del_key]
        delete_item(data, item["name"], item["tab"])
        save_data(data)
        st.success("削除しました")
        st.rerun()
else:
    st.caption("登録アイテムがありません")

st.divider()
st.subheader("🏷 タブ追加")

new_tab = st.text_input("タブ名", key="new_tab_input")

if st.button("追加タブ", key="add_tab_btn"):
    if new_tab.strip():
        tab_id = new_tab.strip()
        if any(t["id"] == tab_id for t in data["tabs"]):
            st.error("同じIDのタブが既にあります")
        else:
            data["tabs"].append({"id": tab_id, "name": tab_id})
            save_data(data)
            st.success("タブを追加しました")
            st.rerun()

st.divider()
st.subheader("✏️ タブ編集")

if editable_tabs:
    edit_tab = st.selectbox(
        "編集するタブ",
        editable_tabs,
        format_func=lambda t: t["name"],
        key="edit_tab_sel"
    )

    new_display_name = st.text_input(
        "表示名",
        value=edit_tab["name"],
        key="edit_tab_name"
    )
    new_tab_id = st.text_input(
        "タブID（内部識別子）",
        value=edit_tab["id"],
        key="edit_tab_id"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("タブを更新", key="update_tab_btn"):
            updated = False
            if new_display_name.strip() and new_display_name.strip() != edit_tab["name"]:
                rename_tab_name(data, edit_tab["id"], new_display_name.strip())
                updated = True

            new_id = new_tab_id.strip()
            if new_id and new_id != edit_tab["id"]:
                if new_id == "all":
                    st.error("「all」は使用できません")
                elif rename_tab_id(data, edit_tab["id"], new_id):
                    updated = True
                else:
                    st.error("そのタブIDは既に使われています")

            if updated:
                save_data(data)
                st.success("タブを更新しました")
                st.rerun()
            elif new_display_name.strip() == edit_tab["name"] and new_id == edit_tab["id"]:
                st.info("変更がありません")

    with col2:
        if st.button("タブを削除", key="delete_tab_btn"):
            if delete_tab(data, edit_tab["id"]):
                save_data(data)
                st.success("タブと関連アイテムを削除しました")
                st.rerun()
else:
    st.caption("編集可能なタブがありません（「全体」以外のタブを追加してください）")
