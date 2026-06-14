from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError, NotFoundError, ValidationError
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas import PostCreate, PostUpdate

MAX_IMAGES_PER_POST = 10


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

    async def add_image(self, post_id: int, image_url: str):
        post = await self.get(post_id)
        if len(post.images) >= MAX_IMAGES_PER_POST:
            raise ValidationError(
                f"Не более {MAX_IMAGES_PER_POST} изображений на пост",
                entity=self.entity,
                field="image",
            )
        try:
            obj = await self.repo.add_image(post_id, image_url)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="add_image", id=post_id)
            raise
        if not obj:
            raise NotFoundError(
                "Публикация не найдена",
                entity=self.entity,
                id=post_id,
            )
        return obj

    async def delete_image(self, post_id: int, image_id: int):
        try:
            result = await self.repo.delete_image(post_id, image_id)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="delete_image", id=post_id)
            raise
        if not result:
            raise NotFoundError(
                "Изображение не найдено",
                entity=self.entity,
                id=image_id,
            )
        obj, _image_url = result
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
