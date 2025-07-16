from aiogram import Router
from aiogram.fsm.state import State, StatesGroup

router = Router()


class EditUserStates(StatesGroup):
    waiting_for_new_data = State()
