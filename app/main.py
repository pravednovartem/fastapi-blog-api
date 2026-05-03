"""Приложение FastAPI: конфигурация API и эндпоинты блога."""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .exceptions import AppError
from .models import User
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
    LoginRequest,
    PostCreate,
    PostOut,
    PostUpdate,
    RegisterRequest,
    TokenResponse,
    UserCreate,
    UserOut,
    UserUpdate,
)
from .use_cases.auth_service import AuthService
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
auth_dependency = Depends(get_current_user)


def _http(exc: AppError) -> HTTPException:
    """Преобразовать доменную ошибку в HTTPException."""
    headers = None
    if exc.status_code == 401:
        headers = {"WWW-Authenticate": "Bearer"}
    return HTTPException(
        status_code=exc.status_code,
        detail=exc.to_dict(),
        headers=headers,
    )


# ---------- Ручки ----------

@app.get("/")
def root():
    """Проверка работоспособности API."""
    return {"message": "Blog API is running"}


@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    """Заглушка favicon, чтобы не было 404 в логах."""
    return Response(status_code=204)


# --- Аутентификация ---

@app.post("/auth/register", response_model=TokenResponse)
def register(data: RegisterRequest, db: Session = db_dependency):
    """Зарегистрировать пользователя и сразу выдать JWT."""
    try:
        _, token = AuthService(db).register(data)
    except AppError as exc:
        raise _http(exc) from exc
    return TokenResponse(access_token=token)


@app.post("/auth/login", response_model=TokenResponse)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = db_dependency,
):
    """Войти по логину/паролю и получить JWT (форма OAuth2)."""
    try:
        _, token = AuthService(db).login(
            LoginRequest(username=form.username, password=form.password),
        )
    except AppError as exc:
        raise _http(exc) from exc
    return TokenResponse(access_token=token)


@app.get("/auth/me", response_model=UserOut)
def me(current_user: User = auth_dependency):
    """Вернуть данные текущего пользователя по JWT."""
    return current_user


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
    current_user: User = auth_dependency,
):
    """Создать категорию (требуется JWT)."""
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
    current_user: User = auth_dependency,
):
    """Обновить категорию (требуется JWT)."""
    try:
        return CategoryService(db).update(category_id, data)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = db_dependency,
    current_user: User = auth_dependency,
):
    """Удалить категорию (требуется JWT)."""
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
    current_user: User = auth_dependency,
):
    """Создать локацию (требуется JWT)."""
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
    current_user: User = auth_dependency,
):
    """Обновить локацию (требуется JWT)."""
    try:
        return LocationService(db).update(location_id, data)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/locations/{location_id}")
def delete_location(
    location_id: int,
    db: Session = db_dependency,
    current_user: User = auth_dependency,
):
    """Удалить локацию (требуется JWT)."""
    try:
        LocationService(db).delete(location_id)
    except AppError as exc:
        raise _http(exc) from exc
    return {"message": "Location deleted successfully"}


# --- Пользователи ---

@app.get("/users", response_model=list[UserOut])
def get_users(
    db: Session = db_dependency,
    current_user: User = auth_dependency,
):
    """Список всех пользователей (требуется JWT)."""
    return UserService(db).list()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(
    user_id: int,
    db: Session = db_dependency,
    current_user: User = auth_dependency,
):
    """Пользователь по id (требуется JWT)."""
    try:
        return UserService(db).get(user_id)
    except AppError as exc:
        raise _http(exc) from exc


@app.post("/users", response_model=UserOut)
def create_user(
    data: UserCreate,
    db: Session = db_dependency,
    current_user: User = auth_dependency,
):
    """Создать пользователя без пароля (требуется JWT)."""
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
    current_user: User = auth_dependency,
):
    """Обновить пользователя (требуется JWT)."""
    try:
        return UserService(db).update(user_id, data)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = db_dependency,
    current_user: User = auth_dependency,
):
    """Удалить пользователя (требуется JWT)."""
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
    current_user: User = auth_dependency,
):
    """Создать публикацию (автор = текущий пользователь)."""
    try:
        post.author_id = current_user.id
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
    current_user: User = auth_dependency,
):
    """Обновить публикацию (требуется JWT)."""
    try:
        return PostService(db).update(post_id, post)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = db_dependency,
    current_user: User = auth_dependency,
):
    """Удалить публикацию (требуется JWT)."""
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
    current_user: User = auth_dependency,
):
    """Создать комментарий (автор = текущий пользователь)."""
    try:
        comment.author_id = current_user.id
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
    current_user: User = auth_dependency,
):
    """Обновить комментарий (требуется JWT)."""
    try:
        return CommentService(db).update(comment_id, comment)
    except AppError as exc:
        raise _http(exc) from exc


@app.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = db_dependency,
    current_user: User = auth_dependency,
):
    """Удалить комментарий (требуется JWT)."""
    try:
        CommentService(db).delete(comment_id)
    except AppError as exc:
        raise _http(exc) from exc
    return {"message": "Comment deleted successfully"}
