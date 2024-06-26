"""create sales table

Revision ID: db4eb538e2ed
Revises: 954771e6af4f
Create Date: 2024-04-22 01:43:33.229382

"""
from __future__ import annotations

from collections.abc import Sequence
from typing import Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "db4eb538e2ed"
down_revision: Union[str, None] = "954771e6af4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "sales",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("lastChangeDate", sa.DateTime(), nullable=False),
        sa.Column("warehouseName", sa.String(), nullable=False),
        sa.Column("countryName", sa.String(), nullable=False),
        sa.Column("oblastOkrugName", sa.String(), nullable=False),
        sa.Column("regionName", sa.String(), nullable=False),
        sa.Column("supplierArticle", sa.String(), nullable=False),
        sa.Column("nmId", sa.Integer(), nullable=False),
        sa.Column("barcode", sa.String(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("subject", sa.String(), nullable=False),
        sa.Column("brand", sa.String(), nullable=False),
        sa.Column("techSize", sa.String(), nullable=False),
        sa.Column("incomeID", sa.Integer(), nullable=False),
        sa.Column("isSupply", sa.Boolean(), nullable=False),
        sa.Column("isRealization", sa.Boolean(), nullable=False),
        sa.Column("totalPrice", sa.Float(), nullable=False),
        sa.Column("discountPercent", sa.Integer(), nullable=False),
        sa.Column("spp", sa.Float(), nullable=False),
        sa.Column("paymentSaleAmount", sa.Integer(), nullable=False),
        sa.Column("forPay", sa.Float(), nullable=False),
        sa.Column("finishedPrice", sa.Float(), nullable=False),
        sa.Column("priceWithDisc", sa.Float(), nullable=False),
        sa.Column("saleID", sa.String(), nullable=False),
        sa.Column("orderType", sa.String(), nullable=False),
        sa.Column("sticker", sa.String(), nullable=False),
        sa.Column("gNumber", sa.String(), nullable=False),
        sa.Column("srid", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sales")),
        sa.UniqueConstraint("srid", name=op.f("uq_sales_srid")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("sales")
    # ### end Alembic commands ###
