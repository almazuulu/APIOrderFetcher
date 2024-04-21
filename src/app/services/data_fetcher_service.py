import httpx
import asyncio

from src.core.services.base import BaseService

class FetchService(BaseService):
    @staticmethod
    async def fetch_orders(api_url: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            return response.json()

    @staticmethod
    async def repeat_every(interval: int, func, *args):
        while True:
            await func(*args)
            await asyncio.sleep(interval)