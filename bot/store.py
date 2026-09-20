from __future__ import annotations

import json
import sqlite3
import threading
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from .srs import due_on, review


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._lock = threading.Lock()
        self._conn = sqlite3.connect(path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA foreign_keys=ON")
        self._migrate()

    def close(self) -> None:
        with self._lock:
            self._conn.close()

    def _migrate(self) -> None:
        self._conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                level TEXT NOT NULL DEFAULT 'A1',
                native_lang TEXT NOT NULL DEFAULT 'bn',
                xp INTEGER NOT NULL DEFAULT 0,
                streak INTEGER NOT NULL DEFAULT 0,
                last_active TEXT,
                last_lesson_date TEXT,
                goal_band TEXT DEFAULT '7.0',
                mode TEXT NOT NULL DEFAULT 'idle',
                payload TEXT NOT NULL DEFAULT '{}',
                completed TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS cards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                word_id TEXT NOT NULL,
                ease REAL NOT NULL DEFAULT 2.5,
                interval INTEGER NOT NULL DEFAULT 0,
                repetitions INTEGER NOT NULL DEFAULT 0,
                due_on TEXT NOT NULL,
                UNIQUE(telegram_id, word_id)
            );

            CREATE TABLE IF NOT EXISTS attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                kind TEXT NOT NULL,
                item_id TEXT NOT NULL,
                correct INTEGER NOT NULL,
                score REAL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS chat_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS exams (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                exam_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                level TEXT NOT NULL,
                score INTEGER NOT NULL,
                total INTEGER NOT NULL,
                item_ids TEXT NOT NULL DEFAULT '[]',
                created_at TEXT NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_cards_due ON cards(telegram_id, due_on);
            CREATE INDEX IF NOT EXISTS idx_attempts_user ON attempts(telegram_id, kind);
            CREATE INDEX IF NOT EXISTS idx_chat_user ON chat_log(telegram_id, id);
            CREATE INDEX IF NOT EXISTS idx_exams_user ON exams(telegram_id, id);
            """
        )
        self._conn.commit()

    def _execute(self, sql: str, params: tuple = ()) -> sqlite3.Cursor:
        with self._lock:
            cur = self._conn.execute(sql, params)
            self._conn.commit()
            return cur

    def _fetchone(self, sql: str, params: tuple = ()) -> sqlite3.Row | None:
        with self._lock:
            return self._conn.execute(sql, params).fetchone()

    def _fetchall(self, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
        with self._lock:
            return list(self._conn.execute(sql, params).fetchall())

    def get_user(self, telegram_id: int) -> dict[str, Any] | None:
        row = self._fetchone("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,))
        return dict(row) if row else None

    def upsert_user(self, telegram_id: int, username: str | None, first_name: str | None) -> dict[str, Any]:
        existing = self.get_user(telegram_id)
        if existing:
            self._execute(
                "UPDATE users SET username = ?, first_name = ? WHERE telegram_id = ?",
                (username, first_name, telegram_id),
            )
            return self.get_user(telegram_id) or existing
        self._execute(
            """
            INSERT INTO users (telegram_id, username, first_name, created_at, last_active)
            VALUES (?, ?, ?, ?, ?)
            """,
            (telegram_id, username, first_name, _now(), _now()),
        )
        return self.get_user(telegram_id)  # type: ignore[return-value]

    def touch(self, telegram_id: int) -> None:
        user = self.get_user(telegram_id)
        if not user:
            return
        today = date.today().isoformat()
        last = (user.get("last_active") or "")[:10]
        streak = int(user["streak"] or 0)
        if last == today:
            new_streak = streak
        elif last == date.fromordinal(date.today().toordinal() - 1).isoformat():
            new_streak = streak + 1
        elif not last:
            new_streak = 1
        else:
            new_streak = 1
        self._execute(
            "UPDATE users SET last_active = ?, streak = ? WHERE telegram_id = ?",
            (_now(), new_streak, telegram_id),
        )

    def set_level(self, telegram_id: int, level: str) -> None:
        self._execute("UPDATE users SET level = ? WHERE telegram_id = ?", (level, telegram_id))

    def set_native(self, telegram_id: int, lang: str) -> None:
        self._execute("UPDATE users SET native_lang = ? WHERE telegram_id = ?", (lang, telegram_id))

    def set_goal(self, telegram_id: int, band: str) -> None:
        self._execute("UPDATE users SET goal_band = ? WHERE telegram_id = ?", (band, telegram_id))

    def set_mode(self, telegram_id: int, mode: str, payload: dict | None = None) -> None:
        self._execute(
            "UPDATE users SET mode = ?, payload = ? WHERE telegram_id = ?",
            (mode, json.dumps(payload or {}, ensure_ascii=False), telegram_id),
        )

    def payload(self, telegram_id: int) -> dict[str, Any]:
        user = self.get_user(telegram_id)
        if not user:
            return {}
        try:
            data = json.loads(user.get("payload") or "{}")
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}

    def completed(self, telegram_id: int) -> list[str]:
        user = self.get_user(telegram_id)
        if not user:
            return []
        try:
            data = json.loads(user.get("completed") or "[]")
            return list(data) if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    def mark_complete(self, telegram_id: int, lesson_id: str) -> None:
        done = self.completed(telegram_id)
        if lesson_id not in done:
            done.append(lesson_id)
        today = date.today().isoformat()
        self._execute(
            "UPDATE users SET completed = ?, last_lesson_date = ? WHERE telegram_id = ?",
            (json.dumps(done), today, telegram_id),
        )

    def add_xp(self, telegram_id: int, amount: int) -> int:
        self._execute("UPDATE users SET xp = xp + ? WHERE telegram_id = ?", (amount, telegram_id))
        user = self.get_user(telegram_id)
        return int(user["xp"]) if user else 0

    def log_attempt(self, telegram_id: int, kind: str, item_id: str, correct: bool, score: float | None = None) -> None:
        self._execute(
            """
            INSERT INTO attempts (telegram_id, kind, item_id, correct, score, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (telegram_id, kind, item_id, int(correct), score, _now()),
        )

    def accuracy(self, telegram_id: int, kind: str | None = None) -> tuple[int, int]:
        if kind:
            rows = self._fetchall(
                "SELECT correct FROM attempts WHERE telegram_id = ? AND kind = ?",
                (telegram_id, kind),
            )
        else:
            rows = self._fetchall("SELECT correct FROM attempts WHERE telegram_id = ?", (telegram_id,))
        total = len(rows)
        right = sum(int(r["correct"]) for r in rows)
        return right, total

    def ensure_card(self, telegram_id: int, word_id: str) -> None:
        today = date.today().isoformat()
        self._execute(
            """
            INSERT OR IGNORE INTO cards (telegram_id, word_id, due_on)
            VALUES (?, ?, ?)
            """,
            (telegram_id, word_id, today),
        )

    def due_cards(self, telegram_id: int, limit: int = 12) -> list[dict[str, Any]]:
        today = date.today().isoformat()
        rows = self._fetchall(
            """
            SELECT * FROM cards
            WHERE telegram_id = ? AND due_on <= ?
            ORDER BY due_on ASC, id ASC
            LIMIT ?
            """,
            (telegram_id, today, limit),
        )
        return [dict(r) for r in rows]

    def card_count(self, telegram_id: int) -> tuple[int, int]:
        today = date.today().isoformat()
        total = self._fetchone(
            "SELECT COUNT(*) AS n FROM cards WHERE telegram_id = ?", (telegram_id,)
        )
        due = self._fetchone(
            "SELECT COUNT(*) AS n FROM cards WHERE telegram_id = ? AND due_on <= ?",
            (telegram_id, today),
        )
        return int(due["n"] if due else 0), int(total["n"] if total else 0)

    def review_card(self, telegram_id: int, word_id: str, quality: int) -> None:
        row = self._fetchone(
            "SELECT * FROM cards WHERE telegram_id = ? AND word_id = ?",
            (telegram_id, word_id),
        )
        if not row:
            self.ensure_card(telegram_id, word_id)
            row = self._fetchone(
                "SELECT * FROM cards WHERE telegram_id = ? AND word_id = ?",
                (telegram_id, word_id),
            )
        if not row:
            return
        ease, interval, reps = review(row["ease"], row["interval"], row["repetitions"], quality)
        self._execute(
            """
            UPDATE cards
            SET ease = ?, interval = ?, repetitions = ?, due_on = ?
            WHERE telegram_id = ? AND word_id = ?
            """,
            (ease, interval, reps, due_on(interval), telegram_id, word_id),
        )

    def add_chat(self, telegram_id: int, role: str, content: str) -> None:
        self._execute(
            "INSERT INTO chat_log (telegram_id, role, content, created_at) VALUES (?, ?, ?, ?)",
            (telegram_id, role, content, _now()),
        )
        extra = self._fetchall(
            """
            SELECT id FROM chat_log WHERE telegram_id = ?
            ORDER BY id DESC LIMIT -1 OFFSET 24
            """,
            (telegram_id,),
        )
        if extra:
            cutoff = extra[-1]["id"]
            self._execute(
                "DELETE FROM chat_log WHERE telegram_id = ? AND id <= ?",
                (telegram_id, cutoff),
            )

    def chat_history(self, telegram_id: int, limit: int = 12) -> list[dict[str, str]]:
        rows = self._fetchall(
            """
            SELECT role, content FROM chat_log
            WHERE telegram_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (telegram_id, limit),
        )
        return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]

    def clear_chat(self, telegram_id: int) -> None:
        self._execute("DELETE FROM chat_log WHERE telegram_id = ?", (telegram_id,))

    def save_exam(
        self,
        telegram_id: int,
        exam_id: str,
        kind: str,
        level: str,
        score: int,
        total: int,
        item_ids: list[str],
    ) -> None:
        self._execute(
            """
            INSERT INTO exams (telegram_id, exam_id, kind, level, score, total, item_ids, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (telegram_id, exam_id, kind, level, score, total, json.dumps(item_ids), _now()),
        )

    def list_exams(self, telegram_id: int, limit: int = 5) -> list[dict[str, Any]]:
        rows = self._fetchall(
            """
            SELECT exam_id, kind, level, score, total, created_at
            FROM exams WHERE telegram_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (telegram_id, limit),
        )
        return [dict(r) for r in rows]

    def exam_count(self, telegram_id: int) -> int:
        row = self._fetchone("SELECT COUNT(*) AS n FROM exams WHERE telegram_id = ?", (telegram_id,))
        return int(row["n"] if row else 0)

    def recent_exam_item_ids(self, telegram_id: int, limit: int = 8) -> list[str]:
        rows = self._fetchall(
            """
            SELECT item_ids FROM exams WHERE telegram_id = ?
            ORDER BY id DESC LIMIT ?
            """,
            (telegram_id, limit),
        )
        out: list[str] = []
        for row in rows:
            try:
                ids = json.loads(row["item_ids"] or "[]")
            except json.JSONDecodeError:
                ids = []
            if isinstance(ids, list):
                out.extend(str(x) for x in ids)
        return out
