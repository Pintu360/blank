from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from .curriculum.levels import LEVELS, LEVEL_META

BTN_LESSON = "📚 Lesson"
BTN_VOCAB = "🧠 Vocab"
BTN_GRAMMAR = "✏️ Grammar"
BTN_READ = "📖 Reading"
BTN_WRITE = "✍️ Writing"
BTN_SPEAK = "🗣️ Speaking"
BTN_TUTOR = "💬 Tutor"
BTN_IELTS = "🎯 IELTS"
BTN_PROGRESS = "📊 Progress"
BTN_SETTINGS = "⚙️ Settings"
BTN_MENU = "🏠 Menu"

MAIN_ROWS = (
    (BTN_LESSON, BTN_VOCAB),
    (BTN_GRAMMAR, BTN_READ),
    (BTN_WRITE, BTN_SPEAK),
    (BTN_TUTOR, BTN_IELTS),
    (BTN_PROGRESS, BTN_SETTINGS),
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(MAIN_ROWS, resize_keyboard=True)

BUTTONS = {btn for row in MAIN_ROWS for btn in row} | {BTN_MENU}


def main_kb() -> ReplyKeyboardMarkup:
    return MAIN_KEYBOARD


def onboarding_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📝 Placement test — লেভেল মাপো", callback_data="ob:place")],
            [InlineKeyboardButton("🌱 আমি একদম নতুন (A1)", callback_data="ob:A1")],
            [InlineKeyboardButton("🎯 IELTS টার্গেট", callback_data="ob:IELTS")],
            [InlineKeyboardButton("📂 নিজে লেভেল বাছো", callback_data="ob:pick")],
        ]
    )


def levels_kb(prefix: str = "lvl") -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for level in LEVELS:
        meta = LEVEL_META[level]
        row.append(InlineKeyboardButton(f"{level} {meta['name']}", callback_data=f"{prefix}:{level}"))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("🏠 Menu", callback_data="m:home")])
    return InlineKeyboardMarkup(rows)


def after_teach_kb(lesson_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("✅ Practice quiz", callback_data=f"lsn:quiz:{lesson_id}")],
            [InlineKeyboardButton("🏠 Menu", callback_data="m:home")],
        ]
    )


def mcq_kb(n: int) -> InlineKeyboardMarkup:
    labels = "ABCD"
    buttons = [InlineKeyboardButton(labels[i], callback_data=f"ans:{i}") for i in range(n)]
    return InlineKeyboardMarkup([buttons, [InlineKeyboardButton("⏭ Skip", callback_data="ans:skip")]])


def vocab_rate_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Again", callback_data="v:1"),
                InlineKeyboardButton("Hard", callback_data="v:3"),
                InlineKeyboardButton("Good", callback_data="v:4"),
                InlineKeyboardButton("Easy", callback_data="v:5"),
            ]
        ]
    )


def reveal_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("👁 Show meaning — অর্থ দেখাও", callback_data="v:show")],
            [InlineKeyboardButton("⏭ Skip", callback_data="v:skip")],
        ]
    )


def settings_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📈 Change level", callback_data="set:level")],
            [
                InlineKeyboardButton("🇧🇩 Bangla help", callback_data="set:bn"),
                InlineKeyboardButton("🇬🇧 English only", callback_data="set:en"),
            ],
            [
                InlineKeyboardButton("Goal 6.0", callback_data="set:g6"),
                InlineKeyboardButton("Goal 7.0", callback_data="set:g7"),
                InlineKeyboardButton("Goal 8.0", callback_data="set:g8"),
            ],
            [InlineKeyboardButton("🏠 Menu", callback_data="m:home")],
        ]
    )


def ielts_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📚 IELTS lessons", callback_data="m:lesson")],
            [InlineKeyboardButton("📖 Reading", callback_data="il:read")],
            [InlineKeyboardButton("✍️ Task 1", callback_data="il:t1")],
            [InlineKeyboardButton("✍️ Task 2", callback_data="il:t2")],
            [InlineKeyboardButton("🗣️ Part 2 cue card", callback_data="il:p2")],
            [InlineKeyboardButton("🗣️ Part 3", callback_data="il:p3")],
            [InlineKeyboardButton("🏠 Menu", callback_data="m:home")],
        ]
    )


def stop_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("⏹ Finish & menu", callback_data="m:home")]])
