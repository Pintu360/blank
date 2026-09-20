# English Ladder

A full English **course** on Telegram — **zero to advanced**, then **IELTS Band 9**. Built for anyone (Bangla help on by default).

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
- **Course map** — every level, ✅ ▶ 🔒
- **Practice** — words, grammar, reading, listen & read, writing, speaking, IELTS
- **Tutor** — Grok corrects your English at your level
- Quizzes are **tap the answer**, not A/B/C/D codes

Lessons and quizzes work without an AI key. Tutor / writing / speaking need `XAI_API_KEY`.

## Setup

1. [@BotFather](https://t.me/BotFather) → `/newbot` → copy the token  
2. Optional tutor key: [console.x.ai](https://console.x.ai)

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
XAI_API_KEY=xai-...
```

Open the bot in Telegram → **Start** → **Start from zero** or **Find my level**.

## Tests

```powershell
python -m pytest -q tests
```
