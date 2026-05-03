"""Приложение FastAPI: конфигурация API и эндпоинты блога."""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response

from sqlalchemy.orm import Session

from .database import get_db
from .exceptions import AppError
from .schemas import (
    CategoryCreate,
    CategoryOut,
    CategoryUpdate,
    CommentCreate,
    CommentOut,
    CommentUpdate,
    LocationCreate,
    LocationOut,
    LocationUpdate,
    PostCreate,
    PostOut,
    PostUpdate,
    UserCreate,
    UserOut,
    UserUpdate,
)
from .use_cases.category_service import CategoryService
from .use_cases.comment_service import CommentService
from .use_cases.location_service import LocationService
from .use_cases.post_service import PostService
from .use_cases.user_service import UserService

# Конфигурация API
app = FastAPI(
    title="Blog API",
    version="1.0.0",
)

db_dependency = Depends(get_db)


def _http(exc: AppError) -> HTTPException:
    """Преобразовать доменную ошибку в HTTPException."""
    return HTTPException(status_code=exc.status_code, detail=exc.to_dict())


# ---------- Ручки ----------

@app.get("/")
def root():
    """Проверка работоспособности API."""
    return {"message": "Blog API is running"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Заглушка favicon, чтобы не было 404 в логах."""
    return Response(status_code=204)


# --- Категории ---

@app.get("/categories", response_model=list[CategoryOut])
def get_categories(db: Session = db_dependency):
    """Список всех категорий."""
    return CategoryService(db).list()


@app.get(
    "/categories/{category_id}",
    response_model=CategoryOut,
)
def get_category(category_id: int, db: Session = db_dependency):
    """Категория по id."""
    try:
        return CategoryService(db).get(category_id)
    except AppError as exc:
        raise _http(exc) from exc


@app.post("/categories", response_model=CategoryOut)
def create_category(
    data: CategoryCreate,
    db: Session = db_dependency,
):
    """Создать категорию."""
    try:
        return CategoryService(db).create(data)
    except AppError as exc:
        raise _http(exc) from exc


@app.put(
    "/categories/{category_id}",
    response_model=CategoryOut,
)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = db_dependency,
):
    """Обновить категорию."""
    try:
        return CategoryService(db).update(category_id, data)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = db_dependency,
):
    """Удалить категорию."""
    try:
        CategoryService(db).delete(category_id)
    except AppError as exc:
        raise _http(exc) from exc
    return {"message": "Category deleted successfully"}


# --- Локации ---

@app.get("/locations", response_model=list[LocationOut])
def get_locations(db: Session = db_dependency):
    """Список всех локаций."""
    return LocationService(db).list()


@app.get(
    "/locations/{location_id}",
    response_model=LocationOut,
)
def get_location(
    location_id: int,
    db: Session = db_dependency,
):
    """Локация по id."""
    try:
        return LocationService(db).get(location_id)
    except AppError as exc:
        raise _http(exc) from exc


@app.post("/locations", response_model=LocationOut)
def create_location(
    data: LocationCreate,
    db: Session = db_dependency,
):
    """Создать локацию."""
    try:
        return LocationService(db).create(data)
    except AppError as exc:
        raise _http(exc) from exc


@app.put(
    "/locations/{location_id}",
    response_model=LocationOut,
)
def update_location(
    location_id: int,
    data: LocationUpdate,
    db: Session = db_dependency,
):
    """Обновить локацию."""
    try:
        return LocationService(db).update(location_id, data)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/locations/{location_id}")
def delete_location(
    location_id: int,
    db: Session = db_dependency,
):
    """Удалить локацию."""
    try:
        LocationService(db).delete(location_id)
    except AppError as exc:
        raise _http(exc) from exc
    return {"message": "Location deleted successfully"}


# --- Пользователи ---

@app.get("/users", response_model=list[UserOut])
def get_users(db: Session = db_dependency):
    """Список всех пользователей."""
    return UserService(db).list()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = db_dependency):
    """Пользователь по id."""
    try:
        return UserService(db).get(user_id)
    except AppError as exc:
        raise _http(exc) from exc


@app.post("/users", response_model=UserOut)
def create_user(
    data: UserCreate,
    db: Session = db_dependency,
):
    """Создать пользователя."""
    try:
        return UserService(db).create(data)
    except AppError as exc:
        raise _http(exc) from exc


@app.put(
    "/users/{user_id}",
    response_model=UserOut,
)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = db_dependency,
):
    """Обновить пользователя."""
    try:
        return UserService(db).update(user_id, data)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = db_dependency,
):
    """Удалить пользователя."""
    try:
        UserService(db).delete(user_id)
    except AppError as exc:
        raise _http(exc) from exc
    return {"message": "User deleted successfully"}


# --- Публикации ---

@app.get("/posts", response_model=list[PostOut])
def get_posts(db: Session = db_dependency):
    """Список всех публикаций."""
    return PostService(db).list()


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = db_dependency):
    """Публикация по id."""
    try:
        return PostService(db).get(post_id)
    except AppError as exc:
        raise _http(exc) from exc


@app.post("/posts", response_model=PostOut)
def create_post(
    post: PostCreate,
    db: Session = db_dependency,
):
    """Создать публикацию."""
    try:
        return PostService(db).create(post)
    except AppError as exc:
        raise _http(exc) from exc


@app.put(
    "/posts/{post_id}",
    response_model=PostOut,
)
def update_post(
    post_id: int,
    post: PostUpdate,
    db: Session = db_dependency,
):
    """Обновить публикацию."""
    try:
        return PostService(db).update(post_id, post)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = db_dependency,
):
    """Удалить публикацию."""
    try:
        PostService(db).delete(post_id)
    except AppError as exc:
        raise _http(exc) from exc
    return {"message": "Post deleted successfully"}


# --- Комментарии ---

@app.get("/comments", response_model=list[CommentOut])
def get_comments(db: Session = db_dependency):
    """Список всех комментариев."""
    return CommentService(db).list()


@app.get(
    "/comments/{comment_id}",
    response_model=CommentOut,
)
def get_comment(
    comment_id: int,
    db: Session = db_dependency,
):
    """Комментарий по id."""
    try:
        return CommentService(db).get(comment_id)
    except AppError as exc:
        raise _http(exc) from exc


@app.post("/comments", response_model=CommentOut)
def create_comment(
    comment: CommentCreate,
    db: Session = db_dependency,
):
    """Создать комментарий."""
    try:
        return CommentService(db).create(comment)
    except AppError as exc:
        raise _http(exc) from exc


@app.put(
    "/comments/{comment_id}",
    response_model=CommentOut,
)
def update_comment(
    comment_id: int,
    comment: CommentUpdate,
    db: Session = db_dependency,
):
    """Обновить комментарий."""
    try:
        return CommentService(db).update(comment_id, comment)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = db_dependency,
):
    """Удалить комментарий."""
    try:
        CommentService(db).delete(comment_id)
    except AppError as exc:
        raise _http(exc) from exc
    return {"message": "Comment deleted successfully"}
