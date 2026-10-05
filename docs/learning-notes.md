# SentinelLab — My Learning Journal

## About This Document

This is a personal learning journal for the SentinelLab project. I use it to:

- Record things I learned in each phase
- Note concepts that were confusing at first and how I resolved them
- Track questions I want to research further
- Record "aha moments" — concepts that suddenly clicked

This journal is committed to the repository intentionally. For a hiring manager
or reviewer, it demonstrates genuine learning depth and intellectual honesty.

---

## Phase 0 — Architecture Planning

**Date**: 2026-10-05

**What I learned today**:

- The difference between a Security Event, an Alert, and an Incident:
  - **Event**: Any observable occurrence in a system (a login attempt, a packet)
  - **Alert**: An event that a detection rule has flagged as potentially suspicious
  - **Incident**: A confirmed or probable security problem that requires a response

- A SOC (Security Operations Center) is a team responsible for monitoring,
  detecting, and responding to security events. SentinelLab simulates what
  the tools in a small SOC might look like.

- Rule-based detection is more explainable than ML-based detection for my
  current level. Every alert can be traced to a specific rule and a specific
  piece of evidence. This is important for triage.

**Questions to research**:

- [ ] What is the difference between a SIEM and an IDS/IPS?
- [ ] What does "alert fatigue" mean in practice, and how do SOC teams manage it?
- [ ] What is the MITRE ATT&CK framework and how do detection rules map to it?

**Resources I found helpful**:

- NIST SP 800-61 Rev 2 (Computer Security Incident Handling Guide)
- OWASP Top 10 (https://owasp.org/www-project-top-ten/)

---

## Phase 1 — Repository Setup

**Date**: *(to be filled)*

**What I learned today**:

*(Add your notes here after completing Phase 1)*

**Concepts that were new to me**:

*(Add concepts here)*

**Questions to research**:

*(Add questions here)*

---

## Phase 2 — Vulnerable Lab Application

*(To be filled after Phase 2)*

---

## Phase 3 — Reconnaissance

*(To be filled after Phase 3)*

---

## Phase 4 — Wireshark / PCAP Workflow

*(To be filled after Phase 4)*

---

## Phase 5 — PCAP Analyzer

*(To be filled after Phase 5)*

---

## Phase 6 — Log Analyzer

*(To be filled after Phase 6)*

---

## Phase 7 — Detection Engine

*(To be filled after Phase 7)*

---

## Phase 8 — Incident Management

*(To be filled after Phase 8)*

---

## Phase 9 — FastAPI Backend

*(To be filled after Phase 9)*

---

## Phase 10 — React Dashboard

*(To be filled after Phase 10)*

---

## Phase 11 — Report Generator

*(To be filled after Phase 11)*

---

## Key Concepts I Now Understand

*(Build this list as you progress through the project)*

- [ ] CIA Triad
- [ ] TCP/IP networking basics
- [ ] HTTP request/response cycle
- [ ] Network packet structure
- [ ] PCAP file format
- [ ] Port scanning and what results mean defensively
- [ ] Log normalization
- [ ] Detection rule anatomy
- [ ] Alert triage methodology
- [ ] Incident response lifecycle
- [ ] Evidence chain of custody
- [ ] OWASP Top 10 categories
- [ ] SQL injection concept
- [ ] Brute force attack pattern
- [ ] Path traversal concept

---

## Recommended Next Steps After This Project

- [ ] TryHackMe SOC Level 1 learning path
- [ ] Blue Team Labs Online (free tier)
- [ ] Splunk free training (SIEM hands-on experience)
- [ ] CompTIA Security+ study
- [ ] SANS reading room — incident response papers
