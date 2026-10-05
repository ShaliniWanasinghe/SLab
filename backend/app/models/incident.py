from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from ..database import Base

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(String, unique=True, index=True)
    title = Column(String)
    severity = Column(String)
    status = Column(String, default="NEW") # NEW, TRIAGED, INVESTIGATING, CONTAINED, RESOLVED
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    affected_asset = Column(String)
    description = Column(Text)
    evidence = Column(Text) # JSON string array
    related_alerts = Column(Text) # JSON string array
    analyst_notes = Column(Text)
    recommended_remediation = Column(Text)
    resolution_notes = Column(Text, nullable=True)
