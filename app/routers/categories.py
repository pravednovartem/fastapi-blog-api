from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import app_http_error, auth_dependency, db_dependency
from app.exceptions import AppError
from app.models import User
from app.schemas import CategoryCreate, CategoryOut, CategoryUpdate
from app.use_cases.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("", response_model=list[CategoryOut])
async def get_categories(db: AsyncSession = db_dependency):
    return await CategoryService(db).list()


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int, db: AsyncSession = db_dependency):
    try:
        return await CategoryService(db).get(category_id)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.post("", response_model=CategoryOut)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await CategoryService(db).create(data)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.put("/{category_id}", response_model=CategoryOut)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await CategoryService(db).update(category_id, data)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        await CategoryService(db).delete(category_id)
    except AppError as exc:
        raise app_http_error(exc) from exc
    return {"message": "Category deleted successfully"}
