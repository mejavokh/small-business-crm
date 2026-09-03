import asyncio
import os
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from bot.handlers.start import router

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
TOKEN = os.getenv("bot_token")

dp = Dispatcher()
dp.include_router(router)

async def main() -> None:
    logger.info("Bot is starting...")

    bot = Bot(token=TOKEN)
    logger.info("Bot started successfully!")

    commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="services", description="Посмотреть услуги"),
    ]

    await bot.set_my_commands(commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
