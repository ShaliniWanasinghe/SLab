# SentinelLab — Kali Linux & Terminal Primer

> This document teaches you the Linux terminal commands and concepts you
> actually need for this project. All examples target the local laboratory.
> No offensive techniques are included.

---

## What Is Kali Linux?

Kali Linux is a Debian-based Linux distribution designed for security
professionals. It comes pre-installed with hundreds of security tools:
Wireshark, Nmap, tshark, Burp Suite, and many others.

For this project, you don't need Kali immediately. The core project runs
on Windows. Kali Linux becomes relevant in the optional Phase 14+ lab
extension when you set up a dedicated attack/analysis virtual machine.

This document prepares you for that environment.

---

## 1. Terminal Navigation

The Linux terminal is your primary interface. There is no clicking — you
type commands.

### Orientation Commands

```bash
# Where am I right now?
pwd
# Output: /home/analyst

# What is in this directory?
ls
# Output: docs  logs  pcap  scripts

# More detailed listing (permissions, size, date)
ls -la
# Output:
# drwxr-xr-x  5 analyst analyst 4096 Oct  5 15:00 .
# drwxr-xr-x 18 analyst analyst 4096 Oct  5 14:55 ..
# -rw-r--r--  1 analyst analyst 1234 Oct  5 15:00 README.md

# Go into a directory
cd docs

# Go back one level
cd ..

# Go to your home directory
cd ~

# Go to the root of the filesystem
cd /
```

### Working with Files

```bash
# Read a file
cat sample_access.log

# Read a large file page by page
less sample_access.log
# Press 'q' to quit, arrow keys to scroll

# Show the first 10 lines
head sample_access.log

# Show the last 10 lines (useful for live log watching)
tail sample_access.log

# Show the last 50 lines, live-updating as new lines appear
tail -f /var/log/apache2/access.log

# Search for text inside a file
grep "Failed password" auth.log

# Search case-insensitively
grep -i "failed" auth.log

# Count matching lines
grep -c "Failed" auth.log

# Create a new empty file
touch new_file.txt

# Create a directory
mkdir my_directory

# Copy a file
cp source.txt destination.txt

# Move or rename a file
mv old_name.txt new_name.txt

# Delete a file (careful — no recycle bin in Linux)
rm file_to_delete.txt
```

---

## 2. File Permissions

Linux has a permission system that controls who can read, write, or execute files.

### Reading Permissions

```bash
ls -la
# -rwxr-xr-- 1 analyst analyst 1234 Oct 5 15:00 script.py
#  ^^^       = owner permissions (read, write, execute)
#     ^^^    = group permissions (read, -, execute)
#        ^^^ = others permissions (read, -, -)
```

| Symbol | Meaning |
|---|---|
| `r` | Read permission |
| `w` | Write permission |
| `x` | Execute permission |
| `-` | Permission not granted |

### Changing Permissions

```bash
# Make a script executable (you need this to run shell scripts)
chmod +x script.sh

# Set specific permissions (owner=rwx, group=r, others=none)
chmod 740 script.sh

# Change file owner
sudo chown analyst:analyst file.txt
```

**Security relevance**: File permissions are a fundamental Linux security control. Misconfigured permissions (e.g., world-writable configuration files) are a common vulnerability finding.

---

## 3. Processes

A process is a running program. Understanding processes helps you see what is running on a system.

```bash
# Show all running processes
ps aux

# Show processes in a live, refreshing view (like Windows Task Manager)
top

# Better version of top
htop

# Find a specific process by name
ps aux | grep python

# Kill a process by its PID (Process ID)
kill 1234

# Force kill (if regular kill doesn't work)
kill -9 1234

# Show what's listening on network ports (important for lab setup)
ss -tulnp
```

**Security relevance**: Incident responders check running processes to identify malicious processes during investigation. Attackers try to hide processes. Process analysis is a fundamental forensics skill.

---

## 4. IP and Network Configuration

```bash
# Show your IP addresses and network interfaces
ip addr
# or the older command:
ifconfig

# Show your routing table (how traffic is directed)
ip route

# Show active network connections
ss -tulnp

# Test connectivity to a host
ping 127.0.0.1

# Stop ping (it runs forever by default)
# Press Ctrl+C

# Trace the path packets take to a destination
traceroute 127.0.0.1
```

### Understanding the Output of `ip addr`

```
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP>
    inet 192.168.56.101/24 brd 192.168.56.255 scope global eth0
```

- `eth0` = the network interface name
- `192.168.56.101` = your IP address
- `/24` = subnet mask (means 255.255.255.0 — your network is 192.168.56.0)

---

## 5. Curl — HTTP from the Command Line

`curl` lets you make HTTP requests from the terminal. This is how you
interact with web applications without a browser.

```bash
# Simple GET request
curl http://localhost:5000

# GET request with verbose output (shows headers)
curl -v http://localhost:5000

# POST request (like submitting a login form)
curl -X POST http://localhost:5000/login \
  -d "username=admin&password=wrongpassword"

# POST with JSON data (like calling an API)
curl -X POST http://localhost:8000/api/alerts \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Alert", "severity": "LOW"}'

# Save response to a file
curl http://localhost:5000 -o response.html

# Follow redirects
curl -L http://localhost:5000

# Show only response headers
curl -I http://localhost:5000
```

**Security relevance**: `curl` is used for manual vulnerability testing, API interaction, and log generation. In this lab, you will use it to generate HTTP traffic that Wireshark can capture.

---

## 6. DNS Commands

DNS (Domain Name System) translates domain names to IP addresses.

```bash
# Look up a domain name
nslookup localhost
# Output: Address: 127.0.0.1

# More detailed DNS lookup
dig localhost

# Reverse lookup (IP to hostname)
nslookup 127.0.0.1

# Show your system's DNS server
cat /etc/resolv.conf
```

**Security relevance**: DNS queries are captured in PCAP files and are valuable evidence in incident investigations. Malware often uses DNS for command-and-control communication.

---

## 7. Nmap Basics

Nmap is the standard tool for network reconnaissance. In this lab, you
**only ever scan localhost** or your private lab network.

```bash
# Basic scan of localhost
nmap 127.0.0.1

# Scan with service version detection
nmap -sV 127.0.0.1

# Scan with OS detection (may need sudo)
sudo nmap -O 127.0.0.1

# Scan specific port range
nmap -p 1-1000 127.0.0.1

# Scan and save output in all formats
nmap -oA scan_results 127.0.0.1
# Creates: scan_results.nmap, scan_results.xml, scan_results.gnmap

# Save as XML (for programmatic parsing)
nmap -oX scan_results.xml 127.0.0.1

# Verbose output
nmap -v 127.0.0.1
```

### Understanding Nmap Output

```
PORT     STATE  SERVICE  VERSION
22/tcp   open   ssh      OpenSSH 8.9
80/tcp   open   http     Apache httpd 2.4.52
443/tcp  closed https
8080/tcp filtered http-proxy
```

| State | Meaning |
|---|---|
| `open` | A service is listening and accepting connections |
| `closed` | Port is reachable but nothing is listening |
| `filtered` | A firewall is blocking the port scan |

**Security relevance**: Nmap shows what an attacker would see when they reconnaissance a target. From a defensive perspective, you use Nmap to inventory your own assets and find unexpected open ports.

---

## 8. Saving Command Output

```bash
# Save output to a file (overwrite)
nmap 127.0.0.1 > scan_output.txt

# Append output to a file
nmap 127.0.0.1 >> scan_output.txt

# Save output AND see it on screen at the same time
nmap 127.0.0.1 | tee scan_output.txt

# Pipe output to grep (filter results)
nmap 127.0.0.1 | grep "open"
```

---

## 9. Useful Shell Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl+C` | Stop current command |
| `Ctrl+Z` | Suspend current command (send to background) |
| `Ctrl+L` | Clear the terminal |
| `Tab` | Autocomplete file/command names |
| `↑` / `↓` | Navigate command history |
| `!!` | Repeat last command |
| `sudo !!` | Repeat last command as root |

---

## 10. Lab-Specific Commands

Commands you will use specifically in this project:

```bash
# Start capturing traffic to a PCAP file (from Linux/Kali)
sudo tshark -i lo -w capture.pcap

# Stop capture
# Press Ctrl+C

# Analyze a PCAP file with tshark
tshark -r capture.pcap

# Filter PCAP to show only HTTP traffic
tshark -r capture.pcap -Y "http"

# Generate HTTP traffic to the vulnerable lab
curl http://localhost:5000/login -d "username=admin&password=test"

# Run Nmap against lab target and save XML
nmap -sV -oX recon/localhost_scan.xml 127.0.0.1

# Check what is running on port 5000
ss -tulnp | grep 5000

# Watch lab application logs in real time
tail -f /var/log/sentinellab/access.log
```

---

## Practice Exercises

1. Open a terminal. Use `pwd` to find your current directory. Use `ls -la` to list its contents. What do the permissions look like on each file?

2. Use `curl -v http://localhost:5000` after starting the vulnerable lab. What HTTP headers does the server send back? What does the `Server:` header reveal?

3. Run `nmap 127.0.0.1`. Note which ports are open. Are any of them unexpected?

4. Run `ss -tulnp` and identify which process is listening on port 5000.

5. Use `grep "POST" sample-data/logs/sample_access.log` to filter only POST requests from the sample log.
