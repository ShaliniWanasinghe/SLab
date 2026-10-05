"""
generate_pcaps.py — SentinelLab synthetic PCAP generator
========================================================

Generates synthetic .pcap files representing common attack scenarios
for use with the PCAP Analyzer.

Usage:
    pip install scapy
    python scripts/generate_pcaps.py
"""

import os
from scapy.all import IP, TCP, Ether, wrpcap, Raw

# Paths
HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE_DIR = os.path.join(HERE, "..", "sample-data", "pcap")
os.makedirs(SAMPLE_DIR, exist_ok=True)

def generate_brute_force():
    """Generate a PCAP showing repeated HTTP POSTs to /login"""
    packets = []
    src_ip = "192.168.1.100"
    dst_ip = "127.0.0.1"
    
    # 5 failed login attempts
    for i in range(1, 6):
        # SYN
        syn = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=10000+i, dport=5000, flags="S", seq=1000)
        packets.append(syn)
        # SYN-ACK
        syn_ack = Ether()/IP(src=dst_ip, dst=src_ip)/TCP(sport=5000, dport=10000+i, flags="SA", seq=2000, ack=1001)
        packets.append(syn_ack)
        # ACK
        ack = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=10000+i, dport=5000, flags="A", seq=1001, ack=2001)
        packets.append(ack)
        
        # HTTP POST
        payload = f"POST /login HTTP/1.1\r\nHost: {dst_ip}:5000\r\nContent-Length: 30\r\n\r\nusername=admin&password=test{i}"
        push = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=10000+i, dport=5000, flags="PA", seq=1001, ack=2001)/Raw(load=payload)
        packets.append(push)
        
        # HTTP 401 Response
        resp_payload = "HTTP/1.1 401 Unauthorized\r\nContent-Length: 17\r\n\r\nInvalid password."
        resp = Ether()/IP(src=dst_ip, dst=src_ip)/TCP(sport=5000, dport=10000+i, flags="PA", seq=2001, ack=1001+len(payload))/Raw(load=resp_payload)
        packets.append(resp)
        
        # FIN-ACK
        fin = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=10000+i, dport=5000, flags="FA", seq=1001+len(payload), ack=2001+len(resp_payload))
        packets.append(fin)

    pcap_path = os.path.join(SAMPLE_DIR, "brute_force_sample.pcap")
    wrpcap(pcap_path, packets)
    print(f"Generated {pcap_path}")

def generate_port_scan():
    """Generate a PCAP showing a SYN scan across many ports"""
    packets = []
    src_ip = "192.168.1.100"
    dst_ip = "127.0.0.1"
    
    ports_to_scan = [21, 22, 23, 25, 53, 80, 443, 3306, 5000, 8000, 8080]
    
    for port in ports_to_scan:
        # SYN sent
        syn = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=35000, dport=port, flags="S", seq=100)
        packets.append(syn)
        
        if port in [22, 5000, 8000]:
            # Port open -> SYN-ACK
            syn_ack = Ether()/IP(src=dst_ip, dst=src_ip)/TCP(sport=port, dport=35000, flags="SA", seq=200, ack=101)
            packets.append(syn_ack)
            # Scanner sends RST to close
            rst = Ether()/IP(src=src_ip, dst=dst_ip)/TCP(sport=35000, dport=port, flags="R", seq=101)
            packets.append(rst)
        else:
            # Port closed -> RST-ACK
            rst_ack = Ether()/IP(src=dst_ip, dst=src_ip)/TCP(sport=port, dport=35000, flags="RA", seq=0, ack=101)
            packets.append(rst_ack)

    pcap_path = os.path.join(SAMPLE_DIR, "port_scan_sample.pcap")
    wrpcap(pcap_path, packets)
    print(f"Generated {pcap_path}")

if __name__ == "__main__":
    print("[*] Generating synthetic PCAP files...")
    generate_brute_force()
    generate_port_scan()
    print("[*] Complete.")
