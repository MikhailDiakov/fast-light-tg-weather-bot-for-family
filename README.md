# 🌤️ Telegram Weather Bot for Family 🌤️

This bot is designed exclusively for users listed in `ALLOWED_USERS`.  
Every user can find out their Telegram ID by sending the command `/myid`.

## Usage

- `/start` — send your location and specify the time when the bot will send you a funny weather message with interesting facts and tips.

- **Показати погоду зараз** button — generates an instant weather report combining data from multiple APIs plus AI-generated commentary (not scheduled, but on demand).

- **Змінити налаштування** — allows you to change your city and notification time.

- **Дізнатися місто** — based on your location coordinates, the bot tells you the name of your city.

## Admin commands

- `/list_users` — shows all users and their saved data.

- `/edit_user ID` — lets the admin update a user's name and notes, so AI can personalize messages better.

---

This bot was quickly built for family use!

`keep_alive` and Flask are included for deployment on Replit and uptime monitoring with UptimeRobot.

---

## Deployment

### 1. Using Docker

Build your Docker image with:

```bash
docker build -t myweatherbot .
```

Run the container with environment variables from a file:

```bash
docker run --rm --env-file .env myweatherbot

```

### 2. Using Replit

Upload all your project files manually to Replit.

Add your environment variables (like your bot token and other secrets) to the Secrets tab in Replit.
For example, add variables like TELEGRAM_TOKEN, WEATHER_API_KEY, API_KEY_AI, ADMIN_ID etc.

Click the Run button to start your bot.

This setup keeps your secrets safe and your bot running smoothly.
