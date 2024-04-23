import uvicorn
from fastapi import FastAPI
from app.api import api as fetcher_api
from core.deps import get_settings

settings = get_settings()


app = FastAPI(
    title=settings.APP_NAME,
    description=f"{settings.OPENAPI_DESCRIPTION}",
)

app.include_router(fetcher_api.router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
