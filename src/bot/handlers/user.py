from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from bot.dialogs.admin.states import AdminSG
from bot.dialogs.main_menu.states import MainMenuSG
from bot.dialogs.onboarding.states import OnboardingSG
from services.user_service import UserService

router = Router()


@router.message(Command("start"))
@inject
async def start_command(
    message: Message,
    dialog_manager: DialogManager,
    user_service: FromDishka[UserService],
) -> None:
    """Handle /start command."""
    user = await user_service.get_or_create_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
    )

    if user and user.subgroup_id:
        await dialog_manager.start(
            MainMenuSG.menu,
            data={"telegram_id": message.from_user.id},
        )
    else:
        await dialog_manager.start(OnboardingSG.welcome)


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    """Handle /help command."""
    help_text = (
        "📚 <b>Справка по боту</b>\n\n"
        "Доступные команды:\n"
        "/start - Начать работу с ботом\n"
        "/help - Показать справку\n"
        "В главном меню доступны:\n"
        "📅 <b>Расписание</b> - Просмотр расписания\n"
        "👥 <b>Выбрать группу</b> - Изменить группу\n"
        "⚙️ <b>Настройки</b> - Настройки уведомлений"
    )
    await message.answer(help_text)


@router.message(Command("admin"))
async def admin_menu(message: Message, dialog_manager: DialogManager) -> None:
    """Show admin menu."""
    admin_ids: list[int] = [123456789]
    if message.from_user.id not in admin_ids:
        await message.answer("❌ Доступ запрещен")
        return

    await dialog_manager.start(AdminSG.menu)


@router.message()
async def default_handler(message: Message) -> None:
    """Handle unknown messages."""
    await message.answer(
        "❓ Команда не понята. Используйте /help для справки или /start для главного меню."
    )
