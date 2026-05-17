"""Движок БД, фабрика сессий и зависимость для FastAPI."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import settings

DATABASE_URL = settings.DATABASE_URL

# connect_args нужны только SQLite (запрет проверки потока).
engine_kwargs: dict = {}
if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, **engine_kwargs)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


def get_db():
    """Создать сессию БД и закрыть после запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
