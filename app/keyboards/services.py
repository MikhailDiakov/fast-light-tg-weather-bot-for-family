from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def services_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Показати погоду зараз 🌤")],
            [KeyboardButton(text="Дізнатись місто 🏙️")],
            [KeyboardButton(text="Дні народження 🎂")],
            [KeyboardButton(text="Назад ⬅️")],
        ],
        resize_keyboard=True,
    )
