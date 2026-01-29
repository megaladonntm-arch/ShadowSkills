#main 
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from handlers.start import dp, command_start_handler, command_help_handler, analyze_code

from loader import bot, dp, storage
from states import CodeAnalysis

from aiogram import html
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import CommandStart, Command


dp.message.register(command_start_handler, CommandStart())
dp.message.register(command_help_handler, Command("help"))
dp.message.register(analyze_code, CodeAnalysis.waiting_for_code)

async def main() -> None:
    await dp.start_polling(bot, storage=storage)

if __name__ == "__main__":
    main()

