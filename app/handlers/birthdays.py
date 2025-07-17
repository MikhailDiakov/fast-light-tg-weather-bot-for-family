from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from app.keyboards import back_only_kb, birthday_menu_kb
from app.states import BirthdayState
from app.storage import add_birthday, delete_birthday, get_all_birthdays
from app.utils.checker import is_family_member
from app.utils.validators import is_valid_date_format

router = Router()


@router.message(F.text == "Дні народження 🎂")
async def birthday_menu(message: types.Message):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await message.answer(
        "Оберіть дію з днями народження:", reply_markup=birthday_menu_kb()
    )


@router.message(F.text == "➕ Додати")
async def add_birthday_start(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await state.set_state(BirthdayState.name)
    await message.answer("Введіть імʼя:", reply_markup=back_only_kb())


@router.message(BirthdayState.name)
async def add_birthday_name(message: types.Message, state: FSMContext):
    if message.text == "Назад ⬅️":
        await state.clear()
        await birthday_menu(message)
        return

    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await state.update_data(name=message.text)
    await state.set_state(BirthdayState.date)
    await message.answer(
        "Введіть дату народження у форматі ДД.ММ.РРРР:", reply_markup=back_only_kb()
    )


@router.message(BirthdayState.date)
async def add_birthday_date(message: types.Message, state: FSMContext):
    if message.text == "Назад ⬅️":
        await state.clear()
        await birthday_menu(message)
        return

    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    date = message.text
    if not is_valid_date_format(date):
        await message.answer(
            "❌ Невірний формат дати або неіснуюча дата. Введіть дату у форматі ДД.ММ.РРРР, наприклад, 15.07.1990",
            reply_markup=back_only_kb(),
        )
        return

    data = await state.get_data()
    name = data["name"]
    success = add_birthday(name, date)
    if not success:
        await message.answer(
            f"❌ Ім'я '{name}' вже є у списку. Використайте інше ім'я.",
            reply_markup=back_only_kb(),
        )
        await state.clear()
        await birthday_menu(message)
        return

    await message.answer(f"✅ Додано: {name} — {date}")
    await state.clear()
    await birthday_menu(message)


@router.message(F.text == "📋 Показати")
async def show_birthdays(message: types.Message):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    bdays = get_all_birthdays()
    if not bdays:
        await message.answer("Немає збережених днів народження.")
    else:
        text = "\n".join([f"{b['name']} — {b['date']}" for b in bdays])
        await message.answer("🎉 Збережені дні народження:\n" + text)
    await birthday_menu(message)


@router.message(F.text == "🗑 Видалити")
async def delete_birthday_prompt(message: types.Message, state: FSMContext):
    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    await state.set_state(BirthdayState.delete_name)
    await message.answer("Введіть імʼя для видалення:", reply_markup=back_only_kb())


@router.message(BirthdayState.delete_name)
async def delete_birthday_name(message: types.Message, state: FSMContext):
    if message.text == "Назад ⬅️":
        await state.clear()
        await birthday_menu(message)
        return

    if not is_family_member(message.from_user.id):
        await message.answer("⛔️ Бот доступний лише для нашої родини ❤️")
        return

    deleted = delete_birthday(message.text)
    if deleted:
        await message.answer("✅ Видалено.")
    else:
        await message.answer("❌ Такого імені в списку немає.")
    await state.clear()
    await birthday_menu(message)
