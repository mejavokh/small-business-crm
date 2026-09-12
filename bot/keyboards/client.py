from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def services_keyboard(services):
    keyboard = []

    for service in services:
        button = InlineKeyboardButton(
            text=f"""{service['name']} -> {service['price']}""",
            callback_data=f"""service_{service['id']}"""
        )

        keyboard.append([button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def employees_keyboard(employees):
    keyboard = []

    for employee in employees:
        button = InlineKeyboardButton(
            text=f"{employee['name']}",
            callback_data=f"employee_{employee['id']}"
        )

        keyboard.append([button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def dates_keyboard():
    keyboard = []
    today = datetime.now().date()

    for i in range(7):
        date = today + timedelta(days=i)

        button = InlineKeyboardButton(
            text=f"{date.strftime('%d.%m')}",
            callback_data=f"date_{date.strftime('%Y-%m-%d')}"
        )

        keyboard.append([button])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def confirm_booking_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text='Подтвердить', callback_data='booking_confirm')
        ],
        [
            InlineKeyboardButton(text="Отмена", callback_data="booking_cancel")
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)