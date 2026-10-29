import os
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta

# Constant disclaimer regarding Laboratory vs Real-User Field Metrics
LAB_VS_FIELD_DISCLAIMER = (
    "Scientific Disclaimer: Laboratory performance metrics (including synthetic Lighthouse, "
    "simulated PageSpeed audits, and local headless browser evaluations) measure performance "
    "under controlled, preset network throttling and device constraints. Laboratory scores represent "
    "diagnostic benchmarks for regression testing and optimization debugging, and do NOT equate to "
    "real-user Core Web Vitals (Chrome User Experience Report / CrUX field data aggregated across "
    "28-day 75th percentile real-world device and network interactions). Field CrUX data may vary "
    "based on end-user hardware, network conditions, cache hit rates, and geographical routing."
)

@dataclass
class AuditIssue:
    id: str
    timestamp: str
    tested_url: str
    category: str  # HTTP_STATUS, INTERNAL_LINKS, ON_PAGE_SEO, STRUCTURED_DATA, ACCESSIBILITY, LIGHTHOUSE, CONTENT_QUALITY, PRICING_CONSISTENCY, BROWSER_INTERACTION
    severity: str  # CRITICAL, ERROR, WARNING, NOTICE
    confidence: str  # CONFIRMED, WARNING, UNCERTAIN
    evidence: str
    recommended_fix: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DeepAuditSummary:
    timestamp: str
    domain: str
    total_pages_discovered: int
    sitemap_urls_count: int
    orphan_pages_count: int
    health_score: int
    issues_by_severity: Dict[str, int]
    issues_by_confidence: Dict[str, int]
    issues_by_category: Dict[str, int]
    laboratory_performance_disclaimer: str = LAB_VS_FIELD_DISCLAIMER

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
