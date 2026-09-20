from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "english.sqlite3"

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
XAI_API_KEY = os.getenv("XAI_API_KEY", "").strip()
XAI_BASE_URL = os.getenv("XAI_BASE_URL", "https://api.x.ai/v1").strip() or "https://api.x.ai/v1"
XAI_MODEL = os.getenv("XAI_MODEL", "grok-4.6").strip() or "grok-4.6"


def _parse_ids(raw: str) -> set[int]:
    out: set[int] = set()
    for chunk in raw.replace(";", ",").split(","):
        chunk = chunk.strip()
        if chunk.lstrip("-").isdigit():
            out.add(int(chunk))
    return out


ALLOWED_USER_IDS: set[int] = _parse_ids(os.getenv("ALLOWED_USER_IDS", ""))


def config_problems(require_telegram: bool = True) -> list[str]:
    problems: list[str] = []
    if require_telegram and not TELEGRAM_BOT_TOKEN:
        problems.append("TELEGRAM_BOT_TOKEN is missing from .env (get one from @BotFather)")
    return problems
