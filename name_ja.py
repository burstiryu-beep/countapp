"""オナペ名を日本語文に自然に差し込む。"""
from __future__ import annotations

import re


_LATIN_RE = re.compile(r"[A-Za-z]")


def nj(name: str, fallback: str = "彼女") -> str:
    """セリフ用の名前表記。

    欧文名・空白入り（例: Emanuelly Raquel）は「」で囲み、
    『離さないわよ、Name』のような語尾呼びが壊れないようにする。
    日本語名はそのまま。
    """
    n = (name or "").strip()
    if not n:
        return fallback
    if _LATIN_RE.search(n) or " " in n or "　" in n:
        # 既に鍵括弧付きなら二重にしない
        if n.startswith("「") and n.endswith("」"):
            return n
        return f"「{n}」"
    return n


def is_western_name(name: str) -> bool:
    n = (name or "").strip()
    return bool(n and (_LATIN_RE.search(n) or " " in n or "　" in n))
