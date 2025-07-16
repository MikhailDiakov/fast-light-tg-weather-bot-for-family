import httpx
from httpx import HTTPStatusError, RequestError

from app.config import API_KEY_AI
from app.storage import get_user_data
from app.utils.greeting import get_greeting
from app.utils.weather import get_weather


async def generate_full_weather_report(
    user_id: int, lat: float, lon: float, forecast_points: list
) -> str:
    greeting = get_greeting(user_id)
    current_weather = await get_weather(lat, lon)
    user_data = get_user_data(user_id)
    notes = user_data.get("notes", "").strip()

    forecast_block = (
        f"Прогноз погоди на найближчі години (координати {lat:.2f}, {lon:.2f}):\n"
    )
    for point in forecast_points:
        time = point["time"][11:16]
        forecast_block += (
            f"{time}: {point['description']}, "
            f"{point['temp']}°C, "
            f"відчувається як {point['feels_like']}°C, "
            f"вітер {point['wind_speed']} м/с, "
            f"опади: {int(point['pop'] * 100)}%\n"
        )

    prompt = (
        f"{greeting}\n\n"
        f"Зараз за вікном:\n{current_weather}\n\n"
        "А тепер вас турбує харизматичний і кумедний синоптик Анатолій Прогнозенко 😎📻\n\n"
        f"{forecast_block}\n"
        "Напиши коротко, весело і по-людськи:\n"
        "- як зміниться погода (коротко, по годинах або загальну тенденцію)\n"
        "- що вдягнути (без вказівки на стать чи конкретний одяг)\n"
        "- що взяти з собою (наприклад: панамка, зонт, окуляри)\n"
        "- 1 смішний факт про погоду, природу або людей\n"
        "- кумедне побажання гарного дня\n"
        "- побажання зроби коротким (2–3 речення), але щирим і з гумором\n"
        "- нагадай в кінці, що Дьякови найкращі 💪\n"
    )

    if notes:
        prompt += (
            f"\n\n⚠️ Вплети цю особливу інструкцію у побажання наприкінці, "
            f"природно, з гумором або тепло:\n{notes}"
        )

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY_AI,
    }
    json_data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=headers, json=json_data)
            response.raise_for_status()
            data = response.json()

        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return raw_text.strip()

    except HTTPStatusError as e:
        status_code = e.response.status_code
        if status_code == 429:
            return "🥵 Зараз дуже багато запитів до AI. Спробуйте ще раз трохи пізніше!"
        elif status_code == 503:
            return (
                "😔 Сервіс тимчасово недоступний. Спробуйте знову через кілька хвилин."
            )
        else:
            return f"🚨 Помилка з боку AI (код {status_code}). Спробуйте пізніше."

    except RequestError:
        return "🚧 Виникла проблема з мережею або сервером. Перевірте з'єднання або спробуйте пізніше."

    except Exception as e:
        return f"⚠️ Непередбачувана помилка: {str(e)}"


async def generate_short_ai_weather_report(
    user_id, forecast_points, current_weather
) -> str:
    greeting = get_greeting(user_id)

    forecast_block = ""
    for point in forecast_points[:4]:
        time = point["time"][11:16]
        forecast_block += (
            f"{time}: {point['description'].capitalize()}, "
            f"{point['temp']}°C, відчувається як {point['feels_like']}°C, "
            f"вітер {point['wind_speed']} м/с, "
            f"опади: {int(point['pop'] * 100)}%\n"
        )

    prompt = (
        f"{greeting}\n\n"
        f"Зараз за вікном:\n{current_weather}\n\n"
        f"Прогноз на найближчі години:\n{forecast_block}\n"
        "Напиши коротко і зрозуміло, без зірочок, форматування чи емодзі, у вигляді простого тексту:\n"
        "- Яка зараз температура і як вона відчувається\n"
        "- Що очікувати у найближчі години (коротко по прогнозу)\n"
    )

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": API_KEY_AI,
    }
    json_data = {"contents": [{"parts": [{"text": prompt}]}]}

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(url, headers=headers, json=json_data)
        response.raise_for_status()
        data = response.json()

    raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
    return raw_text.strip()
