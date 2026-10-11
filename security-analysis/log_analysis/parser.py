"""
parser.py — SentinelLab Log Parser
====================================

Reads raw application and auth logs, normalizing them into
a structured JSON format for the detection engine.
"""

import argparse
import json
import os
import re
from datetime import datetime

# Regex for Apache Combined Log Format (used by our Flask app middleware)
APACHE_LOG_REGEX = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d{3}) .* "(?P<user_agent>.*)"$'
)

def parse_access_log(file_path):
    events = []
    if not os.path.exists(file_path):
        return events
        
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
                
            match = APACHE_LOG_REGEX.match(line)
            if match:
                data = match.groupdict()
                events.append({
                    "timestamp": data['timestamp'],
                    "source": data['ip'],
                    "event_type": "http_request",
                    "method": data['method'],
                    "path": data['path'],
                    "status": int(data['status']),
                    "user_agent": data['user_agent'],
                    "raw": line
                })
    return events

def main():
    parser = argparse.ArgumentParser(description="SentinelLab Log Parser")
    parser.add_argument("--file", required=True, help="Path to access log file")
    args = parser.parse_args()
    
    events = parse_access_log(args.file)
    print(json.dumps({"events": events}, indent=2))

if __name__ == "__main__":
    main()
