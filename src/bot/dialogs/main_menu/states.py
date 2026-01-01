from aiogram.filters.state import State, StatesGroup


class MainMenuSG(StatesGroup):
    """Main menu state group."""

    menu = State()
