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