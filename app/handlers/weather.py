from aiogram import F, Router, types
from httpx import HTTPStatusError, RequestError

from app.ai_integration import generate_short_ai_weather_report
from app.keyboards import main_menu_kb
from app.storage import get_user_data, user_exists
from app.utils.checker import is_family_member
from app.utils.greeting import get_greeting
from app.utils.weather import fetch_forecast_data, get_weather

router = Router()


@router.message(F.text == "Показати погоду зараз 🌤")
async def show_weather_now(message: types.Message):
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
    current_weather = await get_weather(lat, lon)

    if not forecast_points:
        await message.answer("⚠️ Не вдалося отримати прогноз. Спробуй пізніше.")
        return

    try:
        text = await generate_short_ai_weather_report(
            user_id, forecast_points, current_weather
        )
    except (HTTPStatusError, RequestError, Exception):
        text = generate_fallback_weather_text(user_id, forecast_points, current_weather)

    await message.answer(text, reply_markup=main_menu_kb())


def generate_fallback_weather_text(user_id, forecast_points, current_weather) -> str:
    greeting = get_greeting(user_id)

    forecast_summary = []
    for point in forecast_points[:4]:
        time = point["time"][11:16]
        desc = point["description"].capitalize()
        temp = point["temp"]
        feels = point["feels_like"]
        pop = int(point["pop"] * 100)
        wind = point["wind_speed"]

        precip_text = f"Опади: {pop}%" if pop > 0 else "Опадів немає"
        forecast_summary.append(
            f"{time}: {desc}, {temp}°C (ощущается як {feels}°C), вітер {wind} м/с, {precip_text}"
        )

    text = (
        f"{greeting}\n\n"
        f"Зараз за вікном:\n{current_weather}\n\n"
        "Прогноз на найближчі години:\n" + "\n".join(forecast_summary) + "\n\n"
        "🥲 AI-сервіс недоступний. Ось прогноз без жартів і гумору."
    )
    return text
