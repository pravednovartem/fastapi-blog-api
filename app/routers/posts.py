from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories.post_repository import PostRepository
from ..schemas import PostCreate, PostOut, PostUpdate

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=list[PostOut])
def read_posts(db: Session = Depends(get_db)):
    return PostRepository(db).get_all()


@router.get("/{post_id}", response_model=PostOut)
def read_post(post_id: int, db: Session = Depends(get_db)):
    post = PostRepository(db).get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.post("/", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    return PostRepository(db).create(post)


@router.put("/{post_id}", response_model=PostOut)
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    updated_post = PostRepository(db).update(post_id, post)
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post


@router.delete("/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    deleted_post = PostRepository(db).delete(post_id)
    if not deleted_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}
