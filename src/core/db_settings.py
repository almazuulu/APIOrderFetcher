from __future__ import annotations


from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import Settings

settings = Settings()

async_engine = create_async_engine(
    settings.db_url,
    connect_args={"server_settings": {"application_name": "PROJECT_SERVICE_ASYNC"}},
    max_overflow=settings.DB_ENGINE_MAX_OVERFLOW,
    pool_pre_ping=settings.DB_ENGINE_POOL_PRE_PING,
    pool_recycle=settings.DB_ENGINE_POOL_RECYCLE,
    pool_size=settings.DB_ENGINE_POOL_SIZE,
    pool_timeout=settings.DB_ENGINE_POOL_TIMEOUT,
    echo=settings.SQL_ENGINE_ECHO,
)

create_async_session = async_sessionmaker(async_engine, expire_on_commit=False)