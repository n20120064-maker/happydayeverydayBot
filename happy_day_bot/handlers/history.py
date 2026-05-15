from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from database import Database


router = Router()


@router.message(Command("history"))
@router.message(F.text == "История")
async def show_history(message: Message, db: Database) -> None:
    entries = await db.get_recent_entries(message.from_user.id, limit=5)
    if not entries:
        await message.answer("Пока записей нет. Можно начать с /diary 🤍")
        return

    parts = ["Последние записи:"]
    for entry in entries:
        parts.append(
            "\n".join(
                [
                    f"\n{entry['date']}",
                    f"День: {entry['mood']}",
                    f"Победы: {entry['wins']}",
                    f"Благодарность: {entry['gratitude']}",
                    f"Сложное: {entry['difficulties']}",
                    f"Ответ: {entry['ai_response']}",
                ]
            )
        )

    await message.answer("\n".join(parts))
