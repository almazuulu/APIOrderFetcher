from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler

from colorama import Fore
from colorama import init
from colorama import Style


init(autoreset=True)


class CustomFormatter(logging.Formatter):
    """Кастомный форматтер, добавляющий цвета в лог-сообщения."""

    FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Определяем цвета для разных уровней
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        color = self.COLORS.get(record.levelno, Fore.GREEN)  # По умолчанию зелёный
        formatter = logging.Formatter(
            color + self.FORMAT + Style.RESET_ALL,
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        return formatter.format(record)


def setup_logging():
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, "app.log")

    # Настройка формата логирования
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)

    # Создание и настройка корневого логгера
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Создание обработчика, который пишет логи в файл
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024000, backupCount=5)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Создание обработчика для вывода в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)

    return logger
