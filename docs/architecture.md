# SentinelLab — System Architecture

*Detailed architecture documentation. Full diagrams and component descriptions will be added as each phase is completed.*

## Component Overview

| Component | Technology | Port | Role |
|---|---|---|---|
| Vulnerable Lab App | Python / Flask | 5000 | Monitored target (generates traffic + logs) |
| Security Analysis API | Python / FastAPI | 8000 | Core defender backend |
| React Dashboard | React / Vite | 5173 | SOC analyst interface |
| SQLite Database | SQLite | — | Persistent storage |

## Data Flow

```
Vulnerable App (Flask:5000)
    │
    ├─── HTTP Traffic ──────► tshark capture ──► .pcap files
    │                                                │
    │                                         PCAP Analyzer
    │                                                │
    └─── Application Logs ──► Log Parser ────► Normalized Events
                                                     │
                                            Detection Engine
                                                     │
                                           Alerts (SQLite DB)
                                                     │
                                         FastAPI Backend (8000)
                                                     │
                                         React Dashboard (5173)
```

## Directory Map

*(To be expanded in Phase 9)*
