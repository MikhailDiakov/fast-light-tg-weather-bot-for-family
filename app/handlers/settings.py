from aiogram import F, Router, types
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext

from app.keyboards import (
    change_kb,
    location_request_kb_with_back,
    main_menu_kb,
    remove_kb,
    time_change_kb,
)
from app.states import EditUserStates, WeatherForm
from app.storage import get_user_data, save_user_data, user_exists
from app.utils.checker import is_family_member
from app.utils.validators import is_valid_time_format

router = Router()


@router.message(F.text == "Мої налаштування 📋")
async def show_user_settings(message: types.Message):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    user_data = get_user_data(message.from_user.id)
    if not user_data:
        await message.answer("⚠️ Ти ще не налаштував сповіщення. Напиши /start.")
        return

    lat = user_data.get("lat")
    lon = user_data.get("lon")
    time = user_data.get("time", "08:00")
    name = user_data.get("name", "друже")

    await message.answer(
        f"📋 *Твої налаштування:*\n"
        f"👤 Ім'я: *{name}*\n"
        f"🕒 Час сповіщення: *{time}*\n"
        f"🌍 Координати: `{lat:.4f}, {lon:.4f}`\n",
        parse_mode="Markdown",
    )


@router.message(F.text == "Змінити налаштування ⚙️")
async def handle_settings_button(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    if not user_exists(message.from_user.id):
        await message.answer("⚠️ Ти ще не налаштував сповіщення. Напиши /start.")
        return

    await state.set_state(WeatherForm.choice)
    await message.answer("🔧 Що хочеш змінити?", reply_markup=change_kb())


@router.message(WeatherForm.choice, F.text == "Змінити місто 🏙")
async def change_city(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await state.set_state(WeatherForm.city)
    await state.update_data(action="change")
    await message.answer(
        "📍 Надішли нову геолокацію:", reply_markup=location_request_kb_with_back()
    )


@router.message(WeatherForm.choice, F.text == "Змінити час ⏰")
async def change_time(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await state.set_state(WeatherForm.time)
    await message.answer(
        "🕒 Введи новий час сповіщення (наприклад, 08:00):",
        reply_markup=time_change_kb(),
    )


@router.message(WeatherForm.city, F.location)
async def process_location(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

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

        save_user_data(user_id, lat, lon, time_text, name, notes=notes)

        await message.answer(
            f"✅ Геолокацію оновлено: {lat:.4f}, {lon:.4f}.\n"
            f"Час сповіщення залишається {time_text}.",
            reply_markup=main_menu_kb(),
        )
        await state.clear()
    else:
        await state.update_data(lat=lat, lon=lon)
        await state.set_state(WeatherForm.time)
        await message.answer(
            f"Зрозумів, координати: {lat:.4f}, {lon:.4f}.\n"
            "Тепер введи час сповіщення (наприклад, 08:00):",
            reply_markup=remove_kb(),
        )


@router.message(
    F.text == "Назад ⬅️",
    or_f(
        StateFilter(None),
        StateFilter(WeatherForm.city),
        StateFilter(WeatherForm.choice),
        StateFilter(WeatherForm.time),
        StateFilter(EditUserStates.waiting_for_new_data),
    ),
)
async def back_handler(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await state.clear()
    await message.answer("📲 Повертаємось у головне меню:", reply_markup=main_menu_kb())


@router.message(WeatherForm.choice)
async def invalid_choice(message: types.Message):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await message.answer("❌ Обери опцію з меню.", reply_markup=change_kb())


@router.message(WeatherForm.city, ~F.location)
async def process_city_invalid(message: types.Message):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await message.answer(
        "Будь ласка, надсилай лише геолокацію 📍, не вводь місто текстом.",
        reply_markup=location_request_kb_with_back(),
    )


@router.message(WeatherForm.time)
async def process_time(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    time_text = message.text.strip()

    if not is_valid_time_format(time_text):
        await message.answer("❌ Невірний формат часу! Введи, наприклад: 08:00.")
        return

    user_id = message.from_user.id
    user_data = get_user_data(user_id)

    name = "друже"
    notes = ""

    if user_data:
        name = user_data.get("name", "друже")
        notes = user_data.get("notes", "")

    data = await state.get_data()
    lat = data.get("lat")
    lon = data.get("lon")

    if lat is None or lon is None:
        if user_data:
            lat = user_data.get("lat")
            lon = user_data.get("lon")

    if lat is None or lon is None:
        await message.answer(
            "⚠️ Координати не встановлені. Спочатку надішли геолокацію."
        )
        await state.set_state(WeatherForm.city)
        return

    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        await message.answer("⚠️ Некоректні координати. Спробуй змінити налаштування.")
        await state.set_state(WeatherForm.city)
        return

    save_user_data(user_id, lat, lon, time_text, name, notes=notes)

    await message.answer(
        f"✅ Сповіщення налаштовані на {time_text} для координат: {lat:.4f}, {lon:.4f}.",
        reply_markup=main_menu_kb(),
    )
    await state.clear()
