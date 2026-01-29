from aiogram import html
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
#PATHS
import sys
from pathlib import Path
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))
from services.ai_service import get_code_analysis
# =Boots
from app_telegram.bot.loader import dp


