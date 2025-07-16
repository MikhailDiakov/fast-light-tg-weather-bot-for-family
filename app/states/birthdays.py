from aiogram.fsm.state import State, StatesGroup


class BirthdayState(StatesGroup):
    name = State()
    date = State()
    delete_name = State()
