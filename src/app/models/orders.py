import uuid

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import UUID as SQL_UUID, String, DateTime
from datetime import datetime

from models.base_model import Base


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(SQL_UUID, primary_key=True, default=uuid.uuid4)
    date: Mapped[datetime]
    lastChangeDate: Mapped[datetime]
    warehouseName: Mapped[str]
    countryName: Mapped[str]
    oblastOkrugName: Mapped[str]
    regionName: Mapped[str]
    supplierArticle: Mapped[str]
    nmId: Mapped[int]
    barcode: Mapped[str]
    category: Mapped[str]
    subject: Mapped[str]
    brand: Mapped[str]
    techSize: Mapped[str]
    incomeID: Mapped[int]
    isSupply: Mapped[bool]
    isRealization: Mapped[bool]
    totalPrice: Mapped[float]
    discountPercent: Mapped[int]
    spp: Mapped[float]
    finishedPrice: Mapped[float]
    priceWithDisc: Mapped[float]
    isCancel: Mapped[bool]
    cancelDate: Mapped[datetime]
    orderType: Mapped[str]
    sticker: Mapped[str]
    gNumber: Mapped[str]
    srid: Mapped[str] = mapped_column(String, unique=True)