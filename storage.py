import json
from pathlib import Path
from firebase_manager import load_cloud_data, save_cloud_data

BASE = Path.home() / "countapp_dashboard"
BASE.mkdir(parents=True, exist_ok=True)

DATA_FILE = BASE / "data.json"
IMG_DIR = BASE / "images"
IMG_DIR.mkdir(exist_ok=True)


def load_data():
    # local
    if DATA_FILE.exists():
        try:
            data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        except:
            data = default_data()
    else:
        data = default_data()

    # cloud override
    cloud = load_cloud_data()
    if cloud:
        data = cloud

    return data


def save_data(data):
    DATA_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    save_cloud_data(data)


def default_data():
    return {
        "tabs": [{"id": "all", "name": "全体"}],
        "items": {},
        "history": []
    }