"""Pydantic-схемы для валидации запросов и ответов API."""

import re
from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel, field_validator

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]+$")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")


# --- Пользователи ---

class UserOut(BaseModel):
    """Схема ответа: пользователь."""

    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        """Настройки Pydantic."""

        from_attributes = True


class UserCreate(BaseModel):
    """Схема создания пользователя."""

    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        """Длина 3..150, только латиница/цифры/подчёркивание."""
        v = v.strip()
        if not 3 <= len(v) <= 150:
            raise ValueError("username должен быть длиной 3..150 символов")
        if not USERNAME_RE.fullmatch(v):
            raise ValueError(
                "username может содержать только A-Z, a-z, 0-9 и _",
            )
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Базовая проверка формата email."""
        if v is None or v == "":
            return v
        if not EMAIL_RE.fullmatch(v):
            raise ValueError("Некорректный формат email")
        return v


class UserUpdate(BaseModel):
    """Схема обновления пользователя."""

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
        """Если задан — те же правила, что и при создании."""
        if v is None:
            return v
        v = v.strip()
        if not 3 <= len(v) <= 150:
            raise ValueError("username должен быть длиной 3..150 символов")
        if not USERNAME_RE.fullmatch(v):
            raise ValueError(
                "username может содержать только A-Z, a-z, 0-9 и _",
            )
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Базовая проверка формата email."""
        if v is None or v == "":
            return v
        if not EMAIL_RE.fullmatch(v):
            raise ValueError("Некорректный формат email")
        return v


# --- Категории ---

class CategoryOut(BaseModel):
    """Схема ответа: категория."""

    id: int
    title: str
    description: str
    slug: str
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        """Настройки Pydantic."""

        from_attributes = True


class CategoryCreate(BaseModel):
    """Схема создания категории."""

    title: str
    description: str
    slug: str
    is_published: Optional[bool] = True
    created_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Не пусто, длина 1..256."""
        v = v.strip()
        if not v:
            raise ValueError("title не может быть пустым")
        if len(v) > 256:
            raise ValueError("title не может быть длиннее 256 символов")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Не пусто."""
        v = v.strip()
        if not v:
            raise ValueError("description не может быть пустым")
        return v

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        """Только a-z, 0-9 и дефис, длина 1..200."""
        v = v.strip()
        if not 1 <= len(v) <= 200:
            raise ValueError("slug должен быть длиной 1..200 символов")
        if not SLUG_RE.fullmatch(v):
            raise ValueError(
                "slug может содержать только a-z, 0-9 и дефис",
            )
        return v


class CategoryUpdate(BaseModel):
    """Схема обновления категории."""

    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
        """Если задан — те же правила, что и при создании."""
        if v is None:
            return v
        v = v.strip()
        if not 1 <= len(v) <= 200:
            raise ValueError("slug должен быть длиной 1..200 символов")
        if not SLUG_RE.fullmatch(v):
            raise ValueError(
                "slug может содержать только a-z, 0-9 и дефис",
            )
        return v


# --- Локации ---

class LocationOut(BaseModel):
    """Схема ответа: локация."""

    id: int
    name: str
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        """Настройки Pydantic."""

        from_attributes = True


class LocationCreate(BaseModel):
    """Схема создания локации."""

    name: str
    is_published: Optional[bool] = True
    created_at: Optional[datetime] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Не пусто, длина 1..256."""
        v = v.strip()
        if not v:
            raise ValueError("name не может быть пустым")
        if len(v) > 256:
            raise ValueError("name не может быть длиннее 256 символов")
        return v


class LocationUpdate(BaseModel):
    """Схема обновления локации."""

    name: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        """Если задано — не пусто и не длиннее 256."""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("name не может быть пустым")
        if len(v) > 256:
            raise ValueError("name не может быть длиннее 256 символов")
        return v


# --- Публикации ---

class PostOut(BaseModel):
    """Схема ответа: публикация."""

    id: int
    title: str
    text: str
    pub_date: datetime
    image: Optional[str] = None
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        """Настройки Pydantic."""

        from_attributes = True


class PostCreate(BaseModel):
    """Схема создания публикации."""

    title: str
    text: str
    pub_date: datetime
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: Optional[bool] = True
    created_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Не пусто, длина 1..256."""
        v = v.strip()
        if not v:
            raise ValueError("title не может быть пустым")
        if len(v) > 256:
            raise ValueError("title не может быть длиннее 256 символов")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Текст публикации не может быть пустым."""
        v = v.strip()
        if not v:
            raise ValueError("text не может быть пустым")
        return v

    @field_validator("pub_date")
    @classmethod
    def validate_pub_date(cls, v: datetime) -> datetime:
        """Запрещаем даты дальше суток в прошлом."""
        now = datetime.now(timezone.utc)
        v_aware = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
        if v_aware < now - timedelta(days=1):
            raise ValueError(
                "pub_date не может быть более чем на сутки в прошлом",
            )
        return v


class PostUpdate(BaseModel):
    """Схема обновления публикации."""

    title: Optional[str] = None
    text: Optional[str] = None
    pub_date: Optional[datetime] = None
    author_id: Optional[int] = None
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Если задан — не пусто и не длиннее 256."""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("title не может быть пустым")
        if len(v) > 256:
            raise ValueError("title не может быть длиннее 256 символов")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: Optional[str]) -> Optional[str]:
        """Если задан — не пусто."""
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("text не может быть пустым")
        return v


# --- Комментарии ---

class CommentOut(BaseModel):
    """Схема ответа: комментарий."""

    id: int
    text: str
    created_at: Optional[datetime] = None
    author_id: int
    post_id: int

    class Config:
        """Настройки Pydantic."""

        from_attributes = True


class CommentCreate(BaseModel):
    """Схема создания комментария."""

    text: str
    post_id: int
    author_id: int
    created_at: Optional[datetime] = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Не пусто и не длиннее 5000 символов."""
        v = v.strip()
        if not v:
            raise ValueError("text не может быть пустым")
        if len(v) > 5000:
            raise ValueError("text не может быть длиннее 5000 символов")
        return v


class CommentUpdate(BaseModel):
    """Схема обновления комментария."""

    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Не пусто и не длиннее 5000 символов."""
        v = v.strip()
        if not v:
            raise ValueError("text не может быть пустым")
        if len(v) > 5000:
            raise ValueError("text не может быть длиннее 5000 символов")
        return v
