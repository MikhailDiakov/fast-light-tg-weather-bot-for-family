import os

from dotenv import load_dotenv

load_dotenv()

# tg bot token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# openweathermap api key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# gemini-2.0-flash api key
API_KEY_AI = os.getenv("API_KEY_AI")

# allow users to use tg bot
allowed_users_str = os.getenv("ALLOWED_USERS", "")
if allowed_users_str:
    ALLOWED_USERS = [int(user_id.strip()) for user_id in allowed_users_str.split(",")]
else:
    ALLOWED_USERS = []

# admin id
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# secret key
SECRET_KEY = os.getenv("SECRET_KEY")
