"""ORM-модели блога (совместимы со схемой Django)."""

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    """Пользователь (таблица auth_user)."""

    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True)


class Category(Base):
    """Категория блога."""

    __tablename__ = "blog_category"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean)
    created_at = Column(DateTime)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String, unique=True, nullable=False)


class Location(Base):
    """Локация блога."""

    __tablename__ = "blog_location"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean)
    created_at = Column(DateTime)
    name = Column(String(256), nullable=False)


class Post(Base):
    """Публикация блога."""

    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean)
    created_at = Column(DateTime)
    title = Column(String(256), nullable=False)
    text = Column(Text, nullable=False)
    pub_date = Column(DateTime, nullable=False)
    image = Column(String, nullable=True)

    author_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    location_id = Column(
        Integer,
        ForeignKey("blog_location.id"),
        nullable=True,
    )
    category_id = Column(
        Integer,
        ForeignKey("blog_category.id"),
        nullable=True,
    )

    author = relationship("User")
    location = relationship("Location")
    category = relationship("Category")


class Comment(Base):
    """Комментарий к публикации."""

    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime)

    post_id = Column(Integer, ForeignKey("blog_post.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)

    post = relationship("Post")
    author = relationship("User")
