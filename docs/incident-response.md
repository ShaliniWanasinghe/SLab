# SentinelLab — Incident Response Workflow

## The Incident Lifecycle

SentinelLab implements the following incident states, based on the
NIST SP 800-61 Incident Handling Guide:

```
NEW ──► TRIAGED ──► INVESTIGATING ──► CONTAINED ──► RESOLVED
```

### State Definitions

| State | Description | Analyst Action |
|---|---|---|
| NEW | Alert created, not yet reviewed | Assign to analyst, begin initial triage |
| TRIAGED | Initial review complete, priority set | Determine if event is a real incident |
| INVESTIGATING | Active investigation in progress | Collect evidence, trace attack path |
| CONTAINED | Threat contained, damage limited | Isolate affected systems, block attacker |
| RESOLVED | Incident closed, remediation applied | Document lessons learned, update rules |

## Incident Data Model

Each incident contains:

```json
{
  "incident_id": "INC-2026-001",
  "title": "Brute Force Attack on Login Endpoint",
  "severity": "HIGH",
  "status": "INVESTIGATING",
  "created_at": "2026-10-05T15:00:00Z",
  "updated_at": "2026-10-05T15:30:00Z",
  "affected_asset": "localhost:5000/login",
  "description": "Multiple authentication failures from 127.0.0.1",
  "evidence": ["auth.log lines 142-189", "brute_force.pcap"],
  "related_alerts": ["ALERT-001", "ALERT-002"],
  "analyst_notes": "Investigating whether any attempt succeeded.",
  "recommended_remediation": "Implement account lockout policy.",
  "resolution_notes": null
}
```

## Triage Process

1. **Receive alert** from detection engine
2. **Assess severity** — does the evidence support the severity level?
3. **Identify false positives** — is this a legitimate automated process?
4. **Create incident** if event is confirmed or probable attack
5. **Assign** to analyst for investigation
6. **Investigate** — collect all related evidence
7. **Contain** — stop the attack from causing further damage
8. **Remediate** — fix the underlying vulnerability
9. **Document** — write resolution notes and lessons learned

## Evidence Chain

All evidence must be:
- **Timestamped** — exact time the evidence was collected
- **Sourced** — where did the evidence come from?
- **Preserved** — original files should not be modified
- **Linked** — evidence is linked to the specific incident

*(Full workflow details will be added in Phase 8)*
