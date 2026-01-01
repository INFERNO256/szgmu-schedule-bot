from aiogram.filters.state import State, StatesGroup


class SettingsSG(StatesGroup):
    view = State()
