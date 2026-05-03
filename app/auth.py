"""JWT-аутентификация: хеширование паролей, эмиссия и парсинг токенов."""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt  # type: ignore[import-untyped]

from passlib.context import CryptContext  # type: ignore[import-untyped]

from sqlalchemy.orm import Session

from .database import get_db
from .exceptions import AppError
from .models import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"),
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

_token_dep = Depends(oauth2_scheme)
_db_dep = Depends(get_db)


class AuthError(AppError):
    """Ошибка аутентификации/авторизации."""

    status_code = 401


def hash_password(password: str) -> str:
    """Сгенерировать bcrypt-хеш пароля."""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: Optional[str]) -> bool:
    """Сверить пароль с хешем (False если хеша нет)."""
    if not hashed:
        return False
    return pwd_context.verify(plain, hashed)


def create_access_token(
    subject: str,
    expires_minutes: Optional[int] = None,
) -> str:
    """Эмитировать JWT с полями sub, iat, exp."""
    minutes = expires_minutes or ACCESS_TOKEN_EXPIRE_MINUTES
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(subject),
        "iat": now,
        "exp": now + timedelta(minutes=minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Распарсить JWT, поднять AuthError при ошибке."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as exc:
        raise AuthError(
            "Невалидный или просроченный токен",
            reason=str(exc),
        ) from exc


def get_current_user(
    token: str = _token_dep,
    db: Session = _db_dep,
) -> User:
    """FastAPI-зависимость: вернуть текущего пользователя по JWT."""
    payload = decode_token(token)
    sub = payload.get("sub")
    if not sub:
        raise AuthError("Токен не содержит идентификатор пользователя")
    try:
        user_id = int(sub)
    except (TypeError, ValueError) as exc:
        raise AuthError("Некорректный sub в токене") from exc
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise AuthError("Пользователь из токена не найден", id=user_id)
    return user
