"""Use-cases для категорий."""

from app.exceptions import AppError, NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.schemas import CategoryCreate, CategoryUpdate

from sqlalchemy.orm import Session


class CategoryService:
    """Бизнес-операции над категориями с обогащением ошибок."""

    entity = "Category"

    def __init__(self, db: Session):
        """Создать репозиторий на базе сессии."""
        self.repo = CategoryRepository(db)

    def list(self):
        """Вернуть все категории."""
        return self.repo.get_all()

    def get(self, category_id: int):
        """Вернуть категорию по id или поднять NotFoundError."""
        obj = self.repo.get_by_id(category_id)
        if not obj:
            raise NotFoundError(
                "Категория не найдена",
                entity=self.entity,
                id=category_id,
            )
        return obj

    def create(self, data: CategoryCreate):
        """Создать категорию, обогащая ошибки контекстом."""
        try:
            return self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    def update(self, category_id: int, data: CategoryUpdate):
        """Обновить категорию по id."""
        try:
            obj = self.repo.update(category_id, data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="update", id=category_id)
            raise
        if not obj:
            raise NotFoundError(
                "Категория не найдена",
                entity=self.entity,
                id=category_id,
            )
        return obj

    def delete(self, category_id: int):
        """Удалить категорию по id."""
        try:
            obj = self.repo.delete(category_id)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="delete", id=category_id)
            raise
        if not obj:
            raise NotFoundError(
                "Категория не найдена",
                entity=self.entity,
                id=category_id,
            )
        return obj
