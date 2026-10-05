# Sample Reconnaissance Data

This directory contains synthetic Nmap XML output files representing
reconnaissance data against the local lab environment.

## Files

### localhost_scan.xml
Simulated output of running: `nmap -sV -oX localhost_scan.xml 127.0.0.1`
Shows the expected lab ports (5000, 8000) and a simulated SSH port (22).

## Usage

Parse this data with the SentinelLab recon parser:
  python security-analysis/recon/nmap_parser.py --file sample-data/recon/localhost_scan.xml
