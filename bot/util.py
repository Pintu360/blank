from __future__ import annotations

import html
import re
from typing import Iterable

TG_LIMIT = 3900

_SPACE = re.compile(r"\s+")
_PUNCT = re.compile(r"[.!?,'\"“”‘’]+")


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def normalize_answer(text: str) -> str:
    t = text.strip().lower()
    t = t.replace("’", "'").replace("`", "'")
    t = _PUNCT.sub("", t)
    t = _SPACE.sub(" ", t)
    return t


def answers_match(expected: str, given: str) -> bool:
    g = normalize_answer(given)
    if not g:
        return False
    for alt in expected.split("|"):
        if normalize_answer(alt) == g:
            return True
    return False


def chunk(text: str, limit: int = TG_LIMIT) -> list[str]:
    if len(text) <= limit:
        return [text]
    parts: list[str] = []
    rest = text
    while rest:
        if len(rest) <= limit:
            parts.append(rest)
            break
        cut = rest.rfind("\n", 0, limit)
        if cut < limit // 3:
            cut = rest.rfind(" ", 0, limit)
        if cut < limit // 3:
            cut = limit
        parts.append(rest[:cut].rstrip())
        rest = rest[cut:].lstrip()
    return parts


def join_goals(goals: Iterable[str]) -> str:
    return "\n".join(f"• {g}" for g in goals)
