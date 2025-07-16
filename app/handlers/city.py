from aiogram import F, Router, types

from app.storage import get_user_data, user_exists
from app.utils.checker import is_family_member
from app.utils.city import get_city_name_from_coords

router = Router()


@router.message(F.text == "Дізнатись місто 🏙️")
async def get_city_name(message: types.Message):
    user_id = message.from_user.id

    if not is_family_member(user_id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    if not user_exists(user_id):
        await message.answer("⚠️ Ти ще не налаштував сповіщення. Напиши /start.")
        return

    user_data = get_user_data(user_id)
    lat = user_data.get("lat")
    lon = user_data.get("lon")

    if lat is None or lon is None:
        await message.answer(
            "⚠️ Координати не встановлені. Спочатку надішли геолокацію."
        )
        return

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        await message.answer("⚠️ Некоректні координати. Спробуй змінити налаштування.")
        return

    city_name = await get_city_name_from_coords(lat, lon)
    if city_name:
        await message.answer(
            f"Якщо я не помиляюсь, це місто: {city_name}.\n"
            f"Якщо це не правильно — усі питання до розробників Телеграма, я тут ні до чого 😉"
        )
    else:
        await message.answer(
            "Я не зміг визначити місто 😔. Але всі питання — до розробників Телеграма 😉"
        )
