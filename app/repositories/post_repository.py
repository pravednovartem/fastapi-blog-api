from datetime import datetime

from app.exceptions import ConflictError, DatabaseError
from app.models import Comment, Post, PostImage
from app.schemas import PostCreate, PostUpdate

from sqlalchemy import delete, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload


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

    def _with_images(self, query):
        return query.options(selectinload(Post.images))

    async def get_all(self):
        query = self._with_images(select(Post))
        result = await self.db.execute(query)
        return list(result.scalars().unique().all())

    async def get_by_id(self, post_id: int):
        query = self._with_images(
            select(Post).where(Post.id == post_id),
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_author(self, author_id: int):
        query = self._with_images(
            select(Post).where(Post.author_id == author_id),
        )
        result = await self.db.execute(query)
        return list(result.scalars().unique().all())

    async def get_by_category(self, category_id: int):
        query = self._with_images(
            select(Post).where(Post.category_id == category_id),
        )
        result = await self.db.execute(query)
        return list(result.scalars().unique().all())

    async def create(self, data: PostCreate):
        obj = Post(**data.model_dump())
        self.db.add(obj)
        await self._commit()
        await self.db.refresh(obj)
        return await self.get_by_id(int(obj.id))

    async def update(self, post_id: int, data: PostUpdate):
        obj = await self.get_by_id(post_id)
        if not obj:
            return None
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(obj, key, value)
        await self._commit()
        return await self.get_by_id(post_id)

    async def add_image(self, post_id: int, image_url: str):
        obj = await self.get_by_id(post_id)
        if not obj:
            return None
        result = await self.db.execute(
            select(func.max(PostImage.sort_order)).where(
                PostImage.post_id == post_id,
            ),
        )
        max_order = result.scalar_one_or_none() or -1
        image = PostImage(
            post_id=post_id,
            image_url=image_url,
            sort_order=max_order + 1,
            created_at=datetime.utcnow(),
        )
        self.db.add(image)
        if not obj.image:
            obj.image = image_url
        await self._commit()
        return await self.get_by_id(post_id)

    async def delete_image(self, post_id: int, image_id: int):
        obj = await self.get_by_id(post_id)
        if not obj:
            return None
        result = await self.db.execute(
            select(PostImage).where(
                PostImage.id == image_id,
                PostImage.post_id == post_id,
            ),
        )
        image = result.scalar_one_or_none()
        if not image:
            return None
        image_url = image.image_url
        await self.db.delete(image)
        await self._commit()
        obj = await self.get_by_id(post_id)
        if obj and obj.image == image_url:
            first = obj.images[0].image_url if obj.images else None
            obj.image = first
            await self._commit()
            obj = await self.get_by_id(post_id)
        return obj, image_url

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
