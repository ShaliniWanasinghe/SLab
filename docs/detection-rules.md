# SentinelLab — Detection Rules Reference

## Overview

SentinelLab uses a **rule-based detection engine**. All rules are defined in
`security-analysis/detection/rules.yaml` and loaded at runtime.

Each rule is intentionally simple and explainable. When a rule fires, the
alert includes:

- **Why it fired** — the exact condition that was triggered
- **Evidence** — the raw data that caused the match
- **Analyst guidance** — what to do next

## Severity Levels

| Level | Description | Example |
|---|---|---|
| INFO | Informational event, no action required | Single failed login |
| LOW | Suspicious but unlikely to be an attack | Unusual user-agent |
| MEDIUM | Probable attack attempt, needs triage | 5+ failed logins in 60s |
| HIGH | Likely attack, escalate promptly | Port scan detected |
| CRITICAL | Active compromise or critical asset at risk | Admin access without auth |

## Detection Rules

*(Rules will be documented here as they are implemented in Phase 7)*

### Rule Template

```yaml
id: RULE-001
name: Repeated Authentication Failures
description: >
  Detects multiple consecutive failed login attempts from the same
  source IP within a short time window. This pattern is consistent
  with a credential brute-force or password-spraying attack.
condition:
  event_type: auth_failure
  threshold: 5
  window_seconds: 60
  group_by: source_ip
severity: MEDIUM
escalate_to: HIGH  # if threshold > 15
evidence_fields:
  - source_ip
  - timestamp
  - attempt_count
  - usernames_tried
analyst_action: >
  1. Verify the source IP is not a legitimate automated process.
  2. Check if any attempt succeeded after failures.
  3. Review which usernames were targeted.
  4. If attack ongoing: block source IP at the network level.
  5. Notify account owners of targeted usernames.
mitre_tactic: TA0006  # Credential Access
mitre_technique: T1110  # Brute Force
```

## False Positive Guidance

*(To be added in Phase 7)*
