from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories.comment_repository import CommentRepository
from ..schemas import CommentCreate, CommentOut, CommentUpdate

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=list[CommentOut])
def read_comments(db: Session = Depends(get_db)):
    return CommentRepository(db).get_all()


@router.get("/{comment_id}", response_model=CommentOut)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    obj = CommentRepository(db).get_by_id(comment_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Comment not found")
    return obj


@router.post("/", response_model=CommentOut)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return CommentRepository(db).create(comment)


@router.put("/{comment_id}", response_model=CommentOut)
def update_comment(
    comment_id: int, comment: CommentUpdate, db: Session = Depends(get_db)
):
    updated_comment = CommentRepository(db).update(comment_id, comment)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment


@router.delete("/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    deleted_comment = CommentRepository(db).delete(comment_id)
    if not deleted_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return {"message": "Comment deleted successfully"}
