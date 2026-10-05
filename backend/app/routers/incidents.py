from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/incidents",
    tags=["incidents"]
)

@router.get("/", response_model=List[schemas.incident.Incident])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    incidents = db.query(models.incident.Incident).order_by(models.incident.Incident.created_at.desc()).offset(skip).limit(limit).all()
    return incidents

@router.get("/{incident_id}", response_model=schemas.incident.Incident)
def read_incident(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(models.incident.Incident).filter(models.incident.Incident.incident_id == incident_id).first()
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.post("/", response_model=schemas.incident.Incident)
def create_incident(incident: schemas.incident.IncidentCreate, db: Session = Depends(get_db)):
    inc_id = f"INC-{str(uuid.uuid4())[:8].upper()}"
    db_inc = models.incident.Incident(**incident.model_dump(), incident_id=inc_id)
    db.add(db_inc)
    db.commit()
    db.refresh(db_inc)
    return db_inc

@router.patch("/{incident_id}", response_model=schemas.incident.Incident)
def update_incident(incident_id: str, incident: schemas.incident.IncidentUpdate, db: Session = Depends(get_db)):
    db_inc = db.query(models.incident.Incident).filter(models.incident.Incident.incident_id == incident_id).first()
    if not db_inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    update_data = incident.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_inc, key, value)
        
    db.commit()
    db.refresh(db_inc)
    return db_inc
