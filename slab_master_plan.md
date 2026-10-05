# SentinelLab (SLab) — Master Project Plan
### Network Security Monitoring & Incident Analysis Laboratory
**Version 1.0 | Status: Awaiting Approval**

---

> [!IMPORTANT]
> This is a **defensive cybersecurity education project**. All security testing is strictly limited to localhost, private lab networks, and deliberately created laboratory systems that you own and control. This project does not teach, enable, or encourage unauthorized access to any external system.

---

## Table of Contents

1. [Final Architecture](#1-final-architecture)
2. [Repository Structure](#2-repository-structure)
3. [Technology Justification](#3-technology-justification)
4. [Threat Model Overview](#4-threat-model-overview)
5. [Learning Roadmap](#5-learning-roadmap)
6. [Phase-by-Phase Implementation Plan](#6-phase-by-phase-implementation-plan)
7. [Required Software](#7-required-software)
8. [Lab Environment](#8-lab-environment)
9. [Skills You Will Learn](#9-skills-you-will-learn)
10. [Expected Portfolio Outcome](#10-expected-portfolio-outcome)

---

## 1. Final Architecture

### System Overview

SentinelLab is structured as a local SOC (Security Operations Center) simulation. Think of a real-world SOC: there is a monitored environment generating traffic and logs, a set of analysis tools ingesting that data, detection logic triggering alerts, and analysts managing the response workflow. SentinelLab mirrors this at a small, educational scale.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        SENTINELLAB ARCHITECTURE                         │
│                     (All components run locally)                        │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────────┐
  │  LAYER 1 — MONITORED ENVIRONMENT (Target / Victim Simulation)        │
  │                                                                      │
  │  ┌─────────────────────────────────────────────────────────────┐    │
  │  │          Vulnerable Web Application (Flask / Python)        │    │
  │  │     localhost:5000  •  Intentionally flawed for education   │    │
  │  │                                                             │    │
  │  │  • Weak auth endpoint      • Verbose error pages            │    │
  │  │  • Unvalidated inputs      • Sensitive path exposure        │    │
  │  │  • No rate limiting        • Basic SQL injection surface    │    │
  │  └─────────────────────────────────────────────────────────────┘    │
  │                          │ HTTP traffic                              │
  │                          │ Application logs                          │
  └──────────────────────────┼───────────────────────────────────────────┘
                             │
  ┌──────────────────────────▼───────────────────────────────────────────┐
  │  LAYER 2 — DATA COLLECTION                                           │
  │                                                                      │
  │  ┌──────────────────┐    ┌──────────────────┐    ┌───────────────┐  │
  │  │  PCAP Capture    │    │  Log Ingestor     │    │  Recon Module │  │
  │  │  (tshark/tcpdump)│    │  (Python parser)  │    │  (Nmap output)│  │
  │  │                  │    │                   │    │               │  │
  │  │  .pcap files     │    │  Normalized JSON  │    │  Port/service │  │
  │  │  → JSON metadata │    │  security events  │    │  fingerprints │  │
  │  └────────┬─────────┘    └────────┬──────────┘    └───────┬───────┘  │
  └───────────┼──────────────────────┼──────────────────────┼───────────┘
              │                      │                       │
  ┌───────────▼──────────────────────▼───────────────────────▼───────────┐
  │  LAYER 3 — ANALYSIS ENGINE                                           │
  │                                                                      │
  │  ┌──────────────────────────────────────────────────────────────┐   │
  │  │              Rule-Based Detection Engine                      │   │
  │  │                                                               │   │
  │  │  Rule 1: Repeated auth failures  → MEDIUM/HIGH alert         │   │
  │  │  Rule 2: Suspicious HTTP paths   → LOW/MEDIUM alert           │   │
  │  │  Rule 3: Port scan patterns      → HIGH alert                 │   │
  │  │  Rule 4: Abnormal request rate   → MEDIUM alert               │   │
  │  │  Rule 5: Unusual connection vol  → INFO/LOW alert             │   │
  │  │                                                               │   │
  │  │  Each rule: explainable, configurable, documented            │   │
  │  └──────────────────────┬───────────────────────────────────────┘   │
  └─────────────────────────┼────────────────────────────────────────────┘
                            │ Structured Alerts (JSON)
  ┌─────────────────────────▼────────────────────────────────────────────┐
  │  LAYER 4 — BACKEND API (FastAPI / Python)   localhost:8000           │
  │                                                                      │
  │  /api/alerts          — Alert management                             │
  │  /api/incidents       — Incident lifecycle (NEW→RESOLVED)            │
  │  /api/pcap/analyze    — Upload & analyze PCAP files                  │
  │  /api/recon           — Reconnaissance data                          │
  │  /api/findings        — Security findings (OWASP-mapped)             │
  │  /api/reports/{id}    — Generate incident reports (MD / PDF)         │
  │  /api/rules           — View/configure detection rules               │
  │  /api/logs            — Normalized event log access                  │
  │                                                                      │
  │  SQLite Database  (sentinellab.db)                                   │
  │  Tables: alerts, incidents, findings, pcap_sessions, events, rules   │
  └──────────────────────────────┬───────────────────────────────────────┘
                                 │ REST API (JSON)
  ┌──────────────────────────────▼───────────────────────────────────────┐
  │  LAYER 5 — SECURITY DASHBOARD (React / Vite)   localhost:5173        │
  │                                                                      │
  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  ┌───────────┐  │
  │  │ Dashboard   │  │ Alert Table  │  │ Incidents  │  │ PCAP View │  │
  │  │ (KPI cards) │  │ (filterable) │  │ (timeline) │  │ (results) │  │
  │  └─────────────┘  └──────────────┘  └────────────┘  └───────────┘  │
  │  ┌─────────────┐  ┌──────────────┐  ┌────────────┐  ┌───────────┐  │
  │  │ Detection   │  │ Recon Results│  │ Findings   │  │ Report    │  │
  │  │ Rules View  │  │ (port data)  │  │ (OWASP)    │  │ Generator │  │
  │  └─────────────┘  └──────────────┘  └────────────┘  └───────────┘  │
  └──────────────────────────────────────────────────────────────────────┘
```

### Data Flow Summary

```
Vulnerable App  →  Generates HTTP traffic + logs
tshark          →  Captures traffic to .pcap files
PCAP Analyzer   →  Parses .pcap → structured JSON
Log Parser      →  Parses app logs → normalized security events
Detection Engine→  Evaluates events against rules → fires alerts
FastAPI Backend →  Stores everything in SQLite, serves REST API
React Dashboard →  Consumes API, displays SOC-style interface
Report Generator→  Pulls incident data → Markdown/PDF report
```

---

## 2. Repository Structure

```
sentinellab/
│
├── backend/                          # FastAPI application
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                   # FastAPI app entry point
│   │   ├── database.py               # SQLite + SQLAlchemy setup
│   │   ├── models/
│   │   │   ├── alert.py
│   │   │   ├── incident.py
│   │   │   ├── finding.py
│   │   │   ├── event.py
│   │   │   └── pcap_session.py
│   │   ├── routers/
│   │   │   ├── alerts.py
│   │   │   ├── incidents.py
│   │   │   ├── findings.py
│   │   │   ├── pcap.py
│   │   │   ├── recon.py
│   │   │   ├── reports.py
│   │   │   └── rules.py
│   │   ├── services/
│   │   │   ├── detection_engine.py   # Rule evaluation logic
│   │   │   ├── pcap_analyzer.py      # PCAP parsing
│   │   │   ├── log_analyzer.py       # Log normalization
│   │   │   ├── report_generator.py   # MD/PDF reports
│   │   │   └── severity.py           # Severity classification
│   │   └── schemas/
│   │       ├── alert.py              # Pydantic schemas
│   │       ├── incident.py
│   │       └── finding.py
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_alerts.py
│   │   ├── test_incidents.py
│   │   ├── test_detection.py
│   │   ├── test_pcap.py
│   │   ├── test_log_parser.py
│   │   ├── test_severity.py
│   │   └── test_reports.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                         # React + Vite dashboard
│   ├── src/
│   │   ├── components/
│   │   │   ├── Layout/
│   │   │   ├── Dashboard/
│   │   │   ├── Alerts/
│   │   │   ├── Incidents/
│   │   │   ├── PCAP/
│   │   │   ├── Findings/
│   │   │   └── Reports/
│   │   ├── pages/
│   │   │   ├── DashboardPage.jsx
│   │   │   ├── AlertsPage.jsx
│   │   │   ├── IncidentDetailPage.jsx
│   │   │   ├── PCAPAnalysisPage.jsx
│   │   │   ├── FindingsPage.jsx
│   │   │   └── ReportsPage.jsx
│   │   ├── hooks/
│   │   ├── services/
│   │   │   └── api.js                # Axios API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── public/
│   ├── package.json
│   ├── vite.config.js
│   └── .env.example
│
├── vulnerable-lab/                   # Intentionally vulnerable app
│   ├── app.py                        # Flask vulnerable web app
│   ├── templates/
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── admin.html
│   ├── static/
│   ├── lab_db.sqlite                 # Lab database (reset-able)
│   ├── reset_lab.py                  # Reset script
│   ├── requirements.txt
│   └── VULNERABLE_APP_WARNING.md     # Clear safety disclaimer
│
├── security-analysis/
│   ├── pcap/
│   │   ├── analyzer.py               # Standalone PCAP tool
│   │   └── filters.py                # BPF filter helpers
│   ├── logs/
│   │   ├── parser.py                 # Log normalization
│   │   └── normalizer.py             # Event schema enforcement
│   └── detection/
│       ├── engine.py                 # Rule engine (standalone)
│       ├── rules.yaml                # All detection rules (YAML)
│       └── rule_loader.py            # YAML → rule objects
│
├── sample-data/
│   ├── pcap/
│   │   ├── README.md                 # What each file contains
│   │   ├── brute_force_sample.pcap   # Simulated brute force
│   │   ├── port_scan_sample.pcap     # Simulated port scan
│   │   └── normal_traffic.pcap       # Baseline traffic
│   ├── logs/
│   │   ├── sample_access.log         # Apache-style log
│   │   └── sample_auth.log           # Auth failure log
│   └── reports/
│       └── example_incident_report.md
│
├── reports/                          # Generated reports (gitignored)
│   └── .gitkeep
│
├── docs/
│   ├── architecture.md               # System architecture (detailed)
│   ├── lab-setup.md                  # Step-by-step lab setup guide
│   ├── detection-rules.md            # All rules explained
│   ├── incident-response.md          # IR workflow guide
│   ├── learning-notes.md             # Your personal learning journal
│   ├── kali-learning.md              # Kali Linux primer
│   ├── wireshark-learning.md         # Wireshark primer
│   └── security-analyst-learning.md  # SOC analyst concepts
│
├── screenshots/                      # Dashboard + tool screenshots
│   └── .gitkeep
│
├── scripts/
│   ├── setup.sh                      # Unix setup script
│   ├── setup.ps1                     # Windows PowerShell setup
│   └── start_lab.sh / start_lab.ps1  # Start all components
│
├── docker-compose.yml                # Optional containerized run
├── .gitignore
├── README.md
└── LICENSE                           # MIT License
```

### Key Structural Decisions

| Decision | Reason |
|---|---|
| `vulnerable-lab/` is isolated from `backend/` | The vulnerable app is a **target**, not part of the defender stack. Separation makes the architecture clearer and avoids confusion. |
| `security-analysis/` has standalone scripts | These can be run independently of the FastAPI backend — good for CLI-based learning exercises. |
| `detection/rules.yaml` is separate from code | Rules should be configurable without touching Python. This also demonstrates the real-world concept of externalized rule sets (e.g., Sigma rules, Snort rules). |
| `sample-data/` is committed to the repo | Reviewers and learners can run the full pipeline without needing to generate traffic themselves. Clearly documented as synthetic/educational only. |

---

## 3. Technology Justification

### Why Python + FastAPI (Backend)?

| Choice | Justification |
|---|---|
| **Python** | The dominant language in cybersecurity tooling (Scapy, dpkt, Impacket, Volatility, YARA bindings — all Python). Learning Python for this project directly transfers to real security tools. |
| **FastAPI** | Modern, fast, automatically generates OpenAPI docs (`/docs`). Async support is beneficial when waiting for PCAP parsing or subprocess calls. Much cleaner than Flask for API-only backends. |
| **SQLite** | No server setup required. Perfect for a local lab. The database file is portable, inspectable with DB Browser for SQLite, and sufficient for this project scale. SQLAlchemy ORM provides a production-relevant pattern. |
| **Pydantic** | Enforces strict data validation — important in security tooling where malformed input is a real concern and a learning point. |

### Why Flask for the Vulnerable App (Not FastAPI)?

Flask is deliberately chosen because:
- It provides less "magic" — its behavior is more transparent and easier to make intentionally insecure in an educational and controlled way.
- Separating frameworks reinforces that **the target and the defender are different systems**.
- Flask is what you will encounter in many legacy Python web applications — realistic attack surface.

### Why React + Vite (Frontend)?

| Choice | Justification |
|---|---|
| **React** | You already have React knowledge. This project lets you apply it to a professional security context. Real SOC tools (Elastic Security, Splunk SIEM, Wazuh) all have React-based frontends. |
| **Vite** | Fast development server. Minimal configuration. Industry standard for modern React projects. |
| **Vanilla CSS** | Avoids Tailwind dependency confusion. Full control over the SOC dashboard aesthetic. |

### Why tshark / Wireshark?

- **tshark** is the command-line version of Wireshark. It allows programmatic PCAP analysis from Python via `subprocess`, which is exactly how real automation tools work.
- **Wireshark** GUI is used for visual learning — you will understand packets visually before processing them programmatically.
- Industry standard: Wireshark/tshark are used by incident responders, network forensics analysts, and security engineers everywhere.

### Why Nmap?

- The standard tool for network reconnaissance and discovery. Used in every penetration test, vulnerability assessment, and security audit.
- Its output (XML) is machine-parseable — you will learn to parse Nmap XML output programmatically.

### Why NOT Machine Learning?

This is an explicit design decision. A rule-based detection engine is:
1. **Explainable** — every alert can be traced to a specific rule and a specific piece of evidence.
2. **Appropriate** — ML detection requires large, labeled datasets. We have synthetic data.
3. **Educational** — You will understand exactly *why* an alert fired, which is fundamental to triage.
4. **Honest** — Pretending a rule-based system is "AI" is a common portfolio red flag. Hiring managers notice.

### Why Docker (Optional)?

Docker is listed as optional because:
- Installing Docker adds complexity for a beginner lab environment.
- The project must work without Docker.
- Docker Compose is provided for reviewers who want one-command startup, and it demonstrates DevOps awareness for your portfolio.

---

## 4. Threat Model Overview

> **Important note**: This threat model describes the *educational simulation* — the types of attacks the lab is designed to demonstrate and detect. All of these occur within your local environment only.

### Simulated Attacker Profile (Lab Persona)

```
Name:       External Attacker (simulated by lab exercises)
Location:   localhost / local network (192.168.x.x range only)
Goal:       Enumerate the vulnerable lab app, extract information,
            exploit weak authentication
Tools:      curl, nmap, web browser, custom scripts
Scope:      ONLY the vulnerable-lab application (localhost:5000)
```

### Threat Scenarios Modeled

| Scenario | Attack Category | Detection Goal |
|---|---|---|
| Repeated login failures | Credential brute force | Rule 1: Auth failure threshold |
| Accessing `/admin` without auth | Unauthorized path access | Rule 2: Suspicious HTTP pattern |
| Rapid sequential requests | Automated scanning / DoS attempt | Rule 4: Abnormal request rate |
| Nmap port scan of localhost | Network reconnaissance | Rule 3: Port scan pattern (from PCAP) |
| SQL injection attempt in login form | Injection attack | Rule 2: Suspicious input pattern |
| Accessing `/etc/passwd` style paths | Path traversal attempt | Rule 2: Suspicious HTTP pattern |

### Assets Being Protected (in the simulation)

| Asset | Description | Simulated Value |
|---|---|---|
| Vulnerable Lab App | The target application | Represents a corporate web app |
| Lab SQLite DB | App's user data | Represents sensitive PII/credentials |
| Application Logs | Audit trail | Represents SIEM log source |
| API Backend | Analysis infrastructure | Represents the defender's tooling |

### What SentinelLab Does NOT Model

- Network intrusion (lateral movement, pivoting)
- Malware behavior or C2 communication
- Privilege escalation
- Real-world CVEs (only conceptual analogs)
- Any interaction with systems outside localhost

This scoping is intentional and should be stated clearly in the README.

---

## 5. Learning Roadmap

This roadmap is sequenced to build knowledge progressively. Each skill directly supports the next phase.

### Stage 1 — Foundations (Weeks 1–2)

**Goal**: Understand the basic concepts before touching any tool.

| Topic | What You'll Learn |
|---|---|
| What is a SOC? | The role of a Security Operations Center, analyst workflow |
| CIA Triad | Confidentiality, Integrity, Availability — the foundation of all security |
| Security event vs. alert vs. incident | Critical terminology for triage |
| TCP/IP networking basics | How packets travel — essential for PCAP analysis |
| HTTP fundamentals | Request/response, headers, methods, status codes |
| What is a SIEM? | How tools like Splunk/Elastic Security work (SentinelLab is a mini-SIEM) |

**Exercises**: Read `docs/security-analyst-learning.md`, `docs/wireshark-learning.md`

### Stage 2 — Lab Environment (Week 2)

**Goal**: Have all tools installed and running.

| Topic | What You'll Learn |
|---|---|
| Setting up a local lab | Isolation, why localhost matters |
| Running Flask applications | Python web server basics |
| Using `curl` for HTTP testing | CLI-based HTTP interaction |
| Viewing live traffic in Wireshark | Real-time packet capture |

### Stage 3 — Reconnaissance (Week 3)

**Goal**: Understand what an attacker sees before attacking and what a defender should document.

| Topic | What You'll Learn |
|---|---|
| Nmap basics | Port scanning, service enumeration |
| Reading Nmap XML output | Programmatic parsing |
| Port states (open/closed/filtered) | What each state means defensively |
| Service fingerprinting | Why service versions matter for vulnerability assessment |

### Stage 4 — Traffic Analysis (Weeks 3–4)

**Goal**: Be comfortable reading network packets and PCAP files.

| Topic | What You'll Learn |
|---|---|
| Wireshark filters | Display filters vs capture filters |
| Reading a TCP handshake | SYN, SYN-ACK, ACK — the foundation of all TCP |
| HTTP in packets | How requests look at the packet level |
| Identifying brute force in PCAP | Pattern recognition in network data |
| tshark on command line | Scriptable packet analysis |
| Python PCAP parsing (Scapy/dpkt) | Programmatic network forensics |

### Stage 5 — Detection Engineering (Weeks 4–5)

**Goal**: Understand how rules are written and why alerts fire.

| Topic | What You'll Learn |
|---|---|
| What is a detection rule? | The anatomy of a Sigma/Snort/custom rule |
| Threshold-based detection | Counting events over time windows |
| Pattern-based detection | String matching in logs/requests |
| Severity classification | When is something INFO vs CRITICAL? |
| False positives | Why detection is hard, and how to tune rules |

### Stage 6 — Incident Response (Weeks 5–6)

**Goal**: Follow a professional IR workflow.

| Topic | What You'll Learn |
|---|---|
| Triage workflow | How to prioritize alerts |
| Evidence collection | What constitutes forensic evidence |
| Incident lifecycle | NEW → TRIAGED → INVESTIGATING → CONTAINED → RESOLVED |
| Writing incident timelines | Chronological reconstruction of an event |
| Analyst notes | Professional documentation standards |

### Stage 7 — Full Pipeline (Weeks 6–7)

**Goal**: Run the complete workflow end to end.

Trigger attack → Capture PCAP → Parse logs → Fire alerts → Create incident → Generate report → Remediate

---

## 6. Phase-by-Phase Implementation Plan

### PHASE 0 — Architecture & Learning Roadmap *(current phase)*
**Deliverables**: This document. Your approval.
**Learning objective**: Understand the full picture before writing a single line of code.

---

### PHASE 1 — Repository Setup
**Estimated time**: 30–45 minutes

**Learning objectives**:
- Git repository initialization
- Project structure best practices
- `.gitignore` configuration for Python/React/security projects
- Environment file conventions (`.env.example`)
- MIT License and ethical use statement

**Deliverables**:
- Initialized git repo at `c:\Users\User\Desktop\SLab`
- All directories created (empty with `.gitkeep`)
- `README.md` skeleton
- `.gitignore`
- `LICENSE`
- `docs/` skeleton files

**Test**: `git log --oneline` shows initial commit. `tree` shows full structure.

---

### PHASE 2 — Vulnerable Lab Application
**Estimated time**: 2–3 hours

**Learning objectives**:
- What makes a web application "vulnerable"?
- OWASP Top 10 concepts (Broken Access Control, Injection, etc.)
- Why intentionally vulnerable apps exist (DVWA, OWASP Juice Shop, WebGoat)
- The difference between a vulnerability and an exploit
- How weak authentication creates attacker opportunities

**Deliverables**:
- Flask app (`vulnerable-lab/app.py`) with labeled vulnerable endpoints
- Reset script (`reset_lab.py`)
- `VULNERABLE_APP_WARNING.md` with clear ethical scope
- Lab runs at `localhost:5000`

**Test**: `curl http://localhost:5000/login` returns a login page. Reset script clears state.

**Exercise for you**: After the lab is running, use your browser's DevTools Network tab to observe what an HTTP login request looks like. What headers are sent?

---

### PHASE 3 — Reconnaissance Module
**Estimated time**: 1–2 hours

**Learning objectives**:
- Network reconnaissance from a defensive perspective
- Nmap syntax and output formats
- Port states and their security implications
- How attackers enumerate targets (so defenders can detect it)
- Parsing Nmap XML in Python

**Deliverables**:
- `security-analysis/recon/` module
- Nmap XML parser
- Recon data schema (JSON)
- Sample Nmap output files

**Test**: Run Nmap against `localhost`, parse the XML, view structured output.

**Exercise for you**: Identify which services Nmap discovers on localhost. Which ones should NOT be exposed in a production environment?

---

### PHASE 4 — Wireshark / PCAP Workflow
**Estimated time**: 1–2 hours (learning-heavy, minimal code)

**Learning objectives**:
- Packet anatomy (Frame → Ethernet → IP → TCP → Application)
- TCP three-way handshake in Wireshark
- HTTP request/response at the packet level
- Display filters (`http`, `tcp.flags.syn==1`, `ip.addr==127.0.0.1`)
- Following a TCP stream
- Exporting packets for analysis

**Deliverables**:
- `docs/wireshark-learning.md` (complete)
- Capturing traffic from the vulnerable lab
- Sample `.pcap` files for the project

**Test**: Open a `.pcap` in Wireshark and apply a filter to show only HTTP traffic.

**Exercise for you**: Use Wireshark to capture a failed login attempt. What does the HTTP POST request look like? What does the server's response say?

---

### PHASE 5 — PCAP Analyzer
**Estimated time**: 2–3 hours

**Learning objectives**:
- Python network packet processing libraries
- Extracting metadata from packet captures programmatically
- Structuring network forensics data as JSON
- How SIEM tools ingest network data

**Deliverables**:
- `security-analysis/pcap/analyzer.py` (standalone CLI tool)
- `backend/app/services/pcap_analyzer.py` (backend integration)
- Sample PCAP files in `sample-data/pcap/`
- JSON output schema documentation

**Test**: Run `python analyzer.py --file sample-data/pcap/brute_force_sample.pcap` and see structured JSON output.

**Exercise for you**: Modify the analyzer to count how many times each source IP appears. What does this tell you about the traffic?

---

### PHASE 6 — Log Analyzer
**Estimated time**: 1–2 hours

**Learning objectives**:
- Log formats (Apache Common Log Format, combined format, custom formats)
- Log normalization — why different sources need a common schema
- Security events vs. noise
- Log-based threat detection
- Why log integrity matters

**Deliverables**:
- `security-analysis/logs/parser.py`
- `security-analysis/logs/normalizer.py`
- Normalized event JSON schema
- Sample log files in `sample-data/logs/`

**Test**: Parse `sample_access.log` → see normalized JSON events.

**Exercise for you**: Look at a raw Apache access log line. How many pieces of security-relevant information can you identify?

---

### PHASE 7 — Detection Engine
**Estimated time**: 3–4 hours

**Learning objectives**:
- Detection engineering fundamentals
- Rule anatomy (condition, threshold, action)
- YAML as a rule format (how Sigma rules work)
- Threshold vs. pattern-based detection
- Alert fatigue and tuning
- Severity classification rationale

**Deliverables**:
- `security-analysis/detection/rules.yaml` (5+ rules)
- `security-analysis/detection/engine.py`
- `backend/app/services/detection_engine.py`
- Alert schema with explanation fields
- All alerts include: why it fired, what the analyst should do next

**Test**: Feed brute-force log events → detection engine → see `MEDIUM` alert with evidence.

**Exercise for you**: Write one additional detection rule in `rules.yaml` for a scenario you choose. Test it against the sample data.

---

### PHASE 8 — Incident Management
**Estimated time**: 2–3 hours

**Learning objectives**:
- The incident lifecycle (NIST IR framework)
- Incident vs. alert vs. event
- Evidence preservation
- Analyst documentation standards
- Escalation and containment concepts

**Deliverables**:
- Incident data models (SQLAlchemy)
- Incident workflow logic (state machine)
- SQLite database schema

**Test**: Create an incident via API, transition it through states, add analyst notes.

**Exercise for you**: Draft a one-paragraph analyst note for a simulated brute-force incident. What information would you include?

---

### PHASE 9 — FastAPI Backend
**Estimated time**: 3–4 hours

**Learning objectives**:
- REST API design
- Pydantic for data validation (and why validation is a security concern)
- Database ORM patterns (SQLAlchemy)
- API documentation (FastAPI auto-generates `/docs`)
- CORS configuration (why it matters for browser-based frontends)

**Deliverables**:
- All routers implemented
- Database migrations
- API documentation at `localhost:8000/docs`
- `backend/requirements.txt`
- `.env.example`

**Test**: All API endpoints respond correctly. Swagger UI accessible at `/docs`.

**Exercise for you**: Use the Swagger UI at `/docs` to manually create an incident. Then query it back.

---

### PHASE 10 — React Dashboard
**Estimated time**: 4–5 hours

**Learning objectives**:
- Connecting a React app to a REST API
- Data visualization for security data
- Professional UI/UX for security tooling
- React Router for multi-page navigation
- Real-time data patterns (polling)

**Deliverables**:
- Full React dashboard with all pages
- Alert table with severity filtering
- Incident timeline view
- PCAP upload and results viewer
- Network activity visualization
- Detection rules viewer

**Test**: Dashboard loads, displays alerts, can navigate to incident details.

**Exercise for you**: Add a "copy to clipboard" button for the Evidence field in the Alert table.

---

### PHASE 11 — Report Generator
**Estimated time**: 2–3 hours

**Learning objectives**:
- Incident report structure (executive vs. technical sections)
- Markdown as a documentation format
- PDF generation from Python
- What makes a good security report

**Deliverables**:
- `backend/app/services/report_generator.py`
- Markdown report template
- PDF export option (via `reportlab` or `weasyprint`)
- `sample-data/reports/example_incident_report.md`

**Test**: Generate a report for a test incident. Verify Markdown structure. Export PDF.

**Exercise for you**: Read the generated report. What information would you add as a senior analyst?

---

### PHASE 12 — Testing
**Estimated time**: 2–3 hours

**Learning objectives**:
- pytest fundamentals
- Test fixtures for security testing
- API integration testing
- Why testing matters in security tooling (untested detection code is unreliable detection code)

**Deliverables**:
- Full pytest suite
- Test fixtures (synthetic data)
- `pytest` passes with >80% coverage target

**Test**: `pytest backend/tests/ -v` passes all tests.

---

### PHASE 13 — Documentation
**Estimated time**: 2–3 hours

**Deliverables**:
- Complete `README.md`
- `docs/architecture.md` (with diagrams)
- `docs/kali-learning.md`
- `docs/wireshark-learning.md`
- `docs/security-analyst-learning.md`
- `docs/detection-rules.md`
- `docs/incident-response.md`
- `docs/lab-setup.md`

---

### PHASE 14 — Portfolio Polishing
**Estimated time**: 1–2 hours

**Deliverables**:
- Screenshots of dashboard in `screenshots/`
- Clean Git history with meaningful commit messages
- GitHub repository published (public)
- `README.md` renders correctly on GitHub
- Docker Compose verified (optional)

---

## 7. Required Software

### On Your Windows Machine (Primary)

| Software | Purpose | Download |
|---|---|---|
| **Python 3.11+** | Backend, analysis scripts, vulnerable lab | python.org |
| **Node.js 20+ LTS** | React frontend | nodejs.org |
| **Git** | Version control | git-scm.com |
| **Wireshark** | Packet capture and analysis GUI | wireshark.org |
| **Nmap** | Network reconnaissance | nmap.org |
| **VS Code** | Primary editor | code.visualstudio.com |
| **DB Browser for SQLite** | Inspect SQLite database visually | sqlitebrowser.org |
| **Windows Terminal** | Better terminal experience | Microsoft Store |

### Python Packages (Backend — `requirements.txt`)

```
fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.36
pydantic==2.10.0
pydantic-settings==2.7.0
python-multipart==0.0.18
scapy==2.6.1          # PCAP analysis
python-nmap==0.7.1     # Nmap XML parsing
reportlab==4.2.5       # PDF generation
jinja2==3.1.4          # Report templating
pytest==8.3.4
pytest-asyncio==0.24.0
httpx==0.28.0          # API test client
pyyaml==6.0.2          # Detection rules
python-dateutil==2.9.0
```

### Python Packages (Vulnerable Lab — separate `requirements.txt`)

```
flask==3.1.0
flask-sqlalchemy==3.1.1
werkzeug==3.1.3
```

### VS Code Extensions (Recommended)

- Python (Microsoft)
- Pylance
- ES7+ React/Redux/React-Native snippets
- Prettier
- GitLens
- SQLite Viewer
- REST Client (for testing API endpoints)

### Optional

| Software | Purpose |
|---|---|
| **Docker Desktop** | Run Docker Compose setup |
| **VirtualBox / VMware** | Future: Kali Linux VM |
| **Kali Linux ISO** | Future: dedicated attack VM |

---

## 8. Lab Environment

### Phase 1–9 Lab Setup (Windows localhost only)

For the initial phases, everything runs on your Windows machine:

```
┌─────────────────────────────────────────────────────────┐
│                   YOUR WINDOWS MACHINE                  │
│                                                         │
│  localhost:5000  →  Vulnerable Lab App (Flask)          │
│  localhost:8000  →  SentinelLab API (FastAPI)           │
│  localhost:5173  →  SentinelLab Dashboard (React/Vite)  │
│                                                         │
│  Wireshark captures loopback (127.0.0.1) traffic        │
│  Nmap scans localhost only                              │
│  All data stored in sentinellab.db (SQLite)             │
└─────────────────────────────────────────────────────────┘
```

**Network adapter for capture**: Wireshark on Windows captures on the `Npcap Loopback Adapter` (installed with Wireshark/Npcap). This captures all localhost traffic.

### Wireshark on Windows — Important Note

Wireshark on Windows requires **Npcap** (installed automatically with Wireshark). You will capture on the **loopback adapter** (`127.0.0.1`) to observe local lab traffic.

### Future Enhancement (Post Phase 14) — Kali Linux VM

After completing the main project, you can add:

```
┌─────────────────────────────────────────┐
│         VIRTUALBOX / VMWARE             │
│                                         │
│  ┌───────────────────────────────────┐  │
│  │  Kali Linux VM                    │  │
│  │  (Host-Only Network Adapter)      │  │
│  │  IP: 192.168.56.101 (example)     │  │
│  │  Tools: nmap, curl, nikto         │  │
│  └───────────────────────────────────┘  │
│              │                          │
│   Host-Only Network (isolated)          │
│              │                          │
│  ┌───────────────────────────────────┐  │
│  │  Windows Host                     │  │
│  │  Runs vulnerable lab + defender   │  │
│  │  IP: 192.168.56.1 (example)       │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

**This is optional and comes AFTER the core project is complete.** The `docs/kali-learning.md` will prepare you for this phase.

### Safety Configuration

- Vulnerable app binds to `127.0.0.1` only (not `0.0.0.0`)
- All Nmap commands target `127.0.0.1` only
- No firewall rules are modified
- No network services are exposed outside the host

---

## 9. Skills You Will Learn

### Cybersecurity Fundamentals

- [ ] CIA Triad — the foundation of all security decisions
- [ ] Network security fundamentals — TCP/IP, ports, protocols
- [ ] Threat modeling — identifying assets, threats, and mitigations
- [ ] Vulnerability categories — OWASP Top 10 concepts (applied, not memorized)
- [ ] Indicators of Compromise (IOC) — what evidence looks like
- [ ] Triage methodology — how to prioritize security events
- [ ] Incident response lifecycle — NIST IR framework concepts
- [ ] SIEM concepts — log aggregation, correlation, alerting

### Network Analysis

- [ ] Wireshark proficiency — capture, filter, follow streams
- [ ] PCAP analysis — reading packet captures programmatically
- [ ] TCP handshake — SYN, SYN-ACK, ACK in practice
- [ ] Protocol analysis — HTTP, DNS, TCP at packet level
- [ ] tshark (CLI Wireshark) — scriptable packet analysis
- [ ] Network reconnaissance — Nmap, port scanning, service detection
- [ ] Nmap XML parsing — machine-readable recon output

### Detection Engineering

- [ ] Rule-based detection — writing and evaluating detection rules
- [ ] Threshold detection — count-based anomaly detection
- [ ] Pattern detection — signature-based matching
- [ ] Alert severity classification — INFO → CRITICAL
- [ ] False positive analysis — why tuning matters
- [ ] Detection rule documentation — explainability in security tooling

### Software Engineering (Applied to Security)

- [ ] Python for security tooling — scripting, parsing, automation
- [ ] FastAPI — building security APIs
- [ ] SQLAlchemy — ORM for security data persistence
- [ ] Pydantic — data validation in security context
- [ ] React (security-applied) — building SOC dashboards
- [ ] pytest — testing security detection logic
- [ ] Git workflow — professional version control

### Professional Security Skills

- [ ] Security documentation — incident reports, findings
- [ ] Analyst communication — writing for technical and non-technical audiences
- [ ] Evidence handling — structuring evidence for investigation
- [ ] Remediation recommendations — actionable security advice
- [ ] Lab environment design — isolated, reproducible, documented

---

## 10. Expected Portfolio Outcome

### What Your GitHub Repository Will Demonstrate

When a hiring manager or technical interviewer reviews your repository, they will see:

| What They See | What It Demonstrates |
|---|---|
| Structured, well-documented code | Software engineering fundamentals |
| Detection engine with explainable rules | Detection engineering capability |
| PCAP analysis pipeline | Network forensics knowledge |
| Incident management workflow | IR process understanding |
| FastAPI backend with tests | Python proficiency + API design |
| React dashboard | Frontend capability applied to security |
| Comprehensive documentation | Professional communication |
| Ethical use statement | Security ethics awareness |
| Sample data (synthetic only) | Responsible data handling |
| Phased commit history | Methodical development process |

### Interview Talking Points This Project Enables

You will be able to speak credibly about:

1. **"Tell me about your experience with network traffic analysis."**
   → "I built a PCAP analysis pipeline that extracts packet metadata and feeds it into a detection engine. Let me walk you through how it works..."

2. **"What do you know about detection engineering?"**
   → "I designed a rule-based detection engine with configurable YAML rules. Each rule has an explanation field that describes *why* the event is suspicious and what the analyst should do next..."

3. **"How familiar are you with incident response?"**
   → "I implemented an incident management module that follows the NIST IR lifecycle — from initial triage through containment to resolution. I can show you the workflow..."

4. **"Have you worked with security tooling?"**
   → "I integrated Wireshark/tshark, Nmap, and built my own SIEM-like tool. I can parse PCAP files programmatically and correlate events across log sources..."

5. **"Do you have experience with security documentation?"**
   → "I built an automated report generator that produces structured incident reports. Here's an example output..."

### Realistic Expectations

> [!NOTE]
> This project demonstrates **practical capability** and **learning depth**, not enterprise-grade production software. That is appropriate for an entry-level analyst role. Employers at this level are looking for evidence that you can learn, apply concepts, and communicate about security — all of which this project demonstrates.

**What this project is**: A credible, documented, working implementation of core security analyst workflows.

**What this project is not**: A replacement for hands-on experience with enterprise SIEM tools (Splunk, Elastic), real incident response, or enterprise network environments.

**Complementary steps** (recommended after this project):
- TryHackMe SOC Level 1 path (free)
- Blue Team Labs Online
- CompTIA Security+ (certification)
- Splunk free training (Splunk SIEM familiarity)

---

## Approval Checkpoint

Before implementation begins, please review and confirm:

- [ ] Architecture makes sense to you — any questions?
- [ ] Repository structure looks logical?
- [ ] Technology choices are acceptable?
- [ ] Phased plan timeline is reasonable?
- [ ] Lab setup (Windows localhost first) works for you?
- [ ] Any changes to scope, features, or priorities?

**Once you approve, we will begin with PHASE 1 — Repository Setup.**

---

*Document prepared by: Antigravity (Senior Cybersecurity Engineer / Architect)*
*Date: 2026-10-05*
*Project: SentinelLab v1.0*
*Status: Awaiting user approval*
