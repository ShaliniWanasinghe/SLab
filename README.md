<div align="center">

# 🛡️ SentinelLab

### A Local Network Security Monitoring & Incident Analysis Lab

*A student-built cybersecurity project for learning and practicing security monitoring, traffic analysis, detection, and incident documentation.*

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square\&logo=python\&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat-square\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-61DAFB?style=flat-square\&logo=react\&logoColor=black)](https://react.dev)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat-square\&logo=sqlite\&logoColor=white)](https://sqlite.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)
[![Ethical Use](https://img.shields.io/badge/Scope-Local%20Lab%20Only-red?style=flat-square)](#ethical-use--legal-scope)

<img width="1917" height="867" alt="Screenshot 2026-10-06 083741" src="https://github.com/user-attachments/assets/bd825e61-c533-4c2d-a1ff-222e775fde6d" />


</div>

---

> ⚠️ **IMPORTANT:** All security testing in this project is intended for `localhost` and privately owned, isolated lab environments. The project should not be used to scan, probe, or interact with systems without authorization. See [Ethical Use & Legal Scope](#ethical-use--legal-scope).

---

## Overview

SentinelLab is a **local cybersecurity learning laboratory** that brings together several security concepts in one project. It combines network traffic capture, log analysis, rule-based detection, alert management, incident documentation, and report generation.

I built this as a hands-on cybersecurity learning project to strengthen my understanding of security monitoring, network traffic analysis, detection, and incident documentation.

The learning workflow is:

```text
Reconnaissance → Traffic Capture → Log Collection → Detection
→ Alert Review → Investigation → Evidence Analysis
→ Incident Documentation → Remediation Recommendations
```

## Architecture

```text
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

See [`docs/architecture.md`](docs/architecture.md) for more details.

---

## Technology Stack

| Layer            | Technology                  | Purpose                                                |
| ---------------- | --------------------------- | ------------------------------------------------------ |
| Monitored Target | Python / Flask              | Local intentionally vulnerable application for testing |
| Packet Analysis  | tshark / Wireshark / Scapy  | Traffic capture and PCAP analysis                      |
| Reconnaissance   | Nmap                        | Local service and port enumeration                     |
| Detection Engine | Python / YAML rules         | Rule-based security event detection                    |
| Backend API      | Python / FastAPI            | API for security data and analysis functions           |
| Database         | SQLite / SQLAlchemy         | Local storage for alerts, incidents, and findings      |
| Dashboard        | React / Vite                | Web interface for viewing security information         |
| Report Generator | Python / Jinja2 / ReportLab | Generation of incident documentation                   |
| Testing          | pytest / httpx              | Automated testing                                      |

---

## Security Concepts Practiced

This project provides hands-on practice with:

* **Network Reconnaissance** — Nmap-based port and service enumeration in a controlled lab
* **Packet Analysis** — Capturing and examining network traffic with Wireshark, tshark, and Scapy
* **Log Analysis** — Parsing and extracting security-relevant events from application logs
* **Detection Engineering** — Creating simple rule-based detection logic using patterns and thresholds
* **Alert Triage** — Assigning severity levels to detected events
* **Incident Response Concepts** — Applying a simplified incident-handling workflow
* **Evidence Handling** — Organizing evidence and linking it with incidents
* **Security Reporting** — Generating structured technical incident reports
* **OWASP Mapping** — Relating selected application findings to OWASP Top 10 categories
* **Threat Modeling** — Identifying assets, possible threat scenarios, and defensive considerations

---

## Project Structure

```text
sentinellab/
├── backend/               # FastAPI security analysis API
│   ├── app/
│   │   ├── models/        # SQLAlchemy database models
│   │   ├── routers/       # API route handlers
│   │   ├── services/      # Detection, parsing, and reporting logic
│   │   └── schemas/       # Pydantic validation schemas
│   └── tests/             # pytest test suite
├── frontend/              # React + Vite dashboard
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
├── vulnerable-lab/        # Intentionally vulnerable Flask application
├── security-analysis/     # Security analysis utilities
│   ├── pcap/              # PCAP analysis
│   ├── logs/              # Log parsing
│   └── detection/         # Detection engine and rules
├── sample-data/           # Synthetic test data
├── docs/                  # Project and learning documentation
├── reports/               # Generated reports (gitignored)
└── screenshots/           # Dashboard screenshots
```

---

## Quick Start

### Prerequisites

* Python 3.11+
* Node.js 20+
* Wireshark / tshark
* Nmap
* Git

### 1. Clone the Repository

```bash
git clone https://github.com/ShaliniWanasinghe/SLab.git
cd SLab
cd sentinellab
```

### 2. Start the Vulnerable Lab

```bash
cd vulnerable-lab
pip install -r requirements.txt
python app.py
```

The local application should be available at:

```text
http://localhost:5000
```

### 3. Start the Backend API

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### 4. Start the Dashboard

```bash
cd frontend
npm install
npm run dev
```

Dashboard:

```text
http://localhost:5173
```

For the complete setup process, see [`docs/lab-setup.md`](docs/lab-setup.md).

---

## Running the Lab

### Capture Traffic

Use Wireshark to capture traffic from the local loopback interface.

Example filter:

```text
host 127.0.0.1 and port 5000
```

### Analyze a PCAP File

```bash
cd security-analysis/pcap

python analyzer.py \
  --file ../../sample-data/pcap/brute_force_sample.pcap
```

### Run the Detection Engine

```bash
cd security-analysis/detection

python engine.py \
  --log ../../sample-data/logs/sample_auth.log
```

### Generate an Incident Report

```bash
curl http://localhost:8000/api/reports/1
```

### Run Tests

```bash
cd backend

pytest tests/ -v
```

---

## Documentation

| Document                                                                 | Description                                    |
| ------------------------------------------------------------------------ | ---------------------------------------------- |
| [`docs/architecture.md`](docs/architecture.md)                           | Project architecture                           |
| [`docs/lab-setup.md`](docs/lab-setup.md)                                 | Local environment setup                        |
| [`docs/detection-rules.md`](docs/detection-rules.md)                     | Detection rules and logic                      |
| [`docs/incident-response.md`](docs/incident-response.md)                 | Incident response concepts used in the project |
| [`docs/wireshark-learning.md`](docs/wireshark-learning.md)               | Wireshark learning notes                       |
| [`docs/kali-learning.md`](docs/kali-learning.md)                         | Kali Linux and terminal learning notes         |
| [`docs/security-analyst-learning.md`](docs/security-analyst-learning.md) | Security analyst concepts                      |
| [`docs/learning-notes.md`](docs/learning-notes.md)                       | Project learning journal                       |

---

## Example Lab Findings

The following are **simulated findings used within the local vulnerable application and sample data** to demonstrate how security observations can be documented.

| ID       | Example Finding                                        | Severity | OWASP Category                                  |
| -------- | ------------------------------------------------------ | -------- | ----------------------------------------------- |
| FIND-001 | Missing authentication rate limiting                   | HIGH     | A07: Identification and Authentication Failures |
| FIND-002 | Verbose error messages exposing stack traces           | MEDIUM   | A05: Security Misconfiguration                  |
| FIND-003 | SQL injection vulnerability in a test login endpoint   | HIGH     | A03: Injection                                  |
| FIND-004 | Test admin panel without proper authorization controls | CRITICAL | A01: Broken Access Control                      |
| FIND-005 | Unprotected sensitive test paths                       | MEDIUM   | A01: Broken Access Control                      |

> These findings are intentionally included in the lab for educational testing. They should not be interpreted as findings from a real-world security assessment.

---

## Screenshots

<div align= "center">
<img width="1655" height="857" alt="Screenshot 2026-10-06 083712" src="https://github.com/user-attachments/assets/d9d64210-dc71-401a-bd11-7f67f5b460b2" />
<br>
<img width="1658" height="852" alt="Screenshot 2026-10-06 083728" src="https://github.com/user-attachments/assets/21bbd4a5-0f57-435e-91a3-1e984714aff3" />

<br><br>
</div>  

---

## Testing

```bash
cd backend

pytest tests/ -v --tb=short
```

The test suite covers areas such as:

```text
tests/test_alerts.py
tests/test_incidents.py
tests/test_detection.py
tests/test_pcap.py
tests/test_log_parser.py
tests/test_severity.py
tests/test_reports.py
```

---

## Limitations

SentinelLab is a **student-developed educational project** and is not intended to replace a production SOC, SIEM, IDS, or incident response platform.

Current limitations include:

* **Rule-based detection** — Detection logic uses predefined patterns and thresholds rather than machine learning.
* **Limited protocol analysis** — PCAP analysis currently focuses on selected HTTP, TCP, and DNS traffic.
* **Controlled vulnerabilities** — The vulnerable application is designed to demonstrate security concepts in a local environment.
* **Local scale** — The project is intended for individual learning and experimentation rather than production or enterprise deployment.
* **Local scanning** — Nmap usage is restricted to the intended laboratory environment.

---

## Ethical Use & Legal Scope

```text
┌──────────────────────────────────────────────────────────────────┐
│                    ⚠️  ETHICAL USE STATEMENT                     │
│                                                                  │
│  This project is intended for authorized security testing in     │
│  controlled environments, including:                             │
│                                                                  │
│    • localhost (127.0.0.1)                                       │
│    • Private lab networks you own or are authorized to test     │
│    • Systems for which you have explicit permission             │
│                                                                  │
│  Do not use this project for unauthorized scanning, testing,     │
│  access, credential theft, malware deployment, or attacks        │
│  against systems you do not own or have permission to test.     │
│                                                                  │
│  The vulnerable application should never be exposed to a         │
│  public-facing network.                                         │
└──────────────────────────────────────────────────────────────────┘
```

Always follow the applicable laws, organizational policies, and authorization requirements when performing security testing.

---

## License

MIT License — see [`LICENSE`](LICENSE) for the full license text.

---

<div align="center">

*Built to learn. Built to practice. Built defensively.*

</div>
