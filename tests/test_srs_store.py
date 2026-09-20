from __future__ import annotations

import tempfile
from pathlib import Path

from bot.srs import due_on, review
from bot.store import Store


def test_review_again_resets() -> None:
    ease, interval, reps = review(2.5, 10, 4, 1)
    assert reps == 0
    assert interval == 1
    assert ease >= 1.3


def test_review_good_grows_interval() -> None:
    ease, interval, reps = review(2.5, 6, 2, 4)
    assert reps == 3
    assert interval >= 6
    assert ease >= 2.5


def test_due_on_format() -> None:
    assert len(due_on(0)) == 10


def test_store_user_and_cards() -> None:
    with tempfile.TemporaryDirectory() as raw:
        db = Store(Path(raw) / "t.sqlite3")
        user = db.upsert_user(1, "rafi", "Rafi")
        assert user["level"] == "A1"
        assert user["native_lang"] == "bn"
        db.set_level(1, "B1")
        db.add_xp(1, 40)
        db.mark_complete(1, "a1-01")
        assert "a1-01" in db.completed(1)
        db.ensure_card(1, "a1-hello")
        due, total = db.card_count(1)
        assert total == 1
        assert due == 1
        db.review_card(1, "a1-hello", 5)
        due_after, _ = db.card_count(1)
        assert due_after == 0
        db.log_attempt(1, "lesson", "a1-01:0", True)
        right, n = db.accuracy(1)
        assert (right, n) == (1, 1)
        db.close()
