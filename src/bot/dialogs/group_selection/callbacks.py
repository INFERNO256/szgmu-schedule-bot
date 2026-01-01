from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, Select
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from services.user_service import UserService


async def on_speciality_selected(
    _callback: CallbackQuery,
    _widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    """Handle speciality selection."""
    manager.dialog_data["speciality_id"] = int(item_id)
    await manager.next()


async def on_course_selected(
    _callback: CallbackQuery,
    _widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    """Handle course selection."""
    manager.dialog_data["course"] = int(item_id)
    await manager.next()


async def on_stream_selected(
    _callback: CallbackQuery,
    _widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    """Handle stream selection."""
    manager.dialog_data["stream"] = item_id
    await manager.next()


async def on_group_selected(
    _callback: CallbackQuery,
    _widget: Select,
    manager: DialogManager,
    item_id: str,
) -> None:
    """Handle group selection."""
    manager.dialog_data["group_id"] = int(item_id)
    await manager.next()


@inject
async def on_subgroup_selected(
    callback: CallbackQuery,
    _widget: Select,
    manager: DialogManager,
    item_id: str,
    user_service: FromDishka[UserService],
) -> None:
    """Handle subgroup selection and save to database."""
    subgroup_id = int(item_id)
    manager.dialog_data["subgroup_id"] = subgroup_id
    telegram_id = callback.from_user.id
    await user_service.set_user_subgroup(telegram_id, subgroup_id)
    await manager.next()


async def on_success_back_to_menu(
    callback: CallbackQuery,
    _widget: Button,
    manager: DialogManager,
) -> None:
    """Return to main menu from success window."""
    from bot.dialogs.main_menu.states import MainMenuSG

    telegram_id = callback.from_user.id
    await manager.start(
        MainMenuSG.menu,
        data={"telegram_id": telegram_id},
    )


async def on_cancel_to_menu(
    callback: CallbackQuery,
    _widget: Button,
    manager: DialogManager,
) -> None:
    """Cancel group selection and return to main menu."""
    from bot.dialogs.main_menu.states import MainMenuSG

    telegram_id = callback.from_user.id
    await manager.start(
        MainMenuSG.menu,
        data={"telegram_id": telegram_id},
    )
