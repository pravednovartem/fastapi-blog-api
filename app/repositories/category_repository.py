from sqlalchemy.orm import Session

from app.models import Category


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()
 