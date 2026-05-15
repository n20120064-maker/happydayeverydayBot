from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Записать день")],
            [KeyboardButton(text="История"), KeyboardButton(text="Итог недели")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выбери действие",
    )


def style_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤍 мягко и тепло"), KeyboardButton(text="☕ как подруга")],
            [KeyboardButton(text="🌿 спокойно и мудро"), KeyboardButton(text="✨ легко и позитивно")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выбери стиль общения",
    )


def support_type_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🤍 поддержку"), KeyboardButton(text="🌸 похвалу")],
            [KeyboardButton(text="✨ мотивацию"), KeyboardButton(text="🌿 спокойствие")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Что хочется услышать?",
    )
