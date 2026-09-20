from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Question:
    prompt: str
    options: tuple[str, ...] | None
    answer: str
    explain: str
    kind: str = "mcq"  # mcq | fill | tfng


@dataclass(frozen=True)
class Lesson:
    id: str
    level: str
    unit: int
    title: str
    minutes: int
    goals: tuple[str, ...]
    teach: str
    vocab: tuple[tuple[str, str, str], ...] = ()
    questions: tuple[Question, ...] = ()


@dataclass(frozen=True)
class VocabItem:
    id: str
    level: str
    word: str
    meaning: str
    example: str
    extra: str = ""


@dataclass(frozen=True)
class Reading:
    id: str
    level: str
    title: str
    text: str
    questions: tuple[Question, ...] = ()


@dataclass(frozen=True)
class Prompt:
    id: str
    level: str
    skill: str  # writing | speaking
    title: str
    cue: str
    tips: tuple[str, ...] = ()
    minutes: int = 20


def q_mcq(prompt: str, options: list[str], correct_index: int, explain: str) -> Question:
    return Question(
        prompt=prompt,
        options=tuple(options),
        answer=str(correct_index),
        explain=explain,
        kind="mcq",
    )


def q_fill(prompt: str, answer: str, explain: str) -> Question:
    return Question(prompt=prompt, options=None, answer=answer, explain=explain, kind="fill")


def q_tfng(prompt: str, answer: str, explain: str) -> Question:
    """answer is TRUE, FALSE, or NOT GIVEN."""
    return Question(
        prompt=prompt,
        options=("TRUE", "FALSE", "NOT GIVEN"),
        answer={"TRUE": "0", "FALSE": "1", "NOT GIVEN": "2"}[answer.upper()],
        explain=explain,
        kind="tfng",
    )
