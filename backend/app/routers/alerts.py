from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/api/alerts",
    tags=["alerts"]
)

@router.get("/", response_model=List[schemas.alert.Alert])
def read_alerts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alerts = db.query(models.alert.Alert).order_by(models.alert.Alert.timestamp.desc()).offset(skip).limit(limit).all()
    return alerts

@router.post("/", response_model=schemas.alert.Alert)
def create_alert(alert: schemas.alert.AlertCreate, db: Session = Depends(get_db)):
    alert_id = f"ALT-{str(uuid.uuid4())[:8].upper()}"
    db_alert = models.alert.Alert(**alert.model_dump(), alert_id=alert_id)
    db.add(db_alert)
    db.commit()
    db.refresh(db_alert)
    return db_alert
