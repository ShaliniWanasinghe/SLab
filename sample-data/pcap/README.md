Sample PCAP files in this directory are SYNTHETIC.
They were generated in a controlled local lab environment.
They do NOT contain real user traffic or real network data.

Files:
  brute_force_sample.pcap  — Simulated brute force login attack
  port_scan_sample.pcap    — Simulated Nmap port scan
  normal_traffic.pcap      — Baseline normal HTTP traffic

Use these files to:
  1. Learn Wireshark filtering (see docs/wireshark-learning.md)
  2. Test the PCAP analyzer: python security-analysis/pcap/analyzer.py --file <file>
  3. Feed sample data into the detection engine for testing

PCAP files will be generated in Phase 4 of the project.
This placeholder README is committed in Phase 1.
