from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminStates(StatesGroup):
    distribute = State()
