# Sample Security Logs

These log files are SYNTHETIC and generated for educational purposes.
They simulate what real application and authentication logs look like.

## Files

### sample_access.log
Simulated Apache Combined Log Format access log.
Contains a mix of normal traffic and a simulated brute force attack.

Format:
  IP - - [timestamp] "METHOD path HTTP/version" status size "referer" "user-agent"

Example:
  127.0.0.1 - - [05/Oct/2026:15:00:01 +0000] "POST /login HTTP/1.1" 401 143 "-" "curl/7.88.1"

### sample_auth.log
Simulated Linux PAM authentication log format.
Contains a pattern of repeated authentication failures.

Format:
  Month Day HH:MM:SS hostname service[PID]: message

Example:
  Oct  5 15:00:01 sentinellab sshd[1234]: Failed password for admin from 127.0.0.1 port 45678 ssh2

## Usage

Parse these logs with the SentinelLab log analyzer:
  python security-analysis/logs/parser.py --file sample-data/logs/sample_access.log

Logs will be added in Phase 6.
