import logging
import re

from aiogram import Dispatcher
from aiogram.utils.markdown import hcode
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, User

from app.currency_convertor import CurrencyConverter
from app.currency_convertor.codes import CODES

from .texts import Text
from .states import UserState
from .filters import IsPrivate

from .keyboards import CallbackData
from .keyboards import current_currency_markup, choose_currency_markup

from .misc.messages import edit_message, delete_previous_message
from .misc.throttling import rate_limit, waiting_previous_execution


async def convert_message(state: FSMContext,
                          message: Message = None,
                          call: CallbackQuery = None,
                          converted_text: str = None):
    data = await state.get_data()

    convert_to = data["convert_to"]
    convert_from = data["convert_from"]

    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    text = Text(language_code).get("converted")
    markup = current_currency_markup(
        language_code=language_code,
        convert_from=convert_from,
        convert_to=convert_to
    )

    if converted_text:
        await edit_message(message, converted_text)
    if message:
        msg = await message.answer(text, reply_markup=markup)
        await state.update_data(message_id=msg.message_id)
    else:
        await edit_message(call.message, text, reply_markup=markup)

    await UserState.CONVERT.set()


async def choose_currency(state: FSMContext,
                          message: Message = None,
                          call: CallbackQuery = None):
    data = await state.get_data()

    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    text = Text(language_code).get("currencies")
    markup = choose_currency_markup(language_code)

    if message:
        await message.answer(text, reply_markup=markup)
    else:
        await edit_message(call.message, text, reply_markup=markup)

    if data["toggle"] == "FROM":
        await UserState.CONVERT_FROM.set()
    else:
        await UserState.CONVERT_TO.set()


@rate_limit(1)
@waiting_previous_execution
async def convert_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    convert_to = data["convert_to"]
    convert_from = data["convert_from"]

    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    if message.content_type == "text" and re.match(r'(\d+(?:\.\d+)?)', message.text):
        emoji = await message.reply("⌛️")
        await state.update_data(throttling=True)
        await delete_previous_message(message, state)

        try:
            currency_converter = CurrencyConverter(
                from_currency=convert_from, to_currency=convert_to, amount=message.text
            )
            converted_text = await currency_converter.convert()
            converted_text = f"{hcode(converted_text)} {convert_to}"

            await convert_message(state, message=emoji, converted_text=converted_text)
        except Exception as e:
            text = Text(language_code).get("error")
            await edit_message(emoji, text)
            logging.error(e)
        finally:
            await state.update_data(throttling=False)

    else:
        text = Text(language_code).get("unsupported")
        await message.reply(text)


@rate_limit(0.5)
async def convert_message_callback_handler(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    convert_to = data["convert_to"]
    convert_from = data["convert_from"]

    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    if call.data == CallbackData.CHANGE:
        await state.update_data(
            convert_from=convert_to,
            convert_to=convert_from
        )
        await convert_message(state, call=call)
    else:
        toggle, language = call.data.split(":")

        if language in CODES[language_code].keys():
            await state.update_data(toggle=toggle)
            await choose_currency(state, call=call)

    await call.answer()


@rate_limit(0.5)
async def choose_currency_callback_handler(call: CallbackQuery, state: FSMContext):
    language_code = User.get_current().language_code
    language_code = language_code if language_code == "ru" else "en"

    if call.data == CallbackData.BACK:
        await convert_message(state, call=call)

    elif call.data in CODES[language_code].keys():
        if await state.get_state() == UserState.CONVERT_TO.state:
            await state.update_data(convert_to=call.data)
        else:
            await state.update_data(convert_from=call.data)
        await convert_message(state, call=call)

    await call.answer()


def register(dp: Dispatcher):
    dp.register_message_handler(
        convert_message_handler, IsPrivate(),
        state=UserState.CONVERT,
        content_types="any"
    )
    dp.register_callback_query_handler(
        convert_message_callback_handler, IsPrivate(),
        state=UserState.CONVERT
    )
    dp.register_callback_query_handler(
        choose_currency_callback_handler, IsPrivate(),
        state=[UserState.CONVERT_TO, UserState.CONVERT_FROM]
    )
