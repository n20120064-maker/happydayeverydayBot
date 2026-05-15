from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards import main_menu_keyboard


router = Router()


@router.message(Command("help"))
async def show_help(message: Message) -> None:
    await message.answer(
        "🤍 <b>Happy Day</b>\n\n"
        "Я помогу сохранить день бережно и без давления.\n\n"
        "Что можно сделать:\n"
        "• /diary — записать сегодняшний день\n"
        "• /history — посмотреть последние записи\n"
        "• /week — собрать мягкий итог недели\n\n"
        "Можно просто нажимать кнопки ниже.",
        reply_markup=main_menu_keyboard(),
    )
