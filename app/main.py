"""Приложение FastAPI: конфигурация API и эндпоинты блога."""

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.orm import Session

from .database import get_db
from .repositories.category_repository import CategoryRepository
from .repositories.comment_repository import CommentRepository
from .repositories.location_repository import LocationRepository
from .repositories.post_repository import PostRepository
from .repositories.user_repository import UserRepository
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

# Конфигурация API
app = FastAPI(
    title="Blog API",
    version="1.0.0",
)

db_dependency = Depends(get_db)


# ---------- Ручки ----------

@app.get("/")
def root():
    """Проверка работоспособности API."""
    return {"message": "Blog API is running"}


# --- Категории ---

@app.get("/categories", response_model=list[CategoryOut])
def get_categories(db: Session = db_dependency):
    """Список всех категорий."""
    return CategoryRepository(db).get_all()


@app.get(
    "/categories/{category_id}",
    response_model=CategoryOut,
)
def get_category(category_id: int, db: Session = db_dependency):
    """Категория по id."""
    obj = CategoryRepository(db).get_by_id(category_id)
    if not obj:
        raise HTTPException(404, "Category not found")
    return obj


@app.post("/categories", response_model=CategoryOut)
def create_category(
    data: CategoryCreate,
    db: Session = db_dependency,
):
    """Создать категорию."""
    return CategoryRepository(db).create(data)


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
    obj = CategoryRepository(db).update(category_id, data)
    if not obj:
        raise HTTPException(404, "Category not found")
    return obj


@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = db_dependency,
):
    """Удалить категорию."""
    obj = CategoryRepository(db).delete(category_id)
    if not obj:
        raise HTTPException(404, "Category not found")
    return {"message": "Category deleted successfully"}


# --- Локации ---

@app.get("/locations", response_model=list[LocationOut])
def get_locations(db: Session = db_dependency):
    """Список всех локаций."""
    return LocationRepository(db).get_all()


@app.get(
    "/locations/{location_id}",
    response_model=LocationOut,
)
def get_location(
    location_id: int,
    db: Session = db_dependency,
):
    """Локация по id."""
    obj = LocationRepository(db).get_by_id(location_id)
    if not obj:
        raise HTTPException(404, "Location not found")
    return obj


@app.post("/locations", response_model=LocationOut)
def create_location(
    data: LocationCreate,
    db: Session = db_dependency,
):
    """Создать локацию."""
    return LocationRepository(db).create(data)


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
    obj = LocationRepository(db).update(location_id, data)
    if not obj:
        raise HTTPException(404, "Location not found")
    return obj


@app.delete("/locations/{location_id}")
def delete_location(
    location_id: int,
    db: Session = db_dependency,
):
    """Удалить локацию."""
    obj = LocationRepository(db).delete(location_id)
    if not obj:
        raise HTTPException(404, "Location not found")
    return {"message": "Location deleted successfully"}


# --- Пользователи ---

@app.get("/users", response_model=list[UserOut])
def get_users(db: Session = db_dependency):
    """Список всех пользователей."""
    return UserRepository(db).get_all()


@app.get("/users/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = db_dependency):
    """Пользователь по id."""
    obj = UserRepository(db).get_by_id(user_id)
    if not obj:
        raise HTTPException(404, "User not found")
    return obj


@app.post("/users", response_model=UserOut)
def create_user(
    data: UserCreate,
    db: Session = db_dependency,
):
    """Создать пользователя."""
    return UserRepository(db).create(data)


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
    obj = UserRepository(db).update(user_id, data)
    if not obj:
        raise HTTPException(404, "User not found")
    return obj


@app.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = db_dependency,
):
    """Удалить пользователя."""
    obj = UserRepository(db).delete(user_id)
    if not obj:
        raise HTTPException(404, "User not found")
    return {"message": "User deleted successfully"}


# --- Публикации ---

@app.get("/posts", response_model=list[PostOut])
def get_posts(db: Session = db_dependency):
    """Список всех публикаций."""
    return PostRepository(db).get_all()


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = db_dependency):
    """Публикация по id."""
    post = PostRepository(db).get_by_id(post_id)
    if not post:
        raise HTTPException(404, "Post not found")
    return post


@app.post("/posts", response_model=PostOut)
def create_post(
    post: PostCreate,
    db: Session = db_dependency,
):
    """Создать публикацию."""
    return PostRepository(db).create(post)


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
    updated = PostRepository(db).update(post_id, post)
    if not updated:
        raise HTTPException(404, "Post not found")
    return updated


@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = db_dependency,
):
    """Удалить публикацию."""
    deleted = PostRepository(db).delete(post_id)
    if not deleted:
        raise HTTPException(404, "Post not found")
    return {"message": "Post deleted successfully"}


# --- Комментарии ---

@app.get("/comments", response_model=list[CommentOut])
def get_comments(db: Session = db_dependency):
    """Список всех комментариев."""
    return CommentRepository(db).get_all()


@app.get(
    "/comments/{comment_id}",
    response_model=CommentOut,
)
def get_comment(
    comment_id: int,
    db: Session = db_dependency,
):
    """Комментарий по id."""
    obj = CommentRepository(db).get_by_id(comment_id)
    if not obj:
        raise HTTPException(404, "Comment not found")
    return obj


@app.post("/comments", response_model=CommentOut)
def create_comment(
    comment: CommentCreate,
    db: Session = db_dependency,
):
    """Создать комментарий."""
    return CommentRepository(db).create(comment)


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
    updated = CommentRepository(db).update(comment_id, comment)
    if not updated:
        raise HTTPException(404, "Comment not found")
    return updated


@app.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = db_dependency,
):
    """Удалить комментарий."""
    deleted = CommentRepository(db).delete(comment_id)
    if not deleted:
        raise HTTPException(404, "Comment not found")
    return {"message": "Comment deleted successfully"}
