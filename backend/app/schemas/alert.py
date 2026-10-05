from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AlertBase(BaseModel):
    rule_id: str
    rule_name: str
    source: str
    severity: str
    evidence: str
    analyst_action: str

class AlertCreate(AlertBase):
    pass

class Alert(AlertBase):
    id: int
    alert_id: str
    timestamp: datetime
    status: str

    class Config:
        from_attributes = True
