from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from app.ai_integration import generate_full_weather_report
from app.keyboards.weather import (
    change_kb,
    location_request_kb,
    main_menu_kb,
    remove_kb,
)
from app.states.admin import EditUserStates
from app.states.weather import Form
from app.storage import get_all_users, get_user_data, save_user_data, user_exists
from app.utils.checker import is_admin_member, is_family_member
from app.utils.city import get_city_name_from_coords
from app.utils.validators import is_valid_time_format
from app.utils.weather import fetch_forecast_data

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await state.clear()
    await state.set_state(Form.city)
    await state.update_data(action="new")
    await message.answer(
        "Привіт! Надішли, будь ласка, свою геолокацію 📍",
        reply_markup=location_request_kb(),
    )


@router.message(F.text == "Змінити налаштування ⚙️")
async def handle_settings_button(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    if not is_family_member(user_id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    if not user_exists(user_id):
        await message.answer("⚠️ Ти ще не налаштував сповіщення. Напиши /start.")
        return

    await state.set_state(Form.choice)
    await message.answer("🔧 Що хочеш змінити?", reply_markup=change_kb())


@router.message(Form.choice, F.text == "Змінити місто 🏙")
async def change_city(message: types.Message, state: FSMContext):
    await state.set_state(Form.city)
    await state.update_data(action="change")
    await message.answer(
        "📍 Надішли нову геолокацію:", reply_markup=location_request_kb()
    )


@router.message(Form.choice, F.text == "Змінити час ⏰")
async def change_time(message: types.Message, state: FSMContext):
    await state.set_state(Form.time)
    await message.answer(
        "🕒 Введи новий час сповіщення (наприклад, 08:00):",
        reply_markup=remove_kb(),
    )


@router.message(Form.choice)
async def invalid_choice(message: types.Message):
    await message.answer("❌ Обери опцію з меню.", reply_markup=change_kb())


@router.message(Form.city, F.location)
async def process_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude

    data = await state.get_data()
    action = data.get("action")

    if action == "change":
        user_id = message.from_user.id
        user_data = get_user_data(user_id)
        time_text = user_data.get("time", "08:00")
        name = user_data.get("name", "друже")
        notes = user_data.get("notes", "")

        save_user_data(message.from_user.id, lat, lon, time_text, name, notes=notes)

        await message.answer(
            f"✅ Геолокацію оновлено: {lat:.4f}, {lon:.4f}.\n"
            f"Час сповіщення залишається {time_text}.",
            reply_markup=main_menu_kb(),
        )
        await state.clear()
    else:
        await state.update_data(lat=lat, lon=lon)
        await state.set_state(Form.time)
        await message.answer(
            f"Зрозумів, координати: {lat:.4f}, {lon:.4f}.\n"
            "Тепер введи час сповіщення (наприклад, 08:00):",
            reply_markup=remove_kb(),
        )


@router.message(Form.city)
async def process_city_invalid(message: types.Message):
    await message.answer(
        "Будь ласка, надсилай лише геолокацію 📍, не вводь місто текстом.",
        reply_markup=location_request_kb(),
    )


@router.message(Form.time)
async def process_time(message: types.Message, state: FSMContext):
    time_text = message.text.strip()

    if not is_valid_time_format(time_text):
        await message.answer("❌ Невірний формат часу! Введи, наприклад: 08:00.")
        return

    data = await state.get_data()
    lat = data.get("lat")
    lon = data.get("lon")

    if lat is None or lon is None:
        user_id = message.from_user.id
        user_data = get_user_data(user_id)
        lat = user_data.get("lat")
        lon = user_data.get("lon")
        notes = user_data.get("notes", "")

    if lat is None or lon is None:
        await message.answer(
            "⚠️ Координати не встановлені. Спочатку надішли геолокацію."
        )
        await state.set_state(Form.city)
        return

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        await message.answer("⚠️ Некоректні координати. Спробуй змінити налаштування.")
        await state.set_state(Form.city)
        return

    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    name = user_data.get("name", "друже")

    save_user_data(message.from_user.id, lat, lon, time_text, name, notes=notes)

    await message.answer(
        f"✅ Сповіщення налаштовані на {time_text} для координат: {lat:.4f}, {lon:.4f}.",
        reply_markup=main_menu_kb(),
    )
    await state.clear()


@router.message(F.text == "Показати погоду зараз 🌤")
async def show_weather_now(message: types.Message):
    user_id = message.from_user.id

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


@router.message(F.text == "Дізнатись місто 🏙️")
async def get_city_name(message: types.Message):
    user_id = message.from_user.id

    if not user_exists(user_id):
        await message.answer("⚠️ Ти ще не налаштував сповіщення. Напиши /start.")
        return

    user_data = get_user_data(user_id)
    lat = user_data.get("lat")
    lon = user_data.get("lon")

    if lat is None or lon is None:
        await message.answer(
            "⚠️ Координати не встановлені. Спочатку надішли геолокацію."
        )
        return

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        await message.answer("⚠️ Некоректні координати. Спробуй змінити налаштування.")
        return

    city_name = await get_city_name_from_coords(lat, lon)
    if city_name:
        await message.answer(
            f"Якщо я не помиляюсь, це місто: {city_name}.\n"
            f"Якщо це не правильно — усі питання до розробників Телеграма, я тут ні до чого 😉"
        )
    else:
        await message.answer(
            "Якщо це не правильно — усі питання до розробників Телеграма, я тут ні до чого 😉"
        )


@router.message(F.text == "/myid")
async def send_user_id(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"🆔 Твій Telegram ID: `{user_id}`", parse_mode="Markdown")


@router.message(F.text.startswith("/edit_user"))
async def cmd_edit_user_start(message: types.Message, state: FSMContext):
    if not is_admin_member(message.from_user.id):
        await message.answer(
            "⛔️ Ця команда доступна лише адміністратору.", parse_mode=None
        )
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❗️ Використання: /edit_user <user_id>", parse_mode=None)
        return

    try:
        user_id = int(args[1])
    except ValueError:
        await message.answer("❗️ user_id повинен бути числом.", parse_mode=None)
        return

    user_data = get_user_data(user_id)
    if not user_data:
        await message.answer(
            f"❗️ Користувач з ID {user_id} не знайдений.", parse_mode=None
        )
        return

    await state.update_data(user_id=user_id)
    text = (
        f"Поточні дані користувача {user_id}:\n"
        f"Ім'я: {user_data.get('name', '')}\n"
        f"Заметки: {user_data.get('notes', '')}\n\n"
        "Введіть нові ім'я та заметки через | (вертикальна риска), наприклад:\n"
        "Нове ім'я|Нові заметки"
    )
    await message.answer(text, parse_mode=None)
    await state.set_state(EditUserStates.waiting_for_new_data)


@router.message(EditUserStates.waiting_for_new_data)
async def process_new_data(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    if not user_id:
        await message.answer("❗️ Помилка: відсутній user_id у стані.")
        await state.clear()
        return

    if "|" not in message.text:
        await message.answer("❗️ Невірний формат. Використовуйте: Ім'я|Заметки")
        return

    name, notes = map(str.strip, message.text.split("|", maxsplit=1))

    user_data = get_user_data(user_id)
    if not user_data:
        await message.answer(f"❗️ Користувач з ID {user_id} не знайдений.")
        await state.clear()
        return

    save_user_data(
        user_id=user_id,
        lat=user_data.get("lat", 0),
        lon=user_data.get("lon", 0),
        notify_time=user_data.get("time", ""),
        name=name,
        notes=notes,
    )

    await message.answer(
        f"✅ Дані користувача {user_id} оновлено:\nІм'я: {name}\nЗаметки: {notes}"
    )
    await state.clear()


@router.message(F.text == "/list_users")
async def cmd_list_users(message: types.Message):
    if not is_admin_member(message.from_user.id):
        await message.answer("⛔️ Ця команда доступна лише адміністратору.")
        return

    users = get_all_users()
    if not users:
        await message.answer("❗️ Користувачі відсутні.")
        return

    text_lines = ["Список користувачів:"]
    for user_id, data in users.items():
        text_lines.append(
            f"ID: {user_id}\n"
            f"Ім'я: {data.get('name', '')}\n"
            f"Заметки: {data.get('notes', '')}\n"
            f"Локація: ({data.get('lat', '')}, {data.get('lon', '')})\n"
            f"Час сповіщення: {data.get('time', '')}\n"
            "-----------------------"
        )

    for chunk in [text_lines[i : i + 10] for i in range(0, len(text_lines), 10)]:
        await message.answer("\n\n".join(chunk))
