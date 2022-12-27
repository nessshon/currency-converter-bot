from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.currency_convertor.codes import CODES


@dataclass
class CallbackData:
    BACK: str = "BACK"
    CHANGE: str = "CHANGE"
    FROM: str = "FROM:"
    TO: str = "TO:"


def current_currency_markup(language_code: str,
                            convert_from: str,
                            convert_to: str
                            ) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=3)

    markup.add(
        InlineKeyboardButton(
            text=CODES[language_code].get(convert_from),
            callback_data=CallbackData.FROM + convert_from
        ),
        InlineKeyboardButton(
            text="⇌", callback_data=CallbackData.CHANGE
        ),
        InlineKeyboardButton(
            text=CODES[language_code].get(convert_to),
            callback_data=CallbackData.TO + convert_to
        )
    )
    return markup


def choose_currency_markup(language_code: str) -> InlineKeyboardMarkup:
    markup = InlineKeyboardMarkup(row_width=2)

    markup.add(
        *[
            InlineKeyboardButton(
                text=name, callback_data=code
            ) for code, name in
            CODES[language_code].items()
        ],
        InlineKeyboardButton(
            text="←", callback_data=CallbackData.BACK
        )
    )
    return markup
