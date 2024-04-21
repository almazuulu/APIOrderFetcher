from fastapi import APIRouter, BackgroundTasks, Depends

from src.app.services.data_fetcher_service import FetchService

router = APIRouter()

@router.post("/start-fetching")
async def start_fetching(
    background_tasks: BackgroundTasks,
    service: FetchService = Depends(),
):
    url = "http://api.someapi.com/api/v1/supplier/orders"
    background_tasks.add_task(service.repeat_every, 1800, FetchService.fetch_orders, (url,))
    return {"message": "Started fetching data every 30 minutes"}