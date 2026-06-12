from app.exceptions import ConflictError, DatabaseError
from app.models import Location, Post
from app.schemas import LocationCreate, LocationUpdate

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class LocationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _commit(self) -> None:
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            raise ConflictError(
                "Нарушение целостности данных локации",
            ) from exc
        except SQLAlchemyError as exc:
            await self.db.rollback()
            raise DatabaseError(
                "Сбой БД при работе с локацией",
            ) from exc

    async def get_all(self):
        result = await self.db.execute(select(Location))
        return list(result.scalars().all())

    async def get_by_id(self, location_id: int):
        result = await self.db.execute(
            select(Location).where(Location.id == location_id),
        )
        return result.scalar_one_or_none()

    async def create(self, data: LocationCreate):
        obj = Location(**data.model_dump())
        self.db.add(obj)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, location_id: int, data: LocationUpdate):
        obj = await self.get_by_id(location_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, location_id: int):
        obj = await self.get_by_id(location_id)
        if not obj:
            return None
        await self.db.execute(
            update(Post)
            .where(Post.location_id == location_id)
            .values(location_id=None),
        )
        await self.db.delete(obj)
        await self._commit()
        return obj
