"""
engine.py — SentinelLab Detection Engine
==========================================

Evaluates normalized security events against YAML detection rules.
Outputs alerts when thresholds or patterns are matched.
"""

import argparse
import json
import re
import sys
import yaml
from collections import defaultdict
from datetime import datetime

class DetectionEngine:
    def __init__(self, rules_file):
        with open(rules_file, 'r') as f:
            data = yaml.safe_load(f)
            self.rules = data.get('rules', [])
            
        self.state = defaultdict(list) # rule_id -> {group_key -> [timestamps]}
        
    def evaluate_event(self, event):
        alerts = []
        for rule in self.rules:
            if rule['type'] == 'pattern':
                if self._match_pattern(rule, event):
                    alerts.append(self._generate_alert(rule, event, event.get('source')))
            elif rule['type'] == 'threshold':
                if self._match_condition(rule['condition'], event):
                    group_val = event.get(rule.get('group_by', 'source'))
                    if group_val:
                        alert = self._update_threshold(rule, group_val, event)
                        if alert:
                            alerts.append(alert)
        return alerts
        
    def _match_pattern(self, rule, event):
        cond = rule['condition']
        if event.get('event_type') != cond.get('event_type'):
            return False
            
        path = event.get('path', '')
        for pattern in cond.get('path_matches', []):
            if re.search(pattern, path):
                return True
        return False
        
    def _match_condition(self, condition, event):
        for k, v in condition.items():
            if event.get(k) != v:
                return False
        return True
        
    def _update_threshold(self, rule, group_val, event):
        rule_id = rule['id']
        now = datetime.utcnow()
        # For simulation, we assume events are processed live, but we just count them
        self.state[rule_id][group_val].append(now)
        
        count = len(self.state[rule_id][group_val])
        if count == rule['threshold']:
            return self._generate_alert(rule, event, group_val, count)
        elif count == rule.get('escalate_threshold', -1):
            alert = self._generate_alert(rule, event, group_val, count)
            alert['severity'] = rule['escalate_to']
            return alert
        return None

    def _generate_alert(self, rule, event, group_val, count=1):
        return {
            "alert_id": f"ALT-{int(datetime.utcnow().timestamp())}",
            "timestamp": datetime.utcnow().isoformat(),
            "rule_id": rule['id'],
            "rule_name": rule['name'],
            "source": group_val,
            "severity": rule['severity'],
            "evidence": json.dumps(event),
            "analyst_action": rule['analyst_action']
        }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules", required=True)
    parser.add_argument("--events", required=True, help="JSON file of parsed events")
    parser.add_argument("--api", help="Optional URL of the Alerts API to push alerts to (e.g., http://127.0.0.1:8000/api/alerts/)")
    args = parser.parse_args()
    
    engine = DetectionEngine(args.rules)
    
    with open(args.events, 'r') as f:
        data = json.load(f)
        events = data.get('events', [])
        
    all_alerts = []
    for evt in events:
        alerts = engine.evaluate_event(evt)
        all_alerts.extend(alerts)
        
    print(json.dumps({"alerts": all_alerts}, indent=2))

    if args.api:
        import urllib.request
        import urllib.error
        
        print(f"[*] Pushing {len(all_alerts)} alerts to {args.api}...")
        for alert in all_alerts:
            # Drop alert_id and timestamp since the backend generates them
            api_alert = {
                "rule_id": alert["rule_id"],
                "rule_name": alert["rule_name"],
                "source": alert["source"],
                "severity": alert["severity"],
                "evidence": alert["evidence"],
                "analyst_action": alert["analyst_action"]
            }
            
            req = urllib.request.Request(args.api)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            jsondata = json.dumps(api_alert).encode('utf-8')
            try:
                urllib.request.urlopen(req, jsondata, timeout=5)
            except urllib.error.URLError as e:
                print(f"[!] Failed to push alert {alert['rule_id']}: {e}")
        
        print("[*] API push complete.")

if __name__ == "__main__":
    main()
