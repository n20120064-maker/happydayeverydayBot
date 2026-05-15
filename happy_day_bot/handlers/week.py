from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from database import Database
from services.ai import AIService


router = Router()


@router.message(Command("week"))
@router.message(F.text == "Итог недели")
async def week_summary(message: Message, db: Database, ai: AIService) -> None:
    user = await db.get_user_by_telegram_id(message.from_user.id)
    entries = await db.get_week_entries(message.from_user.id)

    if not entries:
        await message.answer("За последние 7 дней записей пока нет. Начать можно с /diary.")
        return

    entries_text = "\n\n".join(
        [
            (
                f"Дата: {entry['date']}\n"
                f"День: {entry['mood']}\n"
                f"Победы: {entry['wins']}\n"
                f"Благодарность: {entry['gratitude']}\n"
                f"Сложное: {entry['difficulties']}"
            )
            for entry in entries
        ]
    )

    await message.answer("Собираю мягкий итог недели...")
    summary = await ai.generate_week_summary(
        name=(user or {}).get("name") or "ты",
        style=(user or {}).get("communication_style") or "мягко и тепло",
        entries_text=entries_text,
    )
    await message.answer(summary)
