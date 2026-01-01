import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties

from bot.app import create_dispatcher, run_bot
from core.config import BotSettings, RedisSettings
from di.container import create_container

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("Initializing bot container...")

    container = create_container()

    bot_settings: BotSettings = await container.get(BotSettings)
    redis_settings: RedisSettings = await container.get(RedisSettings)

    bot = Bot(
        token=bot_settings.token.get_secret_value(), default=DefaultBotProperties(parse_mode="HTML")
    )
    dispatcher = await create_dispatcher(
        bot, container, redis_settings if bot_settings.use_redis else None
    )

    await run_bot(bot, dispatcher)


if __name__ == "__main__":
    # Fix for Windows + psycopg async
    if sys.platform == "win32":
        asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)
    else:
        asyncio.run(main())
