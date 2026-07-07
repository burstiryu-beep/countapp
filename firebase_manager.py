import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

_db = None


def init_firebase():
    global _db
    if _db:
        return _db

    # 1. Streamlit Cloud Secrets から読む（本番環境）
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

    # 2. ローカルファイルから読む（開発環境）
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


def load_cloud_data():
    db = init_firebase()
    if not db:
        return None
    try:
        doc = db.collection("countapp").document("data").get()
        if doc.exists:
            return doc.to_dict()
    except Exception:
        pass
    return None


def save_cloud_data(data):
    db = init_firebase()
    if not db:
        return
    try:
        db.collection("countapp").document("data").set(data)
    except Exception:
        pass
