import copy
import hashlib

import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

_db = None


def _item_doc_id(item_key: str) -> str:
    return hashlib.md5(item_key.encode("utf-8")).hexdigest()


def _images_collection(db):
    return db.collection("countapp").document("data").collection("images")


def init_firebase():
    global _db
    if _db:
        return _db

    try:
        import streamlit as st
        if hasattr(st, "secrets") and "firebase" in st.secrets:
            cred_dict = {k: v for k, v in st.secrets["firebase"].items()}
            if not firebase_admin._apps:
                firebase_admin.initialize_app(credentials.Certificate(cred_dict))
            _db = firestore.client()
            return _db
    except Exception:
        pass

    key_path = Path(__file__).parent / "serviceAccountKey.json"
    if key_path.exists():
        try:
            if not firebase_admin._apps:
                firebase_admin.initialize_app(credentials.Certificate(str(key_path)))
            _db = firestore.client()
            return _db
        except Exception:
            pass

    return None


def fetch_image(img_value: str) -> str:
    """cloud:参照を実際の data URI に解決する"""
    if not img_value or not isinstance(img_value, str):
        return ""
    if img_value.startswith("data:"):
        return img_value
    if not img_value.startswith("cloud:"):
        return img_value

    doc_id = img_value.split(":", 1)[1]
    db = init_firebase()
    if not db:
        return ""

    try:
        snap = _images_collection(db).document(doc_id).get()
        if snap.exists:
            return (snap.to_dict() or {}).get("img", "")
    except Exception:
        pass
    return ""


def _extract_images(data):
    images = {}
    payload = copy.deepcopy(data)
    for key, item in payload.get("items", {}).items():
        img = item.get("img", "")
        if isinstance(img, str) and img.startswith("data:"):
            images[key] = img
            item["img"] = f"cloud:{_item_doc_id(key)}"
    return payload, images


def _merge_images(data):
    db = init_firebase()
    if not db:
        return data

    items = data.get("items", {})
    if not items:
        return data

    refs = []
    key_by_doc = {}
    for key, item in items.items():
        img = item.get("img", "")
        if isinstance(img, str) and img.startswith("cloud:"):
            doc_id = img.split(":", 1)[1]
            refs.append(_images_collection(db).document(doc_id))
            key_by_doc[doc_id] = key

    if not refs:
        return data

    try:
        for snap in db.get_all(refs):
            if not snap.exists:
                continue
            doc = snap.to_dict() or {}
            item_key = doc.get("item_key") or key_by_doc.get(snap.id)
            img = doc.get("img", "")
            if item_key and item_key in items and img:
                items[item_key]["img"] = img
    except Exception:
        pass

    return data


def load_cloud_data():
    db = init_firebase()
    if not db:
        return None
    try:
        doc = db.collection("countapp").document("data").get()
        if not doc.exists:
            return None
        data = doc.to_dict()
        return _merge_images(data)
    except Exception:
        return None


def save_cloud_data(data):
    db = init_firebase()
    if not db:
        return False, "Firebase未接続"

    payload_inline = copy.deepcopy(data)

    # まずインライン画像のまま保存（従来形式・互換性優先）
    try:
        db.collection("countapp").document("data").set(payload_inline)
        return True, ""
    except Exception:
        pass

    # サイズ超過時のみ画像を分離（画像を先に保存してから本体）
    payload, images = _extract_images(data)

    for item_key, img in images.items():
        doc_id = _item_doc_id(item_key)
        try:
            _images_collection(db).document(doc_id).set({
                "item_key": item_key,
                "img": img,
            })
        except Exception as e:
            return False, f"画像保存失敗 ({item_key}): {e}"

    try:
        db.collection("countapp").document("data").set(payload)
    except Exception as e:
        return False, f"データ保存失敗: {e}"

    return True, ""
