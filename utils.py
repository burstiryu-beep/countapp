from datetime import datetime, date, timedelta
from pathlib import Path

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def month():
    return datetime.now().strftime("%Y-%m")

def today():
    return datetime.now().strftime("%Y-%m-%d")

def make_key(name, tab):
    return f"{name}@@{tab}"


def resolve_img_path(img_path):
    if not img_path:
        return None

    p = Path(img_path)
    if p.is_file():
        return p

    name = p.name
    for base in (
        Path.cwd(),
        Path.cwd() / "images",
        Path.home() / "countapp_dashboard" / "images",
        Path(__file__).resolve().parent / "images",
        Path(__file__).resolve().parent / ".data" / "images",
    ):
        candidate = base / name if base.name == "images" else base / img_path
        if candidate.is_file():
            return candidate

    return None


def undo_count_from_history(data, entry):
    key = make_key(entry["name"], entry["tab"])
    if key not in data["items"]:
        return

    m = entry["time"][:7]
    counts = data["items"][key]["counts"]
    if m in counts and counts[m] > 0:
        counts[m] -= 1
        if counts[m] == 0:
            del counts[m]


def calc_continuous_days(history):
    if not history:
        return 0

    dates = sorted({h["time"][:10] for h in history})
    if not dates:
        return 0

    today_d = date.today()
    count = 0
    current = today_d

    for d in reversed(dates):
        dt = datetime.strptime(d, "%Y-%m-%d").date()
        if dt == current:
            count += 1
            current -= timedelta(days=1)
        elif dt < current:
            break

    return count


def tier(points, rank, n):
    if n == 0:
        return "D"

    if rank == 0:
        return "SS"

    r = rank / n
    if r <= 0.10:
        return "S"
    if r <= 0.30:
        return "A"
    if r <= 0.50:
        return "B"
    if r <= 0.80:
        return "C"
    return "D"