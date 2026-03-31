from sqlalchemy.orm import Session

from app.models import Comment


class CommentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Comment).all()

    def get_by_id(self, comment_id: int):
        return self.db.query(Comment).filter(Comment.id == comment_id).first()

    def get_by_post(self, post_id: int):
        return self.db.query(Comment).filter(Comment.post_id == post_id).all()

    def get_by_author(self, author_id: int):
        return self.db.query(Comment).filter(Comment.author_id == author_id).all()
