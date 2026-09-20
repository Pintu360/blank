# English Ladder

A Telegram bot that takes **Bangladeshi learners** from **A1 English** (hello, am/is/are) to **IELTS Band 9**.

Lessons, quizzes, and vocab work **offline** (no AI key). The tutor, writing examiner, and speaking examiner use **SpaceXAI / xAI Grok** when `XAI_API_KEY` is set.

## What you get

| Track | CEFR | IELTS | Focus |
| --- | --- | --- | --- |
| Beginner | A1 | 3.0–3.5 | Greetings, family, food, present simple — with **Bangla glosses** |
| Elementary | A2 | 4.0–4.5 | Past, market English, comparatives, will / going to |
| Intermediate | B1 | 5.0–5.5 | Present perfect, conditionals, opinions, relative clauses |
| Upper-int | B2 | 6.0–6.5 | Passive, reported speech, collocations, cohesion |
| Advanced | C1 | 7.0–8.0 | Inversion, hedging, nominalisation, PEEL essays |
| Exam | IELTS | 6.0–9.0 | Reading TFNG, Task 1/2, Speaking Parts 2–3 |

Examples use Bangladesh (Dhaka, monsoon, cricket, remittances, Sundarbans) so the English is usable at home, not only in a UK textbook.

## Setup

1. Create a bot with [@BotFather](https://t.me/BotFather) and copy the token.
2. (Optional, for the AI tutor) Create an xAI key at [console.x.ai](https://console.x.ai).
3. Install and configure:

```powershell
cd C:\Users\DELL\english-ladder-bot
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env`:

```
TELEGRAM_BOT_TOKEN=123456:ABC...
XAI_API_KEY=xai-...
```

4. Run:

```powershell
python run.py
```

Open Telegram, find your bot, tap **Start**.

## Daily path

1. **Placement test** once (or pick A1 if you are new).
2. **📚 Lesson** — teach + 4-question quiz.
3. **🧠 Vocab** — spaced repetition (Again / Hard / Good / Easy).
4. **✍️ Writing** and **🗣️ Speaking** — Grok marks like a teacher / IELTS examiner.
5. From B2 onward, use **🎯 IELTS** for Task 1, Task 2, and cue cards.

`/stats` shows XP, streak, lesson count, and quiz accuracy.

## Settings

- Bangla help on (default) or English-only feedback
- Goal band 6.0 / 7.0 / 8.0
- Jump levels if the placement test was wrong

## Tests

```powershell
pytest -q
```
