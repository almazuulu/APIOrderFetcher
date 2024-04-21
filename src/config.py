from __future__ import annotations

from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file_path = os.path.join(log_directory, 'app.log')

    # Создание и настройка корневого логгера
    logging.basicConfig(level=logging.INFO)

    # Создание обработчика, который пишет логи в файл
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024000, backupCount=5)
    file_handler.setLevel(logging.INFO)

    # Создание форматтера и добавление его к обработчику
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Получение корневого логгера и добавление обработчика
    logger = logging.getLogger()
    logger.addHandler(file_handler)

    return logger

class APISettings(BaseSettings):
    APP_NAME: str = "API Order fetcher"
    OPENAPI_DESCRIPTION: str = "Сервис для асинхронной загрузки и обработки данных о заказах и продажах"
    ADMIN_EMAIL: str


class DBSettings(BaseSettings):
    DB_ENGINE_POOL_PRE_PING: bool = True
    DB_ENGINE_POOL_RECYCLE: int = -1
    DB_ENGINE_POOL_SIZE: int = 5
    DB_ENGINE_MAX_OVERFLOW: int = 10
    DB_ENGINE_POOL_TIMEOUT: int = 30
    SQL_ENGINE_ECHO: bool = False
    DATABASE_URL: str
    DB_CREDENTIALS: SecretStr

class WBSettings(BaseSettings):
    BEARER_TOKEN: str
    BASE_URL: str

class Settings(APISettings, DBSettings, WBSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")
    DEBUG: bool = False

    # CORS
    CORS_ALLOW_METHODS: list[str] = ["*"]
    CORS_ALLOW_ORIGINS: list[str] = (
        ["*"]
        if DEBUG
        else [
            "http://localhost:8000",
            "http://127.0.0.1:8000",
            "http://0.0.0.0:8000",
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://0.0.0.0:3000",
        ]
    )
    CORS_ALLOW_HEADERS: list[str] = ["*"]

    @property
    def db_url(self) -> str:
        return (
                self.DATABASE_URL % self.DB_CREDENTIALS.get_secret_value()
        )