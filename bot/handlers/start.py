import aiohttp
import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiohttp import ClientConnectorError, ClientResponseError

from bot.keyboards.client import (
services_keyboard, employees_keyboard, dates_keyboard, confirm_booking_keyboard
)
from bot.states.booking import BookingState

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
async def select_service(callback: CallbackQuery, state: FSMContext):
    service_id = int(callback.data.replace("service_", ""))

    await state.update_data(service_id=service_id)
    await state.set_state(BookingState.choosing_employee)

    logger.info(f"Пользователь выбрал услугу с id = {service_id}")

    await callback.answer()

    await callback.message.answer(f"Вы выбрали услугу с id {service_id}")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{URL}/clients") as response:
            response.raise_for_status()
            clients = await response.json()

    employees = []

    for client in clients:
        if client['role'] == 'employee':
            employees.append(client)

    logger.info(f"Сотрудники: {employees}")

    if employees:
        await callback.message.answer(
            "Выберите сотрудника",
            reply_markup=employees_keyboard(employees)
        )
    else:
        await callback.message.answer("Сотрудники пока не доступны")

@router.callback_query(F.data.startswith("employee_"))
async def select_employee(callback: CallbackQuery, state: FSMContext):
    employee_id = int(callback.data.replace("employee_", ""))

    await state.update_data(employee_id=employee_id)
    await state.set_state(BookingState.choosing_date)

    logger.info(
        f"Пользователь выбрал сотрудника с id: {employee_id}"
    )
    await callback.answer()

    await callback.message.answer("Выберите дату", reply_markup=dates_keyboard())

@router.callback_query(F.data.startswith("date_"))
async def select_date(callback: CallbackQuery, state: FSMContext):
    booking_date = callback.data.replace("date_", "")

    await state.update_data(booking_date=booking_date)
    await state.set_state(BookingState.choosing_time)

    logger.info(
        f"Пользователь выбрал дату: {booking_date}"
    )
    await callback.answer()

    await callback.message.answer("Выберите время для бронирования")

@router.message(BookingState.choosing_time)
async def select_time(message: Message, state: FSMContext):
    try:
        booking_time = message.text

        datetime.strptime(booking_time, "%H:%M")

        await state.update_data(booking_time=booking_time)
        data = await state.get_data()

        await message.answer(
            f"Проверьте данные бронирования:\n\n"
            f"Услуга ID: {data['service_id']}\n"
            f"Сотрудник ID: {data['employee_id']}\n"
            f"Дата: {data['booking_date']}\n"
            f"Время: {data['booking_time']}",
            reply_markup=confirm_booking_keyboard()
        )

    except ValueError:
        await message.answer("Неверный формат времени. Введите например: 14:12")
        return

@router.callback_query(F.data == 'booking_confirm')
async def confirm_booking(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    logger.info(f"Данные бронирования: {data}")

    await callback.answer()
