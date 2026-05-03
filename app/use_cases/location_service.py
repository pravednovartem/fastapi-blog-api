"""Use-cases для локаций."""

from app.exceptions import AppError, NotFoundError
from app.repositories.location_repository import LocationRepository
from app.schemas import LocationCreate, LocationUpdate

from sqlalchemy.orm import Session


class LocationService:
    """Бизнес-операции над локациями с обогащением ошибок."""

    entity = "Location"

    def __init__(self, db: Session):
        """Создать репозиторий на базе сессии."""
        self.repo = LocationRepository(db)

    def list(self):
        """Вернуть все локации."""
        return self.repo.get_all()

    def get(self, location_id: int):
        """Вернуть локацию по id или поднять NotFoundError."""
        obj = self.repo.get_by_id(location_id)
        if not obj:
            raise NotFoundError(
                "Локация не найдена",
                entity=self.entity,
                id=location_id,
            )
        return obj

    def create(self, data: LocationCreate):
        """Создать локацию, обогащая ошибки контекстом."""
        try:
            return self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    def update(self, location_id: int, data: LocationUpdate):
        """Обновить локацию по id."""
        try:
            obj = self.repo.update(location_id, data)
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

    def delete(self, location_id: int):
        """Удалить локацию по id."""
        try:
            obj = self.repo.delete(location_id)
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
