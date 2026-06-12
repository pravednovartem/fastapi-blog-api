from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError, NotFoundError
from app.repositories.category_repository import CategoryRepository
from app.schemas import CategoryCreate, CategoryUpdate


class CategoryService:
    entity = "Category"

    def __init__(self, db: AsyncSession):
        self.repo = CategoryRepository(db)

    async def list(self):
        return await self.repo.get_all()

    async def get(self, category_id: int):
        obj = await self.repo.get_by_id(category_id)
        if not obj:
            raise NotFoundError(
                "Категория не найдена",
                entity=self.entity,
                id=category_id,
            )
        return obj

    async def create(self, data: CategoryCreate):
        try:
            return await self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    async def update(self, category_id: int, data: CategoryUpdate):
        try:
            obj = await self.repo.update(category_id, data)
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

    async def delete(self, category_id: int):
        try:
            obj = await self.repo.delete(category_id)
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
