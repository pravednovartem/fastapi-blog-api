"""Репозиторий для категорий блога."""

from app.models import Category, Post
from app.schemas import CategoryCreate, CategoryUpdate

from sqlalchemy.orm import Session


class CategoryRepository:
    """CRUD-операции с таблицей категорий."""

    def __init__(self, db: Session):
        """Принять сессию SQLAlchemy."""
        self.db = db

    def get_all(self):
        """Вернуть все категории."""
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int):
        """Вернуть категорию по id или None."""
        return (
            self.db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    def create(self, data: CategoryCreate):
        """Создать категорию из валидированных данных."""
        obj = Category(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, category_id: int, data: CategoryUpdate):
        """Обновить поля; вернуть None если не найдена."""
        obj = self.get_by_id(category_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, category_id: int):
        """Удалить категорию; обнулить category_id у постов."""
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
