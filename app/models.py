from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "auth_user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=True)


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
    location_id = Column(Integer, ForeignKey("blog_location.id"), nullable=True)
    category_id = Column(Integer, ForeignKey("blog_category.id"), nullable=True)

    author = relationship("User")
    location = relationship("Location")
    category = relationship("Category")


class Comment(Base):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime)

    post_id = Column(Integer, ForeignKey("blog_post.id"), nullable=False)
    author_id = Column(Integer, ForeignKey("auth_user.id"), nullable=False)

    post = relationship("Post")
    author = relationship("User")
