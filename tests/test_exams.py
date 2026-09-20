from __future__ import annotations

from bot.curriculum.exams import BANK, build_exam, dump_exam, load_questions
from bot.curriculum.grammar_rules import BASIC_RULES, get_rule
from bot.curriculum.models import Question


def test_two_papers_are_different() -> None:
    a = build_exam("A1", "quick", "seed-one", [])
    b = build_exam("A1", "quick", "seed-two", [])
    assert a.exam_id != b.exam_id
    ids_a = [item.id for item in a.items]
    ids_b = [item.id for item in b.items]
    assert ids_a != ids_b or [item.question.options for item in a.items] != [
        item.question.options for item in b.items
    ]


def test_avoid_repeats() -> None:
    first = build_exam("A1", "quick", "alpha", [])
    used = [item.id for item in first.items]
    second = build_exam("A1", "quick", "beta", used)
    overlap = set(used) & {item.id for item in second.items}
    # Bank is large enough that a fresh paper should mostly avoid the last one
    assert len(overlap) < len(used)


def test_dump_load_roundtrip() -> None:
    exam = build_exam("B1", "level", "roundtrip", [])
    payload = dump_exam(exam)
    questions = load_questions(payload)
    assert len(questions) == len(exam.items)
    assert questions[0].prompt == exam.items[0].question.prompt
    assert questions[0].answer == exam.items[0].question.answer


def test_basic_test_stays_beginner() -> None:
    exam = build_exam("C1", "basic", "basic-seed", [])
    assert {item.level for item in exam.items} <= {"A1", "A2"}


def test_bank_has_extra_papers() -> None:
    extra = [row for row in BANK if row[0].startswith("ex-")]
    assert len(extra) >= 30


def test_generator_mints_new_paper_every_seed() -> None:
    from bot.curriculum.exams import build_exam

    a = build_exam("A1", "teacher", "teacher-seed-1", [])
    b = build_exam("A1", "teacher", "teacher-seed-2", [])
    assert a.exam_id != b.exam_id
    prompts_a = [item.question.prompt for item in a.items]
    prompts_b = [item.question.prompt for item in b.items]
    assert prompts_a != prompts_b
    assert len(a.items) >= 6


def test_teacher_topics_rotate() -> None:
    from bot.teacher import next_topic

    first = next_topic("A1", 0)
    later = next_topic("A1", 1)
    assert first.id
    assert later.id
    assert first.id != later.id or next_topic("A1", 2).id != first.id


def test_grammar_rules_cover_basics() -> None:
    ids = {rule.id for rule in BASIC_RULES}
    assert {"be", "a-an", "present", "can", "past", "some-any"} <= ids
    assert get_rule("be") is not None
    for rule in BASIC_RULES:
        assert rule.body
        assert len(rule.questions) >= 3
        for q in rule.questions:
            assert isinstance(q, Question)
            if q.options:
                assert 0 <= int(q.answer) < len(q.options)
