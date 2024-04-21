import httpx
import asyncio
from datetime import datetime
from pytz import timezone
from src.core.deps import get_settings
from src.core.services.base import BaseService


class FetchService(BaseService):

    def __init__(self):
        super().__init__()
        settings = get_settings()
        self.base_url = settings.BASE_URL
        self.api_token = settings.BEARER_TOKEN

    async def fetch_data(self, api_url: str, date_from: datetime, flag: int):
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%S'),  # Форматируем datetime в строку RFC3339
            'flag': flag
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, headers=headers, params=params)
                response.raise_for_status()  # Проверяем на наличие HTTP ошибок
                data = response.json()  # Получаем данные в формате JSON
                return data
        except httpx.HTTPStatusError as exc:
            return None
        except httpx.RequestError as exc:
            return None

    async def fetch_orders(self, date_from_tuple: tuple, flag: int = 0):
        date_from = date_from_tuple[0]  # Извлекаем datetime из кортежа
        orders_url = f"{self.base_url}/api/v1/supplier/orders"
        return await self.fetch_data(orders_url, date_from, flag)

    async def fetch_sales(self, date_from_tuple: tuple, flag: int = 0):
        date_from = date_from_tuple[0]  # Извлекаем datetime из кортежа
        sales_url = "https://statistics-api.wildberries.ru/api/v1/supplier/sales"
        return await self.fetch_data(sales_url, date_from, flag)

    async def repeat_every(self, interval: int, func, *args):
        while True:
            await func(*args)
            await asyncio.sleep(interval)

