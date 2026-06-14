from datetime import datetime
from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions import DatabaseError
from app.models import RefreshToken

from sqlalchemy.exc import SQLAlchemyError


class RefreshTokenRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(
        self,
        user_id: int,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshToken:
        obj = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
            created_at=datetime.utcnow(),
        )
        self.db.add(obj)
        try:
            await self.db.commit()
        except SQLAlchemyError as exc:
            await self.db.rollback()
            raise DatabaseError(
                "Сбой БД при сохранении refresh-токена",
            ) from exc
        await self.db.refresh(obj)
        return obj

    async def get_by_hash(self, token_hash: str) -> Optional[RefreshToken]:
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash),
        )
        return result.scalar_one_or_none()

    async def delete_by_hash(self, token_hash: str) -> None:
        await self.db.execute(
            delete(RefreshToken).where(RefreshToken.token_hash == token_hash),
        )
        try:
            await self.db.commit()
        except SQLAlchemyError as exc:
            await self.db.rollback()
            raise DatabaseError(
                "Сбой БД при удалении refresh-токена",
            ) from exc
