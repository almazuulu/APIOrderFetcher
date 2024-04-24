from __future__ import annotations

import uvicorn
from app.api import api as fetcher_api
from core.deps import get_settings
from fastapi import FastAPI
from logger_config import setup_logging

setup_logging()

settings = get_settings()


app = FastAPI(
    title=settings.APP_NAME,
    description=f"{settings.OPENAPI_DESCRIPTION}",
)

app.include_router(fetcher_api.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
