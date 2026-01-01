from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const

from .callbacks import on_group_selection, on_schedule, on_settings
from .getters import get_main_menu_data
from .states import MainMenuSG

dialog = Dialog(
    Window(
        Const("📋 <b>Главное меню</b>"),
        Const("\n\n👥 Группа не выбрана", when=lambda d, _w, _m: not d.get("has_group")),
        Group(
            Button(Const("📅 Расписание"), id="schedule", on_click=on_schedule),
            Button(Const("👥 Выбрать группу"), id="group", on_click=on_group_selection),
            Button(Const("⚙️ Настройки"), id="settings", on_click=on_settings),
            width=1,
        ),
        state=MainMenuSG.menu,
        getter=get_main_menu_data,
    ),
)
