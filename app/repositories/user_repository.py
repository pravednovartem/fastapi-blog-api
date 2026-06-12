from app.exceptions import ConflictError, DatabaseError
from app.models import Comment, Post, User
from app.schemas import UserCreate, UserUpdate

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _commit(self) -> None:
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            raise ConflictError(
                "Нарушение целостности данных пользователя",
            ) from exc
        except SQLAlchemyError as exc:
            await self.db.rollback()
            raise DatabaseError(
                "Сбой БД при работе с пользователем",
            ) from exc

    async def get_all(self):
        result = await self.db.execute(select(User))
        return list(result.scalars().all())

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(User).where(User.id == user_id),
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str):
        result = await self.db.execute(
            select(User).where(User.username == username),
        )
        return result.scalar_one_or_none()

    async def create(self, data: UserCreate):
        obj = User(**data.model_dump())
        self.db.add(obj)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, user_id: int, data: UserUpdate):
        obj = await self.get_by_id(user_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, user_id: int):
        user = await self.get_by_id(user_id)
        if not user:
            return None
        result = await self.db.execute(
            select(Post.id).where(Post.author_id == user_id),
        )
        post_ids = list(result.scalars().all())
        if post_ids:
            await self.db.execute(
                delete(Comment).where(Comment.post_id.in_(post_ids)),
            )
        await self.db.execute(
            delete(Comment).where(Comment.author_id == user_id),
        )
        await self.db.execute(
            delete(Post).where(Post.author_id == user_id),
        )
        await self.db.delete(user)
        await self._commit()
        return user
