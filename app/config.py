"""Настройки приложения на pydantic-settings.

Все параметры читаются из переменных окружения и/или файла .env
в корне проекта. Используется единый экземпляр ``settings``,
который подключается в остальных модулях (БД, auth, логирование).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Конфигурация приложения."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite:///./sqlite.db"

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    LOG_LEVEL: str = "INFO"

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000


settings = Settings()
