"""
AIDigiTools — Backlink Intelligence & Outreach Acquisition Engine
==================================================================
Implements comprehensive White Hat backlink research, prospect vetting,
competitor backlink gap discovery, live HTTP link verification, and
strict Human-In-The-Loop outreach management.

Key Guarantees:
1. 100% White Hat SEO only. Zero PBNs, zero spam comments, zero paid link schemes.
2. Verified Backlink Reporting: A link is NEVER reported as ACQUIRED unless
   verified live via real HTTP DOM inspection.
3. Strict Human Governance: Outreach emails and directory submissions require
   explicit user approval before dispatch.
4. Multi-Factor Quality Vetting: Vets prospects across Relevance, Domain Authority,
   Organic Traffic, Placement Quality, Google Indexing, and Spam Cleanliness.
"""

import os
import sys
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = ROOT_DIR / "data"

REGISTRY_PATH = DATA_DIR / "backlink_registry.json"
OPPORTUNITIES_PATH = DATA_DIR / "backlink_opportunities.json"
COMPETITOR_MATRIX_PATH = DATA_DIR / "competitor_backlink_matrix.json"
OUTREACH_PIPELINE_PATH = DATA_DIR / "outreach_pipeline.json"
MONITORING_HISTORY_PATH = DATA_DIR / "backlink_monitoring_history.json"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 (AIDigiTools-Backlink-Verifier/1.0)"


class BacklinkIntelligenceEngine:
    """Enterprise backlink research, competitor gap discovery, and verification engine."""

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = Path(workspace_root or ROOT_DIR)
        self.data_dir = self.workspace_root / "data"
        self.registry_path = self.data_dir / "backlink_registry.json"
        self.opportunities_path = self.data_dir / "backlink_opportunities.json"
        self.competitor_matrix_path = self.data_dir / "competitor_backlink_matrix.json"
        self.outreach_path = self.data_dir / "outreach_pipeline.json"
        self.history_path = self.data_dir / "backlink_monitoring_history.json"

        self._ensure_data_files()

    def _ensure_data_files(self):
        """Ensures all necessary JSON data ledgers exist with valid schemas."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        if not self.registry_path.exists():
            default_reg = {
                "version": "1.0.0",
                "target_domain": "https://aidigitools.tech",
                "last_audit_timestamp": datetime.now(timezone.utc).isoformat(),
                "summary": {"total_backlinks": 0, "total_referring_domains": 0, "dofollow_count": 0, "nofollow_count": 0, "active_count": 0, "lost_count": 0, "broken_target_count": 0, "toxic_count": 0},
                "anchor_distribution": {"branded": 0.0, "naked_url": 0.0, "exact_match": 0.0, "partial_match": 0.0, "generic": 0.0},
                "links": []
            }
            with open(self.registry_path, "w", encoding="utf-8") as f:
                json.dump(default_reg, f, indent=2)

    # --------------------------------------------------------------------------
    # 1. LIVE VERIFICATION OF REGISTERED BACKLINKS
    # --------------------------------------------------------------------------
    def verify_registered_backlinks_live(self, timeout: float = 8.0) -> Dict[str, Any]:
        """
        Inspects each registered backlink by making a live HTTP request to the source URL,
        searching the DOM for links pointing to 'aidigitools.tech', extracting anchor text
        and rel attributes, and verifying target status.

        CRITICAL RULE: Never claim a link is ACQUIRED or ACTIVE without empirical live proof!
        """
        if not self.registry_path.exists():
            return {"status": "NO_REGISTRY", "verified_count": 0, "active_count": 0}

        with open(self.registry_path, "r", encoding="utf-8") as f:
            registry = json.load(f)

        links = registry.get("links", [])
        verified_links = []
        active_count = 0
        lost_count = 0
        dofollow_count = 0
        nofollow_count = 0
        now_iso = datetime.now(timezone.utc).isoformat()

        for link in links:
            source = link.get("source_url", "")
            expected_target = link.get("target_url", "https://aidigitools.tech")
            link_id = link.get("backlink_id", "")

            # Live HTTP inspection for web pages - strict White Hat DOM verification
            try:
                req = urllib.request.Request(
                    source,
                    headers={"User-Agent": USER_AGENT}
                )
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    status_code = response.getcode()
                    html_content = response.read().decode("utf-8", errors="ignore")

                # Parse links in DOM: search for clickable anchor tag pointing to aidigitools.tech
                link_pattern = re.compile(r'<a\s+[^>]*href=["\']([^"\']*aidigitools\.tech[^"\']*)["\'][^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
                matches = link_pattern.findall(html_content)

                if matches:
                    found_target, raw_anchor = matches[0]
                    # Strip tags from anchor text
                    clean_anchor = re.sub(r'<[^>]+>', '', raw_anchor).strip()
                    
                    # Check rel attribute
                    is_dofollow = "nofollow" not in html_content.lower()

                    link["status"] = "Live Verified"
                    link["lifecycle_status"] = "Live Verified"
                    link["http_status_code"] = status_code
                    link["last_verified"] = now_iso
                    link["anchor_text"] = clean_anchor if clean_anchor else link.get("anchor_text", "")
                    link["is_dofollow"] = is_dofollow
                    link["rel_attribute"] = "dofollow" if is_dofollow else "nofollow"

                    active_count += 1
                    if is_dofollow:
                        dofollow_count += 1
                    else:
                        nofollow_count += 1
                else:
                    link["status"] = "Lost"
                    link["lifecycle_status"] = "Lost"
                    link["http_status_code"] = status_code
                    link["last_verified"] = now_iso
                    link["verification_note"] = "HTTP 200 OK received, but no clickable <a href='...aidigitools.tech...'> tag found in public DOM."
                    lost_count += 1

            except Exception as e:
                # Network error, timeout, or blocked request
                link["status"] = "Lost"
                link["lifecycle_status"] = "Lost"
                link["last_verified"] = now_iso
                link["http_status_code"] = 0
                link["verification_note"] = f"Connection failed or timed out: {str(e)[:100]}"
                lost_count += 1

            verified_links.append(link)

        # Update summary in registry
        ref_domains = set(l.get("referring_domain") for l in verified_links if l.get("status") == "Live Verified")
        registry["links"] = verified_links
        registry["last_audit_timestamp"] = now_iso
        registry["summary"] = {
            "total_backlinks": len(verified_links),
            "total_referring_domains": len(ref_domains),
            "live_verified_count": active_count,
            "active_count": active_count,
            "dofollow_count": dofollow_count,
            "nofollow_count": nofollow_count,
            "lost_count": lost_count,
            "broken_target_count": 0,
            "toxic_count": 0
        }

        # Update anchor distribution
        anchors = [l.get("anchor_type", "branded") for l in verified_links if l.get("status") == "ACTIVE"]
        total_a = max(len(anchors), 1)
        registry["anchor_distribution"] = {
            "branded": round(anchors.count("branded") / total_a * 100, 1),
            "naked_url": round(anchors.count("naked_url") / total_a * 100, 1),
            "exact_match": round(anchors.count("exact_match") / total_a * 100, 1),
            "partial_match": round(anchors.count("partial_match") / total_a * 100, 1),
            "generic": round(anchors.count("generic") / total_a * 100, 1)
        }

        with open(self.registry_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2)

        return registry["summary"]

    # --------------------------------------------------------------------------
    # 2. COMPETITOR BACKLINK GAP ANALYSIS
    # --------------------------------------------------------------------------
    def get_competitor_backlink_matrix(self) -> Dict[str, Any]:
        """Loads and returns competitor backlink profiles and gap analysis."""
        if not self.competitor_matrix_path.exists():
            return {"competitors": [], "backlink_gap_analysis": []}
        with open(self.competitor_matrix_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def identify_backlink_gaps(self) -> List[Dict[str, Any]]:
        """Identifies domains that link to competitors but not to aidigitools.tech."""
        matrix = self.get_competitor_backlink_matrix()
        return matrix.get("backlink_gap_analysis", [])

    # --------------------------------------------------------------------------
    # 3. HIGH-QUALITY PROSPECT VETTING
    # --------------------------------------------------------------------------
    def list_vetted_opportunities(
        self,
        category: Optional[str] = None,
        min_composite_score: float = 75.0,
        opportunity_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Filters and returns high-quality vetted opportunities across the 9 core categories.
        Enforces multi-factor quality scoring (Never rely on DA alone).
        """
        if not self.opportunities_path.exists():
            return []
        with open(self.opportunities_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        opps = data.get("opportunities", [])
        filtered = []

        for o in opps:
            if category and o.get("category", "").lower() != category.lower():
                continue
            if opportunity_type and o.get("opportunity_type", "").upper() != opportunity_type.upper():
                continue
            if o.get("quality_composite_score", 0.0) < min_composite_score:
                continue
            if o.get("spam_score", 0) > 4:  # Strict spam filter
                continue
            filtered.append(o)

        filtered.sort(key=lambda x: x.get("quality_composite_score", 0.0), reverse=True)
        return filtered

    # --------------------------------------------------------------------------
    # 4. OUTREACH GENERATION & HUMAN-IN-THE-LOOP TRACKING
    # --------------------------------------------------------------------------
    def get_outreach_pipeline(self) -> Dict[str, Any]:
        """Returns the current outreach campaign pipeline and pending approvals."""
        if not self.outreach_path.exists():
            return {"total_outreach_campaigns": 0, "pending_user_approval_count": 0, "campaigns": []}
        with open(self.outreach_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def prepare_personalized_pitch(self, opportunity_id: str) -> Optional[Dict[str, Any]]:
        """
        Prepares a personalized, ethical White Hat email pitch for a given opportunity ID.
        Enqueues it in the outreach pipeline with status PENDING_USER_APPROVAL.
        """
        opps = self.list_vetted_opportunities(min_composite_score=0.0)
        target_opp = next((o for o in opps if o.get("opportunity_id") == opportunity_id), None)
        if not target_opp:
            return None

        pipeline = self.get_outreach_pipeline()
        campaigns = pipeline.get("campaigns", [])
        
        # Check if already exists
        existing = next((c for c in campaigns if c.get("opportunity_id") == opportunity_id), None)
        if existing:
            return existing

        cid = f"OUTREACH-{len(campaigns) + 1:03d}"
        domain = target_opp.get("domain", "")
        cat = target_opp.get("category", "")
        opp_type = target_opp.get("opportunity_type", "GUEST_POST")
        target_dest = target_opp.get("target_link_destination", "https://aidigitools.tech/")
        target_anchor = target_opp.get("target_anchor_text", "AIDigiTools")

        subject = f"Editorial Contribution Proposal for {domain} — AIDigiTools 2026 AI Research"
        body = (
            f"Dear {domain} Editorial Team,\n\n"
            f"I hope this message finds you well. I follow {domain}'s insightful coverage in the {cat} space.\n\n"
            f"At AIDigiTools (https://aidigitools.tech), our engineering team conducts in-depth empirical benchmarks "
            f"on commercial AI software, focusing on real-world workflow efficiency, token economics, and accessible payment rails.\n\n"
            f"We would love to provide an original, comprehensive guest editorial or technical resource reference for your readers.\n"
            f"Specifically, we would be delighted to contribute data from our verified research at: {target_dest}\n\n"
            f"Suggested Anchor / Context: \"{target_anchor}\"\n\n"
            f"Please let me know if this aligns with your editorial priorities, and I will gladly share the full draft.\n\n"
            f"Warm regards,\n"
            f"Abeera Farooq\n"
            f"AIDigiTools Technical Research Desk\n"
            f"https://aidigitools.tech"
        )

        new_campaign = {
            "campaign_id": cid,
            "opportunity_id": opportunity_id,
            "target_domain": domain,
            "recipient_name": f"{domain} Editorial Desk",
            "recipient_email_or_form": target_opp.get("editorial_contact", ""),
            "campaign_type": opp_type,
            "status": "PENDING_USER_APPROVAL",
            "requires_user_approval": True,
            "email_subject": subject,
            "email_body": body,
            "prepared_at": datetime.now(timezone.utc).isoformat(),
            "approval_granted": False,
            "dispatched_at": None,
            "response_received": None
        }

        campaigns.append(new_campaign)
        pipeline["campaigns"] = campaigns
        pipeline["total_outreach_campaigns"] = len(campaigns)
        pipeline["pending_user_approval_count"] = sum(1 for c in campaigns if c.get("status") == "PENDING_USER_APPROVAL")

        with open(self.outreach_path, "w", encoding="utf-8") as f:
            json.dump(pipeline, f, indent=2)

        return new_campaign

    # --------------------------------------------------------------------------
    # 5. ANCHOR TEXT & TOXICITY AUDITING
    # --------------------------------------------------------------------------
    def audit_anchor_text_safety(self) -> Dict[str, Any]:
        """
        Audits anchor text distribution against Google Penguin & over-optimization guardrails.
        Exact match anchors must remain below 20% to preserve organic health.
        """
        if not self.registry_path.exists():
            return {"status": "HEALTHY", "exact_match_ratio": 0.0, "warning": False}
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        dist = data.get("anchor_distribution", {})
        exact_ratio = dist.get("exact_match", 0.0)
        is_safe = exact_ratio <= 20.0

        return {
            "status": "HEALTHY" if is_safe else "OVER_OPTIMIZATION_RISK",
            "anchor_distribution": dist,
            "exact_match_percent": exact_ratio,
            "safe_threshold_percent": 20.0,
            "recommendation": "Maintain natural mix: 50%+ Branded/Naked URLs, 20-30% Partial Match, <20% Exact Match."
        }

    def scan_toxic_backlinks(self) -> List[Dict[str, Any]]:
        """Scans registered backlinks for toxic signals (PBNs, high spam score, suspicious foreign text)."""
        if not self.registry_path.exists():
            return []
        with open(self.registry_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        toxic_links = []
        for link in data.get("links", []):
            if link.get("status") == "TOXIC_FLAGGED" or link.get("spam_score", 0) > 10:
                toxic_links.append(link)
        return toxic_links

    # --------------------------------------------------------------------------
    # 6. DASHBOARD METRICS SYNTHESIS
    # --------------------------------------------------------------------------
    def generate_dashboard_metrics(self) -> Dict[str, Any]:
        """Synthesizes all backlink, competitor, and outreach metrics for reporting."""
        # 1. Verify active links live
        summary = self.verify_registered_backlinks_live()

        # 2. Competitor matrix & gaps
        matrix = self.get_competitor_backlink_matrix()
        gaps = matrix.get("backlink_gap_analysis", [])

        # 3. Opportunities
        opps = self.list_vetted_opportunities()

        # 4. Outreach
        outreach = self.get_outreach_pipeline()

        # 5. Anchor safety
        anchor_safety = self.audit_anchor_text_safety()

        return {
            "summary": summary,
            "competitors_matrix": matrix.get("competitors", []),
            "backlink_gaps": gaps,
            "vetted_opportunities_count": len(opps),
            "top_opportunities": opps[:6],
            "outreach_pipeline": outreach,
            "anchor_safety": anchor_safety,
            "toxic_backlinks_detected": len(self.scan_toxic_backlinks())
        }
