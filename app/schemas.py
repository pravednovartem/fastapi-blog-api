"""Pydantic-схемы запросов и ответов."""

import re
from datetime import datetime, timedelta, timezone
from typing import Optional

from pydantic import BaseModel, field_validator

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_]+$")
SLUG_RE = re.compile(r"^[a-z0-9-]+$")


def _to_naive_utc(value: Optional[datetime]) -> Optional[datetime]:
    # PostgreSQL: timestamp without time zone
    if value is None:
        return None
    if value.tzinfo is not None:
        return value.astimezone(timezone.utc).replace(tzinfo=None)
    return value


class RegisterRequest(BaseModel):

    username: str
    password: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        v = v.strip()
        if not 3 <= len(v) <= 150:
            raise ValueError("username должен быть длиной 3..150 символов")
        if not USERNAME_RE.fullmatch(v):
            raise ValueError(
                "username может содержать только A-Z, a-z, 0-9 и _",
            )
        return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("password должен быть не короче 8 символов")
        if len(v) > 128:
            raise ValueError("password не может быть длиннее 128 символов")
        if not any(c.isalpha() for c in v):
            raise ValueError("password должен содержать хотя бы одну букву")
        if not any(c.isdigit() for c in v):
            raise ValueError("password должен содержать хотя бы одну цифру")
        return v

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v is None or v == "":
            return v
        if not EMAIL_RE.fullmatch(v):
            raise ValueError("Некорректный формат email")
        return v


class LoginRequest(BaseModel):

    username: str
    password: str


class TokenResponse(BaseModel):

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):

    refresh_token: str


class UserOut(BaseModel):

    id: int
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):

    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
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
        if v is None or v == "":
            return v
        if not EMAIL_RE.fullmatch(v):
            raise ValueError("Некорректный формат email")
        return v


class UserUpdate(BaseModel):

    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: Optional[str]) -> Optional[str]:
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
        if v is None or v == "":
            return v
        if not EMAIL_RE.fullmatch(v):
            raise ValueError("Некорректный формат email")
        return v


class CategoryOut(BaseModel):

    id: int
    title: str
    description: str
    slug: str
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):

    title: str
    description: str
    slug: str
    is_published: Optional[bool] = True
    created_at: Optional[datetime] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("title не может быть пустым")
        if len(v) > 256:
            raise ValueError("title не может быть длиннее 256 символов")
        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("description не может быть пустым")
        return v

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: str) -> str:
        v = v.strip()
        if not 1 <= len(v) <= 200:
            raise ValueError("slug должен быть длиной 1..200 символов")
        if not SLUG_RE.fullmatch(v):
            raise ValueError(
                "slug может содержать только a-z, 0-9 и дефис",
            )
        return v

    @field_validator("created_at")
    @classmethod
    def normalize_created_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _to_naive_utc(v)


class CategoryUpdate(BaseModel):

    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    @field_validator("slug")
    @classmethod
    def validate_slug(cls, v: Optional[str]) -> Optional[str]:
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

    @field_validator("created_at")
    @classmethod
    def normalize_created_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _to_naive_utc(v)


class LocationOut(BaseModel):

    id: int
    name: str
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LocationCreate(BaseModel):

    name: str
    is_published: Optional[bool] = True
    created_at: Optional[datetime] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name не может быть пустым")
        if len(v) > 256:
            raise ValueError("name не может быть длиннее 256 символов")
        return v

    @field_validator("created_at")
    @classmethod
    def normalize_created_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _to_naive_utc(v)


class LocationUpdate(BaseModel):

    name: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("name не может быть пустым")
        if len(v) > 256:
            raise ValueError("name не может быть длиннее 256 символов")
        return v

    @field_validator("created_at")
    @classmethod
    def normalize_created_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _to_naive_utc(v)


class PostImageOut(BaseModel):

    id: int
    image_url: str
    sort_order: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostOut(BaseModel):

    id: int
    title: str
    text: str
    pub_date: datetime
    image: Optional[str] = None
    images: list[PostImageOut] = []
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostCreate(BaseModel):

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
        v = v.strip()
        if not v:
            raise ValueError("title не может быть пустым")
        if len(v) > 256:
            raise ValueError("title не может быть длиннее 256 символов")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("text не может быть пустым")
        return v

    @field_validator("pub_date")
    @classmethod
    def validate_pub_date(cls, v: datetime) -> datetime:
        now = datetime.now(timezone.utc)
        v_aware = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
        if v_aware < now - timedelta(days=1):
            raise ValueError(
                "pub_date не может быть более чем на сутки в прошлом",
            )
        return _to_naive_utc(v_aware)

    @field_validator("created_at")
    @classmethod
    def normalize_created_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _to_naive_utc(v)


class PostUpdate(BaseModel):

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
        if v is None:
            return v
        v = v.strip()
        if not v:
            raise ValueError("text не может быть пустым")
        return v

    @field_validator("pub_date")
    @classmethod
    def validate_pub_date(cls, v: Optional[datetime]) -> Optional[datetime]:
        if v is None:
            return v
        now = datetime.now(timezone.utc)
        v_aware = v if v.tzinfo else v.replace(tzinfo=timezone.utc)
        if v_aware < now - timedelta(days=1):
            raise ValueError(
                "pub_date не может быть более чем на сутки в прошлом",
            )
        return _to_naive_utc(v_aware)

    @field_validator("created_at")
    @classmethod
    def normalize_created_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _to_naive_utc(v)


class CommentOut(BaseModel):

    id: int
    text: str
    created_at: Optional[datetime] = None
    author_id: int
    post_id: int

    class Config:
        from_attributes = True


class CommentCreate(BaseModel):

    text: str
    post_id: int
    author_id: int
    created_at: Optional[datetime] = None

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("text не может быть пустым")
        if len(v) > 5000:
            raise ValueError("text не может быть длиннее 5000 символов")
        return v

    @field_validator("created_at")
    @classmethod
    def normalize_created_at(cls, v: Optional[datetime]) -> Optional[datetime]:
        return _to_naive_utc(v)


class CommentUpdate(BaseModel):

    text: str

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("text не может быть пустым")
        if len(v) > 5000:
            raise ValueError("text не может быть длиннее 5000 символов")
        return v
