from typing import Optional, cast

from sqlalchemy.ext.asyncio import AsyncSession

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


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)

    async def register(self, data: RegisterRequest) -> tuple[User, str]:
        existing = await self.users.get_by_username(data.username)
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
            await self.db.commit()
        except AppError:
            raise
        except Exception as exc:
            await self.db.rollback()
            raise ConflictError(
                "Не удалось зарегистрировать пользователя",
            ) from exc
        await self.db.refresh(user)
        token = create_access_token(subject=str(user.id))
        return user, token

    async def login(self, data: LoginRequest) -> tuple[User, str]:
        user = await self.users.get_by_username(data.username)
        hashed = cast(Optional[str], user.password) if user else None
        if not user or not verify_password(data.password, hashed):
            raise AuthError(
                "Неверный логин или пароль",
                username=data.username,
            )
        token = create_access_token(subject=str(user.id))
        return user, token
