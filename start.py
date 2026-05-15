from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from config import BASE_DIR
from database import Database
from keyboards import main_menu_keyboard, style_keyboard
from states import StartStates


router = Router()
STYLE_OPTIONS = {
    "🤍 мягко и тепло": "мягко и тепло",
    "☕ как подруга": "как подруга",
    "🌿 спокойно и мудро": "спокойно и мудро",
    "✨ легко и позитивно": "легко и позитивно",
}


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    banner_path = BASE_DIR / "assets" / "banner.jpg"
    caption = (
        "🤍 <b>Добро пожаловать в Happy Day</b>\n\n"
        "Я твой дневник силы. Здесь не нужно быть идеальной.\n"
        "Будем замечать хорошее, благодарность и твои маленькие победы."
    )
    if banner_path.exists():
        await message.answer_photo(photo=FSInputFile(banner_path), caption=caption)
    else:
        await message.answer(caption)

    await message.answer("Как тебя называть? Можно имя или любое нежное обращение.")
    await state.set_state(StartStates.waiting_for_name)


@router.message(StartStates.waiting_for_name)
async def save_name(message: Message, state: FSMContext) -> None:
    name = (message.text or "").strip()
    if not name:
        await message.answer("Напиши, пожалуйста, имя или любое обращение, которое тебе приятно.")
        return

    await state.update_data(name=name)
    await message.answer("В каком стиле с тобой общаться?", reply_markup=style_keyboard())
    await state.set_state(StartStates.waiting_for_style)


@router.message(StartStates.waiting_for_style)
async def save_style(message: Message, state: FSMContext, db: Database) -> None:
    style_text = (message.text or "").strip()
    style = STYLE_OPTIONS.get(style_text)
    if style is None:
        await message.answer("Выбери, пожалуйста, один из вариантов на кнопках.", reply_markup=style_keyboard())
        return

    data = await state.get_data()
    await db.upsert_user(message.from_user.id, name=data["name"], communication_style=style)
    await state.clear()
    await message.answer(
        "Готово, я рядом 🤍\n\n"
        "Можно начать с кнопки «Записать день» или команды /diary.",
        reply_markup=main_menu_keyboard(),
    )
