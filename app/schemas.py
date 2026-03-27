from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PostBase(BaseModel):
    title: str
    text: str
    pub_date: datetime
    image: Optional[str] = None
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    is_published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class PostOut(PostBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    text: str
    author_id: int
    post_id: int


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    text: str


class CommentOut(CommentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True