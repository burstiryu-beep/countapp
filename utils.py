from datetime import datetime, date, timedelta

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def month():
    return datetime.now().strftime("%Y-%m")

def today():
    return datetime.now().strftime("%Y-%m-%d")

def make_key(name, tab):
    return f"{name}@@{tab}"


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