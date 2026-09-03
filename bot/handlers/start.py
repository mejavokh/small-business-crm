from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

router = Router()

@router.message(CommandStart())
async def command_start(message: Message) -> None:
    await message.answer("Bot is working")

@router.message(Command("services"))
async def command_service(message: Message) -> None:
    await message.answer("Here will be services")