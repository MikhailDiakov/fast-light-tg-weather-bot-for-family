from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


def location_request_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Надіслати геолокацію 📍", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def change_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Змінити місто 🏙")],
            [KeyboardButton(text="Змінити час ⏰")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def main_menu_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Показати погоду зараз 🌤")],
            [KeyboardButton(text="Змінити налаштування ⚙️")],
            [KeyboardButton(text="Дізнатись місто 🏙️")],
        ],
        resize_keyboard=True,
    )


def remove_kb():
    return ReplyKeyboardRemove()
