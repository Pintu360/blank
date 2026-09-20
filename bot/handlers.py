from __future__ import annotations

import logging
from functools import wraps

from telegram import Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import ContextTypes

from . import ai, config
from .curriculum.lessons import LESSONS, get_lesson, lessons_for_level, next_lesson
from .curriculum.levels import LEVEL_META, LEVELS, ielts_range, next_level
from .curriculum.models import Question
from .curriculum.placement import PLACEMENT, place_from_results
from .curriculum.reading import get_reading, readings_for_level
from .curriculum.skills import get_prompt, speaking_for_level, writing_for_level
from .curriculum.vocab import VOCAB, get_vocab, vocab_for_level
from .keyboards import (
    BTN_GRAMMAR,
    BTN_IELTS,
    BTN_LESSON,
    BTN_MENU,
    BTN_PROGRESS,
    BTN_READ,
    BTN_SETTINGS,
    BTN_SPEAK,
    BTN_TUTOR,
    BTN_VOCAB,
    BTN_WRITE,
    BUTTONS,
    after_teach_kb,
    ielts_kb,
    levels_kb,
    main_kb,
    mcq_kb,
    onboarding_kb,
    reveal_kb,
    settings_kb,
    stop_kb,
    vocab_rate_kb,
)
from .store import Store
from .util import answers_match, chunk, esc, join_goals

log = logging.getLogger("english-ladder")

XP_Q = 8
XP_LESSON = 40
XP_VOCAB = 6
XP_WRITE = 35
XP_SPEAK = 35
XP_PLACE = 20


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
            msg = update.effective_message
            if update.callback_query:
                await update.callback_query.answer("Private bot.", show_alert=True)
            elif msg:
                await msg.reply_text(f"This bot is private. Your id: {uid}")
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
                await update.callback_query.answer("Something broke. Check the log.", show_alert=True)
            elif update.effective_message:
                await update.effective_message.reply_text("Something broke on my side. Check the console log.")

    return wrapper


async def send_html(update: Update, text: str, reply_markup=None, edit: bool = False) -> None:
    parts = chunk(text)
    markup = reply_markup
    if edit and update.callback_query and update.callback_query.message and len(parts) == 1:
        try:
            await update.callback_query.edit_message_text(
                parts[0], parse_mode=ParseMode.HTML, reply_markup=markup, disable_web_page_preview=True
            )
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
    db = store_of(ctx)
    row = db.get_user(uid_of(update))
    assert row
    return row


# --------------------------------------------------------------------------- start / menu


WELCOME = (
    "<b>English Ladder</b> 🪜\n"
    "বাংলাদেশ থেকে ইংরেজি — একদম বেসিক থেকে IELTS Band 9 পর্যন্ত।\n\n"
    "A1 beginner → A2 → B1 → B2 → C1 → IELTS\n"
    "পাঠ, শব্দভাণ্ডার, গ্রামার, পড়া, লেখা, স্পিকিং, আর Grok tutor।\n\n"
    "আগে লেভেল মাপুন, অথবা A1 থেকে শুরু করুন।"
)


@guard
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    db.set_mode(uid_of(update), "idle")
    await send_html(update, WELCOME, reply_markup=onboarding_kb())
    if update.effective_message:
        await update.effective_message.reply_text("Main menu is under your keyboard.", reply_markup=main_kb())


@guard
async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await send_html(
        update,
        "<b>Commands</b>\n"
        "/start — welcome\n"
        "/menu — main menu\n"
        "/level — change CEFR / IELTS track\n"
        "/stats — XP, streak, accuracy\n"
        "/cancel — stop the current quiz or tutor\n\n"
        "নিচের বাটন দিয়ে Lesson, Vocab, Writing, IELTS চালান।",
        reply_markup=main_kb(),
    )


@guard
async def cmd_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    store_of(ctx).set_mode(uid_of(update), "idle")
    await send_menu(update, ctx)


@guard
async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    store_of(ctx).set_mode(uid_of(update), "idle")
    await send_html(update, "Stopped. Back to the menu.", reply_markup=main_kb())


@guard
async def cmd_level(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await send_html(update, "Choose your track:", reply_markup=levels_kb("lvl"))


@guard
async def cmd_stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    await send_html(update, progress_text(update, ctx), reply_markup=main_kb())


async def send_menu(update: Update, ctx: ContextTypes.DEFAULT_TYPE, edit: bool = False) -> None:
    row = user_row(update, ctx)
    meta = LEVEL_META[row["level"]]
    text = (
        f"<b>Menu</b> — {esc(row['first_name'] or 'friend')}\n"
        f"Level: <b>{row['level']}</b> {meta['name']}  ·  IELTS ~{meta['ielts']}\n"
        f"Goal band: {esc(str(row['goal_band']))}  ·  XP {row['xp']}  ·  🔥 {row['streak']}\n\n"
        f"{meta['blurb']}\n\n"
        "📚 Lesson — আজকের পাঠ\n"
        "🧠 Vocab — স্পেসড রিপিটিশন\n"
        "🎯 IELTS — exam skills"
    )
    await send_html(update, text, reply_markup=main_kb(), edit=edit)


def progress_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> str:
    db = store_of(ctx)
    row = user_row(update, ctx)
    tid = uid_of(update)
    right, total = db.accuracy(tid)
    due, cards = db.card_count(tid)
    done = db.completed(tid)
    level = row["level"]
    lessons = lessons_for_level(level)
    finished = sum(1 for les in lessons if les.id in done)
    pct = f"{round(100 * right / total)}%" if total else "—"
    nxt = next_level(level)
    return (
        f"<b>Progress</b>\n"
        f"Level: {level} ({LEVEL_META[level]['name']})\n"
        f"IELTS range: {ielts_range(level)}  ·  goal {esc(str(row['goal_band']))}\n"
        f"XP: {row['xp']}  ·  streak: {row['streak']} day(s)\n"
        f"Lessons here: {finished}/{len(lessons)}\n"
        f"Quiz accuracy: {right}/{total} ({pct})\n"
        f"Vocab cards due: {due} / {cards} total\n"
        f"Next track: {nxt or 'you are at the top — polish Band 8–9'}"
    )


# --------------------------------------------------------------------------- quizzes


def _format_question(q: Question, index: int, total: int, title: str) -> str:
    head = f"<b>{esc(title)}</b>  ({index + 1}/{total})\n\n{q.prompt}"
    if q.options:
        letters = "ABCD"
        opts = "\n".join(f"{letters[i]}) {esc(opt)}" for i, opt in enumerate(q.options))
        return f"{head}\n\n{opts}"
    return f"{head}\n\nType your answer."


def _check(q: Question, raw: str) -> bool:
    if q.options:
        if raw.isdigit() and 0 <= int(raw) < len(q.options):
            return raw == q.answer
        # typed option text
        for i, opt in enumerate(q.options):
            if answers_match(opt, raw) and str(i) == q.answer:
                return True
        return answers_match(q.options[int(q.answer)], raw) if q.answer.isdigit() else False
    return answers_match(q.answer, raw)


def _correct_label(q: Question) -> str:
    if q.options and q.answer.isdigit():
        i = int(q.answer)
        letter = "ABCD"[i]
        return f"{letter}) {q.options[i]}"
    return q.answer.split("|")[0]


async def _feedback(update: Update, q: Question, ok: bool, xp: int) -> None:
    mark = "✅ ঠিক — Correct." if ok else f"❌ ভুল। Answer: <b>{esc(_correct_label(q))}</b>"
    extra = f"\n+{xp} XP" if ok else ""
    await send_html(update, f"{mark}{extra}\n<i>{q.explain}</i>")


# --------------------------------------------------------------------------- lessons


async def start_lesson(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    row = user_row(update, ctx)
    tid = uid_of(update)
    lesson = next_lesson(row["level"], db.completed(tid))
    if not lesson:
        nxt = next_level(row["level"])
        msg = (
            f"You finished every <b>{row['level']}</b> lesson. দারুণ!\n"
            f"Next track: <b>{nxt}</b>." if nxt else "You finished the ladder. Keep using IELTS Writing/Speaking every day."
        )
        if nxt:
            db.set_level(tid, nxt)
        await send_html(update, msg, reply_markup=main_kb())
        return
    db.set_mode(tid, "idle", {"lesson_id": lesson.id})
    body = (
        f"{lesson.teach}\n\n"
        f"<b>Goals</b>\n{join_goals(lesson.goals)}\n"
        f"⏱ {lesson.minutes} min"
    )
    await send_html(update, body, reply_markup=after_teach_kb(lesson.id))


async def start_lesson_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE, lesson_id: str) -> None:
    lesson = get_lesson(lesson_id)
    if not lesson:
        await send_html(update, "Lesson missing.", reply_markup=main_kb())
        return
    db = store_of(ctx)
    db.set_mode(uid_of(update), "lesson_quiz", {"lesson_id": lesson_id, "q": 0, "score": 0})
    await send_current_q(update, ctx, lesson.questions, 0, f"Lesson · {lesson.title}")


async def send_current_q(update: Update, ctx: ContextTypes.DEFAULT_TYPE, questions: tuple[Question, ...] | list[Question], index: int, title: str) -> None:
    q = questions[index]
    text = _format_question(q, index, len(questions), title)
    markup = mcq_kb(len(q.options)) if q.options else stop_kb()
    await send_html(update, text, reply_markup=markup)


async def advance_quiz(update: Update, ctx: ContextTypes.DEFAULT_TYPE, raw: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    payload = db.payload(tid)
    mode = row["mode"]

    if mode == "placement":
        questions = PLACEMENT
        title = "Placement"
        kind = "placement"
        item_prefix = "place"
    elif mode == "lesson_quiz":
        lesson = get_lesson(payload.get("lesson_id", ""))
        if not lesson:
            return
        questions = lesson.questions
        title = f"Lesson · {lesson.title}"
        kind = "lesson"
        item_prefix = lesson.id
    elif mode == "grammar":
        questions = tuple(payload_questions(payload))
        title = "Grammar drill"
        kind = "grammar"
        item_prefix = "grammar"
    elif mode == "reading":
        reading = get_reading(payload.get("reading_id", ""))
        if not reading:
            return
        questions = reading.questions
        title = f"Reading · {reading.title}"
        kind = "reading"
        item_prefix = reading.id
    else:
        return

    index = int(payload.get("q") or 0)
    score = int(payload.get("score") or 0)
    if index >= len(questions):
        return
    q = questions[index]
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
    await _feedback(update, q, ok, gained)

    index += 1
    if index < len(questions):
        payload["q"] = index
        payload["score"] = score
        db.set_mode(tid, mode, payload)
        await send_current_q(update, ctx, questions, index, title)
        return

    # finished
    db.set_mode(tid, "idle")
    total = len(questions)
    if mode == "placement":
        level = place_from_results(flags)
        db.set_level(tid, level)
        db.add_xp(tid, XP_PLACE)
        meta = LEVEL_META[level]
        await send_html(
            update,
            f"<b>Placement done</b> — {score}/{total} correct.\n"
            f"Your track: <b>{level}</b> {meta['name']}\n"
            f"IELTS ~{meta['ielts']}\n\n{meta['blurb']}\n\n"
            "Start with 📚 Lesson.",
            reply_markup=main_kb(),
        )
        return
    if mode == "lesson_quiz":
        lesson = get_lesson(payload.get("lesson_id", ""))
        if lesson:
            db.mark_complete(tid, lesson.id)
            db.add_xp(tid, XP_LESSON)
            for word, _meaning, _ex in lesson.vocab:
                item = next((v for v in VOCAB if v.word == word and v.level == lesson.level), None)
                if item:
                    db.ensure_card(tid, item.id)
            await send_html(
                update,
                f"<b>{esc(lesson.title)}</b> complete.\n"
                f"Score {score}/{total}  ·  +{XP_LESSON} XP\n"
                "New words went to 🧠 Vocab.",
                reply_markup=main_kb(),
            )
            maybe = next_level(lesson.level)
            remaining = [les for les in lessons_for_level(lesson.level) if les.id not in db.completed(tid)]
            if maybe and not remaining:
                await send_html(
                    update,
                    f"Level {lesson.level} cleared. You can move to <b>{maybe}</b> in ⚙️ Settings.",
                )
        return
    await send_html(update, f"Finished. Score {score}/{total}.", reply_markup=main_kb())


def payload_questions(payload: dict) -> list[Question]:
    ids = payload.get("qids") or []
    bank = {f"{les.id}:{i}": q for les in LESSONS for i, q in enumerate(les.questions)}
    out = []
    for key in ids:
        if key in bank:
            out.append(bank[key])
    return out


async def start_placement(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    db.set_mode(uid_of(update), "placement", {"q": 0, "score": 0, "flags": []})
    await send_html(update, "১২টা প্রশ্ন। অনুমান করবেন না — না জানলে Skip চাপুন.")
    await send_current_q(update, ctx, PLACEMENT, 0, "Placement")


# --------------------------------------------------------------------------- vocab


async def start_vocab(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    for item in vocab_for_level(row["level"]):
        db.ensure_card(tid, item.id)
    due = db.due_cards(tid, 12)
    if not due:
        await send_html(update, "No cards due. নতুন শব্দ পেতে একটি Lesson শেষ করুন।", reply_markup=main_kb())
        return
    card = due[0]
    db.set_mode(tid, "vocab", {"word_id": card["word_id"]})
    item = get_vocab(card["word_id"])
    if not item:
        await send_html(update, "Card data missing.", reply_markup=main_kb())
        return
    due_n, total = db.card_count(tid)
    await send_html(
        update,
        f"<b>Vocab</b>  ·  {due_n} due / {total} cards\n\n"
        f"<b>{esc(item.word)}</b>\n"
        "Meaning টা ভাবুন, তারপর Show চাপুন।",
        reply_markup=reveal_kb(),
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
        f"<b>{esc(item.word)}</b>\n"
        f"{esc(item.meaning)}\n"
        f"<i>{esc(item.example)}</i>{extra}\n\n"
        "কত সহজ লেগেছে?",
        reply_markup=vocab_rate_kb(),
    )


async def vocab_rate(update: Update, ctx: ContextTypes.DEFAULT_TYPE, quality: int) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    payload = db.payload(tid)
    word_id = payload.get("word_id")
    if word_id:
        db.review_card(tid, word_id, quality)
        if quality >= 4:
            db.add_xp(tid, XP_VOCAB)
    await start_vocab(update, ctx)


# --------------------------------------------------------------------------- grammar / reading


async def start_grammar(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    row = user_row(update, ctx)
    bank = []
    for les in lessons_for_level(row["level"]):
        for i, q in enumerate(les.questions):
            bank.append(f"{les.id}:{i}")
    if not bank:
        await send_html(update, "No grammar items at this level.", reply_markup=main_kb())
        return
    # rotate through the bank
    right, total = store_of(ctx).accuracy(uid_of(update), "grammar")
    start = total % len(bank)
    picked = (bank + bank)[start : start + 5]
    questions = payload_questions({"qids": picked})
    store_of(ctx).set_mode(uid_of(update), "grammar", {"qids": picked, "q": 0, "score": 0})
    await send_current_q(update, ctx, questions, 0, "Grammar drill")


async def start_reading(update: Update, ctx: ContextTypes.DEFAULT_TYPE, level: str | None = None) -> None:
    row = user_row(update, ctx)
    lvl = level or row["level"]
    pack = readings_for_level(lvl) or readings_for_level("A1")
    if not pack:
        await send_html(update, "No reading yet.", reply_markup=main_kb())
        return
    reading = pack[0]
    store_of(ctx).set_mode(uid_of(update), "reading", {"reading_id": reading.id, "q": 0, "score": 0, "phase": "text"})
    await send_html(
        update,
        f"<b>Reading · {esc(reading.title)}</b>\n\n{esc(reading.text)}\n\n"
        "পড়ে নিলে Practice quiz চাপুন।",
        reply_markup=after_teach_kb(reading.id),
    )


# --------------------------------------------------------------------------- writing / speaking / tutor


async def start_prompt(update: Update, ctx: ContextTypes.DEFAULT_TYPE, skill: str, prompt_id: str | None = None) -> None:
    row = user_row(update, ctx)
    items = writing_for_level(row["level"]) if skill == "writing" else speaking_for_level(row["level"])
    prompt = get_prompt(prompt_id) if prompt_id else (items[0] if items else None)
    if not prompt:
        await send_html(update, "No prompt at this level.", reply_markup=main_kb())
        return
    mode = "writing" if skill == "writing" else "speaking"
    store_of(ctx).set_mode(uid_of(update), mode, {"prompt_id": prompt.id})
    tips = "\n".join(f"• {t}" for t in prompt.tips)
    voice_hint = "\nVoice note পাঠাতে পারেন, অথবা টাইপ করুন।" if skill == "speaking" else ""
    await send_html(
        update,
        f"<b>{esc(prompt.title)}</b>  ·  {prompt.minutes} min\n\n"
        f"{esc(prompt.cue)}\n\n"
        f"<b>Tips</b>\n{esc(tips)}{voice_hint}\n\n"
        "লিখে পাঠান। /cancel to stop.",
        reply_markup=stop_kb(),
    )


async def start_tutor(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    db.set_mode(tid, "chat", {})
    row = user_row(update, ctx)
    await send_html(
        update,
        f"<b>Tutor</b> — level {row['level']}\n"
        "ইংরেজিতে কথা বলুন। আমি শুধরে দেব।\n"
        "উদাহরণ: <i>How do I ask for the bill?</i> বা <i>Check this sentence: I go yesterday market.</i>\n\n"
        "/cancel to leave.",
        reply_markup=stop_kb(),
    )


async def handle_writing(update: Update, ctx: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    prompt = get_prompt(db.payload(tid).get("prompt_id", ""))
    if not prompt:
        db.set_mode(tid, "idle")
        return
    await send_html(update, "Checking… একটু অপেক্ষা করুন।")
    feedback = ai.grade_writing(text, prompt.cue, row["level"], row["native_lang"])
    db.add_xp(tid, XP_WRITE)
    db.log_attempt(tid, "writing", prompt.id, True, None)
    db.set_mode(tid, "idle")
    await send_html(update, feedback, reply_markup=main_kb())


async def handle_speaking(update: Update, ctx: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    prompt = get_prompt(db.payload(tid).get("prompt_id", ""))
    if not prompt:
        db.set_mode(tid, "idle")
        return
    await send_html(update, "Listening / reading your answer…")
    feedback = ai.grade_speaking(text, prompt.cue, row["level"], row["native_lang"])
    db.add_xp(tid, XP_SPEAK)
    db.log_attempt(tid, "speaking", prompt.id, True, None)
    db.set_mode(tid, "idle")
    await send_html(update, feedback, reply_markup=main_kb())


async def handle_chat(update: Update, ctx: ContextTypes.DEFAULT_TYPE, text: str) -> None:
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)
    db.add_chat(tid, "user", text)
    history = db.chat_history(tid)
    reply = ai.complete(history, row["level"], row["native_lang"], "tutor")
    db.add_chat(tid, "assistant", reply)
    await send_html(update, reply, reply_markup=stop_kb())


# --------------------------------------------------------------------------- routers


@guard
async def on_text(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message
    if not msg or not msg.text:
        return
    text = msg.text.strip()
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)

    if text in BUTTONS or text == BTN_MENU:
        db.set_mode(tid, "idle")
        if text in {BTN_MENU, "🏠 Menu"}:
            await send_menu(update, ctx)
        elif text == BTN_LESSON:
            await start_lesson(update, ctx)
        elif text == BTN_VOCAB:
            await start_vocab(update, ctx)
        elif text == BTN_GRAMMAR:
            await start_grammar(update, ctx)
        elif text == BTN_READ:
            await start_reading(update, ctx)
        elif text == BTN_WRITE:
            await start_prompt(update, ctx, "writing")
        elif text == BTN_SPEAK:
            await start_prompt(update, ctx, "speaking")
        elif text == BTN_TUTOR:
            await start_tutor(update, ctx)
        elif text == BTN_IELTS:
            await send_html(update, "<b>IELTS gym</b>\nAcademic skills for Band 6–9.", reply_markup=ielts_kb())
        elif text == BTN_PROGRESS:
            await send_html(update, progress_text(update, ctx), reply_markup=main_kb())
        elif text == BTN_SETTINGS:
            await send_html(update, "Settings — লেভেল, ভাষা, টার্গেট ব্যান্ড।", reply_markup=settings_kb())
        return

    mode = row["mode"]
    if mode in {"placement", "lesson_quiz", "grammar", "reading"}:
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
    await send_menu(update, ctx)


@guard
async def on_voice(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    row = user_row(update, ctx)
    if row["mode"] not in {"speaking", "chat"}:
        await send_html(update, "Voice is for 🗣️ Speaking or 💬 Tutor. Type if you can — I mark typed answers too.")
        return
    await send_html(
        update,
        "Voice notes: এই ভার্সনে ট্রান্সক্রিপ্ট নেই। যা বলেছেন সেটা টাইপ করে পাঠান "
        "(বা Telegram-এর voice-to-text ব্যবহার করুন)।",
    )


@guard
async def on_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()
    data = query.data
    db = store_of(ctx)
    tid = uid_of(update)
    row = user_row(update, ctx)

    if data == "m:home":
        db.set_mode(tid, "idle")
        await send_menu(update, ctx)
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
            f"Track set to <b>{level}</b> — {LEVEL_META[level]['name']}.\n📚 Lesson দিয়ে শুরু করুন।",
            reply_markup=main_kb(),
        )
        return
    if data == "ob:pick":
        await send_html(update, "Choose a level:", reply_markup=levels_kb("lvl"))
        return
    if data.startswith("lvl:"):
        level = data.split(":", 1)[1]
        if level in LEVELS:
            db.set_level(tid, level)
            await send_html(update, f"Level set to <b>{level}</b>.", reply_markup=main_kb())
        return
    if data.startswith("lsn:quiz:"):
        lesson_id = data.split(":", 2)[2]
        # reading reuse of after_teach_kb
        if lesson_id.startswith("read-"):
            reading = get_reading(lesson_id)
            if reading:
                db.set_mode(tid, "reading", {"reading_id": reading.id, "q": 0, "score": 0})
                await send_current_q(update, ctx, reading.questions, 0, f"Reading · {reading.title}")
            return
        await start_lesson_quiz(update, ctx, lesson_id)
        return
    if data.startswith("ans:"):
        token = data.split(":", 1)[1]
        await advance_quiz(update, ctx, token)
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
        await send_html(update, "Pick a track:", reply_markup=levels_kb("lvl"))
        return
    if data == "set:bn":
        db.set_native(tid, "bn")
        await send_html(update, "Bangla help on — A1–A2 তে অর্থ থাকবে।", reply_markup=main_kb())
        return
    if data == "set:en":
        db.set_native(tid, "en")
        await send_html(update, "Feedback will stay in English.", reply_markup=main_kb())
        return
    if data.startswith("set:g"):
        band = {"set:g6": "6.0", "set:g7": "7.0", "set:g8": "8.0"}[data]
        db.set_goal(tid, band)
        await send_html(update, f"IELTS goal set to {band}.", reply_markup=main_kb())
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
    if data == "m:home":
        await send_menu(update, ctx)
        return

    log.info("unknown callback %s from %s", data, tid)
    _ = row
