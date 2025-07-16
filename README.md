# 🌤️ Telegram Weather Bot for Family

> A private bot made for our family — delivers fun weather reports, birthday reminders, and more!

---

## 📌 What the bot can do

🕒 **Sends daily messages**  
At your chosen time, the bot sends a warm message with:

- Current weather (including "feels like", wind, etc.)
- Clothing tips
- A funny fact
- AI-generated weather commentary 🌦️

⚡ **Show current weather**  
A button for instantly getting the latest weather and a witty AI comment.

🏙 **Change city / notification time**  
Update your city or when you get daily messages.

📍 **Get city from location**  
Send your location and the bot will tell you your city name.

🎉 **Birthday service**

- Add / remove / view birthdays
- Every morning, the bot announces if someone has a birthday today 🎂

---

## 👤 Usage

| Command / Button         | Description                                                                | Access Level                         |
| ------------------------ | -------------------------------------------------------------------------- | ------------------------------------ |
| `/start` and etc buttons | Begin setup: choose your city and notification time, settings, all service | ✅ Only for family (`ALLOWED_USERS`) |
| `/myid`                  | Get your Telegram ID (for admin use or requesting access)                  | ✅ Everyone                          |

---

## 🛠 Admin Commands

> 🔐 Only available for the `ADMIN_ID` (not all allowed users)

| Command         | Description                                              |
| --------------- | -------------------------------------------------------- |
| `/list_users`   | Show all users and their saved settings                  |
| `/edit_user ID` | Update a user’s name or notes to personalize AI messages |

---

## 🚀 Deployment

### 📦 Docker

1. **Build the Docker image:**

```bash
docker build -t myweatherbot .
```

2. **Run with environment variables from a file:**

```bash
docker run --rm --env-file .env myweatherbot
```

---

👨‍👩‍👧‍👦 This bot was quickly built with love, just for our family ❤️
