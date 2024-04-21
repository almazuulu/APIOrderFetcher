import httpx
import asyncio
from datetime import datetime, timezone

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.reposotories.data_fetcher_repository import DataFetcherRepository
from src.core.deps import get_settings, get_session
from src.services.base import BaseService

class FetchService(BaseService):
    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.repository: DataFetcherRepository = DataFetcherRepository(session)
        settings = get_settings()
        self.base_url = settings.BASE_URL
        self.api_token = settings.BEARER_TOKEN

    async def fetch_data(self, api_url: str, date_from: datetime, flag: int):
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }
        params = {
            'dateFrom': date_from.strftime('%Y-%m-%dT%H:%M:%S'),
            'flag': flag
        }
        print("Fetching data from URL:", api_url)
        print("With headers:", headers)
        print("And params:", params)
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(api_url, headers=headers, params=params)
                response.raise_for_status()
                data = response.json()
                print("Response Status:", response.status_code)
                print("Response Data:", data)
                return data
        except httpx.HTTPStatusError as exc:
            print(f"HTTP error occurred: {exc.response.status_code} - {exc.response.text}")
            return None
        except httpx.RequestError as exc:
            print(f"Request error occurred: {exc}")
            return None

    async def process_and_save_data(self, data, data_type):
        tasks = []
        MIN_DATE = datetime(1, 1, 1, tzinfo=timezone.utc)  # Установка минимально возможной даты

        if data:
            for item in data:
                # Преобразуем строки даты в объекты datetime
                if 'date' in item:
                    item['date'] = datetime.fromisoformat(item['date'])
                if 'lastChangeDate' in item:
                    item['lastChangeDate'] = datetime.fromisoformat(item['lastChangeDate'])
                if 'cancelDate' in item:
                    # Применяем MIN_DATE если cancelDate равно '0001-01-01T00:00:00'
                    item['cancelDate'] = datetime.fromisoformat(item['cancelDate']) if item[
                                                                                           'cancelDate'] != '0001-01-01T00:00:00' else MIN_DATE

                # Создаём задачу на сохранение в зависимости от типа данных
                if data_type == 'order':
                    task = asyncio.create_task(self.repository.upsert_order(item))
                elif data_type == 'sale':
                    task = asyncio.create_task(self.repository.upsert_sale(item))
                tasks.append(task)

            if tasks:
                await asyncio.gather(*tasks)
                for task in tasks:
                    await task.result().session.close()

    async def fetch_orders(self, date_from_tuple: tuple, flag: int = 0):
        date_from = date_from_tuple[0]
        orders_url = f"{self.base_url}/api/v1/supplier/orders"
        print("Fetching orders for date:", date_from)
        order_data = await self.fetch_data(orders_url, date_from, flag)
        await self.process_and_save_data(order_data, 'order')

    async def fetch_sales(self, date_from_tuple: tuple, flag: int = 0):
        date_from = date_from_tuple[0]
        sales_url = f"{self.base_url}/api/v1/supplier/sales"
        print("Fetching sales for date:", date_from)
        sale_data = await self.fetch_data(sales_url, date_from, flag)
        await self.process_and_save_data(sale_data, 'sale')

    async def repeat_every(self, interval: int, func, *args):
        while True:
            print("Running task every", interval, "seconds with args:", args)
            await func(*args)
            await asyncio.sleep(interval)
