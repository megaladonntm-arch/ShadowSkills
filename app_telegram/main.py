import asyncio
import logging
import sys
from os import getenv

sys.path.insert(0, '..')

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from sqlalchemy.orm import Session

from app.data_base.crud import crud_user
from app.data_base.base import SessionLocal
from app.schemas import user as schemas_user

TOKEN = getenv("BOT_TOKEN")

dp = Dispatcher()

class Registration(StatesGroup):
    waiting_for_username = State()
    waiting_for_email = State()
    waiting_for_full_name = State()
    waiting_for_password = State()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Hello, {html.bold(message.from_user.full_name)}!")
    await message.answer("To register a new account, use the /register command.")

@dp.message(Command("cancel"))
@dp.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Registration has been cancelled.")

@dp.message(Command("register"))
async def register_start_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(Registration.waiting_for_username)
    await message.answer("Let's start the registration. Please send me your desired username:")

@dp.message(Registration.waiting_for_username)
async def process_username(message: Message, state: FSMContext) -> None:
    db_gen = get_db()
    db: Session = next(db_gen)
    try:
        if not message.text.isalnum():
            await message.answer("Username must be alphanumeric. Please try again or type /cancel to stop.")
            return
        if crud_user.get_user_by_username(db, username=message.text):
            await message.answer("This username is already taken. Please choose another one or type /cancel.")
            return
    finally:
        next(db_gen, None)

    await state.update_data(username=message.text)
    await state.set_state(Registration.waiting_for_email)
    await message.answer("Great! Now, please send me your email address:")

@dp.message(Registration.waiting_for_email)
async def process_email(message: Message, state: FSMContext) -> None:
    if '@' not in message.text or '.' not in message.text:
        await message.answer("This doesn't look like a valid email. Please try again or type /cancel.")
        return

    db_gen = get_db()
    db: Session = next(db_gen)
    try:
        if crud_user.get_user_by_email(db, email=message.text):
            await message.answer("An account with this email already exists. Please use another email or type /cancel.")
            return
    finally:
        next(db_gen, None)

    await state.update_data(email=message.text)
    await state.set_state(Registration.waiting_for_full_name)
    await message.answer("Got it. What is your full name?")

@dp.message(Registration.waiting_for_full_name)
async def process_full_name(message: Message, state: FSMContext) -> None:
    await state.update_data(full_name=message.text)
    await state.set_state(Registration.waiting_for_password)
    await message.answer("Almost done. Please send me a password. I will delete your message for security.")

@dp.message(Registration.waiting_for_password)
async def process_password(message: Message, state: FSMContext) -> None:
    user_data = await state.get_data()
    user_data['password'] = message.text
    await message.delete()

    db_gen = get_db()
    db: Session = next(db_gen)
    try:
        user_in = schemas_user.UserCreate(**user_data)
        crud_user.create_user(db, user=user_in)
        await message.answer("Registration successful! You can now use the service.")
    except Exception as e:
        logging.error(f"Failed to create user: {e}")
        await message.answer("An error occurred during registration. Please start over with /register.")
    finally:
        next(db_gen, None)
        await state.clear()

@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())