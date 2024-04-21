from __future__ import annotations

from datetime import datetime
from typing import ClassVar

from sqlalchemy import DateTime
from sqlalchemy import FetchedValue
from sqlalchemy import func
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

metadata = MetaData(naming_convention=convention)


class Base(DeclarativeBase):
    metadata = metadata

    __allow_unmapped__ = True
    __mapper_args__ = {"eager_defaults": True}

    __repr_cols_num = 3
    __repr_cols: ClassVar[tuple[str, ...]] = tuple()

    def __repr__(self) -> str:
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.__repr_cols or idx < self.__repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"