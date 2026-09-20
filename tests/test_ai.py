from __future__ import annotations

from bot.ai import complete, find_slips, grade_speaking, grade_writing


def test_finds_common_slips() -> None:
    slips = find_slips("I go yesterday market and she have two brother")
    rules = " ".join(s[2].lower() for s in slips)
    assert "went" in rules or "past" in rules
    assert any("has" in s[1].lower() or "has" in s[2].lower() for s in slips)


def test_writing_works_without_api() -> None:
    out = grade_writing(
        "My name is Rafi. I am from Dhaka. I like tea.",
        "Write about yourself.",
        "A1",
        "bn",
    )
    assert "Writing check" in out
    assert "xAI" not in out
    assert "API" not in out


def test_tutor_corrects_offline() -> None:
    reply = complete([{"role": "user", "content": "I go yesterday market"}], "A1", "bn")
    assert "went" in reply.lower() or "Past" in reply
    assert "XAI" not in reply
    assert "console.x.ai" not in reply


def test_tutor_lookup_word() -> None:
    reply = complete([{"role": "user", "content": "what is however"}], "B1", "bn")
    assert "however" in reply.lower()


def test_speaking_offline() -> None:
    out = grade_speaking("I like rain because the city is cooler.", "Do you like rain?", "B1")
    assert "Speaking check" in out
    assert "API" not in out
