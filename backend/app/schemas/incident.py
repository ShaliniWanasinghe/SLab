from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

class IncidentBase(BaseModel):
    title: str
    severity: str
    affected_asset: str
    description: str
    evidence: str
    related_alerts: str
    analyst_notes: Optional[str] = None
    recommended_remediation: Optional[str] = None

class IncidentCreate(IncidentBase):
    pass

class IncidentUpdate(BaseModel):
    status: Optional[str] = None
    analyst_notes: Optional[str] = None
    resolution_notes: Optional[str] = None

class Incident(IncidentBase):
    id: int
    incident_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    resolution_notes: Optional[str]

    class Config:
        from_attributes = True
