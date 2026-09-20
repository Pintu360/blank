from __future__ import annotations

from typing import Any

from .curriculum.lessons import lessons_for_level, next_lesson
from .curriculum.levels import LEVEL_META, LEVELS, next_level
from .util import esc


def is_bangla(row: dict[str, Any]) -> bool:
    lang = str(row.get("native_lang") or "bn").lower()
    return lang in {"bn", "bangla", "bengali", "বাংলা"}


def tr(row: dict[str, Any], en: str, bn: str) -> str:
    return bn if is_bangla(row) else en


def bar(done: int, total: int, width: int = 8) -> str:
    if total <= 0:
        return "▱" * width
    filled = int(round(width * min(max(done, 0), total) / total))
    filled = min(width, max(0, filled))
    return "▰" * filled + "▱" * (width - filled)


def stars(score: int, total: int) -> str:
    if total <= 0:
        return ""
    filled = round(5 * score / total)
    filled = min(5, max(0, filled))
    return "⭐" * filled + "☆" * (5 - filled)


def rule() -> str:
    return "────────"


LEVEL_EMOJI = {
    "A1": "🌱",
    "A2": "🌿",
    "B1": "🌳",
    "B2": "🏔️",
    "C1": "🎯",
    "IELTS": "🏆",
}


def level_badge(level: str) -> str:
    meta = LEVEL_META[level]
    return f"{LEVEL_EMOJI.get(level, '📘')} <b>{level}</b>  {esc(meta['name'])}"


def lesson_unlocked(lessons: list, lesson_id: str, completed: list[str]) -> bool:
    ids = [les.id for les in lessons]
    if lesson_id not in ids:
        return False
    i = ids.index(lesson_id)
    return i == 0 or ids[i - 1] in completed


def home_text(row: dict[str, Any], completed: list[str], due: int, cards: int) -> str:
    name = esc(row.get("first_name") or tr(row, "friend", "বন্ধু"))
    level = row["level"]
    meta = LEVEL_META[level]
    lessons = lessons_for_level(level)
    finished = sum(1 for les in lessons if les.id in completed)
    nxt = next_lesson(level, completed)
    today = (
        f"▶  {esc(nxt.title)}  ·  {nxt.minutes} min"
        if nxt
        else tr(row, "This level is complete. Open the course map.", "এই লেভেল শেষ। কোর্স ম্যাপ খুলুন।")
    )
    vocab_line = (
        tr(row, f"🧠  {due} words to review", f"🧠  {due}টা শব্দ রিভিউ")
        if due
        else tr(row, f"🧠  {cards} words in your deck", f"🧠  ডেকে {cards}টা শব্দ")
    )
    bn_sub = (
        "\n<i>আজকের পথ — একটা পাঠ, একটু শব্দ, একটু কথা।</i>"
        if is_bangla(row)
        else "\n<i>Today: one lesson, a few words, a little speaking.</i>"
    )
    return (
        f"{LEVEL_EMOJI.get(level, '📘')}  <b>English Ladder</b>\n"
        f"{tr(row, 'Hi', 'হ্যালো')}, {name}\n\n"
        f"🔥 {row['streak']}   ·   ⭐ {row['xp']} XP   ·   🎯 {esc(str(row['goal_band']))}\n\n"
        f"{level_badge(level)}\n"
        f"{bar(finished, len(lessons))}  {finished}/{len(lessons)}\n"
        f"IELTS ~ {meta['ielts']}\n"
        f"{bn_sub}\n\n"
        f"<b>{tr(row, 'Today', 'আজ')}</b>\n"
        f"{today}\n"
        f"{vocab_line}"
    )


def course_overview(completed: list[str], current: str) -> str:
    lines = ["<b>Course map</b>  ·  Basic → Advanced\n"]
    for level in LEVELS:
        lessons = lessons_for_level(level)
        done = sum(1 for les in lessons if les.id in completed)
        mark = "●" if level == current else "○"
        lock = "" if done or level == current else ""
        lines.append(
            f"{mark} {LEVEL_EMOJI.get(level, '📘')} <b>{level}</b>  {LEVEL_META[level]['name']}\n"
            f"    {bar(done, len(lessons), 6)}  {done}/{len(lessons)}{lock}"
        )
    return "\n".join(lines)


def level_map_text(level: str, completed: list[str]) -> str:
    lessons = lessons_for_level(level)
    meta = LEVEL_META[level]
    lines = [
        f"{level_badge(level)}",
        f"{bar(sum(1 for les in lessons if les.id in completed), len(lessons))}  "
        f"{sum(1 for les in lessons if les.id in completed)}/{len(lessons)}",
        f"<i>{esc(meta['blurb'])}</i>",
        "",
    ]
    ids = [les.id for les in lessons]
    for les in lessons:
        i = ids.index(les.id)
        if les.id in completed:
            icon = "✅"
        elif i == 0 or ids[i - 1] in completed:
            icon = "▶"
        else:
            icon = "🔒"
        title = les.title.split("—")[0].strip()
        lines.append(f"{icon}  {les.unit}. {esc(title)}")
    return "\n".join(lines)


def quiz_card(title: str, index: int, total: int, prompt: str, result: str | None = None) -> str:
    head = f"<b>{esc(title)}</b>\n{bar(index, total)}  {index + 1}/{total}"
    if result:
        return f"{result}\n{rule()}\n{head}\n\n{prompt}"
    return f"{head}\n\n{prompt}"


def result_card(title: str, score: int, total: int, xp: int, extra: str = "") -> str:
    pct = round(100 * score / total) if total else 0
    return (
        f"<b>{esc(title)}</b>\n"
        f"{stars(score, total)}  {score}/{total}  ({pct}%)\n"
        f"+{xp} XP\n"
        f"{extra}"
    )


def next_track_line(level: str) -> str:
    nxt = next_level(level)
    if nxt:
        return f"\nNext: {LEVEL_EMOJI.get(nxt, '')} <b>{nxt}</b> {LEVEL_META[nxt]['name']}"
    return "\nYou are at the top of the ladder. Keep polishing Band 8–9."
