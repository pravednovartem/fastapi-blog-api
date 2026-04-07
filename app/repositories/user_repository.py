"""Репозиторий для пользователей (auth_user)."""

from app.models import Comment, Post, User
from app.schemas import UserCreate, UserUpdate

from sqlalchemy.orm import Session


class UserRepository:
    """CRUD-операции с таблицей пользователей."""

    def __init__(self, db: Session):
        """Принять сессию SQLAlchemy."""
        self.db = db

    def get_all(self):
        """Вернуть всех пользователей."""
        return self.db.query(User).all()

    def get_by_id(self, user_id: int):
        """Вернуть пользователя по id или None."""
        return self.db.query(User).filter(User.id == user_id).first()

    def create(self, data: UserCreate):
        """Создать пользователя из валидированных данных."""
        obj = User(**data.model_dump())
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def update(self, user_id: int, data: UserUpdate):
        """Обновить поля; вернуть None если не найден."""
        obj = self.get_by_id(user_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete(self, user_id: int):
        """Удалить пользователя и зависимые записи."""
        user = self.get_by_id(user_id)
        if not user:
            return None
        post_ids = [
            r.id
            for r in self.db.query(Post.id).filter(Post.author_id == user_id)
        ]
        if post_ids:
            self.db.query(Comment).filter(
                Comment.post_id.in_(post_ids)
            ).delete(synchronize_session=False)
        self.db.query(Comment).filter(
            Comment.author_id == user_id
        ).delete(synchronize_session=False)
        self.db.query(Post).filter(Post.author_id == user_id).delete(
            synchronize_session=False
        )
        self.db.query(User).filter(User.id == user_id).delete(
            synchronize_session=False
        )
        self.db.commit()
        return user
