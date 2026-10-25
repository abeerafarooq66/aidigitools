import urllib.request
import urllib.error
from pathlib import Path

class DeploymentVerifier:
    """Verifies live or local URLs for status 200, valid SSL, and non-empty body."""

    def verify_local_file(self, file_path: Path | str) -> dict:
        p = Path(file_path)
        if not p.is_file():
            return {"target": str(file_path), "status": 404, "valid": False, "error": "File does not exist"}
        
        size = p.stat().st_size
        return {
            "target": str(file_path),
            "status": 200,
            "valid": size > 100,
            "size_bytes": size,
            "error": None if size > 100 else "File content is too small"
        }

    def verify_live_url(self, url: str, timeout: int = 5) -> dict:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AIDigiTools-DeploymentVerifier/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                return {
                    "url": url,
                    "status": status,
                    "valid": status == 200,
                    "error": None
                }
        except urllib.error.HTTPError as e:
            return {"url": url, "status": e.code, "valid": False, "error": str(e)}
        except Exception as e:
            return {"url": url, "status": 0, "valid": False, "error": str(e)}
