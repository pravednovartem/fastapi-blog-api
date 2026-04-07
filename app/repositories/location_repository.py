"""Репозиторий для локаций блога."""

from app.models import Location, Post
from app.schemas import LocationCreate, LocationUpdate

from sqlalchemy.orm import Session


class LocationRepository:
    """CRUD-операции с таблицей локаций."""

    def __init__(self, db: Session):
        """Принять сессию SQLAlchemy."""
        self.db = db

    def get_all(self):
        """Вернуть все локации."""
        return self.db.query(Location).all()

    def get_by_id(self, location_id: int):
        """Вернуть локацию по id или None."""
        return (
            self.db.query(Location)
            .filter(Location.id == location_id)
            .first()
        )

    def create(self, data: LocationCreate):
        """Создать локацию из валидированных данных."""
        obj = Location(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, location_id: int, data: LocationUpdate):
        """Обновить поля; вернуть None если не найдена."""
        obj = self.get_by_id(location_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, location_id: int):
        """Удалить локацию; обнулить location_id у постов."""
        obj = self.get_by_id(location_id)
        if not obj:
            return None
        self.db.query(Post).filter(Post.location_id == location_id).update(
            {Post.location_id: None},
            synchronize_session=False,
        )
        self.db.delete(obj)
        self.db.commit()
        return obj
