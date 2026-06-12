from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError, NotFoundError, ValidationError
from app.repositories.comment_repository import CommentRepository
from app.repositories.post_repository import PostRepository
from app.repositories.user_repository import UserRepository
from app.schemas import CommentCreate, CommentUpdate


class CommentService:
    entity = "Comment"

    def __init__(self, db: AsyncSession):
        self.repo = CommentRepository(db)
        self.posts = PostRepository(db)
        self.users = UserRepository(db)

    async def list(self):
        return await self.repo.get_all()

    async def get(self, comment_id: int):
        obj = await self.repo.get_by_id(comment_id)
        if not obj:
            raise NotFoundError(
                "Комментарий не найден",
                entity=self.entity,
                id=comment_id,
            )
        return obj

    async def create(self, data: CommentCreate):
        if not await self.users.get_by_id(data.author_id):
            raise ValidationError(
                "Указанный автор не существует",
                entity=self.entity,
                field="author_id",
                value=data.author_id,
            )
        if not await self.posts.get_by_id(data.post_id):
            raise ValidationError(
                "Указанная публикация не существует",
                entity=self.entity,
                field="post_id",
                value=data.post_id,
            )
        try:
            return await self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    async def update(self, comment_id: int, data: CommentUpdate):
        try:
            obj = await self.repo.update(comment_id, data)
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

    async def delete(self, comment_id: int):
        try:
            obj = await self.repo.delete(comment_id)
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
