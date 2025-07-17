from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove


def location_request_kb_no_back():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Надіслати геолокацію 📍", request_location=True)],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def location_request_kb_with_back():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Надіслати геолокацію 📍", request_location=True)],
            [KeyboardButton(text="Назад ⬅️")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def change_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Змінити місто 🏙"),
                KeyboardButton(text="Змінити час ⏰"),
            ],
            [KeyboardButton(text="Назад ⬅️")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def settings_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Мої налаштування 📋")],
            [KeyboardButton(text="Змінити налаштування ⚙️")],
            [KeyboardButton(text="Назад ⬅️")],
        ],
        resize_keyboard=True,
    )


def remove_kb():
    return ReplyKeyboardRemove()


def time_change_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Назад ⬅️")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
