from __future__ import annotations

import logging
from asyncio import shield
from collections.abc import AsyncGenerator
from functools import lru_cache
from logging import Logger

from config import Settings
from core.db_settings import create_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request


def get_logger() -> Logger:
    return logging.getLogger("api")


@lru_cache
def get_settings() -> Settings:
    return Settings()


async def get_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    session = create_async_session()
    yield session
    await session.commit()
    await shield(session.close())
