from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CategoryOut(BaseModel):
    id: int
    title: str
    description: str
    slug: str
    is_published: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class LocationOut(BaseModel):
    id: int
    name: str
    is_published: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    id: int
    title: str
    text: str
    pub_date: datetime
    image: Optional[str] = None
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    is_published: bool
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CommentOut(BaseModel):
    id: int
    text: str
    created_at: Optional[datetime] = None
    author_id: int
    post_id: int

    class Config:
        from_attributes = True
