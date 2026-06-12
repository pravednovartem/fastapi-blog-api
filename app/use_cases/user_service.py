from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import AppError, NotFoundError
from app.repositories.user_repository import UserRepository
from app.schemas import UserCreate, UserUpdate


class UserService:
    entity = "User"

    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def list(self):
        return await self.repo.get_all()

    async def get(self, user_id: int):
        obj = await self.repo.get_by_id(user_id)
        if not obj:
            raise NotFoundError(
                "Пользователь не найден",
                entity=self.entity,
                id=user_id,
            )
        return obj

    async def create(self, data: UserCreate):
        try:
            return await self.repo.create(data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context["operation"] = "create"
            raise

    async def update(self, user_id: int, data: UserUpdate):
        try:
            obj = await self.repo.update(user_id, data)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="update", id=user_id)
            raise
        if not obj:
            raise NotFoundError(
                "Пользователь не найден",
                entity=self.entity,
                id=user_id,
            )
        return obj

    async def delete(self, user_id: int):
        try:
            obj = await self.repo.delete(user_id)
        except AppError as exc:
            exc.context.setdefault("entity", self.entity)
            exc.context.update(operation="delete", id=user_id)
            raise
        if not obj:
            raise NotFoundError(
                "Пользователь не найден",
                entity=self.entity,
                id=user_id,
            )
        return obj
