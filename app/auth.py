"""JWT-аутентификация."""

from datetime import datetime, timedelta, timezone
from typing import Optional

import bcrypt
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt  # type: ignore[import-untyped]
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .config import settings
from .database import get_db
from .exceptions import AppError
from .models import User

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

_token_dep = Depends(oauth2_scheme)
_db_dep = Depends(get_db)


class AuthError(AppError):
    status_code = 401


def _bcrypt_secret(password: str) -> bytes:
    # bcrypt обрезает пароль до 72 байт
    data = password.encode("utf-8")
    return data if len(data) <= 72 else data[:72]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        _bcrypt_secret(password),
        bcrypt.gensalt(),
    ).decode("ascii")


def verify_password(plain: str, hashed: Optional[str]) -> bool:
    if not hashed:
        return False
    try:
        return bcrypt.checkpw(
            _bcrypt_secret(plain),
            hashed.encode("ascii"),
        )
    except (ValueError, TypeError):
        return False


def create_access_token(
    subject: str,
    expires_minutes: Optional[int] = None,
) -> str:
    minutes = expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": now + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise AuthError(
            "Невалидный или просроченный токен",
            reason=str(exc),
        ) from exc


async def get_current_user(
    token: str = _token_dep,
    db: AsyncSession = _db_dep,
) -> User:
    payload = decode_token(token)
    sub = payload.get("sub")
    if not sub:
        raise AuthError("Токен не содержит идентификатор пользователя")
    try:
        user_id = int(sub)
    except (TypeError, ValueError) as exc:
        raise AuthError("Некорректный sub в токене") from exc
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise AuthError("Пользователь из токена не найден", id=user_id)
    return user
