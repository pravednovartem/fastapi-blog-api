"""Use-cases для публикаций."""

from app.exceptions import AppError, NotFoundError, ValidationError
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas import PostCreate, PostUpdate

from sqlalchemy.orm import Session


class PostService:
    """Бизнес-операции над публикациями с обогащением ошибок."""

    entity = "Post"

    def __init__(self, db: Session):
        """Создать необходимые репозитории на базе сессии."""
        self.repo = PostRepository(db)
        self.users = UserRepository(db)

    def list(self):
        """Вернуть все публикации."""
        return self.repo.get_all()

    def get(self, post_id: int):
        """Вернуть публикацию по id или поднять NotFoundError."""
        obj = self.repo.get_by_id(post_id)
        if not obj:
            raise NotFoundError(
                "Публикация не найдена",
                entity=self.entity,
                id=post_id,
            )
        return obj

    def create(self, data: PostCreate):
        """Создать публикацию, проверив существование автора."""
        if not self.users.get_by_id(data.author_id):
            raise ValidationError(
                "Указанный автор не существует",
                entity=self.entity,
                field="author_id",
                value=data.author_id,
            )
        try:
            return self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    def update(self, post_id: int, data: PostUpdate):
        """Обновить публикацию по id."""
        try:
            obj = self.repo.update(post_id, data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="update", id=post_id)
            raise
        if not obj:
            raise NotFoundError(
                "Публикация не найдена",
                entity=self.entity,
                id=post_id,
            )
        return obj

    def delete(self, post_id: int):
        """Удалить публикацию по id."""
        try:
            obj = self.repo.delete(post_id)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="delete", id=post_id)
            raise
        if not obj:
            raise NotFoundError(
                "Публикация не найдена",
                entity=self.entity,
                id=post_id,
            )
        return obj
