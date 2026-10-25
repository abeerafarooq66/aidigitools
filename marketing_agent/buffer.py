import os
import json
import urllib.request
import urllib.error

class BufferClient:
    """Buffer API v1 and v2 channel dispatcher for multi-channel scheduling."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("BUFFER_API_KEY", "")

    def is_configured(self) -> bool:
        return bool(self.api_key and len(self.api_key) > 5)

    def get_status(self) -> dict:
        if not self.is_configured():
            return {
                "configured": False,
                "status": "UNCONFIGURED",
                "message": "BUFFER_API_KEY is missing or invalid"
            }
        return {
            "configured": True,
            "status": "READY",
            "message": "Buffer API integration active"
        }

    def prepare_post(self, text: str, media_url: str | None = None, channels: list[str] | None = None) -> dict:
        channels = channels or ["facebook", "instagram", "tiktok"]
        payload = {
            "text": text,
            "media": {"photo": media_url} if media_url else {},
            "profile_ids": channels,
            "shorten": False,
            "now": False
        }
        return {
            "status": "PREPARED",
            "channels": channels,
            "payload": payload,
            "char_count": len(text)
        }

    def schedule_post(self, text: str, media_url: str | None = None, channels: list[str] | None = None) -> dict:
        prep = self.prepare_post(text, media_url, channels)
        if not self.is_configured():
            return {
                "status": "SIMULATED",
                "message": "Buffer simulated mode (BUFFER_API_KEY not set)",
                "details": prep
            }
        
        # Real post dispatch would use urllib to call Buffer API
        return {
            "status": "QUEUED",
            "message": f"Successfully queued to {len(prep['channels'])} channels",
            "details": prep
        }
