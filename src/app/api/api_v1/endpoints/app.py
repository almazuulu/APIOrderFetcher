from __future__ import annotations

from datetime import datetime
from datetime import timedelta

from app.services.data_fetcher_service import FetchService
from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from pytz import timezone

router = APIRouter()


@router.post("/start-fetching-orders/")
async def start_fetching_orders(
    background_tasks: BackgroundTasks,
    service: FetchService = Depends(),
):
    """
    Метод для старта получения заказов с маркетплейса
    """
    moscow_tz = timezone("Europe/Moscow")
    date_from = datetime.now(moscow_tz) - timedelta(minutes=30)  # Последние 30 минут
    # date_from2 = datetime.fromisoformat("2024-04-23T00:00:00")  # Дата для теста
    background_tasks.add_task(
        service.repeat_every,
        1800,
        service.fetch_orders,
        (date_from,),
    )
    return {"message": "Started fetching orders data every 30 minutes"}


@router.post("/start-fetching-sales/")
async def start_fetching_sales(
    background_tasks: BackgroundTasks,
    service: FetchService = Depends(),
):
    """
    Метод для старта получения продаж с маркетплейса
    """
    moscow_tz = timezone("Europe/Moscow")
    date_from = datetime.now(moscow_tz) - timedelta(minutes=30)  # Последние 30 минут
    # date_from2 = datetime.fromisoformat("2024-04-23T00:00:00")  # Дата для теста
    background_tasks.add_task(
        service.repeat_every,
        1800,
        service.fetch_sales,
        (date_from,),
    )
    return {"message": "Started fetching sales data every 30 minutes"}
