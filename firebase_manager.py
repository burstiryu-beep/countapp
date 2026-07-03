import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

_db = None

def init_firebase():
    global _db
    if _db:
        return _db

    key_path = Path("serviceAccountKey.json")
    if not key_path.exists():
        return None

    if not firebase_admin._apps:
        cred = credentials.Certificate(str(key_path))
        firebase_admin.initialize_app(cred)

    _db = firestore.client()
    return _db


def load_cloud_data():
    db = init_firebase()
    if not db:
        return None

    doc = db.collection("countapp").document("data").get()
    if doc.exists:
        return doc.to_dict()
    return None


def save_cloud_data(data):
    db = init_firebase()
    if not db:
        return

    db.collection("countapp").document("data").set(data)