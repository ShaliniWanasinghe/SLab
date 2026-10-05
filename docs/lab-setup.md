# SentinelLab — Lab Setup Guide

## Prerequisites

| Software | Version | Download |
|---|---|---|
| Python | 3.11+ | https://python.org |
| Node.js | 20 LTS+ | https://nodejs.org |
| Git | Latest | https://git-scm.com |
| Wireshark | Latest | https://wireshark.org |
| Nmap | Latest | https://nmap.org |
| VS Code | Latest | https://code.visualstudio.com |
| DB Browser for SQLite | Latest | https://sqlitebrowser.org |

## Step 1 — Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/sentinellab.git
cd sentinellab
```

## Step 2 — Start the Vulnerable Lab Application

The vulnerable lab is the *target* — the system being monitored.

```bash
cd vulnerable-lab
pip install -r requirements.txt
python app.py
```

The app runs at **http://localhost:5000**

> ⚠️ Never expose this application outside localhost.

## Step 3 — Start the Backend API

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API available at **http://localhost:8000**
Interactive docs at **http://localhost:8000/docs**

## Step 4 — Start the Dashboard

```bash
cd frontend
npm install
npm run dev
```

Dashboard at **http://localhost:5173**

## Step 5 — Verify Everything Is Running

Open three terminal windows. After starting all components, visit:
- http://localhost:5000 — should show the vulnerable lab login page
- http://localhost:8000/docs — should show FastAPI interactive docs
- http://localhost:5173 — should show the SentinelLab dashboard

## Capturing Traffic

1. Open Wireshark
2. Select the **Npcap Loopback Adapter** (Windows) or **lo** (Linux)
3. Apply capture filter: `host 127.0.0.1`
4. Start capture, then interact with localhost:5000
5. Save capture as `.pcap` when done

## Running Tests

```bash
cd backend
pytest tests/ -v
```

*(Full setup details will be expanded as each phase is completed)*
