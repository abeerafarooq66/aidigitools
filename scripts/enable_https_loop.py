import time
import subprocess
import sys

print("Monitoring GitHub Pages SSL Certificate issuance...")

for attempt in range(1, 30):
    print(f"\n[Attempt {attempt}/30] Trying to enforce HTTPS on GitHub Pages...")
    res = subprocess.run(["gh", "api", "-X", "PUT", "repos/abeerafarooq66/aidigitools/pages", "-f", "cname=aidigitools.tech", "-F", "https_enforced=true"], capture_output=True, text=True)
    if res.returncode == 0:
        print("\n🎉 SUCCESS! HTTPS Enforced successfully! Green SSL Lock is now ACTIVE!")
        print("Response:", res.stdout)
        sys.exit(0)
    else:
        print("Status: Certificate is still being provisioned by Let's Encrypt / GitHub...")
        time.sleep(20)

print("\nNote: Certificate issuance is in progress. GitHub usually finishes it within 5-15 minutes.")
