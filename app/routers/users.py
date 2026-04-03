from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories.user_repository import UserRepository
from ..schemas import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    return UserRepository(db).get_all()


@router.get("/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    obj = UserRepository(db).get_by_id(user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return obj


@router.post("/", response_model=UserOut)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return UserRepository(db).create(data)


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    obj = UserRepository(db).update(user_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return obj


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    obj = UserRepository(db).delete(user_id)
    if not obj:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}
