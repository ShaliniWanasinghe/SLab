from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from ..database import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String, unique=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    rule_id = Column(String, index=True)
    rule_name = Column(String)
    source = Column(String)
    severity = Column(String)
    evidence = Column(Text)
    analyst_action = Column(Text)
    status = Column(String, default="NEW") # NEW, REVIEWED, ESCALATED
