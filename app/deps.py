"""Общие зависимости для роутеров."""

from pathlib import Path

from fastapi import Depends, File, HTTPException

from .auth import get_current_user
from .config import settings
from .database import get_db
from .exceptions import AppError

upload_path = Path(settings.UPLOAD_DIR)

db_dependency = Depends(get_db)
auth_dependency = Depends(get_current_user)
oauth2_form_dep = Depends()
image_file_dep = File(...)


def app_http_error(exc: AppError) -> HTTPException:
    if exc.status_code == 401:
        headers = {"WWW-Authenticate": "Bearer"}
    else:
        headers = None
    return HTTPException(
        status_code=exc.status_code,
        detail=exc.to_dict(),
        headers=headers,
    )
