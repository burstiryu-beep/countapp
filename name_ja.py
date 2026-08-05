"""オナペ名を日本語文に自然に差し込む。"""
from __future__ import annotations

import re


_LATIN_RE = re.compile(r"[A-Za-z]")


def nj(name: str, fallback: str = "彼女") -> str:
    """セリフ用の名前表記。

    欧文名・空白入り（例: Emanuelly Raquel）は「」で囲む。
    日本語名はそのまま。
    """
    n = (name or "").strip()
    if not n:
        return fallback
    if _LATIN_RE.search(n) or " " in n or "　" in n:
        if n.startswith("「") and n.endswith("」"):
            return n
        return f"「{n}」"
    return n


def is_western_name(name: str) -> bool:
    n = (name or "").strip()
    return bool(n and (_LATIN_RE.search(n) or " " in n or "　" in n))


def n_no(name: str, noun: str) -> str:
    """「ユキの口」「『Emanuelly Raquel』の口」"""
    return f"{nj(name)}の{noun}"


def n_ga(name: str, pred: str) -> str:
    """「ユキがしてあげる」"""
    return f"{nj(name)}が{pred}"


def n_wa(name: str, pred: str) -> str:
    """「ユキは離さないわよ」"""
    return f"{nj(name)}は{pred}"


def n_mae(name: str) -> str:
    """「ユキの前で」"""
    return f"{nj(name)}の前で"


def n_sei(name: str) -> str:
    """「ユキのせい」"""
    return f"{nj(name)}のせい"
