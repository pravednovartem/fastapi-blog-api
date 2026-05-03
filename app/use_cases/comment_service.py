"""Use-cases для комментариев."""

from app.exceptions import AppError, NotFoundError, ValidationError
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas import CommentCreate, CommentUpdate

from sqlalchemy.orm import Session


class CommentService:
    """Бизнес-операции над комментариями с обогащением ошибок."""

    entity = "Comment"

    def __init__(self, db: Session):
        """Создать необходимые репозитории на базе сессии."""
        self.repo = CommentRepository(db)
        self.posts = PostRepository(db)
        self.users = UserRepository(db)

    def list(self):
        """Вернуть все комментарии."""
        return self.repo.get_all()

    def get(self, comment_id: int):
        """Вернуть комментарий по id или поднять NotFoundError."""
        obj = self.repo.get_by_id(comment_id)
        if not obj:
            raise NotFoundError(
                "Комментарий не найден",
                entity=self.entity,
                id=comment_id,
            )
        return obj

    def create(self, data: CommentCreate):
        """Создать комментарий, проверив автора и публикацию."""
        if not self.users.get_by_id(data.author_id):
            raise ValidationError(
                "Указанный автор не существует",
                entity=self.entity,
                field="author_id",
                value=data.author_id,
            )
        if not self.posts.get_by_id(data.post_id):
            raise ValidationError(
                "Указанная публикация не существует",
                entity=self.entity,
                field="post_id",
                value=data.post_id,
            )
        try:
            return self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    def update(self, comment_id: int, data: CommentUpdate):
        """Обновить комментарий по id."""
        try:
            obj = self.repo.update(comment_id, data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="update", id=comment_id)
            raise
        if not obj:
            raise NotFoundError(
                "Комментарий не найден",
                entity=self.entity,
                id=comment_id,
            )
        return obj

    def delete(self, comment_id: int):
        """Удалить комментарий по id."""
        try:
            obj = self.repo.delete(comment_id)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="delete", id=comment_id)
            raise
        if not obj:
            raise NotFoundError(
                "Комментарий не найден",
                entity=self.entity,
                id=comment_id,
            )
        return obj
