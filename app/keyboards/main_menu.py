from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Сервіси 🛠")],
            [KeyboardButton(text="Налаштування ⚙️")],
        ],
        resize_keyboard=True,
    )
