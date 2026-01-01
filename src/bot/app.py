import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from dishka import AsyncContainer
from dishka.integrations.aiogram import setup_dishka

from bot.dialogs.admin import admin_dialog
from bot.dialogs.group_selection import group_selection_dialog
from bot.dialogs.main_menu import main_menu_dialog
from bot.dialogs.onboarding import onboarding_dialog
from bot.dialogs.schedule import schedule_dialog
from bot.dialogs.settings import settings_dialog
from bot.handlers.user import router as user_router
from core.config import RedisSettings

logger = logging.getLogger(__name__)


async def create_dispatcher(
    _bot: Bot,
    container: AsyncContainer,
    redis_settings: RedisSettings | None = None,
) -> Dispatcher:
    """Create and configure dispatcher."""

    if redis_settings:
        try:
            redis_storage = RedisStorage.from_url(redis_settings.dsn)
            storage = redis_storage
            logger.info("Using Redis storage")
        except Exception as e:
            logger.warning(f"Redis connection failed, using MemoryStorage: {e}")
            storage = MemoryStorage()
    else:
        storage = MemoryStorage()
        logger.info("Using MemoryStorage")

    dp = Dispatcher(storage=storage)

    setup_dishka(container, dp)
    setup_dialogs(dp)

    dp.include_router(user_router)
    dp.include_routers(
        main_menu_dialog,
        onboarding_dialog,
        group_selection_dialog,
        schedule_dialog,
        settings_dialog,
        admin_dialog,
    )

    return dp


async def run_bot(bot: Bot, dispatcher: Dispatcher) -> None:
    """Start polling."""
    try:
        logger.info("Bot started polling...")
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
