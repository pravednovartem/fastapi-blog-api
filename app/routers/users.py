from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import app_http_error, auth_dependency, db_dependency
from app.exceptions import AppError
from app.models import User
from app.schemas import UserCreate, UserOut, UserUpdate
from app.use_cases.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserOut])
async def get_users(
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    return await UserService(db).list()


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await UserService(db).get(user_id)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.post("", response_model=UserOut)
async def create_user(
    data: UserCreate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await UserService(db).create(data)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await UserService(db).update(user_id, data)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        await UserService(db).delete(user_id)
    except AppError as exc:
        raise app_http_error(exc) from exc
    return {"message": "User deleted successfully"}
