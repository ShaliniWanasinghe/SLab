"""
analyzer.py — SentinelLab PCAP Analyzer
=========================================

Parses PCAP files to extract security metadata and HTTP details.
Outputs structured JSON suitable for the detection engine.
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from scapy.all import rdpcap, IP, TCP, UDP, Raw

def analyze_pcap(file_path):
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
        sys.exit(1)
        
    try:
        packets = rdpcap(file_path)
    except Exception as e:
        print(f"Error reading PCAP: {e}")
        sys.exit(1)
        
    summary = {
        "file": file_path,
        "total_packets": len(packets),
        "sessions": [],
        "http_requests": [],
        "suspicious_patterns": []
    }
    
    # Track TCP flags for port scan detection
    syn_counts = defaultdict(set) # src_ip -> set of dest ports
    
    for pkt in packets:
        if IP in pkt:
            src = pkt[IP].src
            dst = pkt[IP].dst
            
            if TCP in pkt:
                sport = pkt[TCP].sport
                dport = pkt[TCP].dport
                flags = pkt[TCP].flags
                
                # Check for SYN scan pattern
                if flags == "S":
                    syn_counts[src].add(dport)
                    
                # Extract HTTP
                if Raw in pkt and (dport == 5000 or sport == 5000 or dport == 80):
                    try:
                        payload = pkt[Raw].load.decode('utf-8', errors='ignore')
                        if payload.startswith(("GET ", "POST ", "PUT ", "DELETE ")):
                            lines = payload.split("\r\n")
                            req_line = lines[0]
                            method, path, _ = req_line.split(" ", 2)
                            summary["http_requests"].append({
                                "source": src,
                                "destination": dst,
                                "port": dport,
                                "method": method,
                                "path": path,
                                "raw_start": payload[:100]
                            })
                    except ValueError:
                        pass
                        
    # Analyze patterns
    for src, ports in syn_counts.items():
        if len(ports) > 10:
            summary["suspicious_patterns"].append({
                "type": "port_scan",
                "source": src,
                "ports_scanned": len(ports),
                "severity": "HIGH"
            })
            
    return summary

def main():
    parser = argparse.ArgumentParser(description="SentinelLab PCAP Analyzer")
    parser.add_argument("--file", required=True, help="Path to PCAP file")
    args = parser.parse_args()
    
    data = analyze_pcap(args.file)
    print(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
