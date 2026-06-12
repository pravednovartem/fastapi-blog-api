from app.exceptions import ConflictError, DatabaseError
from app.models import Category, Post
from app.schemas import CategoryCreate, CategoryUpdate

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _commit(self) -> None:
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            raise ConflictError(
                "Нарушение целостности данных категории",
            ) from exc
        except SQLAlchemyError as exc:
            await self.db.rollback()
            raise DatabaseError(
                "Сбой БД при работе с категорией",
            ) from exc

    async def get_all(self):
        result = await self.db.execute(select(Category))
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int):
        result = await self.db.execute(
            select(Category).where(Category.id == category_id),
        )
        return result.scalar_one_or_none()

    async def create(self, data: CategoryCreate):
        obj = Category(**data.model_dump())
        self.db.add(obj)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, category_id: int, data: CategoryUpdate):
        obj = await self.get_by_id(category_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, category_id: int):
        obj = await self.get_by_id(category_id)
        if not obj:
            return None
        await self.db.execute(
            update(Post)
            .where(Post.category_id == category_id)
            .values(category_id=None),
        )
        await self.db.delete(obj)
        await self._commit()
        return obj
