from datetime import datetime, timezone
from typing import Optional, cast

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import (
    AuthError,
    create_access_token,
    generate_refresh_token,
    hash_password,
    hash_refresh_token,
    refresh_token_expires_at,
    verify_password,
)
from app.exceptions import AppError, ConflictError
from app.models import User
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.users = UserRepository(db)
        self.refresh_tokens = RefreshTokenRepository(db)

    async def _issue_tokens(self, user: User) -> tuple[str, str]:
        access = create_access_token(subject=str(user.id))
        raw_refresh = generate_refresh_token()
        await self.refresh_tokens.create(
            user_id=cast(int, user.id),
            token_hash=hash_refresh_token(raw_refresh),
            expires_at=refresh_token_expires_at(),
        )
        return access, raw_refresh

    async def register(
        self,
        data: RegisterRequest,
    ) -> tuple[User, str, str]:
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
        access, refresh = await self._issue_tokens(user)
        return user, access, refresh

    async def login(self, data: LoginRequest) -> tuple[User, str, str]:
        user = await self.users.get_by_username(data.username)
        hashed = cast(Optional[str], user.password) if user else None
        if not user or not verify_password(data.password, hashed):
            raise AuthError(
                "Неверный логин или пароль",
                username=data.username,
            )
        access, refresh = await self._issue_tokens(user)
        return user, access, refresh

    async def refresh(self, raw_refresh: str) -> tuple[str, str]:
        token_hash = hash_refresh_token(raw_refresh)
        stored = await self.refresh_tokens.get_by_hash(token_hash)
        if not stored:
            raise AuthError("Refresh-токен не найден")
        expires_at = stored.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at < datetime.now(timezone.utc):
            await self.refresh_tokens.delete_by_hash(token_hash)
            raise AuthError("Refresh-токен просрочен")
        user = await self.users.get_by_id(cast(int, stored.user_id))
        if not user:
            await self.refresh_tokens.delete_by_hash(token_hash)
            raise AuthError("Пользователь не найден")
        await self.refresh_tokens.delete_by_hash(token_hash)
        access, new_refresh = await self._issue_tokens(user)
        return access, new_refresh

    async def logout(self, raw_refresh: str) -> None:
        token_hash = hash_refresh_token(raw_refresh)
        stored = await self.refresh_tokens.get_by_hash(token_hash)
        if stored:
            await self.refresh_tokens.delete_by_hash(token_hash)
