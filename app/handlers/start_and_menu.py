from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from app.keyboards import location_request_kb_no_back, services_kb, settings_kb
from app.states import WeatherForm
from app.utils.checker import is_family_member

router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await state.clear()
    await state.set_state(WeatherForm.city)
    await state.update_data(action="new")
    await message.answer(
        "Привіт! Надішли, будь ласка, свою геолокацію 📍",
        reply_markup=location_request_kb_no_back(),
    )


@router.message(F.text == "Налаштування ⚙️")
async def show_settings_menu(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await message.answer("⚙️ Меню налаштувань:", reply_markup=settings_kb())


@router.message(F.text == "Сервіси 🛠")
async def show_services_menu(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await message.answer("🛠 Обери сервіс:", reply_markup=services_kb())


@router.message(F.text == "/myid")
async def send_user_id(message: types.Message):
    user_id = message.from_user.id
    await message.answer(f"🆔 Твій Telegram ID: `{user_id}`", parse_mode="Markdown")
