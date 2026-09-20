# English Ladder

A full English **course** on Telegram — **zero to advanced**, then **IELTS Band 9**. Built for anyone (Bangla help on by default).

**No xAI / OpenAI key.** Only a Telegram bot token.

Tap buttons. You only type for writing, speaking, and the tutor.

## Course path

| | Level | You can… |
| --- | --- | --- |
| 🌱 | **A1 Beginner** | Hello, family, food, time, places, *can / can't* |
| 🌿 | **A2 Elementary** | Past, shopping, comparisons, directions, future |
| 🌳 | **B1 Intermediate** | Experiences, opinions, interviews, conditionals |
| 🏔️ | **B2 Upper-int** | Passive, reported speech, academic collocations |
| 🎯 | **C1 Advanced** | Hedging, inversion, PEEL essays, precise lexis |
| 🏆 | **IELTS** | Reading TFNG, Task 1 & 2, Speaking Parts 2–3 |

Units unlock one by one. Finish a lesson → the next one opens.

## App-style UI

- **Home** — streak, XP, progress bar, today’s lesson
- **Continue** — one tap to the next unlocked unit
- **📝 Test** — a **new paper every time** (code like `EL-A1B2`). Quick / level / basic / mixed
- **📘 Rules** — 12 basic grammar cards (am/is/are, a/an, present, can, past…)
- **Course map** — every level, ✅ ▶ 🔒
- **Practice** — words, grammar, reading, listen & read, writing, speaking, IELTS
- **👩‍🏫 Teacher** — offline. Teaches a grammar point, then **mints a new test every time** (new names, cities, verbs). `/teacher`
- **Tutor** — type a sentence to check (from Teacher → Check a sentence)
- Quizzes are **tap the answer**, not A/B/C/D codes

## Setup

1. [@BotFather](https://t.me/BotFather) → `/newbot` → copy the token

```powershell
cd C:\Users\DELL\english-ladder-bot
python -m pip install -r requirements.txt
copy .env.example .env
notepad .env
python run.py
```

`.env`:

```
TELEGRAM_BOT_TOKEN=123456:ABC...
```

Open the bot in Telegram → **Start** → **Start from zero** or **Find my level**.

## Deploy on Railway

This is a **worker** (long polling), not a website. Do not set a public HTTP port.

1. Push this repo (already on GitHub).
2. [Railway](https://railway.app) → **New project** → **Deploy from GitHub** → `Pintu360/blank`.
3. Variables → add:

```
TELEGRAM_BOT_TOKEN=123456:ABC...
```

4. Deploy. Start command is `python run.py` (see `Procfile` + `railway.toml`).

If Railway marks the service as “web” and it dies, switch it to a **worker** service. No `PORT` is required.

## Tests

```powershell
python -m pytest -q tests
```
