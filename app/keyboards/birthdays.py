from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def birthday_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Додати")],
            [KeyboardButton(text="📋 Показати")],
            [KeyboardButton(text="🗑 Видалити")],
            [KeyboardButton(text="Назад ⬅️")],
        ],
        resize_keyboard=True,
    )


def back_only_kb():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Назад ⬅️")]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
