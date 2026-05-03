"""Use-cases аутентификации: регистрация и вход."""

from typing import Optional, cast

from app.auth import (
    AuthError,
    create_access_token,
    hash_password,
    verify_password,
)
from app.exceptions import AppError, ConflictError
from app.models import User
from app.repositories.user_repository import UserRepository
from app.schemas import LoginRequest, RegisterRequest

from sqlalchemy.orm import Session


class AuthService:
    """Регистрация и вход с эмиссией JWT."""

    def __init__(self, db: Session):
        """Сохранить сессию и репозиторий пользователей."""
        self.db = db
        self.users = UserRepository(db)

    def register(self, data: RegisterRequest) -> tuple[User, str]:
        """Создать пользователя с хешем пароля и вернуть токен."""
        existing = (
            self.db.query(User)
            .filter(User.username == data.username)
            .first()
        )
        if existing:
            raise ConflictError(
                "Пользователь с таким username уже существует",
                entity="User",
                field="username",
            )
        user = User(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            password=hash_password(data.password),
        )
        self.db.add(user)
        try:
            self.db.commit()
        except AppError:
            raise
        except Exception as exc:
            self.db.rollback()
            raise ConflictError(
                "Не удалось зарегистрировать пользователя",
            ) from exc
        self.db.refresh(user)
        token = create_access_token(subject=str(user.id))
        return user, token

    def login(self, data: LoginRequest) -> tuple[User, str]:
        """Проверить пароль и выдать JWT."""
        user = (
            self.db.query(User)
            .filter(User.username == data.username)
            .first()
        )
        hashed = cast(Optional[str], user.password) if user else None
        if not user or not verify_password(data.password, hashed):
            raise AuthError(
                "Неверный логин или пароль",
                username=data.username,
            )
        token = create_access_token(subject=str(user.id))
        return user, token
