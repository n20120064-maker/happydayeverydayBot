from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from database import Database
from keyboards import main_menu_keyboard, support_type_keyboard
from services.ai import AIService, CRISIS_RESPONSE
from states import DiaryStates


router = Router()


@router.message(Command("diary"))
@router.message(F.text == "Записать день")
async def diary_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Как прошёл твой день?")
    await state.set_state(DiaryStates.waiting_for_mood)


@router.message(DiaryStates.waiting_for_mood)
async def diary_mood(message: Message, state: FSMContext) -> None:
    await state.update_data(mood=(message.text or "").strip())
    await message.answer("Что сегодня получилось, даже если это кажется маленьким?")
    await state.set_state(DiaryStates.waiting_for_wins)


@router.message(DiaryStates.waiting_for_wins)
async def diary_wins(message: Message, state: FSMContext) -> None:
    await state.update_data(wins=(message.text or "").strip())
    await message.answer("За что ты сегодня благодарна?")
    await state.set_state(DiaryStates.waiting_for_gratitude)


@router.message(DiaryStates.waiting_for_gratitude)
async def diary_gratitude(message: Message, state: FSMContext) -> None:
    await state.update_data(gratitude=(message.text or "").strip())
    await message.answer("Что было сложным?")
    await state.set_state(DiaryStates.waiting_for_difficulties)


@router.message(DiaryStates.waiting_for_difficulties)
async def diary_difficulties(message: Message, state: FSMContext) -> None:
    await state.update_data(difficulties=(message.text or "").strip())
    await message.answer("Что ты хочешь сейчас услышать?", reply_markup=support_type_keyboard())
    await state.set_state(DiaryStates.waiting_for_support_type)


@router.message(DiaryStates.waiting_for_support_type)
async def diary_finish(message: Message, state: FSMContext, db: Database, ai: AIService) -> None:
    support_type = (message.text or "").strip().lstrip("🤍🌸✨🌿 ").strip()
    data = await state.get_data()
    user = await db.get_user_by_telegram_id(message.from_user.id)

    if user is None:
        user_id = await db.upsert_user(message.from_user.id, name=message.from_user.first_name, communication_style="мягко и тепло")
        user = {"id": user_id, "name": message.from_user.first_name or "ты", "communication_style": "мягко и тепло"}

    await message.answer("Собираю твой день в теплый ответ...", reply_markup=ReplyKeyboardRemove())
    ai_response = await ai.generate_diary_response(
        name=user.get("name") or "ты",
        style=user.get("communication_style") or "мягко и тепло",
        mood=data.get("mood", ""),
        wins=data.get("wins", ""),
        gratitude=data.get("gratitude", ""),
        difficulties=data.get("difficulties", ""),
        support_type=support_type,
    )

    await db.add_diary_entry(
        user_id=user["id"],
        mood=data.get("mood", ""),
        wins=data.get("wins", ""),
        gratitude=data.get("gratitude", ""),
        difficulties=data.get("difficulties", ""),
        support_type=support_type,
        ai_response=ai_response,
    )
    await state.clear()
    await message.answer(ai_response or CRISIS_RESPONSE, reply_markup=main_menu_keyboard())


@router.message()
async def crisis_guard(message: Message, ai: AIService) -> None:
    text = message.text or ""
    if ai.has_crisis_phrase(text):
        await message.answer(CRISIS_RESPONSE)
