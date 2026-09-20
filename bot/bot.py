from __future__ import annotations

import logging

from telegram import BotCommand, Update
from telegram.ext import (
    AIORateLimiter,
    Application,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from . import config
from .handlers import (
    cmd_cancel,
    cmd_help,
    cmd_level,
    cmd_menu,
    cmd_start,
    cmd_stats,
    on_callback,
    on_text,
    on_voice,
)
from .store import Store

log = logging.getLogger("english-ladder")


async def post_init(app: Application) -> None:
    await app.bot.set_my_commands(
        [
            BotCommand("start", "Open English Ladder"),
            BotCommand("menu", "Main menu"),
            BotCommand("level", "Choose A1–IELTS"),
            BotCommand("stats", "XP, streak, accuracy"),
            BotCommand("help", "How the bot works"),
            BotCommand("cancel", "Stop a quiz or tutor"),
        ]
    )


async def on_error(update: object, context) -> None:
    log.exception("unhandled error for update %s", update, exc_info=context.error)
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text("Something broke. Try /menu.")
        except Exception:
            pass


def build_app(token: str | None = None) -> Application:
    tok = token or config.TELEGRAM_BOT_TOKEN
    app = (
        Application.builder()
        .token(tok)
        .rate_limiter(AIORateLimiter())
        .post_init(post_init)
        .build()
    )
    app.bot_data["store"] = Store(config.DB_PATH)
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("menu", cmd_menu))
    app.add_handler(CommandHandler("level", cmd_level))
    app.add_handler(CommandHandler("stats", cmd_stats))
    app.add_handler(CommandHandler("cancel", cmd_cancel))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, on_voice))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_error_handler(on_error)
    return app


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s  %(levelname)-7s %(name)s: %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("httpx").setLevel(logging.WARNING)
    problems = config.config_problems()
    if problems:
        for item in problems:
            log.error(item)
        raise SystemExit(1)
    if not config.XAI_API_KEY:
        log.warning("XAI_API_KEY missing — tutor/writing/speaking AI feedback is off")
    app = build_app()
    log.info("English Ladder polling…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)
