from __future__ import annotations

import logging
import time
from functools import wraps

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from . import ai, config
from . import teacher as teacher_mod
from .curriculum.exams import Exam, ExamItem, KINDS, build_exam, dump_exam, load_questions, shuffle_question
from .curriculum.grammar_rules import get_rule
from .curriculum.lessons import LESSONS, get_lesson, lessons_for_level, next_lesson
from .curriculum.levels import LEVEL_META, LEVELS
from .curriculum.models import Question
from .curriculum.placement import PLACEMENT, place_from_results
from .curriculum.reading import get_reading, readings_for_level
from .curriculum.skills import get_prompt, speaking_for_level, writing_for_level
from .curriculum.vocab import VOCAB, get_vocab, vocab_for_level
from .keyboards import (
    BTN_CONTINUE,
    BTN_COURSE,
    BTN_GRAMMAR,
    BTN_IELTS,
    BTN_LESSON,
    BTN_ME,
    BTN_MENU,
    BTN_PRACTICE,
    BTN_PROGRESS,
    BTN_READ,
    BTN_RULES,
    BTN_SETTINGS,
    BTN_SPEAK,
    BTN_TEST,
    BTN_TUTOR,
    BTN_TUTOR_OLD,
    BTN_VOCAB,
    BTN_WRITE,
    BUTTONS,
    after_teach_kb,
    course_kb,
    done_kb,
    exam_done_kb,
    exam_kb,
    home_kb,
    ielts_kb,
    level_lessons_kb,
    levels_kb,
    main_kb,
    mcq_kb,
    onboarding_kb,
    practice_kb,
    reveal_kb,
    rule_open_kb,
    rules_kb,
    settings_kb,
    stop_kb,
    teacher_after_teach_kb,
    teacher_kb,
    vocab_rate_kb,
)
from .store import Store
from .ui import (
    LEVEL_EMOJI,
    bar,
    course_overview,
    home_text,
    is_bangla,
    lesson_unlocked,
    level_map_text,
    next_track_line,
    quiz_card,
    result_card,
    tr,
)
from .util import answers_match, chunk, esc, join_goals

log = logging.getLogger("english-ladder")

XP_Q = 8
XP_LESSON = 40
XP_VOCAB = 6
XP_WRITE = 35
XP_SPEAK = 35
XP_PLACE = 20
XP_EXAM = 50


def store_of(ctx: ContextTypes.DEFAULT_TYPE) -> Store:
    return ctx.application.bot_data["store"]


def allowed(update: Update) -> bool:
    if not config.ALLOWED_USER_IDS:
        return True
    user = update.effective_user
    return bool(user and user.id in config.ALLOWED_USER_IDS)


def guard(fn):
    @wraps(fn)
    async def wrapper(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        if not allowed(update):
            uid = update.effective_user.id if update.effective_user else "?"
            if update.callback_query:
                await update.callback_query.answer("Private bot.", show_alert=True)
            elif update.effective_message:
                await update.effective_message.reply_text(f"This bot is private. Your id: {uid}")
            return
        user = update.effective_user
        if user:
            db = store_of(ctx)
            db.upsert_user(user.id, user.username, user.first_name)
            db.touch(user.id)
        try:
            if update.effective_chat:
                await ctx.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
            return await fn(update, ctx)
        except Exception:
            log.exception("handler %s failed", fn.__name__)
            if update.callback_query:
                await update.callback_query.answer("Something broke.", show_alert=True)
            elif update.effective_message:
                await update.effective_message.reply_text("Something broke. Try /menu.")

    return wrapper


async def send_html(update: Update, text: str, reply_markup=None, edit: bool | None = None) -> None:
    if edit is None:
        edit = bool(update.callback_query)
    parts = chunk(text)
    markup = reply_markup
    if edit and update.callback_query and update.callback_query.message and len(parts) == 1:
        try:
            await update.callback_query.edit_message_text(
                parts[0],
                parse_mode=ParseMode.HTML,
                reply_markup=markup,
                disable_web_page_preview=True,
            )
            return
        except BadRequest as exc:
            if "not modified" in str(exc).lower():
                return
        except Exception:
            pass
    chat = update.effective_chat
    if not chat:
        return
    bot = update.get_bot()
    for i, part in enumerate(parts):
        await bot.send_message(
            chat.id,
            part,
            parse_mode=ParseMode.HTML,
            reply_markup=markup if i == len(parts) - 1 else None,
            disable_web_page_preview=True,
        )


def uid_of(update: Update) -> int:
    user = update.effective_user
    assert user
    return user.id


def user_row(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> dict:
    row = store_of(ctx).get_user(uid_of(update))
    assert row
    return row


WELCOME_BN = (
    "🌱  <b>English Ladder</b>\n"
    "একদম শূন্য থেকে অ্যাডভান্সড ইংরেজি — তারপর IELTS।\n\n"
    "🌱 A1 beginner  →  🌿 A2  →  🌳 B1\n"
    "🏔️ B2  →  🎯 C1  →  🏆 IELTS Band 9\n\n"
    "প্রতিদিন: একটি পাঠ · কয়েকটা শব্দ · একটু কথা\n"
    "বাটনে ট্যাপ করুন। টাইপ করতে হবে না (শুধু লেখা/কথা অনুশীলনে)।"
)
WELCOME_EN = (
    "🌱  <b>English Ladder</b>\n"
    "A full English course — zero to advanced, then IELTS.\n\n"
    "🌱 A1 beginner  →  🌿 A2  →  🌳 B1\n"
    "🏔️ B2  →  🎯 C1  →  🏆 IELTS Band 9\n\n"
    "Every day: one lesson · a few words · a little speaking\n"
    "Tap the buttons. You only type for writing and speaking."
)


@guard
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    db.set_mode(tid, "idle")
    row = user_row(update, ctx)
    done = db.completed(tid)
    if done or int(row["xp"] or 0) > 0:
        await send_html(update, WELCOME_BN if is_bangla(row) else WELCOME_EN, main_kb(), edit=False)
        await send_home(update, ctx, edit=False)
        return
    welcome = WELCOME_BN if is_bangla(row) else WELCOME_EN
    await send_html(update, welcome, onboarding_kb(), edit=False)
    if update.effective_message:
        await update.effective_message.reply_text(
            "Keep this menu under your keyboard 👇",
            reply_markup=main_kb(),
        )


@guard
async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    row = user_row(update, ctx)
    await send_html(
        update,
        tr(
            row,
            "<b>How to learn</b>\n"
            "▶ Continue — next lesson in your course\n"
            "👩‍🏫 Teacher — teaches a point, then a NEW test every time\n"
            "📝 Test — more unique papers\n"
            "📘 Rules — basic grammar (A1–A2)\n"
            "🗺 Course — every unit, locked until you finish the one before\n"
            "🎯 Practice — words, grammar, reading, writing, speaking, IELTS\n"
            "💬 Tutor — chat and get corrections\n\n"
            "/test /rules /menu /stats /level /cancel",
            "<b>কীভাবে শিখবেন</b>\n"
            "▶ Continue — পরের পাঠ\n"
            "📝 Test — প্রতিবার নতুন প্রশ্নপত্র\n"
            "📘 Rules — বেসিক গ্রামার\n"
            "🗺 Course — পুরো কোর্স ম্যাপ\n"
            "🎯 Practice — শব্দ, গ্রামার, পড়া, লেখা, কথা, IELTS\n"
            "💬 Tutor — কথা বলে শুধরে নিন\n\n"
            "/test /rules /menu /stats /level /cancel",
        ),
        home_kb(),
    )


@guard
async def cmd_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    store_of(ctx).set_mode(uid_of(update), "idle")
    await send_home(update, ctx)


@guard
async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    store_of(ctx).set_mode(uid_of(update), "idle")
    await send_home(update, ctx)


@guard
async def cmd_level(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await send_html(update, "Choose your track:", levels_kb("lvl"))


@guard
async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await send_me(update, ctx)


@guard
async def cmd_test(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    store_of(ctx).set_mode(uid_of(update), "idle")
    await send_test_hub(update, ctx)


@guard
async def cmd_rules(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    store_of(ctx).set_mode(uid_of(update), "idle")
    await send_rules(update, ctx)


@guard
async def cmd_teacher(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    store_of(ctx).set_mode(uid_of(update), "idle")
    await send_teacher(update, ctx)


async def send_home(update: Update, ctx: ContextTypes.DEFAULT_TYPE, edit: bool | None = None) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    due, cards = db.card_count(tid)
    text = home_text(row, db.completed(tid), due, cards)
    await send_html(update, text, home_kb(), edit=edit)


async def send_me(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    row = user_row(update, ctx)
    tid = uid_of(update)
    right, total = db.accuracy(tid)
    due, cards = db.card_count(tid)
    done = db.completed(tid)
    all_lessons = list(LESSONS)
    finished_all = sum(1 for les in all_lessons if les.id in done)
    level = row["level"]
    lessons = lessons_for_level(level)
    finished = sum(1 for les in lessons if les.id in done)
    pct = f"{round(100 * right / total)}%" if total else "—"
    text = (
        f"<b>{tr(row, 'Your progress', 'আপনার অগ্রগতি')}</b>\n\n"
        f"{LEVEL_EMOJI.get(level, '📘')} {level} {LEVEL_META[level]['name']}\n"
        f"{bar(finished, len(lessons))}  {finished}/{len(lessons)} this level\n"
        f"{bar(finished_all, len(all_lessons))}  {finished_all}/{len(all_lessons)} whole course\n\n"
        f"🔥 streak  {row['streak']}   ·   ⭐ {row['xp']} XP\n"
        f"🎯 IELTS goal  {esc(str(row['goal_band']))}  (now ~{LEVEL_META[level]['ielts']})\n"
        f"✅ quiz accuracy  {right}/{total} ({pct})\n"
        f"🧠 words due  {due}/{cards}\n"
    )
    past = db.list_exams(tid, 3)
    if past:
        text += "\n<b>Last tests</b>\n" + "\n".join(
            f"<code>{esc(p['exam_id'])}</code>  {p['score']}/{p['total']}" for p in past
        )
    text += f"\n{next_track_line(level)}"
    await send_html(update, text, home_kb())


async def send_map(update: Update, ctx: ContextTypes.DEFAULT_TYPE, level: str | None = None) -> None:
    db = store_of(ctx)
    row = user_row(update, ctx)
    done = db.completed(uid_of(update))
    if not level:
        await send_html(update, course_overview(done, row["level"]), course_kb())
        return
    await send_html(update, level_map_text(level, done), level_lessons_kb(level, done))


async def send_practice(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    row = user_row(update, ctx)
    await send_html(
        update,
        tr(
            row,
            "<b>Practice gym</b>\nPick a skill. It matches your current level.",
            "<b>প্র্যাকটিস</b>\nআপনার লেভেল অনুযায়ী স্কিল বেছে নিন।",
        ),
        practice_kb(),
    )


def _exam_grade(score: int, total: int) -> str:
    pct = round(100 * score / total) if total else 0
    if pct >= 90:
        return "Distinction"
    if pct >= 75:
        return "Merit"
    if pct >= 50:
        return "Pass"
    return "Keep practising"


async def send_test_hub(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    row = user_row(update, ctx)
    tid = uid_of(update)
    past = db.list_exams(tid, 5)
    lines = [
        f"<b>{tr(row, 'Take a test', 'টেস্ট দিন')}</b>",
        tr(
            row,
            "Every paper is different — new questions and shuffled answers. Your last papers are not reused first.",
            "প্রতিবার নতুন প্রশ্নপত্র। আগের টেস্টের প্রশ্ন আগে আসবে না।",
        ),
        f"\n{LEVEL_EMOJI.get(row['level'], '📘')}  {tr(row, 'Your level', 'আপনার লেভেল')}: <b>{row['level']}</b>",
    ]
    if past:
        lines.append(f"\n<b>{tr(row, 'Recent papers', 'সাম্প্রতিক প্রশ্নপত্র')}</b>")
        for item in past:
            lines.append(
                f"<code>{esc(item['exam_id'])}</code>  {item['kind']}  {item['level']}  "
                f"{item['score']}/{item['total']}"
            )
    await send_html(update, "\n".join(lines), exam_kb())


async def start_exam(update: Update, ctx: ContextTypes.DEFAULT_TYPE, kind: str, topic: str | None = None) -> None:
    if kind not in KINDS:
        kind = "quick"
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    prev = db.payload(tid)
    topic = topic or (prev.get("topic") if kind == "teacher" else None)
    seed = f"{tid}:{kind}:{row['level']}:{topic}:{time.time_ns()}:{db.exam_count(tid)}"
    exam = build_exam(row["level"], kind, seed, db.recent_exam_item_ids(tid), topic=topic)
    payload = dump_exam(exam)
    if prev.get("teacher_n") is not None:
        payload["teacher_n"] = prev["teacher_n"]
    if topic:
        payload["topic"] = topic
    db.set_mode(tid, "exam", payload)
    title = f"Test {exam.exam_id}"
    intro = tr(
        row,
        f"Paper <b>{exam.exam_id}</b>  ·  {len(exam.items)} new questions\n"
        "Minted now — names, places, and order will not match your last paper.",
        f"প্রশ্নপত্র <b>{exam.exam_id}</b>  ·  {len(exam.items)}টা নতুন প্রশ্ন\n"
        "এখন তৈরি — আগের পেপারের মতো হবে না।",
    )
    await send_html(update, intro)
    await send_current_q(update, ctx, load_questions(payload), 0, title)


def _teacher_topic(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    n = int(db.payload(tid).get("teacher_n") or db.exam_count(tid))
    topic = teacher_mod.next_topic(row["level"], n)
    return n, topic


async def send_teacher(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    n, topic = _teacher_topic(update, ctx)
    db.set_mode(tid, "idle", {"teacher_n": n, "topic": topic.id})
    await send_html(
        update,
        tr(
            row,
            f"👩‍🏫  <b>Teacher</b>  ·  {row['level']}\n"
            "No API. I teach a point, then I mint a <b>new</b> test every time "
            "(new names, cities, verbs).\n\n"
            f"Today's topic: <b>{esc(topic.title)}</b>\n<i>{esc(topic.title_bn)}</i>",
            f"👩‍🏫  <b>টিচার</b>  ·  {row['level']}\n"
            "এপিআই লাগে না। আগে পড়াই, তারপর <b>নতুন</b> টেস্ট দেই।\n\n"
            f"আজকের টপিক: <b>{esc(topic.title)}</b>\n<i>{esc(topic.title_bn)}</i>",
        ),
        teacher_kb(),
    )


async def send_teacher_teach(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    n, topic = _teacher_topic(update, ctx)
    store_of(ctx).set_mode(uid_of(update), "idle", {"teacher_n": n, "topic": topic.id})
    body = teacher_mod.teach_text(topic)
    await send_html(
        update,
        body + "\n\n" + tr(user_row(update, ctx), "Now take a brand-new test on this.", "এখন এই টপিকে নতুন টেস্ট দিন।"),
        teacher_after_teach_kb(),
        edit=False,
    )


async def send_rules(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    row = user_row(update, ctx)
    await send_html(
        update,
        tr(
            row,
            "<b>Basic grammar rules</b>\n"
            "A1–A2 cards. Tap a rule, read it, then try 3 questions "
            "(order and options change each time).",
            "<b>বেসিক গ্রামার রুলস</b>\n"
            "A1–A2। একটি রুল খুলুন, পড়ুন, তারপর ৩টা প্রশ্ন "
            "(প্রতিবার নতুন অর্ডার)।",
        ),
        rules_kb(),
    )


async def open_rule(update: Update, ctx: ContextTypes.DEFAULT_TYPE, rule_id: str) -> None:
    rule = get_rule(rule_id)
    if not rule:
        await send_rules(update, ctx)
        return
    row = user_row(update, ctx)
    title = f"<b>{esc(rule.title)}</b>"
    if is_bangla(row):
        title += f"\n<i>{esc(rule.title_bn)}</i>"
    await send_html(update, f"{title}\n\n{rule.body}", rule_open_kb(rule.id), edit=False)


async def start_rule_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE, rule_id: str) -> None:
    import random

    rule = get_rule(rule_id)
    if not rule:
        await send_rules(update, ctx)
        return
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    seed = f"{tid}:rule:{rule_id}:{time.time_ns()}"
    rng = random.Random(seed)
    qs = list(rule.questions)
    rng.shuffle(qs)
    items = tuple(
        ExamItem(id=f"rule-{rule_id}-{i}", level="A1", question=shuffle_question(q, rng))
        for i, q in enumerate(qs)
    )
    exam = Exam(exam_id=_short_code(seed), kind="rule", level=row["level"], seed=seed, items=items)
    payload = dump_exam(exam)
    db.set_mode(tid, "exam", payload)
    await send_current_q(update, ctx, load_questions(payload), 0, rule.title)


def _short_code(seed: str) -> str:
    from .curriculum.exams import _code

    return _code(seed)


# --------------------------------------------------------------------------- quizzes


def _check(q: Question, raw: str) -> bool:
    if q.options:
        if raw.isdigit() and 0 <= int(raw) < len(q.options):
            return raw == q.answer
        for i, opt in enumerate(q.options):
            if answers_match(opt, raw) and str(i) == q.answer:
                return True
        return answers_match(q.options[int(q.answer)], raw) if q.answer.isdigit() else False
    return answers_match(q.answer, raw)


def _correct_label(q: Question) -> str:
    if q.options and q.answer.isdigit():
        i = int(q.answer)
        return q.options[i]
    return q.answer.split("|")[0]


def _q_prompt(q: Question) -> str:
    if q.options:
        return q.prompt
    return f"{q.prompt}\n\n<i>Type the missing word.</i>"


async def send_current_q(
    update: Update,
    ctx: ContextTypes.DEFAULT_TYPE,
    questions: tuple[Question, ...] | list[Question],
    index: int,
    title: str,
    result: str | None = None,
) -> None:
    q = questions[index]
    text = quiz_card(title, index, len(questions), _q_prompt(q), result)
    await send_html(update, text, mcq_kb(q))


def _quiz_bank(mode: str, payload: dict) -> tuple[tuple[Question, ...] | list[Question], str, str, str] | None:
    if mode == "placement":
        return PLACEMENT, "Find your level", "placement", "place"
    if mode == "lesson_quiz":
        lesson = get_lesson(payload.get("lesson_id", ""))
        if not lesson:
            return None
        return lesson.questions, lesson.title.split("—")[0].strip(), "lesson", lesson.id
    if mode == "grammar":
        return payload_questions(payload), "Grammar", "grammar", "grammar"
    if mode == "reading":
        reading = get_reading(payload.get("reading_id", ""))
        if not reading:
            return None
        return reading.questions, reading.title, "reading", reading.id
    if mode == "exam":
        questions = load_questions(payload)
        title = f"Test {payload.get('exam_id', '')}"
        if payload.get("kind") == "rule":
            title = "Grammar check"
        return questions, title, "exam", str(payload.get("exam_id") or "exam")
    return None


async def advance_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE, raw: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    payload = db.payload(tid)
    mode = row["mode"]
    bank = _quiz_bank(mode, payload)
    if not bank:
        return
    questions, title, kind, item_prefix = bank
    index = int(payload.get("q") or 0)
    score = int(payload.get("score") or 0)
    if index >= len(questions):
        return
    q = questions[index]
    if raw == "hint":
        hint = q.explain
        await send_html(update, quiz_card(title, index, len(questions), f"{_q_prompt(q)}\n\n💡 {esc(hint)}"), mcq_kb(q))
        return
    ok = False if raw == "skip" else _check(q, raw)
    db.log_attempt(tid, kind, f"{item_prefix}:{index}", ok)
    gained = 0
    if ok:
        score += 1
        gained = XP_Q
        db.add_xp(tid, gained)
    flags = list(payload.get("flags") or [])
    if mode == "placement":
        flags.append(bool(ok))
        payload["flags"] = flags
    if ok:
        result = f"✅  <b>{tr(row, 'Correct', 'ঠিক')}</b>  ·  +{gained} XP\n<i>{esc(q.explain)}</i>"
    else:
        result = (
            f"❌  <b>{tr(row, 'Not quite', 'ভুল')}</b>  ·  {esc(_correct_label(q))}\n"
            f"<i>{esc(q.explain)}</i>"
        )
    index += 1
    if index < len(questions):
        payload["q"] = index
        payload["score"] = score
        db.set_mode(tid, mode, payload)
        await send_current_q(update, ctx, questions, index, title, result)
        return

    db.set_mode(tid, "idle")
    total = len(questions)
    if mode == "placement":
        level = place_from_results(flags)
        db.set_level(tid, level)
        db.add_xp(tid, XP_PLACE)
        meta = LEVEL_META[level]
        extra = (
            f"\n{LEVEL_EMOJI.get(level, '📘')}  You start at <b>{level}</b> {esc(meta['name'])}\n"
            f"IELTS ~ {meta['ielts']}\n<i>{esc(meta['blurb'])}</i>"
        )
        await send_html(
            update,
            result_card(tr(row, "Placement complete", "লেভেল ঠিক হয়েছে"), score, total, XP_PLACE + score * XP_Q, extra),
            done_kb(level),
        )
        return
    if mode == "lesson_quiz":
        lesson = get_lesson(payload.get("lesson_id", ""))
        if lesson:
            db.mark_complete(tid, lesson.id)
            db.add_xp(tid, XP_LESSON)
            for word, _meaning, _ex in lesson.vocab:
                item = next((v for v in VOCAB if v.word.lower() == word.lower()), None)
                if item:
                    db.ensure_card(tid, item.id)
            remaining = [les for les in lessons_for_level(lesson.level) if les.id not in db.completed(tid)]
            extra = "\n" + tr(row, "New words went to Words practice.", "নতুন শব্দ Words-এ গেছে।")
            if not remaining:
                extra += next_track_line(lesson.level)
            await send_html(
                update,
                result + "\n────────\n" + result_card(lesson.title.split("—")[0].strip(), score, total, XP_LESSON, extra),
                done_kb(lesson.level),
            )
        return
    if mode == "exam":
        exam_id = str(payload.get("exam_id") or "EL")
        kind = str(payload.get("kind") or "quick")
        level = str(payload.get("level") or row["level"])
        item_ids = [str(it.get("id")) for it in (payload.get("items") or [])]
        db.save_exam(tid, exam_id, kind, level, score, total, item_ids)
        db.add_xp(tid, XP_EXAM)
        extra = (
            f"\nPaper <code>{esc(exam_id)}</code>  ·  {_exam_grade(score, total)}\n"
            + tr(
                row,
                "Take another test — you will get a different paper.",
                "আবার টেস্ট দিন — নতুন প্রশ্নপত্র পাবেন।",
            )
        )
        await send_html(
            update,
            result + "\n────────\n" + result_card(f"Test {exam_id}", score, total, XP_EXAM, extra),
            exam_done_kb(),
        )
        return
    await send_html(update, result + "\n────────\n" + result_card(title, score, total, score * XP_Q), done_kb())


def payload_questions(payload: dict) -> list[Question]:
    ids = payload.get("qids") or []
    bank = {f"{les.id}:{i}": q for les in LESSONS for i, q in enumerate(les.questions)}
    return [bank[key] for key in ids if key in bank]


async def start_placement(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    db.set_mode(uid_of(update), "placement", {"q": 0, "score": 0, "flags": []})
    row = user_row(update, ctx)
    await send_html(
        update,
        tr(row, "12 quick questions. Skip if you don't know.", "১২টা ছোট প্রশ্ন। না জানলে Skip."),
        None,
    )
    await send_current_q(update, ctx, PLACEMENT, 0, "Find your level")


# --------------------------------------------------------------------------- lessons


async def open_lesson(update: Update, ctx: ContextTypes.DEFAULT_TYPE, lesson_id: str) -> None:
    lesson = get_lesson(lesson_id)
    if not lesson:
        await send_html(update, "Lesson missing.", home_kb())
        return
    db = store_of(ctx)
    tid = uid_of(update)
    done = db.completed(tid)
    pack = lessons_for_level(lesson.level)
    if lesson.id not in done and not lesson_unlocked(pack, lesson.id, done):
        if update.callback_query:
            await update.callback_query.answer(
                tr(user_row(update, ctx), "Finish the previous lesson first.", "আগে আগের পাঠ শেষ করুন।"),
                show_alert=True,
            )
        return
    db.set_level(tid, lesson.level)
    db.set_mode(tid, "idle", {"lesson_id": lesson.id})
    goals = join_goals(lesson.goals)
    body = (
        f"{lesson.teach}\n\n"
        f"<b>{tr(user_row(update, ctx), 'You will', 'আজ শিখবেন')}</b>\n{goals}\n"
        f"⏱ {lesson.minutes} min"
    )
    await send_html(update, body, after_teach_kb(lesson.id), edit=False)


async def start_lesson(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    row = user_row(update, ctx)
    tid = uid_of(update)
    lesson = next_lesson(row["level"], db.completed(tid))
    if not lesson:
        nxt_level = None
        from .curriculum.levels import next_level as _next

        nxt_level = _next(row["level"])
        if nxt_level:
            db.set_level(tid, nxt_level)
            await send_html(
                update,
                tr(
                    row,
                    f"Level {row['level']} complete. Starting <b>{nxt_level}</b>.",
                    f"{row['level']} শেষ। এখন <b>{nxt_level}</b>.",
                ),
                done_kb(nxt_level),
            )
            await open_lesson(update, ctx, lessons_for_level(nxt_level)[0].id)
            return
        await send_html(
            update,
            tr(row, "You finished the ladder. Use IELTS practice every day.", "কোর্স শেষ। প্রতিদিন IELTS প্র্যাকটিস করুন।"),
            practice_kb(),
        )
        return
    await open_lesson(update, ctx, lesson.id)


async def start_lesson_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE, lesson_id: str) -> None:
    lesson = get_lesson(lesson_id)
    if not lesson:
        await send_html(update, "Lesson missing.", home_kb())
        return
    store_of(ctx).set_mode(uid_of(update), "lesson_quiz", {"lesson_id": lesson_id, "q": 0, "score": 0})
    await send_current_q(update, ctx, lesson.questions, 0, lesson.title.split("—")[0].strip())


# --------------------------------------------------------------------------- vocab / skills


async def start_vocab(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    for item in vocab_for_level(row["level"]):
        db.ensure_card(tid, item.id)
    due = db.due_cards(tid, 12)
    if not due:
        await send_html(
            update,
            tr(row, "No words due. Finish a lesson to add new cards.", "এখন কোনো শব্দ বাকি নেই। একটি পাঠ শেষ করুন।"),
            home_kb(),
        )
        return
    card = due[0]
    db.set_mode(tid, "vocab", {"word_id": card["word_id"]})
    item = get_vocab(card["word_id"])
    if not item:
        await send_html(update, "Card missing.", home_kb())
        return
    due_n, total = db.card_count(tid)
    await send_html(
        update,
        f"<b>{tr(row, 'Words', 'শব্দ')}</b>  ·  {due_n} due / {total}\n"
        f"{bar(0, max(due_n, 1))}\n\n"
        f"<b>{esc(item.word)}</b>\n"
        f"{tr(row, 'Think of the meaning, then reveal.', 'অর্থ ভাবুন, তারপর Show চাপুন।')}",
        reveal_kb(),
    )


async def vocab_show(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    payload = db.payload(uid_of(update))
    item = get_vocab(payload.get("word_id", ""))
    if not item:
        await start_vocab(update, ctx)
        return
    extra = f"\n{esc(item.extra)}" if item.extra else ""
    await send_html(
        update,
        f"<b>{esc(item.word)}</b>\n{esc(item.meaning)}\n<i>{esc(item.example)}</i>{extra}\n\n"
        f"{tr(user_row(update, ctx), 'How easy was that?', 'কত সহজ লেগেছে?')}",
        vocab_rate_kb(),
    )


async def vocab_rate(update: Update, ctx: ContextTypes.DEFAULT_TYPE, quality: int) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    word_id = db.payload(tid).get("word_id")
    if word_id:
        db.review_card(tid, word_id, quality)
        if quality >= 4:
            db.add_xp(tid, XP_VOCAB)
    await start_vocab(update, ctx)


async def start_grammar(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    row = user_row(update, ctx)
    bank = [f"{les.id}:{i}" for les in lessons_for_level(row["level"]) for i, _q in enumerate(les.questions)]
    if not bank:
        await send_html(update, "No grammar items.", home_kb())
        return
    _, total = store_of(ctx).accuracy(uid_of(update), "grammar")
    start = total % len(bank)
    picked = (bank + bank)[start : start + 5]
    questions = payload_questions({"qids": picked})
    store_of(ctx).set_mode(uid_of(update), "grammar", {"qids": picked, "q": 0, "score": 0})
    await send_current_q(update, ctx, questions, 0, "Grammar")


async def start_reading(update: Update, ctx: ContextTypes.DEFAULT_TYPE, level: str | None = None, listen: bool = False) -> None:
    row = user_row(update, ctx)
    lvl = level or row["level"]
    pack = readings_for_level(lvl) or readings_for_level("A1")
    if not pack:
        await send_html(update, "No reading yet.", home_kb())
        return
    reading = pack[0]
    store_of(ctx).set_mode(
        uid_of(update), "reading", {"reading_id": reading.id, "q": 0, "score": 0}
    )
    label = tr(row, "Listen & read", "শুনে পড়ুন") if listen else tr(row, "Reading", "পড়া")
    hint = (
        tr(row, "Read this aloud slowly. Then start the quiz.", "এটা আস্তে আস্তে জোরে পড়ুন। তারপর কুইজ।")
        if listen
        else tr(row, "Read carefully, then start the quiz.", "মন দিয়ে পড়ুন, তারপর কুইজ।")
    )
    await send_html(
        update,
        f"🎧 <b>{label} · {esc(reading.title)}</b>\n\n{esc(reading.text)}\n\n<i>{hint}</i>",
        after_teach_kb(reading.id),
        edit=False,
    )


async def start_prompt(update: Update, ctx: ContextTypes.DEFAULT_TYPE, skill: str, prompt_id: str | None = None) -> None:
    row = user_row(update, ctx)
    items = writing_for_level(row["level"]) if skill == "writing" else speaking_for_level(row["level"])
    prompt = get_prompt(prompt_id) if prompt_id else (items[0] if items else None)
    if not prompt:
        await send_html(update, "No prompt at this level.", home_kb())
        return
    mode = "writing" if skill == "writing" else "speaking"
    store_of(ctx).set_mode(uid_of(update), mode, {"prompt_id": prompt.id})
    tips = "\n".join(f"• {t}" for t in prompt.tips)
    voice = (
        "\n" + tr(row, "Type your answer (or use Telegram voice-to-text).", "উত্তর টাইপ করুন।")
        if skill == "speaking"
        else ""
    )
    await send_html(
        update,
        f"<b>{esc(prompt.title)}</b>  ·  {prompt.minutes} min\n\n"
        f"{esc(prompt.cue)}\n\n<b>Tips</b>\n{esc(tips)}{voice}",
        stop_kb(),
        edit=False,
    )


async def start_tutor(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    db.set_mode(tid, "chat", {})
    row = user_row(update, ctx)
    await send_html(
        update,
        tr(
            row,
            f"<b>Tutor</b> · {row['level']}\nWorks offline. Send a sentence — I correct it.\n"
            "Try: <i>I go yesterday market.</i>  or  <i>what is however</i>",
            f"<b>Tutor</b> · {row['level']}\nঅফলাইন। একটি বাক্য লিখুন — আমি শুধরে দেব।\n"
            "চেষ্টা: <i>I go yesterday market.</i>  বা  <i>what is however</i>",
        ),
        stop_kb(),
        edit=False,
    )


async def handle_writing(update: Update, ctx: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    prompt = get_prompt(db.payload(tid).get("prompt_id", ""))
    if not prompt:
        db.set_mode(tid, "idle")
        return
    await send_html(update, tr(row, "Checking your writing…", "লেখা দেখছি…"), edit=False)
    feedback = ai.grade_writing(text, prompt.cue, row["level"], row["native_lang"])
    db.add_xp(tid, XP_WRITE)
    db.log_attempt(tid, "writing", prompt.id, True, None)
    db.set_mode(tid, "idle")
    await send_html(update, feedback, done_kb(), edit=False)


async def handle_speaking(update: Update, ctx: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    prompt = get_prompt(db.payload(tid).get("prompt_id", ""))
    if not prompt:
        db.set_mode(tid, "idle")
        return
    await send_html(update, tr(row, "Marking your speaking…", "উত্তর দেখছি…"), edit=False)
    feedback = ai.grade_speaking(text, prompt.cue, row["level"], row["native_lang"])
    db.add_xp(tid, XP_SPEAK)
    db.log_attempt(tid, "speaking", prompt.id, True, None)
    db.set_mode(tid, "idle")
    await send_html(update, feedback, done_kb(), edit=False)


async def handle_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    db.add_chat(tid, "user", text)
    reply = ai.complete(db.chat_history(tid), row["level"], row["native_lang"], "tutor")
    db.add_chat(tid, "assistant", reply)
    await send_html(update, reply, stop_kb(), edit=False)


# --------------------------------------------------------------------------- routers


def _route_button(text: str) -> str | None:
    mapping = {
        BTN_CONTINUE: "m:continue",
        BTN_TEST: "m:test",
        BTN_COURSE: "m:map",
        BTN_RULES: "m:rules",
        BTN_PRACTICE: "m:practice",
        BTN_TUTOR: "m:teacher",
        BTN_TUTOR_OLD: "m:teacher",
        BTN_ME: "m:me",
        BTN_MENU: "m:home",
        BTN_LESSON: "m:continue",
        BTN_VOCAB: "p:vocab",
        BTN_GRAMMAR: "p:grammar",
        BTN_READ: "p:read",
        BTN_WRITE: "p:write",
        BTN_SPEAK: "p:speak",
        BTN_IELTS: "p:ielts",
        BTN_PROGRESS: "m:me",
        BTN_SETTINGS: "m:set",
    }
    return mapping.get(text)


@guard
async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    if not msg or not msg.text:
        return
    text = msg.text.strip()
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)

    route = _route_button(text)
    if text in BUTTONS or route:
        db.set_mode(tid, "idle")
        await dispatch(update, ctx, route or "m:home")
        return

    mode = row["mode"]
    if mode in {"placement", "lesson_quiz", "grammar", "reading", "exam"}:
        await advance_quiz(update, ctx, text)
        return
    if mode == "writing":
        await handle_writing(update, ctx, text)
        return
    if mode == "speaking":
        await handle_speaking(update, ctx, text)
        return
    if mode == "chat":
        await handle_chat(update, ctx, text)
        return
    await send_home(update, ctx, edit=False)


@guard
async def on_voice(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    row = user_row(update, ctx)
    if row["mode"] not in {"speaking", "chat"}:
        await send_html(
            update,
            tr(row, "Voice is for Speaking or Tutor. Type your answer here.", "ভয়েস Speaking বা Tutor-এ। এখানে টাইপ করুন।"),
            edit=False,
        )
        return
    await send_html(
        update,
        tr(
            row,
            "Type what you said (or use Telegram’s voice-to-text).",
            "যা বলেছেন সেটা টাইপ করে পাঠান।",
        ),
        edit=False,
    )


async def dispatch(update: Update, ctx: ContextTypes.DEFAULT_TYPE, data: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)

    if data == "m:home":
        db.set_mode(tid, "idle")
        await send_home(update, ctx)
        return
    if data == "m:continue":
        await start_lesson(update, ctx)
        return
    if data == "m:map":
        await send_map(update, ctx)
        return
    if data == "m:practice":
        await send_practice(update, ctx)
        return
    if data == "m:test":
        await send_test_hub(update, ctx)
        return
    if data == "m:rules":
        await send_rules(update, ctx)
        return
    if data.startswith("t:") and data.split(":", 1)[1] in KINDS:
        await start_exam(update, ctx, data.split(":", 1)[1])
        return
    if data.startswith("ruleq:"):
        await start_rule_quiz(update, ctx, data.split(":", 1)[1])
        return
    if data.startswith("rule:"):
        await open_rule(update, ctx, data.split(":", 1)[1])
        return
    if data == "m:teacher":
        await send_teacher(update, ctx)
        return
    if data == "th:teach":
        await send_teacher_teach(update, ctx)
        return
    if data == "th:test":
        await start_exam(update, ctx, "teacher")
        return
    if data == "th:next":
        db = store_of(ctx)
        tid = uid_of(update)
        n = int(db.payload(tid).get("teacher_n") or 0) + 1
        db.set_mode(tid, "idle", {"teacher_n": n})
        await send_teacher(update, ctx)
        return
    if data == "m:tutor":
        await start_tutor(update, ctx)
        return
    if data == "m:me":
        await send_me(update, ctx)
        return
    if data == "m:set":
        await send_html(
            update,
            tr(row, "Settings — level, language, IELTS goal.", "সেটিংস — লেভেল, ভাষা, IELTS টার্গেট।"),
            settings_kb(row),
        )
        return
    if data == "m:lesson":
        await start_lesson(update, ctx)
        return
    if data == "ob:place":
        await start_placement(update, ctx)
        return
    if data in {"ob:A1", "ob:IELTS"}:
        level = data.split(":")[1]
        db.set_level(tid, level)
        await send_html(
            update,
            tr(
                row,
                f"You are on <b>{level}</b> — {LEVEL_META[level]['name']}. Tap Continue.",
                f"আপনি <b>{level}</b> — {LEVEL_META[level]['name']}। Continue চাপুন।",
            ),
            home_kb(),
        )
        return
    if data == "ob:pick":
        await send_html(update, tr(row, "Choose a level:", "লেভেল বাছুন:"), levels_kb("lvl"))
        return
    if data.startswith("lvl:"):
        level = data.split(":", 1)[1]
        if level in LEVELS:
            db.set_level(tid, level)
            await send_html(update, f"{LEVEL_EMOJI.get(level, '')}  Level set to <b>{level}</b>.", home_kb())
        return
    if data.startswith("map:"):
        await send_map(update, ctx, data.split(":", 1)[1])
        return
    if data.startswith("lsn:open:"):
        await open_lesson(update, ctx, data.split(":", 2)[2])
        return
    if data.startswith("lsn:quiz:"):
        lesson_id = data.split(":", 2)[2]
        if lesson_id.startswith("read-"):
            reading = get_reading(lesson_id)
            if reading:
                db.set_mode(tid, "reading", {"reading_id": reading.id, "q": 0, "score": 0})
                await send_current_q(update, ctx, reading.questions, 0, reading.title)
            return
        await start_lesson_quiz(update, ctx, lesson_id)
        return
    if data.startswith("ans:"):
        await advance_quiz(update, ctx, data.split(":", 1)[1])
        return
    if data == "v:show":
        await vocab_show(update, ctx)
        return
    if data == "v:skip":
        await vocab_rate(update, ctx, 1)
        return
    if data.startswith("v:") and data[2:].isdigit():
        await vocab_rate(update, ctx, int(data.split(":")[1]))
        return
    if data == "set:level":
        await send_html(update, tr(row, "Pick a track:", "ট্র্যাক বাছুন:"), levels_kb("lvl"))
        return
    if data == "set:bn":
        db.set_native(tid, "bn")
        await send_html(update, "🇧🇩 Bangla help on.", home_kb())
        return
    if data == "set:en":
        db.set_native(tid, "en")
        await send_html(update, "🇬🇧 Feedback in English only.", home_kb())
        return
    if data.startswith("set:g"):
        band = {"set:g6": "6.0", "set:g7": "7.0", "set:g8": "8.0"}[data]
        db.set_goal(tid, band)
        await send_html(update, f"🎯 IELTS goal {band}.", home_kb())
        return
    if data == "p:vocab":
        await start_vocab(update, ctx)
        return
    if data == "p:grammar":
        await start_grammar(update, ctx)
        return
    if data == "p:read":
        await start_reading(update, ctx)
        return
    if data == "p:listen":
        await start_reading(update, ctx, listen=True)
        return
    if data == "p:write":
        await start_prompt(update, ctx, "writing")
        return
    if data == "p:speak":
        await start_prompt(update, ctx, "speaking")
        return
    if data == "p:ielts":
        await send_html(
            update,
            tr(row, "<b>IELTS gym</b>\nFour papers, Band 6–9.", "<b>IELTS</b>\nচার পেপার, ব্যান্ড ৬–৯।"),
            ielts_kb(),
        )
        return
    if data == "il:read":
        await start_reading(update, ctx, "IELTS")
        return
    if data == "il:t1":
        await start_prompt(update, ctx, "writing", "w-ielts-t1")
        return
    if data == "il:t2":
        await start_prompt(update, ctx, "writing", "w-ielts-t2")
        return
    if data == "il:p2":
        await start_prompt(update, ctx, "speaking", "s-ielts-p2")
        return
    if data == "il:p3":
        await start_prompt(update, ctx, "speaking", "s-ielts-p3")
        return
    log.info("unknown callback %s from %s", data, tid)


@guard
async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()
    await dispatch(update, ctx, query.data)
