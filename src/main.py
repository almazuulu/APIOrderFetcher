import uvicorn
from fastapi import FastAPI
from src.app import api as fetcher_api

app = FastAPI(
    title="API Order fetcher",
    description=f"для асинхронной загрузки и обработки данных о заказах и продажах",
)

app.include_router(fetcher_api.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
