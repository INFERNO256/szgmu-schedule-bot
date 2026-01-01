from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format

from .callbacks import on_settings_cancel, on_toggle_notifications
from .getters import get_user_settings
from .states import SettingsSG

dialog = Dialog(
    Window(
        Format("{settings_text}"),
        Group(
            Button(
                Const("🔔 Включить уведомления"),
                id="toggle_notif",
                on_click=on_toggle_notifications,
                when=lambda data, _widget, _manager: not data.get("is_subscribed"),
            ),
            Button(
                Const("🔕 Отключить уведомления"),
                id="toggle_notif_off",
                on_click=on_toggle_notifications,
                when=lambda data, _widget, _manager: data.get("is_subscribed"),
            ),
            width=1,
        ),
        Button(Const("← Назад"), id="cancel", on_click=on_settings_cancel),
        state=SettingsSG.view,
        getter=get_user_settings,
    ),
)
