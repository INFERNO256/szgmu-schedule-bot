from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const

from .callbacks import on_skip_onboarding, on_start_group_selection
from .states import OnboardingSG

dialog = Dialog(
    Window(
        Const(
            "👋 Добро пожаловать!\n\n"
            "Этот бот помогает просматривать расписание занятий.\n\n"
            "Начнем с выбора группы?"
        ),
        Group(
            Button(
                Const("📚 Выбрать группу"),
                id="start_group",
                on_click=on_start_group_selection,
            ),
            Button(
                Const("↩️ Позже"),
                id="skip",
                on_click=on_skip_onboarding,
            ),
            width=1,
        ),
        state=OnboardingSG.welcome,
    ),
)
