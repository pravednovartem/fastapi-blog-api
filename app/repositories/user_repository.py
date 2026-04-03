"""Repository for users (auth_user)."""

from app.models import Comment, Post, User
from app.schemas import UserCreate, UserUpdate

from sqlalchemy.orm import Session


class UserRepository:
    """CRUD-style access to User rows."""

    def __init__(self, db: Session):
        """Attach SQLAlchemy session."""
        self.db = db

    def get_all(self):
        """Return all users."""
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        """Return user by id or None."""
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, data: UserCreate):
        """Insert a user from validated payload."""
        obj = User(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, user_id: int, data: UserUpdate):
        """Update fields; return None if missing."""
        obj = self.get_by_id(user_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, user_id: int):
        """Delete user and dependent comments/posts."""
        user = self.get_by_id(user_id)
        if not user:
            return None
        post_ids = [
            r.id
            for r in self.db.query(Post.id).filter(Post.author_id == user_id)
        ]
        if post_ids:
            self.db.query(Comment).filter(
                Comment.post_id.in_(post_ids)
            ).delete(synchronize_session=False)
        self.db.query(Comment).filter(
            Comment.author_id == user_id
        ).delete(synchronize_session=False)
        self.db.query(Post).filter(Post.author_id == user_id).delete(
            synchronize_session=False
        )
        self.db.query(User).filter(User.id == user_id).delete(
            synchronize_session=False
        )
        self.db.commit()
        return user
