from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
#PATHS
import sys
from pathlib import Path
# =Boots
from app_telegram.bot.loader import dp

project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

async def command_start_handler(message: Message) -> None:

    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}! "
                         f"I'm a code analyzer bot. "
                         f"Send me a Python code snippet to analyze.")

async def command_help_handler(message: Message) -> None:
    await message.answer("Send me a Python code snippet and I will analyze it for you.")

async def analyze_code(prompt: Message) -> None:
    await prompt.answer("Analyzing code...")


