from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from services.settings_service import SettingsService
from services.user_service import UserService


@inject
async def on_toggle_notifications(
    callback: CallbackQuery,
    _widget: Button,
    manager: DialogManager,
    settings_service: FromDishka[SettingsService],
    user_service: FromDishka[UserService],
) -> None:
    """Toggle notification settings."""
    telegram_id = callback.from_user.id
    manager.dialog_data["telegram_id"] = telegram_id

    user = await user_service.get_or_create_user(
        telegram_id=telegram_id,
        username=callback.from_user.username,
        full_name=callback.from_user.full_name,
    )
    if not user:
        await manager.event.bot.answer_callback_query(callback.id, "❌ Пользователь не найден")
        return
    current_state = user.is_subscribed
    await settings_service.toggle_notifications(telegram_id, not current_state)

    await manager.event.bot.answer_callback_query(callback.id, "✅ Настройки обновлены")


async def on_settings_cancel(
    callback: CallbackQuery,
    _widget: Button,
    manager: DialogManager,
) -> None:
    """Cancel settings dialog and return to main menu."""
    from bot.dialogs.main_menu.states import MainMenuSG

    telegram_id = callback.from_user.id
    await manager.start(
        MainMenuSG.menu,
        data={"telegram_id": telegram_id},
    )
