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
