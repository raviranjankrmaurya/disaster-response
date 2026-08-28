from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_api_key
from app.models import models, schemas

router = APIRouter(prefix="/api/volunteers", tags=["Volunteers"])


@router.post("/", response_model=schemas.VolunteerOut, dependencies=[Depends(require_api_key)])
def create_volunteer(volunteer: schemas.VolunteerCreate, db: Session = Depends(get_db)):
    db_volunteer = models.Volunteer(**volunteer.model_dump())
    db.add(db_volunteer)
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer


@router.get("/", response_model=list[schemas.VolunteerOut])
def list_volunteers(db: Session = Depends(get_db)):
    return db.query(models.Volunteer).all()


@router.get("/{volunteer_id}", response_model=schemas.VolunteerOut)
def get_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    v = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return v


@router.patch("/{volunteer_id}/assign/{zone_id}", response_model=schemas.VolunteerOut, dependencies=[Depends(require_api_key)])
def assign_volunteer(volunteer_id: int, zone_id: int, db: Session = Depends(get_db)):
    v = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    zone = db.query(models.DisasterZone).filter(models.DisasterZone.id == zone_id).first()
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found")
    v.assigned_zone_id = zone_id
    v.status = models.VolunteerStatus.deployed
    db.commit()
    db.refresh(v)
    return v


@router.delete("/{volunteer_id}", dependencies=[Depends(require_api_key)])
def delete_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    v = db.query(models.Volunteer).filter(models.Volunteer.id == volunteer_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    db.delete(v)
    db.commit()
    return {"status": "deleted"}
