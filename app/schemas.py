"""Pydantic-схемы для валидации запросов и ответов API."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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


class UserUpdate(BaseModel):
    """Схема обновления пользователя."""

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


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


class CategoryUpdate(BaseModel):
    """Схема обновления категории."""

    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None


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


class LocationUpdate(BaseModel):
    """Схема обновления локации."""

    name: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None


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


class CommentUpdate(BaseModel):
    """Схема обновления комментария."""

    text: str
