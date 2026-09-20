from __future__ import annotations

import hashlib
import random

from .exams import ExamItem, shuffle_question
from .models import Question, q_fill, q_mcq

NAMES = ("Rafi", "Nabila", "Karim", "Tania", "Omar", "Rina", "Sadia", "Hasan", "Mitu", "Shuvo")
CITIES = ("Dhaka", "Chattogram", "Sylhet", "Khulna", "Rajshahi", "Barishal", "Rangpur", "Cumilla")
JOBS = ("student", "teacher", "nurse", "driver", "farmer", "cook")
FOODS = ("tea", "rice", "fish", "mango", "bread", "coffee")
PLACES = ("home", "school", "college", "market", "hospital", "station", "park")
VERBS = ("swim", "cook", "drive", "sing", "read")
PAST = (("watch", "watched"), ("visit", "visited"), ("play", "played"), ("cook", "cooked"))
IRREG = (("go", "went"), ("eat", "ate"), ("buy", "bought"), ("see", "saw"), ("write", "wrote"))
HOURS = ("6", "7", "8", "9", "10")


def _id(level: str, topic: str, prompt: str) -> str:
    h = hashlib.sha1(prompt.encode("utf-8")).hexdigest()[:10]
    return f"gen:{level}:{topic}:{h}"


def _item(level: str, topic: str, q: Question, rng: random.Random) -> ExamItem:
    q = shuffle_question(q, rng)
    return ExamItem(id=_id(level, topic, q.prompt), level=level, question=q)


def _a1_be(rng: random.Random) -> ExamItem:
    name = rng.choice(NAMES)
    job = rng.choice(JOBS)
    return _item("A1", "be", q_fill(f"{name} ___ a {job}. (is)", "is", "A name + is."), rng)


def _a1_be_pron(rng: random.Random) -> ExamItem:
    subj, ans = rng.choice((("I", "am"), ("You", "are"), ("He", "is"), ("She", "is"), ("They", "are")))
    job = rng.choice(JOBS)
    noun = job if subj != "They" else job + "s"
    art = "a " if subj != "They" else ""
    return _item("A1", "be", q_fill(f"{subj} ___ {art}{noun}. ({ans})", ans, f"{subj} + {ans}."), rng)


def _a1_from(rng: random.Random) -> ExamItem:
    city = rng.choice(CITIES)
    return _item("A1", "be", q_fill(f"I am from {city}. I ___ from {city}. (am)", "am", "I am from + city."), rng)


def _a1_an(rng: random.Random) -> ExamItem:
    word, art = rng.choice((("apple", "an"), ("egg", "an"), ("orange", "an"), ("mango", "a"), ("book", "a"), ("bus", "a")))
    return _item("A1", "a-an", q_fill(f"I want ___ {word}. (a/an)", art, f"{art} + {word}."), rng)


def _a1_like(rng: random.Random) -> ExamItem:
    food = rng.choice(FOODS)
    return _item("A1", "present", q_mcq(f"I ___ {food}.", ["likes", "like", "liking"], 1, "I like."), rng)


def _a1_goes(rng: random.Random) -> ExamItem:
    place = rng.choice(PLACES)
    who = rng.choice(("He", "She"))
    return _item("A1", "present", q_fill(f"{who} ___ to {place}. (goes)", "goes", "He/She + goes."), rng)


def _a1_can(rng: random.Random) -> ExamItem:
    verb = rng.choice(VERBS)
    return _item("A1", "can", q_fill(f"I ___ {verb}. (can)", "can", "can + verb."), rng)


def _a1_cant(rng: random.Random) -> ExamItem:
    verb = rng.choice(VERBS)
    return _item(
        "A1",
        "can",
        q_mcq(f"Sorry, I ___ {verb}.", ["can to", "can't", "am can"], 1, "can't + verb."),
        rng,
    )


def _a1_at(rng: random.Random) -> ExamItem:
    return _item("A1", "place", q_fill("I am ___ home. (at)", "at", "at home."), rng)


def _a1_to(rng: random.Random) -> ExamItem:
    place = rng.choice(tuple(p for p in PLACES if p != "home"))
    return _item("A1", "place", q_mcq(f"We go ___ the {place}.", ["in", "to", "on"], 1, "go to + place."), rng)


def _a1_time(rng: random.Random) -> ExamItem:
    h = rng.choice(HOURS)
    return _item("A1", "time", q_fill(f"It is {h} ___. (o'clock)", "o'clock|oclock", "o'clock."), rng)


def _a1_have(rng: random.Random) -> ExamItem:
    n = rng.choice(("one", "two", "three"))
    who, ans = rng.choice((("I", "have"), ("She", "has"), ("He", "has")))
    return _item("A1", "have", q_fill(f"{who} ___ {n} sister(s). ({ans})", ans, f"{who} {ans}."), rng)


def _a1_hello(rng: random.Random) -> ExamItem:
    return _item(
        "A1",
        "hello",
        q_mcq("Choose a greeting.", ["Goodbye only", "Hello", "Yesterday"], 1, "Hello = greeting."),
        rng,
    )


def _a2_past(rng: random.Random) -> ExamItem:
    name = rng.choice(NAMES)
    base, past = rng.choice(PAST)
    obj = rng.choice(("TV", "football", "a friend"))
    return _item("A2", "past", q_fill(f"Yesterday {name} ___ {obj}. ({past})", past, f"{base} → {past}."), rng)


def _a2_did(rng: random.Random) -> ExamItem:
    place = rng.choice(PLACES)
    return _item("A2", "past", q_mcq(f"Did you ___ to the {place}?", ["went", "go", "gone"], 1, "Did + base verb."), rng)


def _a2_went(rng: random.Random) -> ExamItem:
    city = rng.choice(CITIES)
    base, past = rng.choice(IRREG)
    if base != "go":
        obj = rng.choice(("an apple", "a shirt", "a film"))
        return _item("A2", "past", q_fill(f"Last week I ___ {obj}. ({past})", past, f"{base} → {past}."), rng)
    return _item("A2", "past", q_fill(f"Last year I ___ to {city}. (went)", "went", "go → went."), rng)


def _a2_many(rng: random.Random) -> ExamItem:
    return _item("A2", "some-any", q_fill("How ___ mangoes? (many)", "many", "countable → many."), rng)


def _a2_much(rng: random.Random) -> ExamItem:
    thing = rng.choice(("water", "rice", "tea", "sugar"))
    return _item("A2", "some-any", q_fill(f"How ___ {thing}? (much)", "much", "uncountable → much."), rng)


def _a2_any(rng: random.Random) -> ExamItem:
    thing = rng.choice(("milk", "sugar", "tea"))
    return _item("A2", "some-any", q_mcq(f"We haven't got ___ {thing}.", ["some", "any", "a"], 1, "negative → any."), rng)


def _a2_than(rng: random.Random) -> ExamItem:
    a, b = rng.sample(list(CITIES), 2)
    return _item("A2", "compare", q_fill(f"{a} is bigger ___ {b}. (than)", "than", "comparative + than."), rng)


def _a2_better(rng: random.Random) -> ExamItem:
    return _item("A2", "compare", q_mcq("good → ___", ["gooder", "better", "more good"], 1, "good → better."), rng)


def _a2_going(rng: random.Random) -> ExamItem:
    city = rng.choice(CITIES)
    return _item("A2", "future", q_fill(f"I am ___ to visit {city}. (going)", "going", "going to = plan."), rng)


def _a2_will(rng: random.Random) -> ExamItem:
    return _item("A2", "future", q_fill("I think it ___ rain. (will)", "will", "prediction → will."), rng)


def _a2_dir(rng: random.Random) -> ExamItem:
    way = rng.choice(("left", "right"))
    wrong = "right" if way == "left" else "left"
    return _item("A2", "directions", q_mcq(f"Turn ___.", [wrong, way, "under"], 1, f"Turn {way}."), rng)


def _b1_since(rng: random.Random) -> ExamItem:
    year = rng.choice(("2019", "2020", "2021", "2022"))
    return _item("B1", "perfect", q_fill(f"I have lived here ___ {year}. (since)", "since", "since + point in time."), rng)


def _b1_ever(rng: random.Random) -> ExamItem:
    city = rng.choice(CITIES)
    return _item("B1", "perfect", q_fill(f"Have you ___ been to {city}?", "ever", "ever in questions."), rng)


def _b1_will(rng: random.Random) -> ExamItem:
    return _item("B1", "conditional", q_fill("If I study, I ___ pass. (will)", "will", "first conditional."), rng)


def _b1_were(rng: random.Random) -> ExamItem:
    return _item("B1", "conditional", q_fill("If I ___ you, I would start today. (were)", "were", "If I were you."), rng)


def _b1_should(rng: random.Random) -> ExamItem:
    return _item(
        "B1",
        "modals",
        q_mcq("Advice: you ___ review every day.", ["should", "mustn't to", "are"], 0, "should = advice."),
        rng,
    )


def _b1_who(rng: random.Random) -> ExamItem:
    return _item(
        "B1",
        "relative",
        q_mcq("The woman ___ teaches us is kind.", ["which", "who", "where"], 1, "who + people."),
        rng,
    )


def _b1_opinion(rng: random.Random) -> ExamItem:
    return _item("B1", "opinions", q_fill("___ my opinion, reading helps.", "In", "In my opinion."), rng)


def _b2_passive(rng: random.Random) -> ExamItem:
    return _item("B2", "passive", q_fill("Bangla ___ spoken here. (is)", "is", "present passive."), rng)


def _b2_said(rng: random.Random) -> ExamItem:
    return _item("B2", "reported", q_mcq("She said she ___ tired.", ["is", "was", "were"], 1, "backshift am → was."), rng)


def _b2_make(rng: random.Random) -> ExamItem:
    return _item("B2", "collocation", q_fill("___ a decision (make/do)", "make", "make a decision."), rng)


def _b2_result(rng: random.Random) -> ExamItem:
    return _item("B2", "cohesion", q_fill("As a ___, traffic increased. (result)", "result", "As a result."), rng)


def _b2_told(rng: random.Random) -> ExamItem:
    name = rng.choice(NAMES)
    return _item("B2", "reported", q_fill(f"He ___ {name} to wait. (told)", "told", "tell + person."), rng)


def _c1_never(rng: random.Random) -> ExamItem:
    return _item("C1", "inversion", q_mcq("Never ___ I seen such rain.", ["I have", "have I", "I had"], 1, "Never + have I."), rng)


def _c1_suggest(rng: random.Random) -> ExamItem:
    return _item("C1", "stance", q_fill("The figures ___ that demand rose. (suggest)", "suggest", "figures suggest."), rng)


def _c1_noun(rng: random.Random) -> ExamItem:
    return _item("C1", "nominalisation", q_fill("develop → ___", "development", "verb → noun."), rng)


def _ielts_ng(rng: random.Random) -> ExamItem:
    return _item(
        "IELTS",
        "reading",
        q_mcq("The passage does not mention X.", ["TRUE", "FALSE", "NOT GIVEN"], 2, "No info → NOT GIVEN."),
        rng,
    )


def _ielts_overview(rng: random.Random) -> ExamItem:
    return _item("IELTS", "writing", q_fill("Task 1 needs an ___. (overview)", "overview", "overview is required."), rng)


MAKERS: dict[str, tuple] = {
    "A1": (_a1_be, _a1_be_pron, _a1_from, _a1_an, _a1_like, _a1_goes, _a1_can, _a1_cant, _a1_at, _a1_to, _a1_time, _a1_have, _a1_hello),
    "A2": (_a2_past, _a2_did, _a2_went, _a2_many, _a2_much, _a2_any, _a2_than, _a2_better, _a2_going, _a2_will, _a2_dir, _a1_can, _a1_goes),
    "B1": (_b1_since, _b1_ever, _b1_will, _b1_were, _b1_should, _b1_who, _b1_opinion, _a2_than, _a2_will),
    "B2": (_b2_passive, _b2_said, _b2_make, _b2_result, _b2_told, _b1_should, _b1_who),
    "C1": (_c1_never, _c1_suggest, _c1_noun, _b2_passive, _b2_said, _ielts_overview),
    "IELTS": (_ielts_ng, _ielts_overview, _c1_never, _c1_suggest, _b2_passive, _b1_will),
}

TOPIC_MAKERS: dict[str, tuple] = {
    "be": (_a1_be, _a1_be_pron, _a1_from),
    "a-an": (_a1_an,),
    "present": (_a1_like, _a1_goes, _a1_have),
    "can": (_a1_can, _a1_cant),
    "place": (_a1_at, _a1_to),
    "time": (_a1_time,),
    "have": (_a1_have,),
    "hello": (_a1_hello,),
    "past": (_a2_past, _a2_did, _a2_went),
    "some-any": (_a2_many, _a2_much, _a2_any),
    "compare": (_a2_than, _a2_better),
    "future": (_a2_going, _a2_will),
    "directions": (_a2_dir,),
    "perfect": (_b1_since, _b1_ever),
    "conditional": (_b1_will, _b1_were),
    "modals": (_b1_should,),
    "relative": (_b1_who,),
    "opinions": (_b1_opinion,),
    "passive": (_b2_passive,),
    "reported": (_b2_said, _b2_told),
    "collocation": (_b2_make,),
    "cohesion": (_b2_result,),
    "inversion": (_c1_never,),
    "stance": (_c1_suggest,),
    "nominalisation": (_c1_noun,),
    "reading": (_ielts_ng,),
    "writing": (_ielts_overview,),
}


def generate_items(
    level: str,
    n: int,
    rng: random.Random,
    topic: str | None = None,
    avoid_ids: set[str] | None = None,
) -> list[ExamItem]:
    avoid = avoid_ids or set()
    pool = list(TOPIC_MAKERS.get(topic or "", ())) or list(MAKERS.get(level, MAKERS["A1"]))
    items: list[ExamItem] = []
    seen: set[str] = set()
    tries = 0
    while len(items) < n and tries < n * 25:
        tries += 1
        maker = rng.choice(pool)
        item = maker(rng)
        if item.id in avoid or item.question.prompt in seen:
            continue
        seen.add(item.question.prompt)
        items.append(item)
    return items
