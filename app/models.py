"""ORM-модели блога."""

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
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    password = Column(String, nullable=True)

    refresh_tokens = relationship(
        "RefreshToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )


class RefreshToken(Base):
    __tablename__ = "auth_refresh_token"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)
    token_hash = Column(String, nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="refresh_tokens")


class Category(Base):
    __tablename__ = "blog_category"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean)
    created_at = Column(DateTime)
    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=False)
    slug = Column(String, unique=True, nullable=False)


class Location(Base):
    __tablename__ = "blog_location"

    id = Column(Integer, primary_key=True, index=True)
    is_published = Column(Boolean)
    created_at = Column(DateTime)
    name = Column(String(256), nullable=False)


class Post(Base):
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
    images = relationship(
        "PostImage",
        back_populates="post",
        cascade="all, delete-orphan",
        order_by="PostImage.sort_order",
    )


class PostImage(Base):
    __tablename__ = "blog_post_image"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("blog_post.id"), nullable=False)
    image_url = Column(String, nullable=False)
    sort_order = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=True)

    post = relationship("Post", back_populates="images")


class Comment(Base):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime)

    post_id = Column(Integer, ForeignKey("blog_post.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)

    post = relationship("Post")
    author = relationship("User")
