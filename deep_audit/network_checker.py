import ssl
import time
import socket
import urllib.request
import urllib.error
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from .models import AuditIssue

class NetworkAuditor:
    """Audits HTTP/HTTPS responses, redirects, SSL certificates, and canonical URL alignment."""

    def __init__(self, domain: str = "aidigitools.tech", timeout: int = 8):
        self.domain = domain
        self.base_url = f"https://{domain}"
        self.timeout = timeout
        self.ssl_context = ssl.create_default_context()

    def check_ssl_certificate(self, timestamp: str) -> List[AuditIssue]:
        """Validates SSL certificate expiration and common name."""
        issues = []
        try:
            with socket.create_connection((self.domain, 443), timeout=self.timeout) as sock:
                with self.ssl_context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    not_after = cert.get("notAfter")
                    if not not_after:
                        issues.append(AuditIssue(
                            id="SSL_NO_EXPIRY",
                            timestamp=timestamp,
                            tested_url=self.base_url,
                            category="HTTP_STATUS",
                            severity="CRITICAL",
                            confidence="CONFIRMED",
                            evidence="Certificate did not provide a valid notAfter field.",
                            recommended_fix="Renew or verify SSL certificate provisioning on DNS/CDN."
                        ))
                    else:
                        import datetime
                        expiry = datetime.datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z")
                        days_left = (expiry - datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)).days
                        if days_left < 7:
                            issues.append(AuditIssue(
                                id="SSL_EXPIRING_SOON",
                                timestamp=timestamp,
                                tested_url=self.base_url,
                                category="HTTP_STATUS",
                                severity="CRITICAL" if days_left < 3 else "WARNING",
                                confidence="CONFIRMED",
                                evidence=f"SSL certificate expires in {days_left} days (notAfter: {not_after}).",
                                recommended_fix="Renew SSL certificate immediately."
                            ))
        except Exception as e:
            issues.append(AuditIssue(
                id="SSL_HANDSHAKE_ERROR",
                timestamp=timestamp,
                tested_url=self.base_url,
                category="HTTP_STATUS",
                severity="ERROR",
                confidence="UNCERTAIN",
                evidence=f"Failed to establish SSL handshake: {str(e)}",
                recommended_fix="Verify DNS records, firewall, and web server SSL bindings."
            ))
        return issues

    def probe_url(self, url: str, timestamp: str) -> Tuple[Dict[str, Any], List[AuditIssue]]:
        """Probes a single live URL and checks status, redirects, and HTTPS."""
        issues = []
        result = {"url": url, "status_code": 0, "latency_ms": 0, "redirected": False, "final_url": url}
        start = time.time()
        
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "AIDigiTools-DeepAudit-Engine/1.0 (Mozilla/5.0 compatible)"}
            )
            with urllib.request.urlopen(req, context=self.ssl_context, timeout=self.timeout) as resp:
                result["latency_ms"] = round((time.time() - start) * 1000, 2)
                result["status_code"] = resp.status
                result["final_url"] = resp.geturl()
                result["redirected"] = (resp.geturl() != url)

                if resp.status >= 400:
                    issues.append(AuditIssue(
                        id="HTTP_CLIENT_ERROR",
                        timestamp=timestamp,
                        tested_url=url,
                        category="HTTP_STATUS",
                        severity="ERROR",
                        confidence="CONFIRMED",
                        evidence=f"HTTP status code {resp.status} received.",
                        recommended_fix="Ensure file or route exists and permissions allow reading."
                    ))
                elif not result["final_url"].startswith("https://"):
                    issues.append(AuditIssue(
                        id="INSECURE_HTTP_REDIRECT",
                        timestamp=timestamp,
                        tested_url=url,
                        category="HTTP_STATUS",
                        severity="ERROR",
                        confidence="CONFIRMED",
                        evidence=f"Endpoint resolved to non-HTTPS URL: {result['final_url']}",
                        recommended_fix="Enforce strict HTTPS redirect."
                    ))
        except urllib.error.HTTPError as e:
            result["latency_ms"] = round((time.time() - start) * 1000, 2)
            result["status_code"] = e.code
            issues.append(AuditIssue(
                id=f"HTTP_{e.code}",
                timestamp=timestamp,
                tested_url=url,
                category="HTTP_STATUS",
                severity="CRITICAL" if e.code in (404, 500, 502, 503) else "WARNING",
                confidence="CONFIRMED",
                evidence=f"HTTP Error {e.code}: {e.reason}",
                recommended_fix="Check web server routing and eliminate broken URL path."
            ))
        except Exception as e:
            result["latency_ms"] = round((time.time() - start) * 1000, 2)
            issues.append(AuditIssue(
                id="NETWORK_UNREACHABLE",
                timestamp=timestamp,
                tested_url=url,
                category="HTTP_STATUS",
                severity="WARNING",
                confidence="UNCERTAIN",
                evidence=f"Network probe failed: {str(e)}",
                recommended_fix="Verify internet connectivity and server availability."
            ))

        return result, issues
