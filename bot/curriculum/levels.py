from __future__ import annotations

LEVELS = ("A1", "A2", "B1", "B2", "C1", "IELTS")

LEVEL_META = {
    "A1": {
        "name": "Beginner",
        "cefr": "A1",
        "ielts": "3.0–3.5",
        "blurb": "Hello, names, numbers, family, and simple present.",
        "ai": "Use very short, simple sentences. Teach like a kind classroom teacher. Avoid idioms.",
    },
    "A2": {
        "name": "Elementary",
        "cefr": "A2",
        "ielts": "4.0–4.5",
        "blurb": "Past and future, shopping, travel, and everyday stories.",
        "ai": "Use simple sentences and high-frequency words. Introduce one new structure at a time.",
    },
    "B1": {
        "name": "Intermediate",
        "cefr": "B1",
        "ielts": "5.0–5.5",
        "blurb": "Opinions, experiences, work, and connected paragraphs.",
        "ai": "Natural intermediate English. Correct errors clearly. Model linking words.",
    },
    "B2": {
        "name": "Upper-intermediate",
        "cefr": "B2",
        "ielts": "6.0–6.5",
        "blurb": "Arguments, passives, reported speech, and academic tone.",
        "ai": "Fluent B2 English. Push precision, collocations, and paragraph structure.",
    },
    "C1": {
        "name": "Advanced",
        "cefr": "C1",
        "ielts": "7.0–8.0",
        "blurb": "Nuance, hedging, inversion, and high-band essays.",
        "ai": "Sophisticated C1 English. Comment on register, stance, and lexical nuance.",
    },
    "IELTS": {
        "name": "IELTS 6.0–9.0",
        "cefr": "C1–C2",
        "ielts": "6.0–9.0",
        "blurb": "Exam skills for Listening, Reading, Writing, and Speaking.",
        "ai": "Behave like a strict but fair IELTS examiner. Use official band descriptors.",
    },
}


def level_index(level: str) -> int:
    try:
        return LEVELS.index(level)
    except ValueError:
        return 0


def next_level(level: str) -> str | None:
    i = level_index(level)
    if i + 1 < len(LEVELS):
        return LEVELS[i + 1]
    return None


def prev_level(level: str) -> str | None:
    i = level_index(level)
    if i > 0:
        return LEVELS[i - 1]
    return None


def ielts_range(level: str) -> str:
    return LEVEL_META.get(level, LEVEL_META["A1"])["ielts"]
