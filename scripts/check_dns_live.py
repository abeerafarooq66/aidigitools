import time
import subprocess
import json

def check_dns():
    print("Checking DNS for aidigitools.tech...")
    res = subprocess.run(["powershell", "-Command", "Resolve-DnsName aidigitools.tech -Type A -ErrorAction SilentlyContinue | Select-Object -ExpandProperty IPAddress"], capture_output=True, text=True)
    ips = [line.strip() for line in res.stdout.strip().splitlines() if line.strip()]
    print("Resolved IPs:", ips)
    github_ips = {"185.199.108.153", "185.199.109.153", "185.199.110.153", "185.199.111.153"}
    matched = set(ips).intersection(github_ips)
    if matched:
        print(f"SUCCESS: DNS is pointing to GitHub IPs! ({matched})")
        print("Enforcing HTTPS on GitHub Pages...")
        sub = subprocess.run(["gh", "api", "-X", "PUT", "repos/abeerafarooq66/aidigitools/pages", "-f", "cname=aidigitools.tech", "-F", "https_enforced=true"], capture_output=True, text=True)
        print("GitHub Pages update response:", sub.stdout or sub.stderr)
        return True
    else:
        print("DNS not yet propagated or A records not added yet.")
        return False

if __name__ == "__main__":
    check_dns()
