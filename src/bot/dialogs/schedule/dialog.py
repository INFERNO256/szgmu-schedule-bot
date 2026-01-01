from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Checkbox, Group
from aiogram_dialog.widgets.text import Const, Format

from .callbacks import (
    on_mode_changed,
    on_next,
    on_prev,
    on_schedule_cancel,
)
from .getters import get_schedule
from .states import ScheduleSG

dialog = Dialog(
    Window(
        Format("{schedule_text}"),
        Group(
            Button(Const("◀️"), id="prev", on_click=on_prev),
            Button(Const("▶️"), id="next", on_click=on_next),
            width=2,
        ),
        Checkbox(
            Const("📆 Неделя"),
            Const("📅 День"),
            id="mode",
            default=False,
            on_state_changed=on_mode_changed,
        ),
        Button(Const("← В меню"), id="cancel", on_click=on_schedule_cancel),
        state=ScheduleSG.view,
        getter=get_schedule,
    ),
)
