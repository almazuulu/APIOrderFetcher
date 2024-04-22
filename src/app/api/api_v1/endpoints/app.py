from fastapi import APIRouter, BackgroundTasks, Depends
from datetime import datetime, timedelta
from pytz import timezone

from src.app.services.data_fetcher_service import FetchService

router = APIRouter()

@router.post("/start-fetching-orders/")
async def start_fetching_orders(
    background_tasks: BackgroundTasks,
    service: FetchService = Depends(),
):
    moscow_tz = timezone('Europe/Moscow')
    date_from = datetime.now(moscow_tz) - timedelta(minutes=30)
    date_from2 = datetime.fromisoformat('2024-04-19T00:00:00') # TODO: Убрать после
    background_tasks.add_task(service.repeat_every, 1800, service.fetch_orders, (date_from2,))
    return {"message": "Started fetching orders data every 30 minutes"}

@router.post("/start-fetching-sales/")
async def start_fetching_sales(
    background_tasks: BackgroundTasks,
    service: FetchService = Depends(),
):
    moscow_tz = timezone('Europe/Moscow')
    date_from = datetime.now(moscow_tz) - timedelta(minutes=30)  # Последние 30 минут
    date_from2 = datetime.fromisoformat('2024-04-20T00:00:00') # TODO: Убрать после
    background_tasks.add_task(service.repeat_every, 1800, service.fetch_sales, (date_from2,))
    return {"message": "Started fetching sales data every 30 minutes"}

