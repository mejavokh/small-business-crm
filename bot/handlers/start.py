import aiohttp
import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiohttp import ClientConnectorError, ClientResponseError

from bot.keyboards.client import services_keyboard

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
                response.raise_for_status()
                services = await response.json()
                logger.info(f"\nкол-во услуг: {len(services)}\n"
                            f"список услуг: {services}")

        if services:
            await message.answer(
                "Выберите услугу",
                reply_markup=services_keyboard(services)
            )
        else:
            await message.answer("Сервисы пока недоступны")
    except ClientConnectorError:
        logger.exception("Не удалось подключиться к сервису")
        await message.answer("Что-то пошло не так, попробуйте позже")
    except ClientResponseError as e:
        logger.error(f"Сервер вернул ошибку: {e.status}")
        await message.answer("Произошла ошибка на сервере")


@router.callback_query(F.data.startswith("service_"))
async def select_service(callback: CallbackQuery):
    service_id = int(callback.data.replace("service_", ""))
    logger.info(f"Пользователь выбрал услугу с id = {service_id}")

    await callback.answer()

    await callback.message.answer(f"Вы выбрали услугу с id {service_id}")

