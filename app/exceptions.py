"""Доменные исключения приложения и их HTTP-статусы."""


class AppError(Exception):
    """Базовое исключение приложения."""

    status_code = 500

    def __init__(self, message: str, **context):
        """Сохранить сообщение и произвольный контекст ошибки."""
        super().__init__(message)
        self.message = message
        self.context = context

    def to_dict(self) -> dict:
        """Сериализовать ошибку для ответа API."""
        return {"message": self.message, **self.context}


class NotFoundError(AppError):
    """Сущность не найдена в БД."""

    status_code = 404


class ValidationError(AppError):
    """Ошибка бизнес-валидации (после Pydantic)."""

    status_code = 422


class ConflictError(AppError):
    """Конфликт целостности (уникальность, FK и т.п.)."""

    status_code = 409


class DatabaseError(AppError):
    """Сбой работы с БД, не относящийся к другим категориям."""

    status_code = 500
