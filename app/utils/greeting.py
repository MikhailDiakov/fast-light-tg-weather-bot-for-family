from datetime import datetime
from zoneinfo import ZoneInfo

from app.storage import get_user_data

LOCAL_TZ = ZoneInfo("Europe/Kiev")


def get_greeting(user_id: int) -> str:
    user_data = get_user_data(user_id) or {}
    name = user_data.get("name", "друже")

    hour = datetime.now(LOCAL_TZ).hour
    if 5 <= hour < 12:
        part = "Доброго ранку"
    elif 12 <= hour < 18:
        part = "Доброго дня"
    elif 18 <= hour < 23:
        part = "Доброго вечора"
    else:
        part = "Доброї ночі"

    return f"{part}, {name}!"
