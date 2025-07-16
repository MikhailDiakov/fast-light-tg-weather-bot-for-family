from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext

from app.states import EditUserStates
from app.storage import get_all_users, get_user_data, save_user_data
from app.utils.checker import is_admin_member

router = Router()


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
            f"Нотатки: {data.get('notes', '')}\n"
            f"Локація: ({data.get('lat', '')}, {data.get('lon', '')})\n"
            f"Час сповіщення: {data.get('time', '')}\n"
            "-----------------------"
        )

    for chunk in [text_lines[i : i + 10] for i in range(0, len(text_lines), 10)]:
        await message.answer("\n\n".join(chunk))
