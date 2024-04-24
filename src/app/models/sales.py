from __future__ import annotations

import uuid
from datetime import datetime

from models.base_model import BaseCreateUpdated
from sqlalchemy import String
from sqlalchemy import UUID as SQL_UUID
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Sale(BaseCreateUpdated):
    __tablename__ = "sales"

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
    paymentSaleAmount: Mapped[int]
    forPay: Mapped[float]
    finishedPrice: Mapped[float]
    priceWithDisc: Mapped[float]
    saleID: Mapped[str]
    orderType: Mapped[str]
    sticker: Mapped[str]
    gNumber: Mapped[str]
    srid: Mapped[str] = mapped_column(String, unique=True)
