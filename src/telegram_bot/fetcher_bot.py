import os
import asyncio
import logging
from aiogram import Bot
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from aiogram.dispatcher.router import Router
from aiogram.client.default import DefaultBotProperties
from aiogram.dispatcher.dispatcher import Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

load_dotenv()
API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')
EXCEL_FOLDER_PATH = "../app/excel_data"

bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
router = Router()
dispatcher = Dispatcher()

dispatcher.include_router(router)

@router.message(Command(commands=["start"]))
async def send_welcome(message: Message):
    await message.answer("Привет! Используй команду /getfile, чтобы получить последние файлы Excel.")

@router.message(Command(commands=["getfile"]))
async def send_excel_files(message: Message):
    # Фильтрация файлов по категориям
    order_files = [f for f in os.listdir(EXCEL_FOLDER_PATH) if f.startswith('order_')]
    sale_files = [f for f in os.listdir(EXCEL_FOLDER_PATH) if f.startswith('sale_')]

    # Поиск последнего файла в каждой категории
    if order_files:
        latest_order_file = max(order_files, key=lambda x: os.path.getctime(os.path.join(EXCEL_FOLDER_PATH, x)))
        order_file_path = os.path.join(EXCEL_FOLDER_PATH, latest_order_file)
        order_file = FSInputFile(order_file_path)
        await message.answer_document(document=order_file, caption="Вот последний файл заказов:")

    if sale_files:
        latest_sale_file = max(sale_files, key=lambda x: os.path.getctime(os.path.join(EXCEL_FOLDER_PATH, x)))
        sale_file_path = os.path.join(EXCEL_FOLDER_PATH, latest_sale_file)
        sale_file = FSInputFile(sale_file_path)
        await message.answer_document(document=sale_file, caption="Вот последний файл продаж:")

    if not order_files and not sale_files:
        await message.answer("Нет доступных файлов Excel для заказов или продаж.")

async def main():
    await dispatcher.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
