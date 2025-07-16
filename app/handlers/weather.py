from aiogram import F, Router, types

from app.ai_integration import generate_full_weather_report
from app.keyboards import main_menu_kb
from app.storage import get_user_data, user_exists
from app.utils.checker import is_family_member
from app.utils.weather import fetch_forecast_data

router = Router()


@router.message(F.text == "Показати погоду зараз 🌤")
async def show_weather_now(message: types.Message):
    user_id = message.from_user.id

    if not is_family_member(message.from_user.id):
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
            "⚠️ Координати не встановлені. Спробуй змінити налаштування."
        )
        return

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        await message.answer("⚠️ Некоректні координати. Спробуй змінити налаштування.")
        return

    forecast_points = await fetch_forecast_data(lat, lon)
    if not forecast_points:
        await message.answer("⚠️ Не вдалося отримати прогноз. Спробуй пізніше.")
        return

    text = await generate_full_weather_report(user_id, lat, lon, forecast_points)
    await message.answer(text, reply_markup=main_menu_kb())
