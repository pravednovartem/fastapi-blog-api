"""Репозиторий для комментариев."""

from app.models import Comment
from app.schemas import (
    CommentCreate,
    CommentUpdate,
)

from sqlalchemy.orm import Session


class CommentRepository:
    """CRUD-операции с таблицей комментариев."""

    def __init__(self, db: Session):
        """Принять сессию SQLAlchemy."""
        self.db = db

    def get_all(self):
        """Вернуть все комментарии."""
        return self.db.query(Comment).all()

    def get_by_id(self, comment_id: int):
        """Вернуть комментарий по id или None."""
        return (
            self.db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

    def get_by_post(self, post_id: int):
        """Вернуть комментарии к публикации."""
        return (
            self.db.query(Comment)
            .filter(Comment.post_id == post_id)
            .all()
        )

    def get_by_author(self, author_id: int):
        """Вернуть комментарии по id автора."""
        return (
            self.db.query(Comment)
            .filter(Comment.author_id == author_id)
            .all()
        )

    def create(self, data: CommentCreate):
        """Создать комментарий из валидированных данных."""
        obj = Comment(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, comment_id: int, data: CommentUpdate):
        """Обновить текст; вернуть None если не найден."""
        obj = self.get_by_id(comment_id)
        if not obj:
            return None
        obj.text = data.text
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, comment_id: int):
        """Удалить комментарий."""
        obj = self.get_by_id(
            comment_id,
        )
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return obj
