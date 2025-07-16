from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import aiohttp

from app.config import WEATHER_API_KEY

KYIV_TZ = ZoneInfo("Europe/Kiev")


async def get_weather(lat: float, lon: float) -> str:
    url = (
        f"http://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=ua"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status != 200:
                return (
                    f"⚠️ Не вдалося отримати погоду для координат {lat:.2f}, {lon:.2f}."
                )

            temp = round(data["main"]["temp"])
            feels_like = round(data["main"]["feels_like"])
            wind = round(data["wind"]["speed"])
            desc = data["weather"][0]["description"]

            return (
                f"🌤 Погода:\n"
                f"Температура: {temp}°C\n"
                f"Відчувається як: {feels_like}°C\n"
                f"Вітер: {wind} м/с\n"
                f"{desc.capitalize()}"
            )


async def fetch_forecast_data(lat: float, lon: float):
    url = (
        f"http://api.openweathermap.org/data/2.5/forecast"
        f"?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=ua"
    )
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()

    now_kyiv = datetime.now(tz=KYIV_TZ)
    end_period = now_kyiv + timedelta(hours=18)

    forecast_points = []
    for entry in data.get("list", []):
        dt_utc = datetime.fromtimestamp(entry["dt"], tz=timezone.utc)
        if dt_utc > end_period:
            break

        forecast_points.append(
            {
                "time": dt_utc.isoformat(),
                "temp": round(entry["main"]["temp"]),
                "feels_like": round(entry["main"]["feels_like"]),
                "wind_speed": round(entry["wind"]["speed"]),
                "description": entry["weather"][0]["description"].capitalize(),
                "pop": entry.get("pop", 0),
                "clouds": entry["clouds"]["all"],
            }
        )

    return forecast_points
