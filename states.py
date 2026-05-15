from aiogram.fsm.state import State, StatesGroup


class StartStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_style = State()


class DiaryStates(StatesGroup):
    waiting_for_mood = State()
    waiting_for_wins = State()
    waiting_for_gratitude = State()
    waiting_for_difficulties = State()
    waiting_for_support_type = State()
