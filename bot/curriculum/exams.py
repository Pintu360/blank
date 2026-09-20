from __future__ import annotations

import hashlib
import random
import string
from dataclasses import dataclass

from .lessons import LESSONS
from .levels import LEVELS, level_index
from .models import Question, q_fill, q_mcq

# Extra papers so tests are not a copy of the lesson quizzes.
EXTRA: tuple[tuple[str, str, Question], ...] = (
    ("ex-a1-01", "A1", q_mcq("Choose the greeting.", ["See you later only", "Hello", "Yesterday"], 1, "Hello = greeting.")),
    ("ex-a1-02", "A1", q_fill("I ___ Rina. (am/is/are)", "am", "I am.")),
    ("ex-a1-03", "A1", q_mcq("She ___ a doctor.", ["am", "is", "are"], 1, "She is.")),
    ("ex-a1-04", "A1", q_fill("They ___ students. (are)", "are", "They are.")),
    ("ex-a1-05", "A1", q_mcq("“Thank you” মানে", ["দুঃখিত", "ধন্যবাদ", "দয়া করে"], 1, "thank you = ধন্যবাদ.")),
    ("ex-a1-06", "A1", q_fill("This is ___ apple. (a/an)", "an", "an + vowel sound.")),
    ("ex-a1-07", "A1", q_mcq("I ___ tea.", ["likes", "like", "liking"], 1, "I like.")),
    ("ex-a1-08", "A1", q_fill("He ___ to school. (go/goes)", "goes", "He/She + -s.")),
    ("ex-a1-09", "A1", q_mcq("I am ___ home.", ["to", "at", "on"], 1, "at home.")),
    ("ex-a1-10", "A1", q_fill("I ___ swim. (can)", "can", "can + verb.")),
    ("ex-a1-11", "A1", q_mcq("What ___ your name?", ["is", "are", "am"], 0, "What is your name?")),
    ("ex-a1-12", "A1", q_fill("___ you from Bangladesh? (Are)", "Are", "Are you…?")),
    ("ex-a1-13", "A1", q_mcq("We ___ rice every day.", ["eats", "eat", "eating"], 1, "We eat.")),
    ("ex-a1-14", "A1", q_fill("It is 7 ___. (o'clock)", "o'clock|oclock", "o'clock.")),
    ("ex-a1-15", "A1", q_mcq("Turn ___ please. (not right)", ["left", "up", "under"], 0, "left / right.")),
    ("ex-a2-01", "A2", q_fill("Yesterday I ___ TV. (watched)", "watched", "past + ed.")),
    ("ex-a2-02", "A2", q_mcq("Did you ___ to the shop?", ["went", "go", "gone"], 1, "Did + base verb.")),
    ("ex-a2-03", "A2", q_fill("I ___ to Sylhet last year. (went)", "went", "go → went.")),
    ("ex-a2-04", "A2", q_mcq("How ___ bananas?", ["much", "many", "long"], 1, "countable → many.")),
    ("ex-a2-05", "A2", q_fill("How ___ water? (much)", "much", "uncountable → much.")),
    ("ex-a2-06", "A2", q_mcq("Dhaka is bigger ___ Khulna.", ["then", "than", "that"], 1, "than.")),
    ("ex-a2-07", "A2", q_fill("I am ___ to visit my village. (going)", "going", "going to + plan.")),
    ("ex-a2-08", "A2", q_mcq("I think it ___ rain.", ["will", "going", "is"], 0, "prediction → will.")),
    ("ex-a2-09", "A2", q_fill("She ___ an apple. (ate)", "ate", "eat → ate.")),
    ("ex-a2-10", "A2", q_mcq("We haven't got ___ sugar.", ["some", "any", "a"], 1, "negative → any.")),
    ("ex-a2-11", "A2", q_fill("Go ___, then turn left. (straight)", "straight", "go straight.")),
    ("ex-a2-12", "A2", q_mcq("good → ___", ["gooder", "better", "more good"], 1, "better.")),
    ("ex-b1-01", "B1", q_mcq("I have lived here ___ 2020.", ["for", "since", "ago"], 1, "since + point.")),
    ("ex-b1-02", "B1", q_fill("If I study, I ___ pass. (will)", "will", "first conditional.")),
    ("ex-b1-03", "B1", q_mcq("You ___ review every day. (advice)", ["should", "mustn't to", "are"], 0, "should = advice.")),
    ("ex-b1-04", "B1", q_fill("___ my opinion, reading helps.", "In", "In my opinion.")),
    ("ex-b1-05", "B1", q_mcq("The woman ___ teaches us is kind.", ["which", "who", "where"], 1, "who + people.")),
    ("ex-b1-06", "B1", q_fill("Have you ___ been to Cox's Bazar?", "ever", "ever in questions.")),
    ("ex-b1-07", "B1", q_mcq("Unless you practise, you ___ improve.", ["will", "won't", "would"], 1, "unless = if not.")),
    ("ex-b1-08", "B1", q_fill("If I ___ you, I would start today. (were)", "were", "If I were you.")),
    ("ex-b2-01", "B2", q_fill("Bangla ___ spoken here. (is)", "is", "passive.")),
    ("ex-b2-02", "B2", q_mcq("She said she ___ tired.", ["is", "was", "were"], 1, "backshift.")),
    ("ex-b2-03", "B2", q_fill("___ a decision (make/do)", "make", "make a decision.")),
    ("ex-b2-04", "B2", q_mcq("Hedged claim:", ["Everyone is lazy.", "Students tend to delay practice.", "Nobody studies."], 1, "tend to.")),
    ("ex-b2-05", "B2", q_fill("As a ___, traffic increased. (result)", "result", "As a result.")),
    ("ex-b2-06", "B2", q_mcq("He ___ me to wait.", ["said", "told", "says"], 1, "tell + person.")),
    ("ex-c1-01", "C1", q_mcq("Never ___ I seen such rain.", ["I have", "have I", "I had"], 1, "inversion.")),
    ("ex-c1-02", "C1", q_fill("The figures ___ that demand rose. (suggest)", "suggest", "figures suggest.")),
    ("ex-c1-03", "C1", q_mcq("Upgrade “very big problem”:", ["huge bad thing", "a pressing structural problem", "problem big"], 1, "precise lexis.")),
    ("ex-c1-04", "C1", q_fill("develop → ___", "development", "nominalisation.")),
    ("ex-ielts-01", "IELTS", q_mcq("Passage silent on X →", ["TRUE", "FALSE", "NOT GIVEN"], 2, "NG.")),
    ("ex-ielts-02", "IELTS", q_fill("Task 1 needs an ___. (overview)", "overview", "overview is required.")),
    ("ex-ielts-03", "IELTS", q_mcq("Task 2 intro needs:", ["a joke", "paraphrase + position", "your CV"], 1, "thesis.")),
    ("ex-ielts-04", "IELTS", q_fill("Speaking Part 2 prep is ___ minute.", "1|one", "one minute.")),
)


def _lesson_bank() -> list[tuple[str, str, Question]]:
    out: list[tuple[str, str, Question]] = []
    for les in LESSONS:
        for i, q in enumerate(les.questions):
            out.append((f"{les.id}:{i}", les.level, q))
    out.extend(EXTRA)
    return out


BANK = _lesson_bank()


@dataclass(frozen=True)
class ExamItem:
    id: str
    level: str
    question: Question


@dataclass(frozen=True)
class Exam:
    exam_id: str
    kind: str
    level: str
    seed: str
    items: tuple[ExamItem, ...]


KINDS = {
    "quick": 10,
    "level": 15,
    "basic": 12,
    "mixed": 20,
    "teacher": 8,
}


def _levels_for(kind: str, level: str) -> tuple[str, ...]:
    if kind == "basic":
        return ("A1", "A2")
    if kind == "mixed":
        i = level_index(level)
        pick = [LEVELS[max(0, i - 1)], LEVELS[i]]
        if i + 1 < len(LEVELS):
            pick.append(LEVELS[i + 1])
        return tuple(dict.fromkeys(pick))
    return (level,)


def shuffle_question(q: Question, rng: random.Random) -> Question:
    if not q.options:
        return q
    correct = q.options[int(q.answer)] if q.answer.isdigit() else q.options[0]
    opts = list(q.options)
    rng.shuffle(opts)
    return Question(
        prompt=q.prompt,
        options=tuple(opts),
        answer=str(opts.index(correct)),
        explain=q.explain,
        kind=q.kind,
    )


def _code(seed: str) -> str:
    raw = hashlib.sha256(seed.encode("utf-8")).hexdigest()[:6].upper()
    letters = "".join(ch if ch in string.ascii_uppercase + string.digits else "X" for ch in raw)
    return f"EL-{letters}"


def build_exam(
    level: str,
    kind: str,
    seed: str,
    avoid_ids: list[str] | None = None,
    topic: str | None = None,
) -> Exam:
    from .generator import generate_items

    n = KINDS.get(kind, 10)
    avoid = set(avoid_ids or [])
    rng = random.Random(seed)
    items: list[ExamItem] = []
    if kind == "basic":
        items.extend(generate_items("A1", n // 2 + 2, rng, avoid_ids=avoid))
        items.extend(generate_items("A2", n, rng, avoid_ids=avoid | {it.id for it in items}))
    elif kind == "mixed":
        for lv in _levels_for("mixed", level):
            items.extend(generate_items(lv, max(4, n // 3 + 1), rng, avoid_ids=avoid | {it.id for it in items}))
    else:
        gen_level = level if kind != "basic" else "A1"
        items.extend(generate_items(gen_level, n, rng, topic=topic, avoid_ids=avoid))

    uniq: list[ExamItem] = []
    seen_prompts: set[str] = set()
    for it in items:
        if it.question.prompt in seen_prompts:
            continue
        seen_prompts.add(it.question.prompt)
        uniq.append(it)
    rng.shuffle(uniq)
    items = uniq[:n]

    if len(items) < n:
        allowed = set(_levels_for(kind if kind != "teacher" else "quick", level))
        pool = [(qid, lvl, q) for qid, lvl, q in BANK if lvl in allowed and qid not in avoid]
        rng.shuffle(pool)
        for qid, lvl, q in pool:
            if len(items) >= n:
                break
            items.append(ExamItem(id=qid, level=lvl, question=shuffle_question(q, rng)))

    exam_id = _code(seed)
    return Exam(exam_id=exam_id, kind=kind, level=level, seed=seed, items=tuple(items[:n]))


def dump_exam(exam: Exam) -> dict:
    return {
        "exam_id": exam.exam_id,
        "kind": exam.kind,
        "level": exam.level,
        "seed": exam.seed,
        "q": 0,
        "score": 0,
        "items": [
            {
                "id": item.id,
                "level": item.level,
                "prompt": item.question.prompt,
                "options": list(item.question.options) if item.question.options else None,
                "answer": item.question.answer,
                "explain": item.question.explain,
                "kind": item.question.kind,
            }
            for item in exam.items
        ],
    }


def load_questions(payload: dict) -> list[Question]:
    out: list[Question] = []
    for raw in payload.get("items") or []:
        opts = raw.get("options")
        out.append(
            Question(
                prompt=raw["prompt"],
                options=tuple(opts) if opts else None,
                answer=str(raw["answer"]),
                explain=raw.get("explain") or "",
                kind=raw.get("kind") or "mcq",
            )
        )
    return out
