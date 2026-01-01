from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def on_start_group_selection(
    _callback: CallbackQuery,
    _widget: Button,
    manager: DialogManager,
) -> None:
    """Start group selection from onboarding."""
    from bot.dialogs.group_selection.states import GroupSelectionSG

    await manager.start(GroupSelectionSG.speciality)


async def on_skip_onboarding(
    callback: CallbackQuery,
    _widget: Button,
    manager: DialogManager,
) -> None:
    """Skip onboarding and go to main menu."""
    from bot.dialogs.main_menu.states import MainMenuSG

    telegram_id = callback.from_user.id
    await manager.start(
        MainMenuSG.menu,
        data={"telegram_id": telegram_id},
    )
