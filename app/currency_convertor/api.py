import aiohttp
from bs4 import BeautifulSoup
from getuseragent import UserAgent

from . import config


class CurrencyConverter:
    user_agent = UserAgent().Random()
    headers = {"user-agent": user_agent, "Range": "bytes=0-1"}

    def __init__(self, from_currency: str, to_currency: str,
                 amount: int | float | str):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.amount = amount

    async def _request(self):
        async with aiohttp.ClientSession(headers=self.headers) as session:
            base_url = config.BASE_URL.format(
                self.to_currency, self.from_currency, self.amount)
            response = await session.get(url=base_url)

            return await response.read()

    async def convert(self) -> str | int:
        request = await self._request()
        bs4 = BeautifulSoup(request.decode('utf-8'), "html.parser")

        return bs4.find("span", class_="DFlfde SwHCTb").text
