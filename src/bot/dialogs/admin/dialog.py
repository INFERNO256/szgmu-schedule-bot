from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from .callbacks import on_admin_cancel, on_sync_all
from .states import AdminSG

dialog = Dialog(
    Window(
        Const("⚙️ <b>Панель администратора</b>\n\nВыберите действие:"),
        Button(Const("🔄 Принудительная синхронизация"), id="sync_all", on_click=on_sync_all),
        Button(Const("← Назад"), id="cancel", on_click=on_admin_cancel),
        state=AdminSG.menu,
    ),
)
