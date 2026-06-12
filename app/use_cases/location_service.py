from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError, NotFoundError
from app.repositories.location_repository import LocationRepository
from app.schemas import LocationCreate, LocationUpdate


class LocationService:
    entity = "Location"

    def __init__(self, db: AsyncSession):
        self.repo = LocationRepository(db)

    async def list(self):
        return await self.repo.get_all()

    async def get(self, location_id: int):
        obj = await self.repo.get_by_id(location_id)
        if not obj:
            raise NotFoundError(
                "Локация не найдена",
                entity=self.entity,
                id=location_id,
            )
        return obj

    async def create(self, data: LocationCreate):
        try:
            return await self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    async def update(self, location_id: int, data: LocationUpdate):
        try:
            obj = await self.repo.update(location_id, data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="update", id=location_id)
            raise
        if not obj:
            raise NotFoundError(
                "Локация не найдена",
                entity=self.entity,
                id=location_id,
            )
        return obj

    async def delete(self, location_id: int):
        try:
            obj = await self.repo.delete(location_id)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="delete", id=location_id)
            raise
        if not obj:
            raise NotFoundError(
                "Локация не найдена",
                entity=self.entity,
                id=location_id,
            )
        return obj
