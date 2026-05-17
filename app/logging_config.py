"""Настройка логирования приложения.

Все логи пишутся в stdout — это поведение по умолчанию ожидаемо
в контейнере (журналирует docker logs / docker compose logs).
"""

import logging
import sys

from .config import settings


_LOG_FORMAT = (
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
_LOG_DATEFMT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    """Сконфигурировать корневой логгер по LOG_LEVEL из .env."""
    level = logging.getLevelName(settings.LOG_LEVEL.upper())
    if not isinstance(level, int):
        level = logging.INFO

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_LOG_DATEFMT))

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    # uvicorn по умолчанию вешает свои хендлеры — пробрасываем их в наш формат.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uv_logger = logging.getLogger(name)
        uv_logger.handlers.clear()
        uv_logger.propagate = True
