from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
import os

from .. import models
from ..database import get_db
from ..services.report_generator import generate_markdown_report

router = APIRouter(
    prefix="/api/reports",
    tags=["reports"]
)

@router.get("/{incident_id}", response_class=PlainTextResponse)
def generate_report(incident_id: str, db: Session = Depends(get_db)):
    incident = db.query(models.incident.Incident).filter(models.incident.Incident.incident_id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
        
    report_md = generate_markdown_report(incident)
    
    # Optionally save to disk
    reports_dir = os.environ.get("REPORTS_DIR", "../reports")
    os.makedirs(reports_dir, exist_ok=True)
    report_path = os.path.join(reports_dir, f"{incident_id}_report.md")
    
    with open(report_path, "w") as f:
        f.write(report_md)
        
    return report_md
