from __future__ import annotations

import abc
import logging
from collections.abc import Iterable
from typing import Any
from typing import Generic
from typing import Optional
from typing import TypeVar

from sqlalchemy import Result
from sqlalchemy import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Delete
from sqlalchemy.sql import Select
from sqlalchemy.sql import Update

logger = logging.getLogger("api")

T = TypeVar("T")


class BaseRepository(abc.ABC, Generic[T]):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def save(self, obj: T) -> T:
        self.session.add(obj)
        await self.session.flush()
        await self.session.refresh(obj)
        return obj

    async def bulk_save(self, objs: list[T]) -> None:
        self.session.add_all(objs)

    async def one_or_none(self, statement: Select) -> Optional[Result]:
        return (await self.session.execute(statement)).scalars().one_or_none()

    async def one_or_none_unique(self, statement: Select) -> Optional[Any]:
        return (await self.session.execute(statement)).scalars().unique().one_or_none()

    async def all(self, statement: Select) -> Iterable[Any]:
        return (await self.session.execute(statement)).scalars().all()

    async def all_unique(self, statement: Select) -> Iterable[Any]:
        result = await self.session.execute(statement)
        return result.scalars().unique().all()

    async def execute(self, statement: Select | Update | Delete) -> Any:
        return await self.session.execute(statement)

    async def save_all(self, objects: list[T]) -> None:
        self.session.add_all(objects)

    async def first(self, statement: Select) -> Optional[Any]:
        return (await self.session.execute(statement)).scalars().first()

    async def remove(self, obj: T) -> None:
        return await self.session.delete(obj)

    async def fetch_mapped_results(self, statement: Select) -> list[RowMapping]:
        result = await self.session.execute(statement)
        return list(result.mappings())
