class Text:
    strings = {
        "en": {
            "start": (
                "<b>Hi {}!</b>\n\n"
                "Telegram Bot currency converter based on Google Search.\n\n"
                "<b>Select currency and send amount:</b>\n"
            ),
            "source": (
                "https://github.com/nessshon/currency-converter-bot"
            ),
            "converted": (
                "<b>Choose a currency and send a number:</b>\n"
            ),
            "currency": (
                "<b>Select currency:</b>"
            ),
            "unsupported": (
                "<b>Unsupported message type!</b>\n<i>Send a number:</i>"
            ),
            "error": (
                "<b>Unexpected error!</b>\n<i>Please wait and try again later.</i>"
            )
        },
        "ru": {
            "start": (
                "<b>Привет {}!</b>\n\n"
                "Telegram Бот конвертер валют, основанный на Google Search.\n\n"
                "<b>Выберите валюту и отправьте число:</b>\n"
            ),
            "source": (
                "https://github.com/nessshon/currency-converter-bot"
            ),
            "converted": (
                "<b>Выберите валюту и отправьте число:</b>\n"
            ),
            "currencies": (
                "<b>Выберите валюту:</b>"
            ),
            "unsupported": (
                "<b>Неподдерживаемый тип сообщения!</b>\n<i>Отправьте число:</i>"
            ),
            "error": (
                "<b>Непредвиденная ошибка!</b>\n<i>Подождите и повторите попытку позже.</i>"
            )
        }
    }

    def __init__(self, language: str):
        self.language = language

    def get(self, key: str) -> str:
        return self.strings[self.language][key]
