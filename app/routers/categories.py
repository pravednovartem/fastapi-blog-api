from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories.category_repository import CategoryRepository
from ..schemas import CategoryCreate, CategoryOut, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return CategoryRepository(db).get_all()


@router.get("/{category_id}", response_model=CategoryOut)
def read_category(category_id: int, db: Session = Depends(get_db)):
    obj = CategoryRepository(db).get_by_id(category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return obj


@router.post("/", response_model=CategoryOut)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    return CategoryRepository(db).create(data)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)
):
    obj = CategoryRepository(db).update(category_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return obj


@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    obj = CategoryRepository(db).delete(category_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"message": "Category deleted successfully"}
