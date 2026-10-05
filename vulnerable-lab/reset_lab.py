"""
reset_lab.py — SentinelLab Vulnerable Lab Reset Script
=======================================================

Resets the lab database and application log to their initial state.
Run this between exercises to start fresh.

Usage:
    python reset_lab.py

What it does:
    1. Deletes the SQLite database
    2. Re-creates and re-seeds it with default users and data
    3. Clears the application log file
    4. Confirms reset is complete
"""

import os
import sqlite3
from datetime import datetime

# Paths (relative to this file's directory)
HERE = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(HERE, "lab_db.sqlite")
LOG_FILE = os.path.join(HERE, "lab_access.log")


def reset_database():
    """Drop and recreate the lab database with seed data."""
    print("[*] Removing existing database...")
    if os.path.exists(DATABASE):
        os.remove(DATABASE)
        print(f"    Deleted: {DATABASE}")

    print("[*] Creating fresh database...")
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Recreate schema
    cursor.executescript(
        """
        CREATE TABLE users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT UNIQUE NOT NULL,
            password  TEXT NOT NULL,
            role      TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        );

        CREATE TABLE sensitive_data (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            value TEXT NOT NULL
        );

        CREATE TABLE auth_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp  TEXT NOT NULL,
            source_ip  TEXT NOT NULL,
            username   TEXT NOT NULL,
            success    INTEGER NOT NULL,
            user_agent TEXT
        );
    """
    )

    # Seed users
    now = datetime.utcnow().isoformat()
    cursor.executemany(
        "INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)",
        [
            ("admin", "admin123", "admin", now),
            ("alice", "password", "user", now),
            ("bob", "letmein", "user", now),
        ],
    )

    # Seed sensitive data
    cursor.executemany(
        "INSERT INTO sensitive_data (label, value) VALUES (?, ?)",
        [
            ("Internal API Key", "sk-lab-fake-key-do-not-use-xyz"),
            ("Database Connection", "sqlite:///lab_db.sqlite"),
            ("Admin Email", "admin@sentinellab.local"),
        ],
    )

    db.commit()
    db.close()
    print("    Database initialized with 3 users and sample sensitive data.")


def reset_log():
    """Clear the application log file."""
    print("[*] Resetting application log...")
    with open(LOG_FILE, "w") as f:
        f.write(
            f"# Lab log cleared at {datetime.utcnow().isoformat()} by reset_lab.py\n"
        )
    print(f"    Log cleared: {LOG_FILE}")


def main():
    print()
    print("=" * 60)
    print("  SentinelLab — Lab Reset Script")
    print("=" * 60)
    print()

    reset_database()
    reset_log()

    print()
    print("=" * 60)
    print("  ✅ Reset complete!")
    print()
    print("  Default credentials:")
    print("    admin  / admin123  (role: admin)")
    print("    alice  / password  (role: user)")
    print("    bob    / letmein   (role: user)")
    print()
    print("  Start the lab:  python app.py")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
