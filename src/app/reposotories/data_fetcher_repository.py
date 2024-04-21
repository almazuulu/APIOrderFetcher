from sqlalchemy import select, update, insert
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.models.orders import Order
from app.models.sales import Sale
from repositories.base import BaseRepository

class DataFetcherRepository(BaseRepository):
    async def upsert_order(self, order_data: dict) -> None:
        """Inserts or updates an order based on srid."""
        stmt = select(Order).where(Order.srid == order_data['srid'])
        result = await self.one_or_none(stmt)
        if result:
            # Если запись существует, обновляем её
            update_stmt = (
                update(Order)
                .where(Order.srid == order_data['srid'])
                .values(**order_data)
                .execution_options(synchronize_session="fetch")
            )
            await self.execute(update_stmt)
        else:
            # Если запись не существует, вставляем новую
            new_order = Order(**order_data)
            await self.save(new_order)

    async def upsert_sale(self, sale_data: dict) -> None:
        """Inserts or updates a sale based on srid."""
        stmt = select(Sale).where(Sale.srid == sale_data['srid'])
        result = await self.one_or_none(stmt)
        if result:
            # Если запись существует, обновляем её
            update_stmt = (
                update(Sale)
                .where(Sale.srid == sale_data['srid'])
                .values(**sale_data)
                .execution_options(synchronize_session="fetch")
            )
            await self.execute(update_stmt)
        else:
            # Если запись не существует, вставляем новую
            new_sale = Sale(**sale_data)
            await self.save(new_sale)
