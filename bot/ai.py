from __future__ import annotations

import re

from .curriculum.grammar_rules import BASIC_RULES
from .curriculum.lessons import LESSONS
from .curriculum.levels import LEVEL_META
from .curriculum.vocab import VOCAB
from .util import esc

# Typical learner slips (especially L1 Bangla → English).
_FIXES: tuple[tuple[str, str, str], ...] = (
    (r"\bi go yesterday\b", "I went yesterday", "Past: go → went."),
    (r"\bi am go\b", "I go / I am going", "Don't mix am + go."),
    (r"\bi am went\b", "I went", "Past needs went, not am went."),
    (r"\bdid you went\b", "Did you go", "Did + base verb."),
    (r"\bi didn't went\b", "I didn't go", "didn't + go."),
    (r"\bi didn't ate\b", "I didn't eat", "didn't + eat."),
    (r"\bhe go\b", "he goes", "He/She + -s."),
    (r"\bshe go\b", "she goes", "He/She + -s."),
    (r"\bhe have\b", "he has", "He/She has."),
    (r"\bshe have\b", "she has", "He/She has."),
    (r"\bshe don't\b", "she doesn't", "She doesn't."),
    (r"\bhe don't\b", "he doesn't", "He doesn't."),
    (r"\bi can to\b", "I can", "can + verb, no to."),
    (r"\bi am agree\b", "I agree", "agree, not am agree."),
    (r"\bi am understand\b", "I understand", "understand, not am understand."),
    (r"\bmore better\b", "better", "better already means more good."),
    (r"\bdiscuss about\b", "discuss", "discuss something (no about)."),
    (r"\breturn back\b", "return", "return = go back."),
    (r"\brepeat again\b", "repeat", "repeat already means again."),
    (r"\bpeoples\b", "people", "people is already plural."),
    (r"\binformations\b", "information", "information has no -s."),
    (r"\badvices\b", "advice", "advice has no -s. An advice → some advice."),
    (r"\ba apple\b", "an apple", "an + vowel sound."),
    (r"\ba egg\b", "an egg", "an + vowel sound."),
    (r"\ba orange\b", "an orange", "an + vowel sound."),
    (r"\bi no have\b", "I don't have", "don't have."),
    (r"\bi not have\b", "I don't have", "don't have."),
    (r"\bwhere you live\b", "where do you live", "Do/does in questions."),
    (r"\bhow you are\b", "how are you", "How are you?"),
    (r"\bwhat you doing\b", "what are you doing", "be + -ing."),
    (r"\bi living in\b", "I live in / I am living in", "habit = I live."),
    (r"\bvery much happy\b", "very happy", "very + adjective."),
    (r"\bi want that i\b", "I want to", "want to + verb."),
    (r"\baccording to me\b", "in my opinion", "in my opinion / I think."),
    (r"\bone of my friend\b", "one of my friends", "one of + plural."),
)


_WORD = re.compile(r"[A-Za-z']+")
_TARGETS = {"A1": 50, "A2": 80, "B1": 140, "B2": 200, "C1": 260, "IELTS": 250}


def _bn(native: str) -> bool:
    return native.lower() in {"bn", "bangla", "bengali", "বাংলা"}


def find_slips(text: str) -> list[tuple[str, str, str]]:
    low = " " + re.sub(r"\s+", " ", text.strip().lower()) + " "
    found: list[tuple[str, str, str]] = []
    seen: set[str] = set()
    for pattern, better, rule in _FIXES:
        if re.search(pattern, low) and pattern not in seen:
            seen.add(pattern)
            found.append((pattern, better, rule))
    if text and text[0].isalpha() and text[0].islower():
        found.append(("capital", text[0].upper() + text[1:], "Start a sentence with a capital letter."))
    if re.search(r"\bi\b", text) and not re.search(r"\bI\b", text):
        found.append(("i", "I", "Write I with a capital letter."))
    return found[:5]


def _word_count(text: str) -> int:
    return len(_WORD.findall(text))


def _cue_cover(cue: str, text: str) -> bool:
    keys = {w.lower() for w in _WORD.findall(cue) if len(w) > 3} - {
        "write",
        "describe",
        "about",
        "should",
        "would",
        "your",
        "this",
        "that",
        "with",
        "from",
        "have",
        "some",
        "people",
        "words",
        "minutes",
    }
    if not keys:
        return _word_count(text) >= 20
    body = set(w.lower() for w in _WORD.findall(text))
    return len(keys & body) >= min(3, max(1, len(keys) // 8))


def _model_writing(level: str, cue: str) -> str:
    if level == "A1":
        return (
            "My name is Rafi. I am from Dhaka. I have one sister. "
            "I like rice and fish. Every day I go to college by bus."
        )
    if level == "A2":
        return (
            "Yesterday I went to the market with my mother. We bought fish and vegetables. "
            "Then we cooked dinner. I didn't play cricket because it rained."
        )
    if level == "B1":
        return (
            "My town is busy but friendly. The metro helps, however the roads are still slow. "
            "For example, I need one hour to reach college. I think more buses would help."
        )
    if level in {"B2", "C1", "IELTS"}:
        return (
            "While studying abroad can widen a student's skills, it also risks a brain drain "
            "if graduates do not return. In Bangladesh, remittances help families, but local "
            "universities still need investment. On balance, exchange programmes with a clear "
            "return plan are more useful than a one-way exit."
        )
    return "Write short, clear sentences. One idea per sentence. Then add because + a reason."


def _model_speaking(level: str) -> str:
    if level in {"A1", "A2"}:
        return (
            "My name is Nabila. I live in Chattogram. "
            "I like tea in the morning. Last Friday I visited my aunt."
        )
    return (
        "I'd like to talk about cooking rice. I learned it from my mother. "
        "It matters because sharing food is how we welcome people at home. "
        "I still need more practice speaking about it in English."
    )


def _band(level: str, words: int, slips: int, covered: bool) -> str:
    meta = LEVEL_META.get(level, LEVEL_META["A1"])
    target = _TARGETS.get(level, 80)
    if words < max(15, target // 4) or slips >= 4 or not covered:
        return f"below {level}  (IELTS ~{meta['ielts']} — too short or off-task)"
    if slips == 0 and words >= target:
        return f"solid {level}  (IELTS ~{meta['ielts']})"
    return f"around {level}  (IELTS ~{meta['ielts']})"


def _slip_block(slips: list[tuple[str, str, str]], native: str) -> str:
    if not slips:
        extra = "ভালো হয়েছে — I didn't find the usual beginner slips." if _bn(native) else "Clean — no common slips found."
        return extra
    lines = []
    for i, (_pat, better, rule) in enumerate(slips, start=1):
        lines.append(f"{i}. {rule}\n   → <b>{better}</b>")
    return "\n".join(lines)


def grade_writing(text: str, cue: str, level: str, native: str = "bn") -> str:
    body = text.strip()
    words = _word_count(body)
    target = _TARGETS.get(level, 80)
    slips = find_slips(body)
    covered = _cue_cover(cue, body)
    task = "Yes — you stayed on the topic." if covered else "Partly — add 2 details from the question."
    if _bn(native) and not covered:
        task += " প্রশ্ন থেকে আরও ২টা পয়েন্ট লিখুন।"
    return (
        f"<b>Writing check</b>  ·  {level}\n"
        f"Band: {_band(level, words, len(slips), covered)}\n"
        f"Words: {words}  (aim ~{target})\n"
        f"Task: {task}\n\n"
        f"<b>Fixes</b>\n{_slip_block(slips, native)}\n\n"
        f"<b>Model</b>\n<i>{_model_writing(level, cue)}</i>\n\n"
        "Tomorrow: copy the model, then change the names and places to yours."
    )


def grade_speaking(text: str, cue: str, level: str, native: str = "bn") -> str:
    body = text.strip()
    words = _word_count(body)
    slips = find_slips(body)
    covered = _cue_cover(cue, body)
    length_note = "Good length." if words >= 40 else "Too short — add because + one example."
    if _bn(native) and words < 40:
        length_note = "আরও বলুন — because + একটি উদাহরণ।"
    return (
        f"<b>Speaking check</b>  ·  {level}\n"
        f"Band: {_band(level, words, len(slips), covered)}\n"
        f"{length_note}  ({words} words)\n\n"
        f"<b>Fixes</b>\n{_slip_block(slips, native)}\n\n"
        f"<b>Say it like this</b>\n<i>{_model_speaking(level)}</i>\n\n"
        "Tip: 3–4 sentences. Don't stop at yes/no."
    )


def _lookup_vocab(query: str) -> str | None:
    q = query.lower().strip()
    q = re.sub(r"^(what is|what's|meaning of|mean of|translate|মানে)\s+", "", q)
    q = q.strip(" ??.!")
    if not q:
        return None
    for item in VOCAB:
        if item.word.lower() == q or q == item.word.lower():
            return (
                f"<b>{item.word}</b>  ·  {item.level}\n"
                f"{item.meaning}\n"
                f"<i>{item.example}</i>"
            )
    for les in LESSONS:
        for word, meaning, example in les.vocab:
            if word.lower() == q:
                return f"<b>{word}</b>  ·  {les.level}\n{meaning}\n<i>{example}</i>"
    return None


def _lookup_rule(query: str) -> str | None:
    q = query.lower()
    if re.match(r"what('?s| is| does)\s+\S+", q):
        return None
    keys = (
        ("going to", "future"),
        ("there is", "there"),
        ("in the morning", "prepositions"),
        ("at home", "prepositions"),
        ("a/an", "a-an"),
        ("present", "present"),
        ("yesterday", "past"),
        ("better", "compare"),
        ("can't", "can"),
        ("will", "future"),
        ("past", "past"),
        ("have", "have"),
        ("has", "have"),
        ("some", "some-any"),
        ("any", "some-any"),
        ("than", "compare"),
        ("can", "can"),
        ("are", "be"),
        ("an", "a-an"),
        ("am", "be"),
    )
    for needle, rid in keys:
        if re.search(rf"\b{re.escape(needle)}\b", q):
            for rule in BASIC_RULES:
                if rule.id == rid:
                    return f"<b>{rule.title}</b>\n<i>{rule.title_bn}</i>\n\n{rule.body}"
    return None


def _greet(level: str, native: str) -> str:
    if _bn(native):
        return (
            f"Hi — I'm your English teacher ({level}). No internet AI needed.\n"
            "একটা বাক্য লিখুন, আমি শুধরে দেব।\n"
            "উদাহরণ: <i>I go yesterday market.</i>\n"
            "Or ask: <i>what is however</i>  /  <i>can / can't</i>"
        )
    return (
        f"Hi — I'm your English teacher ({level}). I work fully offline.\n"
        "Send a sentence and I'll correct it.\n"
        "Try: <i>I go yesterday market.</i>"
    )


def complete(messages: list[dict[str, str]], level: str, native: str = "bn", skill: str = "tutor") -> str:
    user_msgs = [m.get("content", "") for m in messages if m.get("role") == "user"]
    text = (user_msgs[-1] if user_msgs else "").strip()
    if not text:
        return _greet(level, native)

    low = text.lower().strip()
    if low in {"hi", "hello", "hey", "salam", "assalamu alaikum", "help", "start"}:
        return _greet(level, native)

    vocab = _lookup_vocab(text)
    if vocab and any(w in low for w in ("what", "mean", "meaning", "translate", "মানে", "word")):
        return vocab

    rule = _lookup_rule(text)
    if rule and any(w in low for w in ("rule", "grammar", "how", "use", "when", "why", "কীভাবে", "গ্রামার")):
        return rule

    vocab2 = _lookup_vocab(text)
    if vocab2:
        return vocab2
    rule2 = _lookup_rule(text)
    if rule2:
        return rule2

    slips = find_slips(text)
    if slips:
        better = text
        for _pat, repl, _rule in slips:
            if _pat in {"capital", "i"}:
                continue
            better = re.sub(_pat, repl, better, flags=re.I)
        if better and better[0].isalpha():
            better = better[0].upper() + better[1:]
        return (
            f"<b>Check</b>\nYou wrote: <i>{esc(text)}</i>\n"
            f"Better: <b>{esc(better)}</b>\n\n"
            f"{_slip_block(slips, native)}\n\n"
            "Send another sentence."
        )

    words = _word_count(text)
    if words <= 2:
        return (
            _greet(level, native)
            if words == 0
            else f"Say more. Example: I like tea because it is cheap and hot."
        )
    return (
        f"Clear enough for {level}. "
        f"Add <b>because</b> + one example to make it stronger.\n\n"
        f"You wrote: <i>{esc(text)}</i>\n"
        "Now try it in the past tense, or ask me a word."
    )
