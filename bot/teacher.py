from __future__ import annotations

from dataclasses import dataclass

from .curriculum.grammar_rules import get_rule
from .curriculum.levels import LEVELS, level_index


@dataclass(frozen=True)
class Topic:
    id: str
    title: str
    title_bn: str
    levels: tuple[str, ...]
    teach: str


TOPICS: tuple[Topic, ...] = (
    Topic("hello", "Hello and names", "নমস্কার", ("A1",), "Say Hello / Hi. My name is … I am from Bangladesh."),
    Topic("be", "I am / You are / He is", "আমি / তুমি / সে", ("A1",), ""),
    Topic("a-an", "a / an", "একটা", ("A1",), ""),
    Topic("have", "have / has", "আছে", ("A1",), ""),
    Topic("present", "Present simple", "প্রতিদিন", ("A1", "A2"), ""),
    Topic("can", "can / can't", "পারা", ("A1", "A2"), ""),
    Topic("place", "in / on / at / to", "জায়গা", ("A1", "A2"), ""),
    Topic("time", "Days and time", "সময়", ("A1",), ""),
    Topic("past", "Past simple", "গতকাল", ("A2", "B1"), ""),
    Topic("some-any", "some / any / much / many", "কিছু / কোনো", ("A2",), ""),
    Topic("compare", "bigger / better / than", "তুলনা", ("A2", "B1"), ""),
    Topic("future", "will / going to", "ভবিষ্যৎ", ("A2", "B1"), ""),
    Topic("directions", "left / right / straight", "রাস্তা", ("A2",), ""),
    Topic("perfect", "Present perfect", "অভিজ্ঞতা", ("B1", "B2"), "I have visited Cox's Bazar. I went in 2022. for + period, since + start."),
    Topic("conditional", "If… will / would", "শর্ত", ("B1", "B2"), "If I study, I will pass. If I were you, I would start today."),
    Topic("modals", "should / must / might", "পরামর্শ", ("B1", "B2"), ""),
    Topic("relative", "who / which / that", "যে / যা", ("B1", "B2"), ""),
    Topic("opinions", "In my opinion", "মতামত", ("B1", "B2"), ""),
    Topic("passive", "is spoken / was built", "passive", ("B2", "C1", "IELTS"), ""),
    Topic("reported", "She said that…", "reported speech", ("B2", "C1"), ""),
    Topic("collocation", "make a decision", "word pairs", ("B2", "C1"), ""),
    Topic("cohesion", "As a result / this", "সংযোগ", ("B2", "C1"), ""),
    Topic("inversion", "Never have I…", "জোর", ("C1", "IELTS"), ""),
    Topic("stance", "The data suggest…", "সতর্ক দাবি", ("C1", "IELTS"), ""),
    Topic("nominalisation", "reduction / development", "noun from verb", ("C1", "IELTS"), ""),
    Topic("reading", "TRUE / FALSE / NOT GIVEN", "IELTS reading", ("IELTS",), ""),
    Topic("writing", "Task 1 overview", "IELTS writing", ("IELTS",), ""),
)


RULE_FOR_TOPIC = {
    "be": "be",
    "a-an": "a-an",
    "present": "present",
    "have": "have",
    "can": "can",
    "place": "prepositions",
    "time": "prepositions",
    "past": "past",
    "some-any": "some-any",
    "compare": "compare",
    "future": "future",
}


def topics_for(level: str) -> list[Topic]:
    i = level_index(level)
    allowed = set(LEVELS[: i + 1])
    # prefer this level, but keep earlier basics in the mix
    here = [t for t in TOPICS if level in t.levels]
    earlier = [t for t in TOPICS if level not in t.levels and any(lv in allowed for lv in t.levels)]
    return here or earlier or list(TOPICS)


def next_topic(level: str, n: int) -> Topic:
    pool = topics_for(level)
    return pool[n % len(pool)]


def teach_text(topic: Topic) -> str:
    rid = RULE_FOR_TOPIC.get(topic.id)
    if rid:
        rule = get_rule(rid)
        if rule:
            return f"<b>{rule.title}</b>\n<i>{rule.title_bn}</i>\n\n{rule.body}"
    extra = topic.teach or "Read the examples. Then take a new test — the questions will not repeat."
    return f"<b>{topic.title}</b>\n<i>{topic.title_bn}</i>\n\n{extra}"
