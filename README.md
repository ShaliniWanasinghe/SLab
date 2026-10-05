<div align="center">

# 🛡️ SentinelLab

### Network Security Monitoring & Incident Analysis Laboratory

*A portfolio-grade cybersecurity project demonstrating practical Security Analyst workflows*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Ethical Use](https://img.shields.io/badge/Scope-Local%20Lab%20Only-red?style=flat-square)](#ethical-use--legal-scope)

</div>

---

> ⚠️ **IMPORTANT**: All security testing in this project is strictly limited to `localhost` and privately owned, isolated lab networks. This project does not interact with, scan, or probe any external system. See [Ethical Use & Legal Scope](#ethical-use--legal-scope).

---

## Overview

SentinelLab is a local Security Operations Center (SOC) simulation built to demonstrate practical security analyst workflows from first principles. It integrates network traffic capture, log analysis, rule-based threat detection, incident management, and automated report generation into a single cohesive platform.

This project simulates the day-to-day workflow of a junior security analyst:

```
Reconnaissance → Traffic Capture → Log Collection → Detection
→ Alert Triage → Investigation → Evidence Analysis
→ Incident Documentation → Remediation Recommendations
```

**Why this project exists**: Breaking into cybersecurity requires demonstrating practical knowledge, not just theoretical understanding. SentinelLab was built to bridge that gap — every component maps to a real-world security concept and a real tool that security teams use.

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│              SENTINELLAB — SYSTEM ARCHITECTURE          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [Vulnerable Lab App]  ──traffic──►  [PCAP Capture]    │
│      localhost:5000    ──logs───►   [Log Ingestor]     │
│                                          │              │
│                                    [Detection Engine]   │
│                                          │              │
│                                    [FastAPI Backend]    │
│                                     localhost:8000      │
│                                          │              │
│                                  [React Dashboard]      │
│                                   localhost:5173        │
└─────────────────────────────────────────────────────────┘
```

See [`docs/architecture.md`](docs/architecture.md) for the full architecture diagram.

---

## Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Monitored Target | Python / Flask | Intentionally vulnerable web application |
| Packet Analysis | tshark / Wireshark / Scapy | Network traffic capture and PCAP parsing |
| Reconnaissance | Nmap | Network service enumeration |
| Detection Engine | Python / YAML rules | Rule-based security alert generation |
| Backend API | Python / FastAPI | Security data API and analysis orchestration |
| Database | SQLite / SQLAlchemy | Persistent storage for alerts, incidents, findings |
| Dashboard | React / Vite | SOC-style security monitoring interface |
| Report Generator | Python / Jinja2 / ReportLab | Incident report generation (Markdown + PDF) |
| Testing | pytest / httpx | Automated test suite |

---

## Security Concepts Demonstrated

- **Network Reconnaissance** — Nmap port scanning and service enumeration
- **Packet Analysis** — PCAP capture and parsing with tshark/Scapy
- **Log Analysis** — Normalized security event extraction from application logs
- **Detection Engineering** — Rule-based threat detection (threshold + pattern)
- **Alert Triage** — Severity classification (INFO → CRITICAL)
- **Incident Response** — NIST IR lifecycle (Detection → Containment → Resolution)
- **Evidence Handling** — Structured evidence collection linked to incidents
- **Security Reporting** — Incident report generation with executive and technical sections
- **OWASP Mapping** — Findings mapped to OWASP Top 10 categories
- **Threat Modeling** — Asset identification, threat scenarios, defensive observations

---

## Project Structure

```
sentinellab/
├── backend/               # FastAPI security analysis API
│   ├── app/
│   │   ├── models/        # SQLAlchemy database models
│   │   ├── routers/       # API route handlers
│   │   ├── services/      # Detection, parsing, reporting logic
│   │   └── schemas/       # Pydantic validation schemas
│   └── tests/             # pytest test suite
├── frontend/              # React + Vite SOC dashboard
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
├── vulnerable-lab/        # Intentionally vulnerable Flask app (TARGET)
├── security-analysis/     # Standalone analysis tools
│   ├── pcap/              # PCAP analyzer
│   ├── logs/              # Log parser
│   └── detection/         # Detection engine + YAML rules
├── sample-data/           # Synthetic test data (PCAP, logs, reports)
├── docs/                  # Learning documentation
├── reports/               # Generated incident reports (gitignored)
└── screenshots/           # Dashboard screenshots
```

---

## Quick Start

> 📋 **Prerequisites**: Python 3.11+, Node.js 20+, Wireshark (with Npcap), Nmap, Git

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/sentinellab.git
cd sentinellab
```

### 2. Start the Vulnerable Lab (Target)
```bash
cd vulnerable-lab
pip install -r requirements.txt
python app.py
# Vulnerable app running at http://localhost:5000
```

### 3. Start the Backend API
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# API running at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 4. Start the Dashboard
```bash
cd frontend
npm install
npm run dev
# Dashboard at http://localhost:5173
```

See [`docs/lab-setup.md`](docs/lab-setup.md) for detailed setup instructions.

---

## Running the Lab

### Capture Traffic
```bash
# Start Wireshark and capture on the loopback adapter (127.0.0.1)
# Apply filter: host 127.0.0.1 and port 5000
```

### Analyze a PCAP File
```bash
cd security-analysis/pcap
python analyzer.py --file ../../sample-data/pcap/brute_force_sample.pcap
```

### Run the Detection Engine
```bash
cd security-analysis/detection
python engine.py --log ../../sample-data/logs/sample_auth.log
```

### Generate an Incident Report
```bash
# Via API
curl http://localhost:8000/api/reports/1
```

### Run Tests
```bash
cd backend
pytest tests/ -v
```

---

## Documentation

| Document | Description |
|---|---|
| [`docs/architecture.md`](docs/architecture.md) | Full system architecture |
| [`docs/lab-setup.md`](docs/lab-setup.md) | Step-by-step environment setup |
| [`docs/detection-rules.md`](docs/detection-rules.md) | All detection rules explained |
| [`docs/incident-response.md`](docs/incident-response.md) | IR workflow guide |
| [`docs/wireshark-learning.md`](docs/wireshark-learning.md) | Wireshark primer for beginners |
| [`docs/kali-learning.md`](docs/kali-learning.md) | Kali Linux / terminal primer |
| [`docs/security-analyst-learning.md`](docs/security-analyst-learning.md) | SOC analyst concepts |
| [`docs/learning-notes.md`](docs/learning-notes.md) | Project learning journal |

---

## Example Findings

| ID | Title | Severity | OWASP Category |
|---|---|---|---|
| FIND-001 | No authentication rate limiting | HIGH | A07: Identification and Auth Failures |
| FIND-002 | Verbose error messages expose stack traces | MEDIUM | A05: Security Misconfiguration |
| FIND-003 | SQL injection surface in login endpoint | HIGH | A03: Injection |
| FIND-004 | Admin panel accessible without authorization | CRITICAL | A01: Broken Access Control |
| FIND-005 | Sensitive paths not protected | MEDIUM | A01: Broken Access Control |

---

## Screenshots

*Screenshots will be added as each component is completed.*

---

## Testing

```bash
cd backend
pytest tests/ -v --tb=short

# Expected output:
# tests/test_alerts.py          PASSED
# tests/test_incidents.py       PASSED
# tests/test_detection.py       PASSED
# tests/test_pcap.py            PASSED
# tests/test_log_parser.py      PASSED
# tests/test_severity.py        PASSED
# tests/test_reports.py         PASSED
```

---

## Limitations

This project is designed for educational purposes in a local laboratory environment. It has the following intentional limitations:

- **Detection engine is rule-based**, not machine learning. Rules are simple and educational, not production-grade.
- **PCAP analysis** targets HTTP/TCP/DNS. Advanced protocols are out of scope.
- **Vulnerable lab** demonstrates conceptual vulnerabilities only — not weaponized exploits.
- **Scale**: Designed for single-user local use. Not suitable for production deployment.
- **Nmap scanning** is configured for localhost only. No external scanning is implemented.

---

## Ethical Use & Legal Scope

```
┌──────────────────────────────────────────────────────────────────┐
│                    ⚠️  ETHICAL USE STATEMENT                      │
│                                                                  │
│  All security testing, scanning, and analysis in this project    │
│  is strictly limited to:                                         │
│                                                                  │
│    • localhost (127.0.0.1)                                       │
│    • Private, isolated lab networks you own and control          │
│    • Systems for which you have explicit written authorization   │
│                                                                  │
│  This project does NOT provide tools or instructions for:        │
│                                                                  │
│    • Unauthorized access to external systems                     │
│    • Attacks against public IP addresses or domains              │
│    • Credential theft, malware, or persistence mechanisms        │
│    • Any activity violating applicable computer crime laws       │
│                                                                  │
│  The vulnerable application must NEVER be deployed on a          │
│  public-facing server or network interface.                      │
└──────────────────────────────────────────────────────────────────┘
```

Applicable laws include but are not limited to: Computer Fraud and Abuse Act (CFAA, USA), Computer Misuse Act (UK), and equivalent legislation in your jurisdiction.

---

## License

MIT License — see [`LICENSE`](LICENSE) for full text and the ethical use statement.

---

<div align="center">

*Built for learning. Built for understanding. Built defensively.*

</div>
