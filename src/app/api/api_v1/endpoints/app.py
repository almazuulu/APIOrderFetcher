from fastapi import APIRouter, BackgroundTasks, Depends
from datetime import datetime, timedelta
from pytz import timezone

from app.services.data_fetcher_service import FetchService

router = APIRouter()

@router.post("/start-fetching-orders/")
async def start_fetching_orders(
    background_tasks: BackgroundTasks,
    service: FetchService = Depends(),
):
    moscow_tz = timezone('Europe/Moscow')
    date_from = datetime.now(moscow_tz) - timedelta(minutes=30)
    background_tasks.add_task(service.repeat_every, 1800, service.fetch_orders, (date_from,))
    return {"message": "Started fetching orders data every 30 minutes"}

@router.post("/start-fetching-sales/")
async def start_fetching_sales(
    background_tasks: BackgroundTasks,
    service: FetchService = Depends(),
):
    moscow_tz = timezone('Europe/Moscow')
    date_from = datetime.now(moscow_tz) - timedelta(minutes=30)  # Последние 30 минут
    background_tasks.add_task(service.repeat_every, 1800, service.fetch_sales, (date_from,))
    return {"message": "Started fetching sales data every 30 minutes"}

