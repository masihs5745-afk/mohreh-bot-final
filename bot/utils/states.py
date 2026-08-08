
from aiogram.fsm.state import State, StatesGroup


class OrderStates(StatesGroup):
    name = State()
    phone = State()
    description = State()


class SupportStates(StatesGroup):
    waiting_for_message = State()
