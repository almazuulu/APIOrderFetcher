import httpx
import asyncio
from datetime import datetime, timezone

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.reposotories.data_fetcher_repository import DataFetcherRepository
from src.core.deps import get_settings, get_session
from src.services.base import BaseService
from src.core.db_settings import create_async_session

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
        except httpx.RequestError as exc:
            print(f"Request error occurred: {exc}")
        return []  # Возвращаем пустой список, если возникла ошибка

    async def process_and_save_data(self, data, data_type):
        if not data:
            print("No data to process.")
            return

        tasks = []
        processed_data = []
        for item in data:
            # Создание задачи для обработки каждого элемента
            task = asyncio.create_task(self.process_item(item, data_type, processed_data))
            tasks.append(task)
        await asyncio.gather(*tasks)

        # Сохранение обработанных данных в Excel
        if processed_data:
            await self.repository.save_data_to_excel(processed_data, data_type)

    async def process_item(self, item, data_type, processed_data):
        MIN_DATE = datetime(2000, 1, 1, tzinfo=timezone.utc)
        async with create_async_session() as session:
            repository = DataFetcherRepository(session)

            # Обработка данных элемента
            if 'date' in item:
                item_date = datetime.fromisoformat(item['date'])
                item['date'] = item_date.replace(tzinfo=None) if item_date.tzinfo else item_date

            if 'lastChangeDate' in item:
                last_change_date = datetime.fromisoformat(item['lastChangeDate'])
                item['lastChangeDate'] = last_change_date.replace(
                    tzinfo=None) if last_change_date.tzinfo else last_change_date

            if 'cancelDate' in item:
                if item['cancelDate'] == '0001-01-01T00:00:00':
                    item['cancelDate'] = MIN_DATE.replace(tzinfo=None)
                else:
                    cancel_date = datetime.fromisoformat(item['cancelDate'])
                    item['cancelDate'] = cancel_date.replace(tzinfo=None) if cancel_date.tzinfo else cancel_date

            # Добавление обработанных данных в список
            processed_data.append(item)

            # Сохранение данных в базе данных
            if data_type == 'order':
                await repository.upsert_order(item)
            elif data_type == 'sale':
                await repository.upsert_sale(item)

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
