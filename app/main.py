from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import get_db
from .repositories.category_repository import CategoryRepository
from .repositories.location_repository import LocationRepository
from .repositories.post_repository import PostRepository
from .repositories.comment_repository import CommentRepository
from .schemas import CategoryOut, LocationOut, PostOut, CommentOut

app = FastAPI(title="FastAPI + Django SQLite")


@app.get("/")
def root():
    return {"message": "FastAPI works with Django SQLite database"}


@app.get("/categories", response_model=list[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return CategoryRepository(db).get_all()


@app.get("/categories/{category_id}", response_model=CategoryOut)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = CategoryRepository(db).get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@app.get("/locations", response_model=list[LocationOut])
def get_locations(db: Session = Depends(get_db)):
    return LocationRepository(db).get_all()


@app.get("/locations/{location_id}", response_model=LocationOut)
def get_location(location_id: int, db: Session = Depends(get_db)):
    location = LocationRepository(db).get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")
    return location


@app.get("/posts", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db)):
    return PostRepository(db).get_all()


@app.get("/posts/{post_id}", response_model=PostOut)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = PostRepository(db).get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/comments", response_model=list[CommentOut])
def get_comments(db: Session = Depends(get_db)):
    return CommentRepository(db).get_all()


@app.get("/comments/{comment_id}", response_model=CommentOut)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = CommentRepository(db).get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
