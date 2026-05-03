"""Репозиторий для публикаций блога."""

from app.exceptions import ConflictError, DatabaseError
from app.models import Comment, Post
from app.schemas import PostCreate, PostUpdate

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session


class PostRepository:
    """CRUD-операции с таблицей публикаций."""

    def __init__(self, db: Session):
        """Принять сессию SQLAlchemy."""
        self.db = db

    def _commit(self) -> None:
        """Закоммитить транзакцию, преобразовав SQL-ошибки в доменные."""
        try:
            self.db.commit()
        except IntegrityError as exc:
            self.db.rollback()
            raise ConflictError(
                "Нарушение целостности данных публикации",
            ) from exc
        except SQLAlchemyError as exc:
            self.db.rollback()
            raise DatabaseError(
                "Сбой БД при работе с публикацией",
            ) from exc

    def get_all(self):
        """Вернуть все публикации."""
        return self.db.query(Post).all()

    def get_by_id(self, post_id: int):
        """Вернуть публикацию по id или None."""
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_by_author(self, author_id: int):
        """Вернуть публикации по id автора."""
        return self.db.query(Post).filter(Post.author_id == author_id).all()

    def get_by_category(self, category_id: int):
        """Вернуть публикации по категории."""
        return (
            self.db.query(Post)
            .filter(Post.category_id == category_id)
            .all()
        )

    def create(self, data: PostCreate):
        """Создать публикацию из валидированных данных."""
        obj = Post(**data.model_dump())
        self.db.add(obj)
        self._commit()
        self.db.refresh(obj)
        return obj

    def update(self, post_id: int, data: PostUpdate):
        """Обновить поля; вернуть None если не найдена."""
        obj = self.get_by_id(post_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self._commit()
        self.db.refresh(obj)
        return obj

    def delete(self, post_id: int):
        """Удалить публикацию и её комментарии."""
        obj = self.get_by_id(post_id)
        if not obj:
            return None
        q = self.db.query(Comment).filter(Comment.post_id == post_id)
        for comment in q.all():
            self.db.delete(comment)
        self.db.delete(obj)
        self._commit()
        return obj
