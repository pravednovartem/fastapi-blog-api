from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError, NotFoundError, ValidationError
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas import PostCreate, PostUpdate


class PostService:
    entity = "Post"

    def __init__(self, db: AsyncSession):
        self.repo = PostRepository(db)
        self.users = UserRepository(db)

    async def list(self):
        return await self.repo.get_all()

    async def get(self, post_id: int):
        obj = await self.repo.get_by_id(post_id)
        if not obj:
            raise NotFoundError(
                "Публикация не найдена",
                entity=self.entity,
                id=post_id,
            )
        return obj

    async def create(self, data: PostCreate):
        if not await self.users.get_by_id(data.author_id):
            raise ValidationError(
                "Указанный автор не существует",
                entity=self.entity,
                field="author_id",
                value=data.author_id,
            )
        try:
            return await self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    async def update(self, post_id: int, data: PostUpdate):
        try:
            obj = await self.repo.update(post_id, data)
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

    async def attach_image(self, post_id: int, image_url: str):
        try:
            obj = await self.repo.set_image(post_id, image_url)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="attach_image", id=post_id)
            raise
        if not obj:
            raise NotFoundError(
                "Публикация не найдена",
                entity=self.entity,
                id=post_id,
            )
        return obj

    async def delete(self, post_id: int):
        try:
            obj = await self.repo.delete(post_id)
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
