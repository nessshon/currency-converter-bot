import asyncio

from aiogram.utils import markdown
from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import (BotCommand, BotCommandScopeAllPrivateChats,
                           Message, User)

from .texts import Text
from .states import UserState
from .filters import IsPrivate
from .keyboards import current_currency_markup

from .misc.throttling import rate_limit
from .misc.messages import delete_previous_message, delete_message, edit_message


@rate_limit(2)
async def command_start(message: Message, state: FSMContext):
    emoji = await message.answer("👋")

    convert_to = "USD"
    convert_from = "RUB"

    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    await delete_previous_message(message, state)
    await delete_message(message)
    await asyncio.sleep(2)

    user_link = markdown.hlink(
        title=message.from_user.first_name,
        url=message.from_user.url
    )
    text = Text(language_code).get("start")
    markup = current_currency_markup(
        language_code=language_code,
        convert_from=convert_from,
        convert_to=convert_to
    )

    await edit_message(emoji, text.format(user_link), reply_markup=markup)
    async with state.proxy() as data:
        data.clear()
    await state.update_data(
        message_id=emoji.message_id,
        convert_to=convert_to,
        convert_from=convert_from,
    )
    await UserState.CONVERT.set()


@rate_limit(2)
async def command_source(message: Message, state: FSMContext):
    emoji = await message.answer("👨‍💻")
    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    await delete_previous_message(message, state)
    await delete_message(message)
    await asyncio.sleep(2)

    text = Text(language_code).get("source")
    await edit_message(emoji, text)
    await state.update_data(message_id=emoji.message_id)


async def setup(bot: Bot):
    commands = {
        "en": [
            BotCommand("start", "Restart"),
            BotCommand("source", "Source code"),
        ],
        "ru": [
            BotCommand("start", "Перезапустить"),
            BotCommand("source", "Исходный код"),
        ]
    }

    await bot.set_my_commands(
        commands=commands["ru"],
        scope=BotCommandScopeAllPrivateChats(),
        language_code="ru"
    )
    await bot.set_my_commands(
        commands=commands["en"],
        scope=BotCommandScopeAllPrivateChats(),
    )


def register(dp: Dispatcher):
    dp.register_message_handler(
        command_start, CommandStart(), IsPrivate(), state="*"
    )
    dp.register_message_handler(
        command_source, IsPrivate(), commands="source", state="*"
    )
