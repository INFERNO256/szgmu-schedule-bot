from aiogram.filters.state import State, StatesGroup


class OnboardingSG(StatesGroup):
    welcome = State()
