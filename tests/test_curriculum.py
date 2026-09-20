from __future__ import annotations

from bot.curriculum.lessons import LESSONS, get_lesson, lessons_for_level, next_lesson
from bot.ui import bar, lesson_unlocked, stars
from bot.curriculum.levels import LEVELS
from bot.curriculum.placement import PLACEMENT, PLACEMENT_LEVELS, place_from_results
from bot.curriculum.reading import READINGS
from bot.curriculum.skills import SPEAKING, WRITING
from bot.curriculum.vocab import VOCAB
from bot.util import answers_match


def test_every_level_has_lessons() -> None:
    for level in LEVELS:
        pack = lessons_for_level(level)
        assert len(pack) >= 5, level
        for lesson in pack:
            assert lesson.questions, lesson.id
            assert lesson.teach
            assert lesson.level == level


def test_lesson_ids_unique() -> None:
    ids = [lesson.id for lesson in LESSONS]
    assert len(ids) == len(set(ids))


def test_next_lesson_skips_completed() -> None:
    first = lessons_for_level("A1")[0]
    nxt = next_lesson("A1", [first.id])
    assert nxt is not None
    assert nxt.id != first.id
    all_ids = [lesson.id for lesson in lessons_for_level("A1")]
    assert next_lesson("A1", all_ids) is None


def test_get_lesson() -> None:
    assert get_lesson("a1-01") is not None
    assert get_lesson("missing") is None


def test_vocab_unique_and_complete() -> None:
    ids = [item.id for item in VOCAB]
    assert len(ids) == len(set(ids))
    for level in LEVELS:
        assert any(item.level == level for item in VOCAB), level


def test_placement_maps_levels() -> None:
    assert len(PLACEMENT) == len(PLACEMENT_LEVELS) == 12
    none_right = [False] * 12
    assert place_from_results(none_right) == "A1"
    all_right = [True] * 12
    assert place_from_results(all_right) == "IELTS"
    a2_only = [True, True, True, True] + [False] * 8
    assert place_from_results(a2_only) in {"A2", "A1"}


def test_reading_and_prompts_cover_ladder() -> None:
    reading_levels = {item.level for item in READINGS}
    for level in LEVELS:
        assert level in reading_levels
    assert any(p.id.startswith("w-ielts") for p in WRITING)
    assert any(p.id.startswith("s-ielts") for p in SPEAKING)


def test_mcq_answers_in_range() -> None:
    for lesson in LESSONS:
        for q in lesson.questions:
            if q.options:
                idx = int(q.answer)
                assert 0 <= idx < len(q.options)


def test_answer_matching() -> None:
    assert answers_match("am", "AM")
    assert answers_match("I'll|I will", "I will")
    assert answers_match("mustn't|must not", "must not")
    assert not answers_match("am", "is")


def test_beginner_track_has_time_places_can() -> None:
    ids = {les.id for les in lessons_for_level("A1")}
    assert {"a1-06", "a1-07", "a1-08"} <= ids
    assert get_lesson("a1-08") is not None


def test_progress_bar_and_unlock() -> None:
    assert bar(0, 8) == "▱" * 8
    assert bar(8, 8) == "▰" * 8
    assert stars(4, 4) == "⭐" * 5
    pack = lessons_for_level("A1")
    first = pack[0]
    second = pack[1]
    assert lesson_unlocked(pack, first.id, [])
    assert not lesson_unlocked(pack, second.id, [])
    assert lesson_unlocked(pack, second.id, [first.id])
