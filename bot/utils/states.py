
from aiogram.fsm.state import State, StatesGroup


class OrderState(StatesGroup):
    name = State()
    phone = State()
    description = State()
    confirm = State()


class SupportStates(StatesGroup):
    waiting_for_message = State()
