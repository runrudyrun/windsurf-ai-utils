"""Module for managing configuration and environment variables."""

import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

# Load environment variables from .env file
load_dotenv()

class ClickHouseSettings(BaseSettings):
    """Settings for ClickHouse connection."""
    host: str = 'localhost'
    port: int = 9000
    user: str = 'default'
    password: SecretStr
    database: str = 'default'

    class Config:
        env_prefix = 'CLICKHOUSE_'

class MiroSettings(BaseSettings):
    """Settings for Miro API."""
    access_token: SecretStr
    board_id: str

    class Config:
        env_prefix = 'MIRO_'

class StripeSettings(BaseSettings):
    """Settings for Stripe API."""
    api_key: SecretStr

    class Config:
        env_prefix = 'STRIPE_'

class SecuritySettings(BaseSettings):
    """Security settings."""
    encryption_key: SecretStr

    class Config:
        env_prefix = ''

class Settings:
    """Main application settings class."""
    def __init__(self):
        self.clickhouse = ClickHouseSettings()
        self.miro = MiroSettings()
        self.stripe = StripeSettings()
        self.security = SecuritySettings()

    @property
    def clickhouse_dsn(self) -> str:
        """Get ClickHouse connection string."""
        return f"clickhouse://{self.clickhouse.user}:{self.clickhouse.password.get_secret_value()}@{self.clickhouse.host}:{self.clickhouse.port}/{self.clickhouse.database}"

# Create global settings instance
settings = Settings()
