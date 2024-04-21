from __future__ import annotations

import logging

from src.app.api.api_v1.endpoints import router as api_router
from fastapi import APIRouter

router = APIRouter()

logger = logging.getLogger("api")


router.include_router(api_router, prefix="/", tags=["api-fetcher"])
