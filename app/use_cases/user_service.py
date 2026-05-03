"""Use-cases для пользователей."""

from app.exceptions import AppError, NotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate

from sqlalchemy.orm import Session


class UserService:
    """Бизнес-операции над пользователями с обогащением ошибок."""

    entity = "User"

    def __init__(self, db: Session):
        """Создать репозиторий на базе сессии."""
        self.repo = UserRepository(db)

    def list(self):
        """Вернуть всех пользователей."""
        return self.repo.get_all()

    def get(self, user_id: int):
        """Вернуть пользователя по id или поднять NotFoundError."""
        obj = self.repo.get_by_id(user_id)
        if not obj:
            raise NotFoundError(
                "Пользователь не найден",
                entity=self.entity,
                id=user_id,
            )
        return obj

    def create(self, data: UserCreate):
        """Создать пользователя, обогащая ошибки контекстом."""
        try:
            return self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    def update(self, user_id: int, data: UserUpdate):
        """Обновить пользователя по id."""
        try:
            obj = self.repo.update(user_id, data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="update", id=user_id)
            raise
        if not obj:
            raise NotFoundError(
                "Пользователь не найден",
                entity=self.entity,
                id=user_id,
            )
        return obj

    def delete(self, user_id: int):
        """Удалить пользователя по id."""
        try:
            obj = self.repo.delete(user_id)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="delete", id=user_id)
            raise
        if not obj:
            raise NotFoundError(
                "Пользователь не найден",
                entity=self.entity,
                id=user_id,
            )
        return obj
