"""Repository for post comments."""

from app.models import Comment
from app.schemas import (
    CommentCreate,
    CommentUpdate,
)

from sqlalchemy.orm import Session


class CommentRepository:
    """CRUD-style access to Comment rows."""

    def __init__(self, db: Session):
        """Attach SQLAlchemy session."""
        self.db = db

    def get_all(self):
        """Return all comments."""
        return self.db.query(Comment).all()

    def get_by_id(self, comment_id: int):
        """Return comment by id or None."""
        return (
            self.db.query(Comment)
            .filter(Comment.id == comment_id)
            .first()
        )

    def get_by_post(self, post_id: int):
        """Return comments for a post."""
        return (
            self.db.query(Comment)
            .filter(Comment.post_id == post_id)
            .all()
        )

    def get_by_author(self, author_id: int):
        """Return comments by author id."""
        return (
            self.db.query(Comment)
            .filter(Comment.author_id == author_id)
            .all()
        )

    def create(self, data: CommentCreate):
        """Insert a comment from validated payload."""
        obj = Comment(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, comment_id: int, data: CommentUpdate):
        """Update comment text; return None if missing."""
        obj = self.get_by_id(comment_id)
        if not obj:
            return None
        obj.text = data.text
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, comment_id: int):
        """Delete comment."""
        obj = self.get_by_id(
            comment_id,
        )
        if not obj:
            return None
        self.db.delete(obj)
        self.db.commit()
        return obj
