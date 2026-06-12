from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import app_http_error, auth_dependency, db_dependency
from app.exceptions import AppError
from app.models import User
from app.schemas import LocationCreate, LocationOut, LocationUpdate
from app.use_cases.location_service import LocationService

router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("", response_model=list[LocationOut])
async def get_locations(db: AsyncSession = db_dependency):
    return await LocationService(db).list()


@router.get("/{location_id}", response_model=LocationOut)
async def get_location(location_id: int, db: AsyncSession = db_dependency):
    try:
        return await LocationService(db).get(location_id)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.post("", response_model=LocationOut)
async def create_location(
    data: LocationCreate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await LocationService(db).create(data)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.put("/{location_id}", response_model=LocationOut)
async def update_location(
    location_id: int,
    data: LocationUpdate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await LocationService(db).update(location_id, data)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        await LocationService(db).delete(location_id)
    except AppError as exc:
        raise app_http_error(exc) from exc
    return {"message": "Location deleted successfully"}
