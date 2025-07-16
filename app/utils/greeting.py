from datetime import datetime, timedelta, timezone

from app.storage import get_user_data

LOCAL_TZ = timezone(timedelta(hours=3))


def get_greeting(user_id: int) -> str:
    user_data = get_user_data(user_id) or {}
    name = user_data.get("name", "друже")

    hour = datetime.now(LOCAL_TZ).hour
    if hour < 12:
        part = "Доброго ранку"
    elif hour < 18:
        part = "Доброго дня"
    else:
        part = "Доброго вечора"

    return f"{part}, {name}!"
