from datetime import datetime
from zoneinfo import ZoneInfo

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from app.ai_integration import generate_full_weather_report
from app.storage import get_all_users, load_birthdays
from app.utils.weather import fetch_forecast_data

scheduler = AsyncIOScheduler()

KYIV_TZ = ZoneInfo("Europe/Kiev")


def setup_scheduler(bot):
    scheduler.add_job(check_and_notify, "interval", minutes=1, kwargs={"bot": bot})
    scheduler.add_job(
        send_birthday_notifications,
        "cron",
        hour=0,
        minute=0,
        timezone=KYIV_TZ,
        kwargs={"bot": bot},
    )
    scheduler.start()


async def check_and_notify(bot):
    now = datetime.now(tz=KYIV_TZ).strftime("%H:%M")
    for user_id_str, data in get_all_users().items():
        if data.get("time") == now:
            user_id = int(user_id_str)
            lat = data.get("lat")
            lon = data.get("lon")

            if lat is None or lon is None:
                print(
                    f"⚠️ User {user_id} has no coordinates set, skipping notification."
                )
                continue

            try:
                lat = float(lat)
                lon = float(lon)
            except (TypeError, ValueError):
                print(
                    f"⚠️ User {user_id} has invalid coordinates, skipping notification."
                )
                continue

            forecast_points = await fetch_forecast_data(lat, lon)
            if not forecast_points:
                print(f"⚠️ Не вдалося отримати прогноз для user {user_id}, skipping.")
                continue

            try:
                text = await generate_full_weather_report(
                    user_id, lat, lon, forecast_points
                )
                await bot.send_message(user_id, text)
            except Exception as e:
                print(f"❌ Помилка відправки {user_id}: {e}")


async def send_birthday_notifications(bot):
    now = datetime.now(tz=KYIV_TZ)

    birthdays = load_birthdays()
    users = get_all_users()

    todays_bdays = []
    for b in birthdays:
        try:
            b_date = datetime.strptime(b["date"], "%d.%m.%Y")
            if b_date.day == now.day and b_date.month == now.month:
                age = now.year - b_date.year
                todays_bdays.append((b["name"], age))
        except Exception:
            continue

    if not todays_bdays:
        return

    bday_messages = [
        f"🎉 {name} святкує сьогодні {age} років!" for name, age in todays_bdays
    ]
    full_message = "Сьогодні іменинники:\n" + "\n".join(bday_messages)

    for user_id_str in users.keys():
        try:
            user_id = int(user_id_str)
            await bot.send_message(user_id, full_message)
        except Exception as e:
            print(f"❌ Помилка відправки повідомлення user {user_id}: {e}")
