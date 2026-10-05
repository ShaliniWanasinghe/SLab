"""
nmap_parser.py — SentinelLab Reconnaissance Parser
===================================================

Parses Nmap XML output into a normalized JSON schema for the backend.
Also maps open ports and services to defensive observations.

Usage:
    python nmap_parser.py --file <path_to_xml>

This script demonstrates how defenders take raw scanner output,
parse it programmatically, and enrich it with defensive context.
"""

import argparse
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime

# Defensive observations mapping based on common lab findings
DEFENSIVE_CONTEXT = {
    22: "SSH is exposed. Ensure strong authentication (keys, not passwords) and disable root login. Consider moving to a non-standard port to reduce noise.",
    5000: "Flask development server detected. This should NEVER be exposed in production. Development servers lack security controls like rate limiting and often expose verbose stack traces.",
    8000: "API endpoint detected (FastAPI/uvicorn). Ensure all sensitive endpoints require authentication and implement proper CORS restrictions.",
}


def parse_nmap_xml(file_path: str) -> dict:
    """
    Parse an Nmap XML file and extract relevant security metadata.
    """
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        sys.exit(1)

    # Standardized output schema
    recon_data = {
        "scan_time": None,
        "scanner_version": root.attrib.get("version"),
        "scan_args": root.attrib.get("args"),
        "hosts": [],
    }

    # Get scan start time
    start_time = root.attrib.get("startstr")
    if start_time:
        recon_data["scan_time"] = start_time
    else:
        recon_data["scan_time"] = datetime.utcnow().isoformat()

    # Iterate through all scanned hosts
    for host in root.findall("host"):
        host_info = {
            "ip": None,
            "status": None,
            "hostnames": [],
            "open_ports": [],
        }

        # Get IP address
        address = host.find("address")
        if address is not None:
            host_info["ip"] = address.attrib.get("addr")

        # Get status (up/down)
        status = host.find("status")
        if status is not None:
            host_info["status"] = status.attrib.get("state")

        # Get hostnames
        hostnames = host.find("hostnames")
        if hostnames is not None:
            for hn in hostnames.findall("hostname"):
                name = hn.attrib.get("name")
                if name:
                    host_info["hostnames"].append(name)

        # Get ports
        ports_elem = host.find("ports")
        if ports_elem is not None:
            for port in ports_elem.findall("port"):
                state_elem = port.find("state")
                if state_elem is not None and state_elem.attrib.get("state") == "open":
                    port_id = int(port.attrib.get("portid"))
                    protocol = port.attrib.get("protocol")
                    
                    # Extract service info if available
                    service_elem = port.find("service")
                    service_name = service_elem.attrib.get("name") if service_elem is not None else "unknown"
                    product = service_elem.attrib.get("product") if service_elem is not None else "unknown"
                    version = service_elem.attrib.get("version") if service_elem is not None else "unknown"
                    
                    observation = DEFENSIVE_CONTEXT.get(port_id, "No specific defensive observation for this port.")

                    host_info["open_ports"].append({
                        "port": port_id,
                        "protocol": protocol,
                        "service": service_name,
                        "product": product,
                        "version": version,
                        "defensive_observation": observation
                    })

        recon_data["hosts"].append(host_info)

    return recon_data


def main():
    parser = argparse.ArgumentParser(description="SentinelLab Nmap XML Parser")
    parser.add_argument("--file", required=True, help="Path to the Nmap XML output file")
    args = parser.parse_args()

    print(f"[*] Parsing Nmap XML file: {args.file}")
    data = parse_nmap_xml(args.file)
    
    # Print the normalized JSON
    print("\n--- Normalized Reconnaissance Data ---")
    print(json.dumps(data, indent=2))
    print("--------------------------------------\n")
    
    # Summary for the analyst
    print(f"[*] Scan Time: {data['scan_time']}")
    for host in data['hosts']:
        print(f"[*] Host: {host['ip']} ({host['status']})")
        print(f"[*] Open Ports: {len(host['open_ports'])}")
        for p in host['open_ports']:
            print(f"    - Port {p['port']}/{p['protocol']} ({p['service']}): {p['product']} {p['version']}")
            print(f"      Defensive Context: {p['defensive_observation']}")


if __name__ == "__main__":
    main()
