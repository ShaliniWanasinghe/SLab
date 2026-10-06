"""
seed_data.py — Populate the SentinelLab database with sample security data.
Run from the backend/ directory:  python seed_data.py
"""
import sys
import os

# Ensure the backend app package is importable
sys.path.insert(0, os.path.dirname(__file__))

from app.database import engine, SessionLocal, Base
from app.models.alert import Alert
from app.models.incident import Incident
from datetime import datetime, timedelta, UTC
import uuid
import random

# Create all tables
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# --- Clear existing data ---
db.query(Alert).delete()
db.query(Incident).delete()
db.commit()

# --- Sample Alerts ---
RULES = [
    ("RULE-001", "Brute Force SSH", "HIGH"),
    ("RULE-002", "Port Scan Detected", "MEDIUM"),
    ("RULE-003", "SQL Injection Attempt", "CRITICAL"),
    ("RULE-004", "Suspicious DNS Query", "LOW"),
    ("RULE-005", "Privilege Escalation Attempt", "CRITICAL"),
    ("RULE-006", "Malware C2 Beacon", "HIGH"),
    ("RULE-007", "Unauthorized File Access", "MEDIUM"),
    ("RULE-008", "Data Exfiltration Detected", "CRITICAL"),
    ("RULE-009", "Failed Login Spike", "MEDIUM"),
    ("RULE-010", "Lateral Movement Detected", "HIGH"),
]

SOURCES = [
    "192.168.1.105", "10.0.0.42", "172.16.0.88",
    "192.168.1.200", "10.0.0.15", "203.0.113.77",
    "192.168.2.33", "10.10.10.50", "172.16.5.12",
    "192.168.1.99",
]

now = datetime.now(UTC)
alerts = []
for i in range(25):
    rule_id, rule_name, severity = random.choice(RULES)
    alert = Alert(
        alert_id=f"ALT-{str(uuid.uuid4())[:8].upper()}",
        timestamp=now - timedelta(minutes=random.randint(1, 1440)),
        rule_id=rule_id,
        rule_name=rule_name,
        source=random.choice(SOURCES),
        severity=severity,
        evidence=f"Detected {rule_name.lower()} from source host. Packet analysis confirms suspicious traffic pattern.",
        analyst_action="Pending review",
        status=random.choice(["NEW", "REVIEWED", "ESCALATED"]),
    )
    alerts.append(alert)

db.add_all(alerts)
db.commit()

# --- Sample Incidents ---
INCIDENT_DATA = [
    {
        "title": "Active Brute Force Attack on SSH Server",
        "severity": "HIGH",
        "status": "INVESTIGATING",
        "affected_asset": "prod-web-01 (192.168.1.105)",
        "description": "Multiple failed SSH login attempts detected from external IP 203.0.113.77. Over 500 attempts in the last hour targeting root and admin accounts.",
        "evidence": "Auth logs show 547 failed attempts. Source IP geolocated to known threat actor infrastructure.",
        "related_alerts": "ALT-SSH001, ALT-SSH002",
        "analyst_notes": "Blocked source IP at firewall. Monitoring for additional attempts from related IPs.",
        "recommended_remediation": "1. Block source IP range\n2. Enable fail2ban\n3. Disable password auth, use key-based only",
    },
    {
        "title": "SQL Injection on Customer Portal",
        "severity": "CRITICAL",
        "status": "CONTAINED",
        "affected_asset": "customer-portal (10.0.0.42)",
        "description": "SQL injection payload detected in login form. Attacker attempted to extract user credentials via UNION-based injection.",
        "evidence": "WAF logs captured payload: ' UNION SELECT username,password FROM users--. Database audit log shows unauthorized SELECT queries.",
        "related_alerts": "ALT-SQLi001",
        "analyst_notes": "Application taken offline. WAF rules updated. Database credentials rotated.",
        "recommended_remediation": "1. Patch vulnerable endpoint\n2. Implement parameterized queries\n3. Add input validation\n4. Full security audit of application",
    },
    {
        "title": "Suspected Data Exfiltration via DNS Tunneling",
        "severity": "CRITICAL",
        "status": "NEW",
        "affected_asset": "finance-server (172.16.0.88)",
        "description": "Anomalous DNS query patterns detected from finance server. High volume of TXT record queries to suspicious domain.",
        "evidence": "DNS logs show 3,400 queries to *.data.evil-domain.com in 2 hours. Query subdomains appear to be base64-encoded data.",
        "related_alerts": "ALT-DNS001, ALT-DNS002, ALT-EXFIL001",
        "analyst_notes": None,
        "recommended_remediation": "1. Isolate affected server\n2. Block malicious domain\n3. Forensic analysis of server\n4. Check for lateral movement",
    },
    {
        "title": "Ransomware Indicator - File Encryption Activity",
        "severity": "HIGH",
        "status": "TRIAGED",
        "affected_asset": "file-server-01 (10.10.10.50)",
        "description": "Rapid file modification pattern detected on shared drive. Files being renamed with .encrypted extension.",
        "evidence": "File audit logs show 1,200 files modified in 5 minutes. New process 'svchost32.exe' spawned from temp directory.",
        "related_alerts": "ALT-MAL001, ALT-FILE001",
        "analyst_notes": "Server network access restricted. Snapshot taken before isolation.",
        "recommended_remediation": "1. Immediately isolate server\n2. Identify patient zero\n3. Restore from clean backups\n4. Scan all endpoints",
    },
    {
        "title": "Privilege Escalation via Kernel Exploit",
        "severity": "HIGH",
        "status": "RESOLVED",
        "affected_asset": "dev-workstation-07 (192.168.2.33)",
        "description": "Local privilege escalation detected. User account escalated to root using known kernel vulnerability CVE-2024-1234.",
        "evidence": "Audit log shows uid change from 1001 to 0. Exploit binary found in /tmp/.hidden/exploit.",
        "related_alerts": "ALT-PRIV001",
        "analyst_notes": "System rebuilt from clean image. User account disabled pending investigation.",
        "recommended_remediation": "1. Patch kernel\n2. Restrict tmp exec permissions\n3. Enhanced monitoring on endpoint",
        "resolution_notes": "System re-imaged. Kernel patched. User cleared after investigation.",
    },
]

for inc_data in INCIDENT_DATA:
    resolution = inc_data.pop("resolution_notes", None)
    incident = Incident(
        incident_id=f"INC-{str(uuid.uuid4())[:8].upper()}",
        created_at=now - timedelta(hours=random.randint(1, 72)),
        updated_at=now - timedelta(minutes=random.randint(1, 120)),
        resolution_notes=resolution,
        **inc_data,
    )
    db.add(incident)

db.commit()
db.close()

print("[OK] Database seeded successfully!")
print(f"   - {len(alerts)} alerts created")
print(f"   - {len(INCIDENT_DATA)} incidents created")
