from aiogram.dispatcher.filters.state import StatesGroup, State


class UserState(StatesGroup):
    CONVERT = State()
    CONVERT_TO = State()
    CONVERT_FROM = State()
