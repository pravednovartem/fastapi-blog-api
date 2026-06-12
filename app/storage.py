"""Загрузка изображений постов."""

import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from .exceptions import ValidationError

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


async def save_post_image(upload_dir: Path, file: UploadFile) -> str:
    filename = file.filename or ""
    ext = Path(filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(
            "Допустимы только jpg, jpeg, png, gif, webp",
            field="image",
        )

    upload_dir.mkdir(parents=True, exist_ok=True)
    stored_name = f"{uuid.uuid4().hex}{ext}"
    dest = upload_dir / stored_name

    size = 0
    async with aiofiles.open(dest, "wb") as out:
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_IMAGE_SIZE:
                await out.close()
                dest.unlink(missing_ok=True)
                raise ValidationError(
                    "Размер изображения не может превышать 5 MB",
                    field="image",
                )
            await out.write(chunk)

    return f"/uploads/{stored_name}"
