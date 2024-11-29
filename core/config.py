"""Модуль для управления конфигурацией и переменными окружения."""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseSettings, SecretStr

# Загружаем переменные окружения из файла .env
load_dotenv()

class ClickHouseSettings(BaseSettings):
    """Настройки подключения к ClickHouse."""
    host: str = 'localhost'
    port: int = 9000
    user: str = 'default'
    password: SecretStr
    database: str = 'default'

    class Config:
        env_prefix = 'CLICKHOUSE_'

class MiroSettings(BaseSettings):
    """Настройки для работы с Miro API."""
    access_token: SecretStr
    board_id: str

    class Config:
        env_prefix = 'MIRO_'

class SecuritySettings(BaseSettings):
    """Настройки безопасности."""
    encryption_key: SecretStr

    class Config:
        env_prefix = ''

class Settings:
    """Основной класс настроек приложения."""
    def __init__(self):
        self.clickhouse = ClickHouseSettings()
        self.miro = MiroSettings()
        self.security = SecuritySettings()

    @property
    def clickhouse_dsn(self) -> str:
        """Получить строку подключения к ClickHouse."""
        return f"clickhouse://{self.clickhouse.user}:{self.clickhouse.password.get_secret_value()}@{self.clickhouse.host}:{self.clickhouse.port}/{self.clickhouse.database}"

# Создаем глобальный экземпляр настроек
settings = Settings()
