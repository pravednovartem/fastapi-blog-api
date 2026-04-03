from datetime import datetime
from typing import Optional

from pydantic import BaseModel


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


class UserUpdate(BaseModel):
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


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


class CategoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None


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


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    is_published: Optional[bool] = None
    created_at: Optional[datetime] = None


class PostOut(BaseModel):
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


class CommentUpdate(BaseModel):
    text: str
