import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from config import get_settings
from database import Database
from handlers import diary, help, history, start, week
from services.ai import AIService
from services.reminders import setup_reminders


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())

    db = Database(settings.database_path)
    await db.init()

    ai = AIService(api_key=settings.openrouter_api_key, model=settings.openrouter_model)
    dp["db"] = db
    dp["ai"] = ai

    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(history.router)
    dp.include_router(week.router)
    dp.include_router(diary.router)

    scheduler = setup_reminders(bot, db, settings.timezone)
    scheduler.start()

    try:
        await bot.set_my_commands(
            [
                BotCommand(command="start", description="Начать и настроить дневник"),
                BotCommand(command="diary", description="Записать сегодняшний день"),
                BotCommand(command="history", description="Последние 5 записей"),
                BotCommand(command="week", description="Итог недели"),
                BotCommand(command="help", description="Как пользоваться ботом"),
            ]
        )
        await bot.set_my_short_description("Дневник силы, маленьких побед и бережной поддержки 🤍")
        await bot.set_my_description(
            "Happy Day — мягкий AI-дневник силы. "
            "Записывай, как прошел день, что получилось, за что ты благодарна, "
            "и получай короткую персональную поддержку без давления и токсичной мотивации."
        )
        await dp.start_polling(bot)
    finally:
        scheduler.shutdown(wait=False)
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
