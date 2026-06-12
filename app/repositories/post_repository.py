from app.exceptions import ConflictError, DatabaseError
from app.models import Comment, Post
from app.schemas import PostCreate, PostUpdate

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession


class PostRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _commit(self) -> None:
        try:
            await self.db.commit()
        except IntegrityError as exc:
            await self.db.rollback()
            raise ConflictError(
                "Нарушение целостности данных публикации",
            ) from exc
        except SQLAlchemyError as exc:
            await self.db.rollback()
            raise DatabaseError(
                "Сбой БД при работе с публикацией",
            ) from exc

    async def get_all(self):
        result = await self.db.execute(select(Post))
        return list(result.scalars().all())

    async def get_by_id(self, post_id: int):
        result = await self.db.execute(
            select(Post).where(Post.id == post_id),
        )
        return result.scalar_one_or_none()

    async def get_by_author(self, author_id: int):
        result = await self.db.execute(
            select(Post).where(Post.author_id == author_id),
        )
        return list(result.scalars().all())

    async def get_by_category(self, category_id: int):
        result = await self.db.execute(
            select(Post).where(Post.category_id == category_id),
        )
        return list(result.scalars().all())

    async def create(self, data: PostCreate):
        obj = Post(**data.model_dump())
        self.db.add(obj)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def update(self, post_id: int, data: PostUpdate):
        obj = await self.get_by_id(post_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await self._commit()
        await self.db.refresh(obj)
        return obj

    async def set_image(self, post_id: int, image_url: str):
        return await self.update(post_id, PostUpdate(image=image_url))

    async def delete(self, post_id: int):
        obj = await self.get_by_id(post_id)
        if not obj:
            return None
        await self.db.execute(
            delete(Comment).where(Comment.post_id == post_id),
        )
        await self.db.delete(obj)
        await self._commit()
        return obj
