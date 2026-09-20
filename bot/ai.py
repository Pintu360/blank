from __future__ import annotations

import logging

from openai import OpenAI

from . import config
from .curriculum.levels import LEVEL_META

log = logging.getLogger("english-ladder.ai")

_client: OpenAI | None = None


def available() -> bool:
    return bool(config.XAI_API_KEY)


def client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=config.XAI_API_KEY, base_url=config.XAI_BASE_URL)
    return _client


def _system(level: str, native: str, skill: str) -> str:
    meta = LEVEL_META.get(level, LEVEL_META["A1"])
    bangla = native.lower() in {"bn", "bangla", "bengali", "বাংলা"}
    lang_rule = (
        "The learner is from Bangladesh and is most comfortable in Bangla. "
        "For A1–A2: write the main teaching in simple English, then add a short Bangla gloss "
        "in parentheses or on the next line. For B1 and above, stay in English and only use "
        "Bangla for a difficult word if needed. Never dump a full Bangla essay when the task "
        "is to practise English."
        if bangla
        else "Keep feedback in clear English matched to the learner's level."
    )
    return (
        "You are English Ladder, a patient teacher taking Bangladeshi learners from A1 to IELTS Band 9.\n"
        f"Current level: {level} ({meta['name']}, IELTS ~{meta['ielts']}).\n"
        f"{meta['ai']}\n"
        f"{lang_rule}\n"
        "Use examples from Bangladesh when they help (Dhaka traffic, monsoon, cricket, "
        "family, rice and fish, SSC/HSC, garment work, remittances) — never stereotypes.\n"
        "Correct errors. Show a better sentence. Explain the rule in one short line.\n"
        "Be warm, specific, and not fluffy. No slang the learner could copy into IELTS.\n"
        f"Skill mode: {skill}."
    )


def complete(messages: list[dict[str, str]], level: str, native: str = "bn", skill: str = "tutor") -> str:
    if not available():
        return (
            "AI tutor is off until you add XAI_API_KEY to the .env file "
            "(https://console.x.ai). Lessons, vocab, grammar, and reading still work."
        )
    payload = [{"role": "system", "content": _system(level, native, skill)}, *messages]
    try:
        resp = client().chat.completions.create(
            model=config.XAI_MODEL,
            messages=payload,
            temperature=0.4,
        )
        text = (resp.choices[0].message.content or "").strip()
        return text or "I could not write a reply. Try again."
    except Exception:
        log.exception("xAI request failed")
        return "The tutor had a connection problem. Your lesson progress is saved — try again in a moment."


def grade_writing(text: str, cue: str, level: str, native: str = "bn") -> str:
    return complete(
        [
            {
                "role": "user",
                "content": (
                    f"Writing task:\n{cue}\n\nLearner's text:\n{text}\n\n"
                    "Reply with:\n"
                    "1) Estimated CEFR / IELTS band (honest, not kind)\n"
                    "2) Task — did they answer the question?\n"
                    "3) Three concrete errors with corrections\n"
                    "4) One upgraded model paragraph they can steal from\n"
                    "5) One practice drill for tomorrow"
                ),
            }
        ],
        level,
        native,
        "writing",
    )


def grade_speaking(text: str, cue: str, level: str, native: str = "bn") -> str:
    return complete(
        [
            {
                "role": "user",
                "content": (
                    f"Speaking task:\n{cue}\n\nLearner's answer (transcript or typed):\n{text}\n\n"
                    "Score fluency, vocabulary, grammar, and (if obvious) pronunciation from the spelling. "
                    "Give a band/CEFR estimate, 3 corrections, and a 6-line model answer at their next level."
                ),
            }
        ],
        level,
        native,
        "speaking",
    )
