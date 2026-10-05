import os
from datetime import datetime

def generate_markdown_report(incident) -> str:
    """Generate a markdown report for an incident."""
    md = f"""# Incident Report: {incident.incident_id}
**Title:** {incident.title}
**Date Generated:** {datetime.utcnow().isoformat()}

## Executive Summary
**Severity:** {incident.severity}
**Status:** {incident.status}
**Affected Asset:** {incident.affected_asset}

## Details
{incident.description}

## Evidence
```
{incident.evidence}
```

## Analyst Notes
{incident.analyst_notes or 'No notes provided.'}

## Recommended Remediation
{incident.recommended_remediation or 'No remediation provided.'}

## Resolution Notes
{incident.resolution_notes or 'Not resolved yet.'}
"""
    return md
