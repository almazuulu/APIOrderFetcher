from __future__ import annotations

import logging

from app.api.api_v1.endpoints.app import router as api_router
from fastapi import APIRouter

router = APIRouter()

logger = logging.getLogger("api")


router.include_router(api_router, prefix="/fetcher", tags=["api-fetcher"])
