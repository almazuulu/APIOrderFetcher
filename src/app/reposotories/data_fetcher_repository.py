from __future__ import annotations

import logging
import os
from datetime import datetime

import pandas as pd
from app.models.orders import Order
from app.models.sales import Sale
from repositories.base import BaseRepository
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)


class DataFetcherRepository(BaseRepository):
    async def save_data_to_excel(self, data, type_of_data):
        if not data:
            logger.info("No data provided to save to Excel.")
            return

        try:
            # Создание DataFrame из данных
            new_data_df = pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Error creating DataFrame from data: {e}")
            return

        # Определение пути и имени файла с текущей датой и временем
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = "app/excel_data"  # Вы можете изменить этот путь по вашему желанию
        excel_filepath = os.path.join(folder_path, f"{type_of_data}_{now}.xlsx")

        # Проверяем, существует ли директория, и если нет, создаем ее
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if os.path.exists(excel_filepath):
            # Чтение существующего файла и добавление новых данных
            existing_df = pd.read_excel(excel_filepath)
            updated_df = pd.concat([existing_df, new_data_df], ignore_index=True)
        else:
            updated_df = new_data_df

        # Удаление столбца id, если он существует
        if "id" in updated_df.columns:
            updated_df = updated_df.drop(columns=["id"])

        # Сохранение DataFrame в Excel
        updated_df.to_excel(excel_filepath, index=False)
        logger.info(f"Data appended to {excel_filepath}")

    async def upsert_order(self, order_data: dict) -> None:
        """Inserts or updates an order based on srid."""
        try:
            stmt = select(Order).where(Order.srid == order_data["srid"])
            result = await self.one_or_none(stmt)
            if result:
                # Если запись существует, обновляем её
                update_stmt = (
                    update(Order)
                    .where(Order.srid == order_data["srid"])
                    .values(**order_data)
                    .execution_options(synchronize_session="fetch")
                )
                await self.execute(update_stmt)
                logger.info(f"Updated order with srid: {order_data['srid']}")
            else:
                # Если запись не существует, вставляем новую
                new_order = Order(**order_data)
                await self.save(new_order)
                logger.info(f"Inserted new order with srid: {order_data['srid']}")
            await self.session.commit()  # Фиксируем изменения в базе данных
        except SQLAlchemyError as e:
            logger.error(f"Database error when upserting order: {e}")

    async def upsert_sale(self, sale_data: dict) -> None:
        """Inserts or updates a sale based on srid."""
        try:
            stmt = select(Sale).where(Sale.srid == sale_data["srid"])
            result = await self.one_or_none(stmt)
            if result:
                # Если запись существует, обновляем её
                update_stmt = (
                    update(Sale)
                    .where(Sale.srid == sale_data["srid"])
                    .values(**sale_data)
                    .execution_options(synchronize_session="fetch")
                )
                await self.execute(update_stmt)
                logger.info(f"Updated sale with srid: {sale_data['srid']}")
            else:
                # Если запись не существует, вставляем новую
                new_sale = Sale(**sale_data)
                await self.save(new_sale)
                logger.info(f"Inserted new sale with srid: {sale_data['srid']}")
            await self.session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Database error when upserting sale: {e}")
