# SentinelLab — Security Analyst Concepts

> This guide explains the core concepts a Security Analyst uses every day,
> with each concept tied directly to SentinelLab so you understand it in
> practical terms, not just theory.

---

## 1. Event

**Definition**: Any observable, recorded occurrence in a system or network.

An event is simply something that happened. Not every event is suspicious.
Most events are completely normal.

**Examples of events**:
- A user successfully logs in at 9:00 AM *(normal)*
- A file is created in a directory *(normal)*
- A web server receives a GET request *(normal)*
- A user fails to log in once *(probably a typo — still normal)*
- A user fails to log in 50 times in 60 seconds *(suspicious — now interesting)*

**In SentinelLab**: The Log Analyzer reads application logs and normalizes
them into structured security events. Every login attempt, every HTTP
request, every authentication failure becomes an event in our database.

```json
{
  "timestamp": "2026-10-05T15:00:00Z",
  "source": "127.0.0.1",
  "destination": "127.0.0.1:5000",
  "event_type": "auth_failure",
  "severity": "INFO",
  "description": "Failed login attempt for user 'admin'",
  "evidence": "POST /login 401 - username=admin"
}
```

---

## 2. Alert

**Definition**: A notification generated when an event (or pattern of events)
matches a detection rule.

An alert means: "something matched our criteria for potential suspicious
behavior." Alerts are generated automatically by detection systems. They
do NOT necessarily mean an attack is occurring — they mean "pay attention
to this."

**The crucial distinction**: An alert is a signal. An incident is a confirmed problem.

**In SentinelLab**: The Detection Engine evaluates security events against
YAML rules. When a rule triggers, it creates an alert with:
- The specific rule that fired
- The evidence that caused it
- An explanation of why it's suspicious
- Recommended analyst actions

---

## 3. Incident

**Definition**: A security event (or group of events/alerts) that has been
confirmed as an actual security problem requiring investigation and response.

Not every alert becomes an incident. An alert might be a false positive
(see below). An analyst reviews alerts and decides which ones represent
real incidents.

**In SentinelLab**: When you review an alert and decide it represents a
real attack or security problem, you create an Incident and link the
alert to it. The incident then follows the lifecycle: NEW → TRIAGED →
INVESTIGATING → CONTAINED → RESOLVED.

---

## 4. Threat

**Definition**: A potential cause of harm to a system or organization.

A threat is something that *could* harm you. It is theoretical until
it is exploited.

**Examples**:
- An attacker trying to guess your password *(threat)*
- A vulnerability in your web application *(threat + vulnerability)*
- An insider with excessive access *(insider threat)*

**Types of threats**:
- External threats: attackers outside your organization
- Internal threats: malicious or negligent insiders
- Environmental threats: power failures, hardware failures

---

## 5. Vulnerability

**Definition**: A weakness in a system, application, or process that a
threat actor could exploit to cause harm.

A vulnerability is a flaw. It is not harmful by itself — it becomes
dangerous when a threat actor discovers and exploits it.

**In SentinelLab**: The vulnerable lab application has intentional vulnerabilities:
- No rate limiting on the login endpoint *(vulnerability)*
- Verbose error messages that reveal internal details *(vulnerability)*
- An admin page accessible without authentication *(vulnerability)*

Each of these is documented as a **Finding** in the Findings module.

---

## 6. Risk

**Definition**: The likelihood that a threat will exploit a vulnerability,
combined with the impact if it does.

```
Risk = Likelihood × Impact
```

**Example**:

| Vulnerability | Likelihood | Impact | Risk |
|---|---|---|---|
| No rate limiting on login | HIGH | HIGH | CRITICAL |
| Verbose error messages | MEDIUM | LOW | LOW |
| Admin page unprotected | HIGH | CRITICAL | CRITICAL |

This is why not all vulnerabilities are treated equally. Risk prioritization
tells you what to fix first.

---

## 7. Severity

**Definition**: A rating that indicates how serious an alert or incident is.

SentinelLab uses five severity levels:

| Level | Meaning | Response Time |
|---|---|---|
| INFO | Normal or expected behavior, recorded for context | No action required |
| LOW | Potentially suspicious but unlikely to be an attack | Review when convenient |
| MEDIUM | Probable attack attempt, warrants investigation | Investigate within hours |
| HIGH | Likely attack, significant potential impact | Investigate immediately |
| CRITICAL | Active compromise, critical system at risk | Drop everything — respond now |

**How severity is determined**:
- Number of events (5 failed logins = MEDIUM, 100 = HIGH)
- Type of asset targeted (admin accounts = higher severity)
- Evidence of success (a failed attempt vs. a successful one)
- Combination of multiple indicators

---

## 8. IOC — Indicator of Compromise

**Definition**: A piece of evidence that suggests a system may have been
compromised or an attack may be occurring.

IOCs are the "fingerprints" left by attackers. They are what you look for
during an investigation to prove (or disprove) that an attack occurred.

**Common IOC types**:

| IOC Type | Example |
|---|---|
| IP address | Attacker's source IP: 192.168.1.100 |
| URL/path | Requests to `/admin`, `/etc/passwd`, `/../` |
| User-agent | Automated scanner user-agent strings |
| Timestamp pattern | 50 requests in 2 seconds |
| HTTP status pattern | 49 × 401 followed by 1 × 200 |
| DNS query | Unusual domain lookup |

**In SentinelLab**: Every alert contains an `evidence` field that stores
the raw IOCs that triggered the detection rule. When you create an
incident, you link these IOCs as evidence.

---

## 9. False Positive

**Definition**: An alert that fires but does not represent a real attack.
The detection rule triggered, but the activity is actually legitimate.

False positives are a major challenge in security operations. Too many
false positives cause **alert fatigue** — analysts start ignoring alerts
because most of them turn out to be nothing. This is dangerous, because
real attacks can be buried in the noise.

**Examples of false positives**:
- Your automated deployment script logs in 100 times per minute → triggers brute force rule
- A legitimate user mistyped their password 6 times → triggers auth failure threshold
- A security scanner you ran yourself → triggers port scan detection

**How to handle them**:
1. Identify the legitimate source of the activity
2. Tune the detection rule (adjust threshold, add an exclusion)
3. Document the false positive in the incident notes

**In SentinelLab**: You will encounter this during exercises. When the
detection engine fires on your own legitimate test activity, you will
need to distinguish it from a simulated attack.

---

## 10. Triage

**Definition**: The process of quickly reviewing and prioritizing incoming
alerts to determine which ones represent real incidents and which should
be investigated first.

Triage comes from the French word for "to sort." In emergency medicine,
triage determines which patients need immediate care. In security, it
determines which alerts need immediate investigation.

**The triage process**:
1. **Receive alert** — automated detection fires
2. **Initial review** — is this alert plausible given the source and time?
3. **Enrich** — gather additional context (is this IP known malicious? is this user legitimate?)
4. **Classify** — is this a true positive or false positive?
5. **Prioritize** — if true positive, what severity? What should be done first?
6. **Action** — create incident, assign to analyst, or close as false positive

---

## 11. Evidence

**Definition**: Data that supports or refutes the occurrence of a security
event. Evidence must be collected, preserved, and documented carefully.

**Types of evidence in network security**:

| Evidence Type | Example |
|---|---|
| Network logs | HTTP access log entries showing 50 failed logins |
| PCAP file | Packet capture showing the brute force traffic |
| Application logs | Authentication failure log entries |
| Database records | Alert and incident records in SentinelLab |
| Screenshots | Wireshark view showing the attack pattern |
| Timestamps | Exact times of events for the incident timeline |

**Evidence handling principles**:
- **Preserve originals**: Never modify raw evidence files
- **Document collection**: Record when and where evidence was collected
- **Chain of custody**: Document everyone who handled the evidence
- **Timestamps matter**: Evidence without reliable timestamps is weaker

---

## 12. Containment

**Definition**: Actions taken to stop an attack from spreading or causing
further damage, without necessarily eliminating the threat.

Containment is the "stop the bleeding" phase of incident response. The
goal is to limit damage while you investigate.

**Containment examples**:

| Attack Type | Containment Action |
|---|---|
| Brute force attack | Block source IP at firewall |
| Compromised account | Disable the account, force password reset |
| Malware infection | Isolate the infected host from the network |
| Data exfiltration | Block outbound connections to the destination |

**In SentinelLab**: When you move an incident to the CONTAINED state, you
document what containment action was taken and when.

---

## 13. Remediation

**Definition**: Fixing the underlying vulnerability or weakness that was
exploited, so the same attack cannot succeed again.

Containment stops the immediate attack. Remediation prevents the next one.

**Examples**:

| Finding | Remediation |
|---|---|
| No rate limiting on login | Implement account lockout after N failures |
| Verbose error messages | Configure generic error messages for production |
| Admin page without auth | Require strong authentication for admin access |
| SQL injection surface | Use parameterized queries / prepared statements |

**SentinelLab findings** all include a `recommended_remediation` field with
specific, actionable steps.

---

## 14. Incident Timeline

**Definition**: A chronological reconstruction of all events related to an
incident, from first indicator to resolution.

A timeline answers: "What happened, in what order, at what time?"

**Example Incident Timeline**:

```
2026-10-05 15:00:00  —  First failed login attempt detected
2026-10-05 15:00:01  —  Second failed attempt (same source IP)
2026-10-05 15:00:30  —  RULE-001 fires: 5 failures in 60 seconds
2026-10-05 15:00:31  —  Alert ALERT-0042 created (severity: MEDIUM)
2026-10-05 15:01:00  —  Analyst reviews alert, triage begins
2026-10-05 15:02:00  —  Incident INC-2026-001 created
2026-10-05 15:05:00  —  100+ more attempts detected, severity escalated to HIGH
2026-10-05 15:06:00  —  Containment: source IP blocked at application level
2026-10-05 15:07:00  —  Attack stops (no more requests from source IP)
2026-10-05 15:20:00  —  Investigation complete: no successful logins confirmed
2026-10-05 15:25:00  —  Incident moved to RESOLVED
2026-10-05 15:30:00  —  Remediation ticket created: implement rate limiting
```

**In SentinelLab**: Every state change on an incident is timestamped.
The report generator assembles these timestamps into a readable timeline.

---

## How These Concepts Connect in SentinelLab

```
System generates EVENTS (login attempts, HTTP requests)
         │
         ▼
Detection Engine evaluates events against rules
         │
         ▼
Suspicious pattern → ALERT created (with IOCs as evidence)
         │
         ▼
Analyst TRIAGES alert
         │
         ├──► False Positive → Close alert, tune rule
         │
         └──► True Positive → Create INCIDENT
                    │
                    ▼
             Assess SEVERITY
                    │
                    ▼
             Collect EVIDENCE (PCAP, logs, alerts)
                    │
                    ▼
             CONTAIN the threat
                    │
                    ▼
             Recommend REMEDIATION
                    │
                    ▼
             Generate INCIDENT REPORT
                    │
                    ▼
             RESOLVED + Lessons Learned
```

---

## Self-Assessment Questions

After completing SentinelLab, you should be able to answer these without notes:

1. What is the difference between a security event, an alert, and an incident?
2. Why is every alert not automatically an incident?
3. What is a false positive and why does it matter for SOC efficiency?
4. What IOCs would you look for when investigating a suspected brute force attack?
5. What is the difference between containment and remediation?
6. What should an incident timeline contain?
7. How does severity affect your response time?
8. What is alert fatigue and how do detection teams address it?
