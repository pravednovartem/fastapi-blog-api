from typing import cast

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import app_http_error, auth_dependency, db_dependency
from app.exceptions import AppError
from app.models import User
from app.schemas import CommentCreate, CommentOut, CommentUpdate
from app.use_cases.comment_service import CommentService

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("", response_model=list[CommentOut])
async def get_comments(db: AsyncSession = db_dependency):
    return await CommentService(db).list()


@router.get("/{comment_id}", response_model=CommentOut)
async def get_comment(comment_id: int, db: AsyncSession = db_dependency):
    try:
        return await CommentService(db).get(comment_id)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.post("", response_model=CommentOut)
async def create_comment(
    comment: CommentCreate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        comment.author_id = cast(int, current_user.id)
        return await CommentService(db).create(comment)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.put("/{comment_id}", response_model=CommentOut)
async def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await CommentService(db).update(comment_id, comment)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        await CommentService(db).delete(comment_id)
    except AppError as exc:
        raise app_http_error(exc) from exc
    return {"message": "Comment deleted successfully"}
