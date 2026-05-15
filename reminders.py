from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

from database import Database


REMINDER_TEXT = "Давай сохраним этот день 🤍 Что сегодня получилось?"


def setup_reminders(bot: Bot, db: Database, timezone: str) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone=timezone)

    async def send_daily_reminders() -> None:
        users = await db.list_users()
        for user in users:
            try:
                await bot.send_message(user["telegram_id"], REMINDER_TEXT)
            except Exception:
                # Пользователь мог заблокировать бота или удалить чат.
                continue

    scheduler.add_job(send_daily_reminders, CronTrigger(hour=21, minute=0, timezone=timezone))
    return scheduler
