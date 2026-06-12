from app.exceptions import ConflictError, DatabaseError
from app.models import Comment
from app.schemas import CommentCreate, CommentUpdate

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class CommentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _commit(self) -> None:
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            raise ConflictError(
                "Нарушение целостности данных комментария",
            ) from exc
        except SQLAlchemyError as exc:
            await self.db.rollback()
            raise DatabaseError(
                "Сбой БД при работе с комментарием",
            ) from exc

    async def get_all(self):
        result = await self.db.execute(select(Comment))
        return list(result.scalars().all())

    async def get_by_id(self, comment_id: int):
        result = await self.db.execute(
            select(Comment).where(Comment.id == comment_id),
        )
        return result.scalar_one_or_none()

    async def get_by_post(self, post_id: int):
        result = await self.db.execute(
            select(Comment).where(Comment.post_id == post_id),
        )
        return list(result.scalars().all())

    async def get_by_author(self, author_id: int):
        result = await self.db.execute(
            select(Comment).where(Comment.author_id == author_id),
        )
        return list(result.scalars().all())

    async def create(self, data: CommentCreate):
        obj = Comment(**data.model_dump())
        self.db.add(obj)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, comment_id: int, data: CommentUpdate):
        obj = await self.get_by_id(comment_id)
        if not obj:
            return None
        obj.text = data.text
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def delete(self, comment_id: int):
        obj = await self.get_by_id(comment_id)
        if not obj:
            return None
        await self.db.delete(obj)
        await self._commit()
        return obj
