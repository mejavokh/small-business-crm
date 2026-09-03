import aiohttp
import logging
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiohttp import ClientConnectorError

router = Router()
URL = "http://127.0.0.1:8000"
logger = logging.getLogger(__name__)

@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer("Bot is working")

@router.message(Command("services"))
async def command_service(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{URL}/services/") as response:
                services = await response.json()
                logger.info(f"\nкол-во услуг: {len(services)}\n"
                            f"список услуг: {services}")

        if services:
            for service in services:
                await message.answer(f"{service['name']} -> {service['price']}")
        else:
            await message.answer("Сервисы пока недоступны")
    except ClientConnectorError:
        logger.exception("Не удалось подключиться к сервису")
        await message.answer("Что-то пошло не так, попробуйте позже")


