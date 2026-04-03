from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..repositories.location_repository import LocationRepository
from ..schemas import LocationCreate, LocationOut, LocationUpdate

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=list[LocationOut])
def read_locations(db: Session = Depends(get_db)):
    return LocationRepository(db).get_all()


@router.get("/{location_id}", response_model=LocationOut)
def read_location(location_id: int, db: Session = Depends(get_db)):
    obj = LocationRepository(db).get_by_id(location_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Location not found")
    return obj


@router.post("/", response_model=LocationOut)
def create_location(data: LocationCreate, db: Session = Depends(get_db)):
    return LocationRepository(db).create(data)


@router.put("/{location_id}", response_model=LocationOut)
def update_location(
    location_id: int, data: LocationUpdate, db: Session = Depends(get_db)
):
    obj = LocationRepository(db).update(location_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Location not found")
    return obj


@router.delete("/{location_id}")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    obj = LocationRepository(db).delete(location_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Location not found")
    return {"message": "Location deleted successfully"}
