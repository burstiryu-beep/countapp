import json
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent

try:
    from firebase_manager import load_cloud_data, save_cloud_data
except Exception:
    def load_cloud_data():
        return None

    def save_cloud_data(data):
        pass


def _init_dirs():
    for base in (Path.home() / "countapp_dashboard", APP_DIR / ".data"):
        try:
            base.mkdir(parents=True, exist_ok=True)
            img_dir = base / "images"
            img_dir.mkdir(exist_ok=True)
            return base, img_dir
        except OSError:
            continue

    base = APP_DIR / ".data"
    base.mkdir(parents=True, exist_ok=True)
    img_dir = base / "images"
    img_dir.mkdir(exist_ok=True)
    return base, img_dir


BASE, IMG_DIR = _init_dirs()
DATA_FILE = BASE / "data.json"


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