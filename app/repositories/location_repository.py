from sqlalchemy.orm import Session

from app.models import Location


class LocationRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        return self.db.query(Location).all()

    def get_by_id(self, location_id: int):
        return self.db.query(Location).filter(Location.id == location_id).first()
