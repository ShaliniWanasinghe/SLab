"""
generate_traffic.py — SentinelLab Traffic Generator
====================================================

Generates realistic HTTP traffic against the vulnerable lab application.
This produces the log entries and network traffic that the SentinelLab
detection engine and PCAP analyzer are designed to detect.

Use this script to:
  1. Generate sample traffic for log analysis (Phase 6)
  2. Produce traffic to capture with Wireshark (Phase 4)
  3. Trigger detection engine rules (Phase 7)

⚠️  Only runs against localhost:5000 — the local lab only.

Usage:
    python generate_traffic.py --scenario all
    python generate_traffic.py --scenario brute_force
    python generate_traffic.py --scenario normal
    python generate_traffic.py --scenario path_probe

Scenarios:
    normal       — Normal login + browse (baseline traffic)
    brute_force  — Rapid repeated failed login attempts
    path_probe   — Requests to admin/debug/sensitive paths
    all          — Run all scenarios in sequence (recommended)
"""

import argparse
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

# Target — LOCAL LAB ONLY. Never change this to an external address.
LAB_BASE_URL = "http://127.0.0.1:5000"


def log(message: str) -> None:
    """Print a timestamped status message."""
    ts = datetime.utcnow().strftime("%H:%M:%S")
    print(f"[{ts}] {message}")


def http_post(path: str, data: dict, label: str = "") -> tuple[int, str]:
    """
    Make an HTTP POST request to the lab application.
    Returns (status_code, response_body).
    """
    url = f"{LAB_BASE_URL}{path}"
    encoded = urllib.parse.urlencode(data).encode("utf-8")
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": f"SentinelLab-TrafficGen/1.0 ({label})",
    }
    req = urllib.request.Request(url, data=encoded, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read(512).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except urllib.error.URLError as e:
        return 0, str(e)


def http_get(path: str, label: str = "") -> tuple[int, str]:
    """
    Make an HTTP GET request to the lab application.
    Returns (status_code, response_body).
    """
    url = f"{LAB_BASE_URL}{path}"
    headers = {"User-Agent": f"SentinelLab-TrafficGen/1.0 ({label})"}
    req = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            return resp.status, resp.read(256).decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except urllib.error.URLError as e:
        return 0, str(e)


# ─── Scenarios ────────────────────────────────────────────────────────────────


def scenario_normal_traffic():
    """
    Scenario: Normal user activity (baseline traffic).

    What this generates:
      - GET /  (home page)
      - GET /login  (login page load)
      - POST /login  (successful login)
      - GET /dashboard  (authenticated browsing)
      - GET /logout
    """
    print()
    log("=" * 50)
    log("SCENARIO: Normal Traffic (Baseline)")
    log("=" * 50)

    log("GET / ...")
    status, _ = http_get("/", label="normal")
    log(f"  → {status}")

    time.sleep(0.5)

    log("GET /login ...")
    status, _ = http_get("/login", label="normal")
    log(f"  → {status}")

    time.sleep(0.8)

    log("POST /login (admin / admin123) ...")
    status, _ = http_post(
        "/login",
        {"username": "admin", "password": "admin123"},
        label="normal-login",
    )
    log(f"  → {status} ({'SUCCESS' if status == 200 else 'REDIRECT/FAILURE'})")

    time.sleep(1)

    log("GET /api/status ...")
    status, body = http_get("/api/status", label="normal")
    log(f"  → {status}")

    time.sleep(0.5)

    log("Normal traffic scenario complete. ✓")


def scenario_brute_force():
    """
    Scenario: Credential brute force attack.

    What this generates:
      - Rapid repeated POST /login with wrong passwords
      - Triggered detection: RULE-001 (auth failure threshold)
      - Triggered alert severity: MEDIUM → HIGH

    This is the primary test for the detection engine's
    authentication failure rule.
    """
    print()
    log("=" * 50)
    log("SCENARIO: Brute Force Login Attack")
    log("⚠️  Triggering detection rules...")
    log("=" * 50)

    # Common passwords an attacker might try
    # These are fictional/commonly known weak passwords — not real credentials
    password_attempts = [
        "123456",
        "password",
        "qwerty",
        "letmein",
        "monkey",
        "dragon",
        "1234567",
        "baseball",
        "iloveyou",
        "trustno1",
        "sunshine",
        "master",
        "hello",
        "shadow",
        "superman",
        "michael",
    ]

    log(f"Attempting {len(password_attempts)} passwords for 'admin' account...")
    failures = 0

    for i, pwd in enumerate(password_attempts, 1):
        status, _ = http_post(
            "/login",
            {"username": "admin", "password": pwd},
            label="brute-force",
        )
        result = "✓ SUCCESS" if status in (200, 302) else "✗ FAIL"
        log(f"  Attempt {i:02d}: admin / {'*' * len(pwd):<12} → {status} {result}")
        failures += 1 if status not in (200, 302) else 0
        # Small delay between attempts (realistic attacker behavior)
        time.sleep(0.1)

    log(f"Brute force complete. Failures: {failures}/{len(password_attempts)}")
    log("→ Check SentinelLab dashboard — RULE-001 should have fired!")


def scenario_path_probe():
    """
    Scenario: Attacker probing sensitive paths.

    What this generates:
      - GET requests to admin, debug, and sensitive API paths
      - Mix of authenticated and unauthenticated access attempts
      - Triggered detection: RULE-002 (suspicious path access)
    """
    print()
    log("=" * 50)
    log("SCENARIO: Sensitive Path Probing")
    log("⚠️  Triggering path-based detection rules...")
    log("=" * 50)

    # Paths an attacker might probe
    probe_paths = [
        "/admin",
        "/debug",
        "/api/users",
        "/api/logs",
        "/config",
        "/env",
        "/backup",
        "/.env",
        "/admin/users",
        "/api/admin",
    ]

    log(f"Probing {len(probe_paths)} paths (unauthenticated)...")
    for path in probe_paths:
        status, _ = http_get(path, label="path-probe")
        log(f"  GET {path:<25} → {status}")
        time.sleep(0.15)

    log("Path probe complete.")
    log("→ Check SentinelLab dashboard — RULE-002 should have fired!")


def scenario_all():
    """Run all scenarios in sequence with pauses between them."""
    print()
    log("Running ALL scenarios...")
    log("Make sure Wireshark is capturing on the loopback adapter!")
    time.sleep(2)

    scenario_normal_traffic()
    time.sleep(2)

    scenario_brute_force()
    time.sleep(2)

    scenario_path_probe()

    print()
    log("=" * 50)
    log("All scenarios complete!")
    log("")
    log("Next steps:")
    log("  1. Stop your Wireshark capture and save as .pcap")
    log("  2. Run: python security-analysis/pcap/analyzer.py --file <your.pcap>")
    log("  3. Check the SentinelLab dashboard for alerts")
    log("=" * 50)


# ─── Entry Point ──────────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="SentinelLab Traffic Generator — generates lab traffic for security analysis"
    )
    parser.add_argument(
        "--scenario",
        choices=["normal", "brute_force", "path_probe", "all"],
        default="all",
        help="Which traffic scenario to generate (default: all)",
    )
    args = parser.parse_args()

    print()
    print("=" * 60)
    print("  SentinelLab Traffic Generator")
    print("  Target: http://127.0.0.1:5000 (LOCAL LAB ONLY)")
    print("=" * 60)

    # Verify the lab is running
    status, _ = http_get("/api/status", label="health-check")
    if status == 0:
        print()
        print("ERROR: Cannot reach the vulnerable lab at http://127.0.0.1:5000")
        print("Start the lab first:  python vulnerable-lab/app.py")
        return

    log(f"Lab reachable (status: {status}). Starting scenario: {args.scenario}")

    scenarios = {
        "normal": scenario_normal_traffic,
        "brute_force": scenario_brute_force,
        "path_probe": scenario_path_probe,
        "all": scenario_all,
    }

    scenarios[args.scenario]()


if __name__ == "__main__":
    main()
