"""
SentinelLab — Intentionally Vulnerable Web Application
=======================================================

⚠️  WARNING: This application is deliberately insecure.
    It exists ONLY for local cybersecurity education.
    NEVER deploy this on a public-facing server.
    See VULNERABLE_APP_WARNING.md for full ethical scope.

Each vulnerability is labeled with:
    [VULN-XXX] Description (OWASP Category)

Author:  SentinelLab Project
Purpose: Generate realistic, controllable attack traffic for security
         analysis exercises in an isolated local laboratory.
"""

import logging
import os
import sqlite3
from datetime import datetime
from functools import wraps

from flask import (
    Flask,
    g,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

# ─── Application Setup ────────────────────────────────────────────────────────

app = Flask(__name__)

# [VULN-002] Hardcoded, weak secret key.
# In production: use a long random key from environment variables.
# Here: intentionally weak so the lab is reproducible and simple.
app.secret_key = "sentinellab-not-secret-key-123"

# [VULN-002] Debug mode is ON — this causes Flask to expose full stack traces
# in the browser on any unhandled exception.
# In production: NEVER run debug=True.
app.config["DEBUG"] = True

# Database file — sits in the same directory as app.py
# Reset by running reset_lab.py
DATABASE = os.path.join(os.path.dirname(__file__), "lab_db.sqlite")

# ─── Application-level logging ────────────────────────────────────────────────
# These logs feed the SentinelLab Log Analyzer module.

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        # Console output
        logging.StreamHandler(),
        # File output — this is what the log analyzer reads
        logging.FileHandler(
            os.path.join(os.path.dirname(__file__), "lab_access.log")
        ),
    ],
)
logger = logging.getLogger("sentinellab.vuln_app")


# ─── Database Helpers ─────────────────────────────────────────────────────────


def get_db():
    """Get a database connection for the current request context."""
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Rows accessible by column name
    return db


@app.teardown_appcontext
def close_db(exception):
    """Close the database connection at the end of each request."""
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_db():
    """
    Initialize the lab database with tables and seed data.
    Called once when the application starts.
    """
    db = sqlite3.connect(DATABASE)
    cursor = db.cursor()

    # Users table
    # [VULN-004] Passwords are stored as plain text.
    # In production: use bcrypt or Argon2 for password hashing.
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT UNIQUE NOT NULL,
            password  TEXT NOT NULL,
            role      TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
    """
    )

    # Sensitive data table — represents valuable data the attacker wants
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sensitive_data (
            id    INTEGER PRIMARY KEY AUTOINCREMENT,
            label TEXT NOT NULL,
            value TEXT NOT NULL
        )
    """
    )

    # Auth log table — records every login attempt
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS auth_log (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp  TEXT NOT NULL,
            source_ip  TEXT NOT NULL,
            username   TEXT NOT NULL,
            success    INTEGER NOT NULL,
            user_agent TEXT
        )
    """
    )

    # Seed users (only if table is empty)
    existing = cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing == 0:
        now = datetime.utcnow().isoformat()
        cursor.executemany(
            "INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)",
            [
                # [VULN-004] Plain text passwords — intentional for lab
                ("admin", "admin123", "admin", now),
                ("alice", "password", "user", now),
                ("bob", "letmein", "user", now),
            ],
        )
        # Seed some "sensitive" data to make the app realistic
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
    logger.info("Lab database initialized successfully.")


# ─── Request Logging Middleware ───────────────────────────────────────────────
# Every HTTP request is logged. This is the primary data source for the
# Log Analyzer module (Phase 6).


@app.before_request
def log_request():
    """Log every incoming HTTP request in Apache Combined Log Format."""
    logger.info(
        '%s - - [%s] "%s %s %s" - "%s" "%s"',
        request.remote_addr,
        datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S +0000"),
        request.method,
        request.path,
        request.environ.get("SERVER_PROTOCOL", "HTTP/1.1"),
        request.referrer or "-",
        request.user_agent.string or "-",
    )


# ─── Authentication Helper ────────────────────────────────────────────────────


def login_required(f):
    """Decorator: require a valid login session to access a route."""

    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            logger.warning(
                "Unauthenticated access attempt to %s from %s",
                request.path,
                request.remote_addr,
            )
            return redirect(url_for("login_page"))
        return f(*args, **kwargs)

    return decorated


# ─── Routes ───────────────────────────────────────────────────────────────────


@app.route("/")
def index():
    """Home page — redirect to dashboard if logged in, else login."""
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login_page"))


# ── Authentication ────────────────────────────────────────────────────────────


@app.route("/login", methods=["GET"])
def login_page():
    """Render the login form."""
    error = request.args.get("error")
    return render_template("login.html", error=error)


@app.route("/login", methods=["POST"])
def login_submit():
    """
    Handle login form submission.

    [VULN-001] BROKEN AUTH — No rate limiting.
    An attacker can submit thousands of login attempts per second.
    A secure application would:
      - Lock an account after N failures
      - Implement exponential backoff
      - Use CAPTCHA for repeated failures
      - Alert on anomalous login patterns

    [VULN-004] INJECTION SURFACE — SQL built via string concatenation.
    The query below constructs SQL by directly inserting user input.
    Input like: username = admin'-- will manipulate the SQL structure.
    A secure application would use parameterized queries (shown in comment).
    """
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    source_ip = request.remote_addr
    user_agent = request.user_agent.string

    db = get_db()

    # ────────────────────────────────────────────────────────────────────────
    # [VULN-004] INTENTIONALLY UNSAFE SQL — DO NOT USE THIS PATTERN IN REAL CODE
    #
    # This query is vulnerable to SQL injection because user input is
    # embedded directly into the SQL string using Python string formatting.
    #
    # Example attack input:
    #   username = admin'--
    #   The resulting SQL becomes:
    #   SELECT * FROM users WHERE username='admin'--' AND password='...'
    #   The '--' comments out the password check → login succeeds without password.
    #
    # SECURE version (parameterized query — use this in real applications):
    #   cursor.execute(
    #       "SELECT * FROM users WHERE username = ? AND password = ?",
    #       (username, password)
    #   )
    # ────────────────────────────────────────────────────────────────────────
    try:
        cursor = db.execute(
            f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"  # noqa: S608
        )
        user = cursor.fetchone()
    except sqlite3.OperationalError as e:
        # [VULN-002] VERBOSE ERROR — exposes internal SQL error to the user.
        # A secure app would log this privately and show a generic message.
        logger.error("SQL error during login: %s (input: %s)", e, username)
        return render_template(
            "login.html",
            error=f"Database error: {e}",  # Intentionally verbose
        )

    # Log the authentication attempt to the database
    now = datetime.utcnow().isoformat()
    if user:
        # Successful login
        db.execute(
            "INSERT INTO auth_log (timestamp, source_ip, username, success, user_agent) VALUES (?, ?, ?, ?, ?)",
            (now, source_ip, username, 1, user_agent),
        )
        db.commit()
        session["user_id"] = user["id"]
        session["username"] = user["username"]
        session["role"] = user["role"]
        logger.info("AUTH_SUCCESS: user=%s source=%s", username, source_ip)
        return redirect(url_for("dashboard"))
    else:
        # Failed login
        db.execute(
            "INSERT INTO auth_log (timestamp, source_ip, username, success, user_agent) VALUES (?, ?, ?, ?, ?)",
            (now, source_ip, username, 0, user_agent),
        )
        db.commit()
        logger.warning(
            "AUTH_FAILURE: user=%s source=%s ua=%s", username, source_ip, user_agent
        )
        return render_template(
            "login.html",
            error="Invalid username or password.",
        )


@app.route("/logout")
def logout():
    """Clear the session and redirect to login."""
    username = session.get("username", "unknown")
    session.clear()
    logger.info("LOGOUT: user=%s source=%s", username, request.remote_addr)
    return redirect(url_for("login_page"))


# ── Protected Pages ───────────────────────────────────────────────────────────


@app.route("/dashboard")
@login_required
def dashboard():
    """
    Main user dashboard — requires authentication.
    This is the 'protected' area of the application.
    """
    db = get_db()
    # Fetch recent auth log entries (last 20)
    recent_logins = db.execute(
        "SELECT * FROM auth_log ORDER BY timestamp DESC LIMIT 20"
    ).fetchall()
    return render_template(
        "dashboard.html",
        username=session.get("username"),
        role=session.get("role"),
        recent_logins=recent_logins,
    )


# ── Admin Panel ───────────────────────────────────────────────────────────────


@app.route("/admin")
def admin_panel():
    """
    Admin panel showing sensitive application data.

    [VULN-003] BROKEN ACCESS CONTROL — Insufficient authorization check.
    This route checks only that SOMEONE is logged in, not that they
    are an administrator. Any authenticated user can access admin data.

    Furthermore, the check is trivially bypassable by manipulating the
    session cookie (since our secret key is weak — see VULN-002).

    A secure application would:
      - Check: session.get('role') == 'admin'
      - Use server-side session validation
      - Log all admin panel access attempts
      - Use a strong, randomly generated secret key
    """
    # [VULN-003] Only checks login, NOT role == 'admin'
    if "user_id" not in session:
        logger.warning(
            "UNAUTH_ADMIN_ACCESS: source=%s path=/admin", request.remote_addr
        )
        return redirect(url_for("login_page"))

    # Any logged-in user reaches here — including non-admins
    logger.warning(
        "ADMIN_ACCESS: user=%s role=%s source=%s",
        session.get("username"),
        session.get("role"),
        request.remote_addr,
    )

    db = get_db()
    users = db.execute("SELECT id, username, role, created_at FROM users").fetchall()
    sensitive = db.execute("SELECT * FROM sensitive_data").fetchall()
    return render_template(
        "admin.html",
        users=users,
        sensitive=sensitive,
        username=session.get("username"),
        role=session.get("role"),
    )


# ── Debug / Info Endpoints ────────────────────────────────────────────────────


@app.route("/debug")
def debug_info():
    """
    [VULN-002] SECURITY MISCONFIGURATION — Exposes internal configuration.

    This endpoint returns application internals: environment variables,
    request headers, and session data. In a real attack, this gives an
    attacker a blueprint of the application.

    A secure application would:
      - Remove debug endpoints entirely before production
      - Require strong authentication for any diagnostic endpoints
      - Never expose environment variables or session data to users
    """
    logger.warning(
        "DEBUG_ENDPOINT_ACCESS: source=%s ua=%s",
        request.remote_addr,
        request.user_agent.string,
    )

    # [VULN-002] Intentionally verbose — exposes internals
    debug_data = {
        "warning": "THIS ENDPOINT IS INTENTIONALLY VULNERABLE — EDUCATIONAL USE ONLY",
        "application": {
            "name": "SentinelLab Vulnerable Lab",
            "debug_mode": app.config.get("DEBUG"),
            "secret_key_hint": app.secret_key[:8] + "...",  # Partial leak
            "database": DATABASE,
        },
        "request": {
            "method": request.method,
            "path": request.path,
            "remote_addr": request.remote_addr,
            "headers": dict(request.headers),
            "args": dict(request.args),
        },
        "session": dict(session),  # Exposes full session data
        "environment": {
            k: v
            for k, v in os.environ.items()
            if k.startswith(("FLASK", "PYTHON", "PATH"))
        },
    }
    return jsonify(debug_data)


# ── API Endpoints ─────────────────────────────────────────────────────────────


@app.route("/api/status")
def api_status():
    """Public API status endpoint — no authentication required."""
    return jsonify(
        {
            "status": "running",
            "application": "SentinelLab Vulnerable Lab",
            "version": "1.0.0",
            "timestamp": datetime.utcnow().isoformat(),
            "lab_mode": "vulnerable",
            # [VULN-002] Exposes internal path — shouldn't be public
            "database_path": DATABASE,
        }
    )


@app.route("/api/users")
def api_users():
    """
    [VULN-005] BROKEN ACCESS CONTROL — Sensitive data with no authentication.

    This endpoint returns user account information without requiring
    any login. In a real application, user data is private and should
    require authentication + authorization.

    A secure application would:
      - Require a valid authenticated session
      - Return only the data the requesting user is authorized to see
      - Never expose password fields (even hashed)
    """
    logger.warning(
        "UNAUTH_API_ACCESS: path=/api/users source=%s", request.remote_addr
    )
    db = get_db()
    # [VULN-005] Returns username and role to unauthenticated caller
    # [VULN-004] Also leaks that passwords exist as a field (not returned here
    #            but schema is implied)
    users = db.execute("SELECT id, username, role, created_at FROM users").fetchall()
    return jsonify(
        {
            "warning": "INTENTIONALLY VULNERABLE — EDUCATIONAL USE ONLY",
            "users": [dict(u) for u in users],
        }
    )


@app.route("/api/logs")
def api_logs():
    """
    [VULN-005] Authentication log accessible without authorization.

    Returns authentication history — which usernames were tried,
    whether attempts succeeded, and source IPs. In a real attack
    this gives an attacker enumeration information.
    """
    logger.warning(
        "UNAUTH_API_ACCESS: path=/api/logs source=%s", request.remote_addr
    )
    db = get_db()
    logs = db.execute(
        "SELECT timestamp, source_ip, username, success FROM auth_log ORDER BY timestamp DESC LIMIT 50"
    ).fetchall()
    return jsonify(
        {
            "warning": "INTENTIONALLY VULNERABLE — EDUCATIONAL USE ONLY",
            "auth_log": [dict(entry) for entry in logs],
        }
    )


# ── Lab Reset ─────────────────────────────────────────────────────────────────


@app.route("/reset", methods=["POST"])
def reset_lab():
    """
    Reset the lab database to its initial state.
    Clears all auth log entries, restores seed data.
    The application log file is NOT cleared (it is evidence).
    """
    logger.info("LAB_RESET: Resetting database. source=%s", request.remote_addr)
    db = get_db()

    # Clear auth log
    db.execute("DELETE FROM auth_log")

    # Clear and re-seed users
    db.execute("DELETE FROM users")
    now = datetime.utcnow().isoformat()
    db.executemany(
        "INSERT INTO users (username, password, role, created_at) VALUES (?, ?, ?, ?)",
        [
            ("admin", "admin123", "admin", now),
            ("alice", "password", "user", now),
            ("bob", "letmein", "user", now),
        ],
    )

    # Clear and re-seed sensitive data
    db.execute("DELETE FROM sensitive_data")
    db.executemany(
        "INSERT INTO sensitive_data (label, value) VALUES (?, ?)",
        [
            ("Internal API Key", "sk-lab-fake-key-do-not-use-xyz"),
            ("Database Connection", "sqlite:///lab_db.sqlite"),
            ("Admin Email", "admin@sentinellab.local"),
        ],
    )

    db.commit()
    session.clear()
    logger.info("LAB_RESET: Complete. Database restored to initial state.")
    return jsonify({"status": "reset_complete", "message": "Lab database reset."})


# ─── Application Entry Point ──────────────────────────────────────────────────

if __name__ == "__main__":
    # Initialize database on startup
    if not os.path.exists(DATABASE):
        logger.info("Database not found. Initializing...")
        init_db()
    else:
        logger.info("Database found at %s", DATABASE)
        # Ensure schema is up to date
        init_db()

    logger.info("=" * 60)
    logger.info("  SentinelLab Vulnerable Lab Starting")
    logger.info("  ⚠️  FOR LOCAL EDUCATIONAL USE ONLY")
    logger.info("  Binding to 127.0.0.1:5000 (localhost only)")
    logger.info("=" * 60)

    # IMPORTANT: Binds to 127.0.0.1 ONLY — not 0.0.0.0
    # This ensures the app is never accidentally accessible from the network
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,  # [VULN-002] Debug intentionally on for lab visibility
        use_reloader=True,
    )
