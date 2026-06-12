"""FastAPI Blog API."""

import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from jose import JWTError, jwt  # type: ignore[import-untyped]

from .auth import ALGORITHM, SECRET_KEY
from .deps import upload_path
from .logging_config import setup_logging
from .routers import auth, categories, comments, locations, posts, users

setup_logging()
logger = logging.getLogger("app.access")

upload_path.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="Blog API", version="1.0.0")
app.mount("/uploads", StaticFiles(directory=upload_path), name="uploads")

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)


def _extract_user_label(request: Request) -> str:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.lower().startswith("bearer "):
        return "anonymous"
    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return "invalid_token"
    sub = payload.get("sub")
    return f"user_id={sub}" if sub else "anonymous"


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    user_label = _extract_user_label(request)
    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (time.perf_counter() - start) * 1000
        logger.exception(
            "%s %s -> 500 [%s] %.2fms",
            request.method,
            request.url.path,
            user_label,
            duration_ms,
        )
        raise
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %s [%s] %.2fms",
        request.method,
        request.url.path,
        response.status_code,
        user_label,
        duration_ms,
    )
    return response


@app.on_event("startup")
async def on_startup() -> None:
    upload_path.mkdir(parents=True, exist_ok=True)
    logging.getLogger("app").info("Blog API started (async)")


@app.get("/")
async def root():
    return {"message": "Blog API is running"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)
