from aiogram.filters.state import State, StatesGroup


class ScheduleSG(StatesGroup):
    view = State()
