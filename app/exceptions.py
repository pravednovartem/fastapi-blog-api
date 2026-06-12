"""Исключения приложения и HTTP-статусы."""


class AppError(Exception):
    status_code = 500

    def __init__(self, message: str, **context):
        super().__init__(message)
        self.message = message
        self.context = context

    def to_dict(self) -> dict:
        return {"message": self.message, **self.context}


class NotFoundError(AppError):
    status_code = 404


class ValidationError(AppError):
    status_code = 422


class ConflictError(AppError):
    status_code = 409


class DatabaseError(AppError):
    status_code = 500
