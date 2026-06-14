"""Эндпоинты постов."""
# flake8: noqa: D103

from typing import cast

from fastapi import APIRouter, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import (
    app_http_error,
    auth_dependency,
    db_dependency,
    image_file_dep,
    upload_path,
)
from app.exceptions import AppError
from app.models import User
from app.schemas import PostCreate, PostOut, PostUpdate
from app.storage import save_post_image
from app.use_cases.post_service import PostService

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("", response_model=list[PostOut])
async def get_posts(db: AsyncSession = db_dependency):
    return await PostService(db).list()


@router.get("/{post_id}", response_model=PostOut)
async def get_post(post_id: int, db: AsyncSession = db_dependency):
    try:
        return await PostService(db).get(post_id)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.post("", response_model=PostOut)
async def create_post(
    post: PostCreate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        post.author_id = cast(int, current_user.id)
        return await PostService(db).create(post)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.put("/{post_id}", response_model=PostOut)
async def update_post(
    post_id: int,
    post: PostUpdate,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await PostService(db).update(post_id, post)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.post("/{post_id}/image", response_model=PostOut)
async def upload_post_image(
    post_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
    image: UploadFile = image_file_dep,
):
    try:
        image_url = await save_post_image(upload_path, image)
        return await PostService(db).add_image(post_id, image_url)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.post("/{post_id}/images", response_model=PostOut)
async def upload_post_images(
    post_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
    image: UploadFile = image_file_dep,
):
    try:
        image_url = await save_post_image(upload_path, image)
        return await PostService(db).add_image(post_id, image_url)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.delete("/{post_id}/images/{image_id}", response_model=PostOut)
async def delete_post_image(
    post_id: int,
    image_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        return await PostService(db).delete_image(post_id, image_id)
    except AppError as exc:
        raise app_http_error(exc) from exc


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    db: AsyncSession = db_dependency,
    current_user: User = auth_dependency,
):
    try:
        await PostService(db).delete(post_id)
    except AppError as exc:
        raise app_http_error(exc) from exc
    return {"message": "Post deleted successfully"}
