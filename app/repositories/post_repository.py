"""Repository for blog posts."""

from app.models import Comment, Post
from app.schemas import PostCreate, PostUpdate

from sqlalchemy.orm import Session


class PostRepository:
    """CRUD-style access to Post rows."""

    def __init__(self, db: Session):
        """Attach SQLAlchemy session."""
        self.db = db

    def get_all(self):
        """Return all posts."""
        return self.db.query(Post).all()

    def get_by_id(self, post_id: int):
        """Return post by id or None."""
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_by_author(self, author_id: int):
        """Return posts by author id."""
        return self.db.query(Post).filter(Post.author_id == author_id).all()

    def get_by_category(self, category_id: int):
        """Return posts in a category."""
        return (
            self.db.query(Post)
            .filter(Post.category_id == category_id)
            .all()
        )

    def create(self, data: PostCreate):
        """Insert a post from validated payload."""
        obj = Post(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, post_id: int, data: PostUpdate):
        """Update fields; return None if missing."""
        obj = self.get_by_id(post_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, post_id: int):
        """Delete post and its comments."""
        obj = self.get_by_id(post_id)
        if not obj:
            return None
        q = self.db.query(Comment).filter(Comment.post_id == post_id)
        for comment in q.all():
            self.db.delete(comment)
        self.db.delete(obj)
        self.db.commit()
        return obj
