import asyncio
import contextlib
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka

from bot.dialogs import (
    admin_dialog,
    group_selection_dialog,
    main_menu_dialog,
    onboarding_dialog,
    schedule_dialog,
    settings_dialog,
)
from bot.handlers.user import router as user_router
from core.config import BotSettings, RedisSettings
from di.container import create_container
from services.sync_service import SyncService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def setup_bot_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="📝 Главное меню"),
        BotCommand(command="help", description="📅 Помощь"),
    ]
    await bot.set_my_commands(commands)


def create_storage(
    use_redis: bool = False,
    redis_settings: RedisSettings | None = None,
) -> MemoryStorage | RedisStorage:
    """Create FSM storage based on configuration."""
    if use_redis and redis_settings:
        try:
            storage = RedisStorage.from_url(
                redis_settings.dsn, key_builder=DefaultKeyBuilder(with_destiny=True)
            )
            logger.info("Using Redis storage")
            return storage
        except (RuntimeError, ConnectionError) as e:
            logger.warning("Redis connection failed, using MemoryStorage: %s", e)

    logger.info("Using MemoryStorage")
    return MemoryStorage()


async def run_initial_sync(sync_service: SyncService):
    """Run initial sync on startup."""
    logger.info("Running initial sync...")

    try:
        await sync_service.sync_all_schedules()
        logger.info("Initial sync completed")

    except Exception as e:
        logger.error("Initial sync failed: %s", e)


async def main() -> None:
    logger.info("Starting bot initialization...")

    container = create_container()

    bot_settings: BotSettings = await container.get(BotSettings)
    redis_settings: RedisSettings = await container.get(RedisSettings)

    storage = create_storage(use_redis=bot_settings.use_redis, redis_settings=redis_settings)

    bot = Bot(
        token=bot_settings.token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML")
    )

    dp = Dispatcher(storage=storage)

    await setup_bot_commands(bot)
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

    sync_task: asyncio.Task | None = None
    if bot_settings.run_initial_sync:
        async with container() as nested_container:
            sync_service = await nested_container.get(SyncService)
            sync_task = asyncio.create_task(run_initial_sync(sync_service))

    try:
        logger.info("Bot started polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error("Bot polling failed: %s", e)
        raise
    finally:
        # Ensure sync task is completed or cancelled
        if sync_task and not sync_task.done():
            sync_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await sync_task
        await container.close()
        await bot.session.close()


if __name__ == "__main__":
    if sys.platform == "win32":
        # Windows with psycopg async requires SelectorEventLoop
        asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)
    else:
        asyncio.run(main())
