from __future__ import annotations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup

from .curriculum.lessons import get_lesson, lessons_for_level
from .curriculum.levels import LEVELS, LEVEL_META
from .curriculum.models import Question
from .ui import LEVEL_EMOJI, lesson_unlocked

BTN_CONTINUE = "▶ Continue"
BTN_TEST = "📝 Test"
BTN_COURSE = "🗺 Course"
BTN_RULES = "📘 Rules"
BTN_PRACTICE = "🎯 Practice"
BTN_TUTOR = "👩‍🏫 Teacher"
BTN_TUTOR_OLD = "💬 Tutor"
BTN_ME = "👤 Me"

# Keep old labels so existing chats still work
BTN_LESSON = "📚 Lesson"
BTN_VOCAB = "🧠 Vocab"
BTN_GRAMMAR = "✏️ Grammar"
BTN_READ = "📖 Reading"
BTN_WRITE = "✍️ Writing"
BTN_SPEAK = "🗣️ Speaking"
BTN_IELTS = "🎯 IELTS"
BTN_PROGRESS = "📊 Progress"
BTN_SETTINGS = "⚙️ Settings"
BTN_MENU = "🏠 Menu"

MAIN_ROWS = (
    (BTN_CONTINUE, BTN_TEST),
    (BTN_COURSE, BTN_RULES),
    (BTN_PRACTICE, BTN_TUTOR),
    (BTN_ME,),
)

MAIN_KEYBOARD = ReplyKeyboardMarkup(MAIN_ROWS, resize_keyboard=True, is_persistent=True)

BUTTONS = {btn for row in MAIN_ROWS for btn in row} | {
    BTN_MENU,
    BTN_LESSON,
    BTN_VOCAB,
    BTN_GRAMMAR,
    BTN_READ,
    BTN_WRITE,
    BTN_SPEAK,
    BTN_IELTS,
    BTN_PROGRESS,
    BTN_SETTINGS,
    BTN_TUTOR_OLD,
}


def main_kb() -> ReplyKeyboardMarkup:
    return MAIN_KEYBOARD


def B(text: str, data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text, callback_data=data)


def home_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("👩‍🏫  Teacher — new test", "m:teacher")],
            [B("▶  Continue lesson", "m:continue")],
            [B("📝  Take a test", "m:test"), B("📘  Grammar rules", "m:rules")],
            [B("🗺  Course map", "m:map"), B("🎯  Practice", "m:practice")],
            [B("👤  Progress", "m:me"), B("⚙️  Settings", "m:set")],
        ]
    )


def onboarding_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("📝  Find my level  ·  লেভেল মাপো", "ob:place")],
            [B("🌱  Start from zero  ·  A1", "ob:A1")],
            [B("🏆  I want IELTS", "ob:IELTS")],
            [B("📂  Choose a level", "ob:pick")],
        ]
    )


def levels_kb(prefix: str = "lvl") -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for level in LEVELS:
        emoji = LEVEL_EMOJI.get(level, "📘")
        label = f"{emoji} {level}"
        row.append(B(label, f"{prefix}:{level}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([B("🏠 Home", "m:home")])
    return InlineKeyboardMarkup(rows)


def course_kb() -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    for level in LEVELS:
        row.append(B(f"{LEVEL_EMOJI.get(level, '📘')} {level}", f"map:{level}"))
        if len(row) == 3:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    rows.append([B("🏠 Home", "m:home")])
    return InlineKeyboardMarkup(rows)


def level_lessons_kb(level: str, completed: list[str]) -> InlineKeyboardMarkup:
    lessons = lessons_for_level(level)
    rows: list[list[InlineKeyboardButton]] = []
    for les in lessons:
        short = les.title.split("—")[0].strip()
        if len(short) > 28:
            short = short[:27] + "…"
        if les.id in completed:
            label = f"✅ {les.unit}. {short}"
        elif lesson_unlocked(lessons, les.id, completed):
            label = f"▶ {les.unit}. {short}"
        else:
            label = f"🔒 {les.unit}. {short}"
        rows.append([B(label, f"lsn:open:{les.id}")])
    rows.append([B("‹ Course", "m:map"), B("🏠 Home", "m:home")])
    return InlineKeyboardMarkup(rows)


def after_teach_kb(lesson_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("✅  Start quiz", f"lsn:quiz:{lesson_id}")],
            [B("🗺  Course", f"map:{ (get_lesson(lesson_id).level if get_lesson(lesson_id) else 'A1') }"), B("🏠 Home", "m:home")],
        ]
    )


def mcq_kb(q: Question) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []
    if q.options:
        for i, opt in enumerate(q.options):
            label = opt if len(opt) <= 56 else opt[:55] + "…"
            rows.append([B(label, f"ans:{i}")])
    else:
        rows.append([B("💡 Hint", "ans:hint")])
    rows.append([B("⏭ Skip", "ans:skip"), B("🏠 Home", "m:home")])
    return InlineKeyboardMarkup(rows)


def vocab_rate_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [
                B("🔁 Again", "v:1"),
                B("😅 Hard", "v:3"),
                B("👍 Good", "v:4"),
                B("⚡ Easy", "v:5"),
            ],
            [B("🏠 Home", "m:home")],
        ]
    )


def reveal_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("👁  Show meaning  ·  অর্থ", "v:show")],
            [B("⏭ Skip", "v:skip"), B("🏠 Home", "m:home")],
        ]
    )


def practice_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("🧠  Words", "p:vocab"), B("✏️  Grammar", "p:grammar")],
            [B("📖  Reading", "p:read"), B("🎧  Listen & read", "p:listen")],
            [B("✍️  Writing", "p:write"), B("🗣️  Speaking", "p:speak")],
            [B("🏆  IELTS gym", "p:ielts")],
            [B("📝  Take a test", "m:test"), B("📘  Grammar rules", "m:rules")],
            [B("🏠 Home", "m:home")],
        ]
    )


def settings_kb(row: dict | None = None) -> InlineKeyboardMarkup:
    lang = (row or {}).get("native_lang", "bn")
    bn = "🇧🇩 Bangla · ON" if str(lang).lower() in {"bn", "bangla", "bengali"} else "🇧🇩 Bangla help"
    en = "🇬🇧 English only · ON" if str(lang).lower() in {"en", "english"} else "🇬🇧 English only"
    return InlineKeyboardMarkup(
        [
            [B("📈  Change level", "set:level")],
            [B(bn, "set:bn"), B(en, "set:en")],
            [B("Goal 6.0", "set:g6"), B("Goal 7.0", "set:g7"), B("Goal 8.0", "set:g8")],
            [B("🏠 Home", "m:home")],
        ]
    )


def ielts_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("📚  IELTS lessons", "map:IELTS")],
            [B("📖  Reading", "il:read")],
            [B("✍️  Task 1", "il:t1"), B("✍️  Task 2", "il:t2")],
            [B("🗣️  Part 2", "il:p2"), B("🗣️  Part 3", "il:p3")],
            [B("‹ Practice", "m:practice"), B("🏠 Home", "m:home")],
        ]
    )


def exam_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("👩‍🏫  Teacher test  ·  8 new Qs", "t:teacher")],
            [B("⚡  Quick test  ·  10 new Qs", "t:quick")],
            [B("📋  Level test  ·  15 new Qs", "t:level")],
            [B("🌱  Basic grammar test  ·  12 Qs", "t:basic")],
            [B("🌈  Mixed test  ·  20 Qs", "t:mixed")],
            [B("🏠 Home", "m:home")],
        ]
    )


def teacher_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("📖  Teach this + new test", "th:teach")],
            [B("📝  Surprise new test", "th:test")],
            [B("⏭  Next topic", "th:next"), B("✍️  Check a sentence", "m:tutor")],
            [B("🏠 Home", "m:home")],
        ]
    )


def teacher_after_teach_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("✅  Start a NEW test on this", "th:test")],
            [B("⏭  Next topic", "th:next"), B("🏠 Home", "m:home")],
        ]
    )


def rules_kb() -> InlineKeyboardMarkup:
    from .curriculum.grammar_rules import BASIC_RULES

    rows: list[list[InlineKeyboardButton]] = []
    for i, rule in enumerate(BASIC_RULES, start=1):
        rows.append([B(f"{i}. {rule.title}", f"rule:{rule.id}")])
    rows.append([B("📝  Basic grammar test", "t:basic"), B("🏠 Home", "m:home")])
    return InlineKeyboardMarkup(rows)


def rule_open_kb(rule_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("✅  Try 3 questions", f"ruleq:{rule_id}")],
            [B("‹ All rules", "m:rules"), B("🏠 Home", "m:home")],
        ]
    )


def exam_done_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [B("👩‍🏫  Another NEW teacher test", "th:test")],
            [B("📝  More tests", "m:test")],
            [B("📘  Grammar rules", "m:rules"), B("🏠 Home", "m:home")],
        ]
    )


def stop_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[B("⏹  Finish", "m:home")]])


def done_kb(level: str | None = None) -> InlineKeyboardMarkup:
    rows = [[B("▶  Continue", "m:continue")]]
    if level:
        rows.append([B("🗺  This level", f"map:{level}"), B("🏠 Home", "m:home")])
    else:
        rows.append([B("🏠 Home", "m:home")])
    return InlineKeyboardMarkup(rows)
