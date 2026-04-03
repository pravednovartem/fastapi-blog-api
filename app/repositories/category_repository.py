"""Repository for blog categories."""

from app.models import Category, Post
from app.schemas import CategoryCreate, CategoryUpdate

from sqlalchemy.orm import Session


class CategoryRepository:
    """CRUD-style access to Category rows."""

    def __init__(self, db: Session):
        """Attach SQLAlchemy session."""
        self.db = db

    def get_all(self):
        """Return all categories."""
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int):
        """Return category by id or None."""
        return (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def create(self, data: CategoryCreate):
        """Insert a category from validated payload."""
        obj = Category(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, category_id: int, data: CategoryUpdate):
        """Update fields; return None if missing."""
        obj = self.get_by_id(category_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, category_id: int):
        """Delete category; null post.category_id first."""
        obj = self.get_by_id(category_id)
        if not obj:
            return None
        self.db.query(Post).filter(Post.category_id == category_id).update(
            {Post.category_id: None},
            synchronize_session=False,
        )
        self.db.delete(obj)
        self.db.commit()
        return obj
