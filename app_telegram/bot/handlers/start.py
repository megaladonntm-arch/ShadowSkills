from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from app_telegram.bot.loader import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! "
                         f"I'm a code analyzer bot. "
                         f"Send me a Python code snippet to analyze.")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer("Send me a Python code snippet and I will analyze it for you.")
