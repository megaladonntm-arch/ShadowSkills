from aiogram.fsm.state import State, StatesGroup


class CodeAnalysis(StatesGroup):
    waiting_for_code = State()
