from sqlalchemy.orm import Session

from app.models import Post


class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Post).all()

    def get_by_id(self, post_id: int):
        return self.db.query(Post).filter(Post.id == post_id).first()

    def get_by_author(self, author_id: int):
        return self.db.query(Post).filter(Post.author_id == author_id).all()

    def get_by_category(self, category_id: int):
        return self.db.query(Post).filter(Post.category_id == category_id).all()
