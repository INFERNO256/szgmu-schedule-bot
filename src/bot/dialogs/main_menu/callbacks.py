from datetime import date

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from bot.dialogs.schedule.states import ScheduleSG
from services.user_service import UserService


@inject
async def on_schedule(
    callback: CallbackQuery,
    _widget: Button,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
) -> None:
    """Navigate to schedule dialog."""

    telegram_id = dialog_manager.middleware_data["event_from_user"].id
    user = await user_service.get_by_telegram_id(telegram_id)
    if not user or not user.subgroup_id:
        await callback.answer("❌ Сначала выберите группу")
        return

    await dialog_manager.start(
        ScheduleSG.view,
        data={
            "subgroup_id": user.subgroup_id,
            "mode": "day",
            "anchor_date": date.today().isoformat(),
        },
    )


async def on_group_selection(
    _callback: CallbackQuery,
    _widget: Button,
    manager: DialogManager,
) -> None:
    """Navigate to group selection dialog."""
    from bot.dialogs.group_selection.states import GroupSelectionSG

    await manager.start(GroupSelectionSG.speciality)


async def on_settings(
    callback: CallbackQuery,
    _widget: Button,
    manager: DialogManager,
) -> None:
    """Navigate to settings dialog."""
    from bot.dialogs.settings.states import SettingsSG

    await manager.start(
        SettingsSG.view,
        data={"telegram_id": callback.from_user.id},
    )
