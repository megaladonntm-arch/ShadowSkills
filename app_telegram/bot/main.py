import asyncio
import logging
import sys
from os import getenv
from pathlib import Path
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# Добавляем путь к проекту
project_root = Path(__file__).resolve().parents[3]
sys.path.append(str(project_root))
from services.ai_service import get_code_analysis
from app_telegram.bot.config import ADMIN_ID, BOT_TOKEN


# Получаем токен из переменной окружения


# Создаем диспетчер
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Обработчик команды /start"""
    await message.answer(
        f"👋 Привет, {hbold(message.from_user.full_name)}!\n\n"
        f"Я бот для анализа Python кода.\n"
        f"Отправь мне код, и я его проанализирую!\n\n"
        f"Команды:\n"
        f"/start - Начать работу\n"
        f"/analyze - Режим анализа кода\n"
        f"/help - Помощь"
    )


@dp.message(Command("help"))
async def help_handler(message: Message) -> None:
    """Обработчик команды /help"""
    await message.answer(
        f"{hbold('📚 Как использовать бот:')}\n\n"
        f"1. Просто отправь мне Python код\n"
        f"2. Я проанализирую его и дам рекомендации\n\n"
        f"Команды:\n"
        f"/start - Начать работу\n"
        f"/analyze - Активировать режим анализа\n"
        f"/help - Показать эту справку"
    )


@dp.message(Command("analyze"))
async def analyze_command_handler(message: Message) -> None:
    await message.answer(
        f"{hbold('🔍 Режим анализа кода активирован!')}\n\n"
        f"Отправьте мне Python код, и я проанализирую его для вас."
    )


async def send_typing_action(bot: Bot, chat_id: int, duration: int = 30):
    try:
        for _ in range(duration):
            await bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
            await asyncio.sleep(5)
    except:
        pass


@dp.message()
async def code_analysis_handler(message: Message) -> None:
    try:
        # Проверяем, что сообщение содержит текст
        if not message.text:
            await message.answer("❌ Пожалуйста, отправьте текстовое сообщение с кодом.")
            return
        
        # Получаем бот из контекста
        bot = message.bot
        
        # Запускаем индикатор "печатает" в фоне
        typing_task = asyncio.create_task(
            send_typing_action(bot, message.chat.id)
        )
        
        try:
            # Получаем анализ от AI
            ai_result = get_code_analysis(message.text)
            
            # Останавливаем индикатор "печатает"
            typing_task.cancel()
            
            max_length = 4000
            
            if len(str(ai_result)) > max_length:
                # Разбиваем на несколько сообщений
                result_str = str(ai_result)
                chunks = []#alghortims for doin well 
                current_chunk = ""
                
                for line in result_str.split('\n'):
                    if len(current_chunk) + len(line) + 1 > max_length:
                        chunks.append(current_chunk)
                        current_chunk = line
                    else:
                        current_chunk += line + '\n'
                
                if current_chunk:
                    chunks.append(current_chunk)
                
                for i, chunk in enumerate(chunks, 1):
                    await message.answer(
                        f"📄 Часть {i}/{len(chunks)}:\n\n{chunk}",
                        parse_mode=None
                    )
            else:
                # Отправляем одним сообщением
                await message.answer(
                    f"✅ Результат анализа:\n\n{ai_result}",
                    parse_mode=None
                )
        
        except asyncio.CancelledError:
            typing_task.cancel()
            raise
        
    except Exception as e:
        logging.error(f"Ошибка при анализе кода: {e}", exc_info=True)
        await message.answer(
            "❌ Произошла ошибка при анализе кода.\n"
            "Попробуйте еще раз или отправьте другой код."
        )


async def main() -> None:
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    try:
        # Удаляем старые webhook (если есть)
        await bot.delete_webhook(drop_pending_updates=True)
        
        # Запускаем polling
        logging.info("🚀 Бот запущен!")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout
    )
    
    # Запускаем бота
    asyncio.run(main())