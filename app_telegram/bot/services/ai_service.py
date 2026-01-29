import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))

from Openrouter.src.Service.ai_code_analyzer import analyze_code
from app_telegram.bot.config import OPENROUTER_API_KEY


async def get_code_analysis(code: str):
    return analyze_code(code_to_analyze=code, api_key=OPENROUTER_API_KEY)