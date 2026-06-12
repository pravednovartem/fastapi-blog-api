"""Настройки приложения (.env)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


def to_async_database_url(url: str) -> str:
    """DSN для FastAPI (asyncpg / aiosqlite)."""
    if url.startswith("sqlite://"):
        return url.replace("sqlite://", "sqlite+aiosqlite://", 1)
    if url.startswith("postgresql+psycopg2://"):
        return url.replace(
            "postgresql+psycopg2://",
            "postgresql+asyncpg://",
            1,
        )
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    return url


def to_sync_database_url(url: str) -> str:
    """DSN для Alembic и entrypoint (psycopg2)."""
    if url.startswith("sqlite+aiosqlite://"):
        return url.replace("sqlite+aiosqlite://", "sqlite://", 1)
    if url.startswith("postgresql+asyncpg://"):
        return url.replace(
            "postgresql+asyncpg://",
            "postgresql+psycopg2://",
            1,
        )
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite+aiosqlite:///./sqlite.db"

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    LOG_LEVEL: str = "INFO"

    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000

    UPLOAD_DIR: str = "uploads"

    @property
    def async_database_url(self) -> str:
        return to_async_database_url(self.DATABASE_URL)

    @property
    def sync_database_url(self) -> str:
        return to_sync_database_url(self.DATABASE_URL)


settings = Settings()
