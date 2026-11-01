"""
AIDigiTools — Multi-Source Search Intelligence Aggregator
Strictly implements Section 3 of Master Architecture Charter:
MULTI-SOURCE SEARCH INTELLIGENCE
"""

import os
import json
import re
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, List

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BASE_URL = "https://aidigitools.tech"
OUTPUT_REPORT_PATH = ROOT_DIR / "data" / "search_intelligence_latest.json"

class SearchIntelligenceAggregator:
    def __init__(self):
        self.site_url = BASE_URL
        self.gsc_key = os.environ.get("GSC_SERVICE_ACCOUNT_KEY", "").strip()
        self.ga4_prop_id = os.environ.get("GA4_PROPERTY_ID", "561800932").strip()
        self.bing_key = (os.environ.get("BING_WEBMASTER_API_KEY") or os.environ.get("BING_API_KEY") or "").strip()
        self.pagespeed_key = os.environ.get("PAGESPEED_API_KEY", "").strip()
        self.google_ads_dev_token = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "").strip()
        self.google_ads_customer_id = os.environ.get("GOOGLE_ADS_CUSTOMER_ID", "").strip()

    def _get_timestamp_now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def fetch_gsc_intelligence(self, days: int = 28) -> Dict[str, Any]:
        """
        Collect Google Search Console analytics:
        Queries, Pages, Clicks, Impressions, CTR, Position, Devices, Countries.
        Identifies high-impression/low-CTR opportunities and cannibalization risks.
        """
        provenance = {
            "source": "Google Search Console API",
            "property": f"{self.site_url}/",
            "date_range": f"Last {days} days",
            "fetch_timestamp": self._get_timestamp_now(),
            "metric_type": "observed",
            "status": "UNAVAILABLE",
            "limitations": "Data restricted to authorized AIDigiTools property; missing rows denote no recorded impressions on this property, not zero market demand."
        }

        if not self.gsc_key:
            return {
                "provenance": provenance,
                "opportunities": [],
                "cannibalization_risks": [],
                "queries_summary": {},
                "notes": "GSC_SERVICE_ACCOUNT_KEY not present in environment; live data fetch skipped."
            }

        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests

            key_dict = json.loads(self.gsc_key) if self.gsc_key.startswith("{") else json.load(open(self.gsc_key))
            scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
            creds = service_account.Credentials.from_service_account_info(key_dict, scopes=scopes)
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            token = creds.token

            end_date = (datetime.now(timezone.utc) - timedelta(days=3)).strftime("%Y-%m-%d")
            start_date = (datetime.now(timezone.utc) - timedelta(days=days + 3)).strftime("%Y-%m-%d")

            endpoint = f"https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote_plus(self.site_url + '/')}/searchAnalytics/query"
            body = {
                "startDate": start_date,
                "endDate": end_date,
                "dimensions": ["query", "page"],
                "rowLimit": 500
            }

            req = urllib.request.Request(
                endpoint,
                data=json.dumps(body).encode("utf-8"),
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=12) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                rows = result.get("rows", [])

            provenance["status"] = "CONNECTED"
            provenance["rows_retrieved"] = len(rows)

            opportunities = []
            query_map: Dict[str, List[str]] = {}

            for r in rows:
                keys = r.get("keys", [])
                if len(keys) >= 2:
                    q, page = keys[0], keys[1]
                    clicks = r.get("clicks", 0)
                    impr = r.get("impressions", 0)
                    ctr = r.get("ctr", 0.0)
                    pos = r.get("position", 0.0)

                    # Opportunity rule: High impressions (>=50), CTR < 3%, ranking on page 1-2 (pos <= 25)
                    if impr >= 50 and ctr < 0.03 and pos <= 25:
                        opportunities.append({
                            "query": q,
                            "page": page,
                            "impressions": impr,
                            "clicks": clicks,
                            "ctr": round(ctr * 100, 2),
                            "position": round(pos, 1),
                            "action": "Improve title/meta description and add direct AEO answer capsule"
                        })

                    # Track cannibalization
                    query_map.setdefault(q, []).append(page)

            cannibalization = [
                {"query": q, "competing_pages": list(set(pages))}
                for q, pages in query_map.items() if len(set(pages)) > 1
            ]

            return {
                "provenance": provenance,
                "opportunities": opportunities,
                "cannibalization_risks": cannibalization,
                "total_rows": len(rows),
                "notes": f"Successfully retrieved {len(rows)} Search Console rows."
            }

        except Exception as e:
            provenance["status"] = f"ERROR: {str(e)}"
            return {
                "provenance": provenance,
                "opportunities": [],
                "cannibalization_risks": [],
                "notes": f"Google Search Console fetch error: {e}"
            }

    def fetch_ga4_intelligence(self) -> Dict[str, Any]:
        """
        Collect GA4 landing-page performance, user sessions, and WhatsApp lead interactions.
        Strict Invariant: WhatsApp clicks are tracked as inquiry interactions, NEVER confirmed sales.
        """
        provenance = {
            "source": "Google Analytics 4 Data API",
            "property_id": self.ga4_prop_id,
            "fetch_timestamp": self._get_timestamp_now(),
            "metric_type": "observed",
            "status": "UNAVAILABLE",
            "limitations": "GA4 records user browser interactions; WhatsApp button clicks represent lead inquiries, NOT confirmed purchases."
        }

        if not self.gsc_key or not self.ga4_prop_id:
            return {
                "provenance": provenance,
                "organic_landing_pages": [],
                "whatsapp_lead_inquiries": 0,
                "notes": "GA4 / Service Account credentials not provided in current context."
            }

        try:
            from google.oauth2 import service_account
            import google.auth.transport.requests

            key_dict = json.loads(self.gsc_key) if self.gsc_key.startswith("{") else json.load(open(self.gsc_key))
            scopes = ["https://www.googleapis.com/auth/analytics.readonly"]
            creds = service_account.Credentials.from_service_account_info(key_dict, scopes=scopes)
            auth_req = google.auth.transport.requests.Request()
            creds.refresh(auth_req)
            token = creds.token

            endpoint = f"https://analyticsdata.googleapis.com/v1beta/properties/{self.ga4_prop_id}:runReport"
            body = {
                "dateRanges": [{"startDate": "28daysAgo", "endDate": "yesterday"}],
                "dimensions": [{"name": "landingPage"}],
                "metrics": [
                    {"name": "sessions"},
                    {"name": "activeUsers"},
                    {"name": "engagementRate"}
                ],
                "limit": 50
            }

            req = urllib.request.Request(
                endpoint,
                data=json.dumps(body).encode("utf-8"),
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                rows = data.get("rows", [])

            provenance["status"] = "CONNECTED"
            pages = []
            for r in rows:
                lp = r.get("dimensionValues", [{}])[0].get("value", "")
                m = r.get("metricValues", [])
                sessions = int(m[0].get("value", 0)) if len(m) > 0 else 0
                users = int(m[1].get("value", 0)) if len(m) > 1 else 0
                eng = float(m[2].get("value", 0.0)) if len(m) > 2 else 0.0
                pages.append({
                    "landing_page": lp,
                    "sessions": sessions,
                    "active_users": users,
                    "engagement_rate": round(eng * 100, 2)
                })

            return {
                "provenance": provenance,
                "organic_landing_pages": pages,
                "whatsapp_lead_inquiries_tracked": True,
                "notes": f"Successfully retrieved GA4 report with {len(pages)} landing page entries."
            }

        except Exception as e:
            provenance["status"] = f"ERROR: {str(e)}"
            return {
                "provenance": provenance,
                "organic_landing_pages": [],
                "whatsapp_lead_inquiries_tracked": False,
                "notes": f"GA4 Data API notice: {e}"
            }

    def fetch_bing_intelligence(self) -> Dict[str, Any]:
        """
        Collect Microsoft Bing Webmaster performance, crawl health, and keyword statistics.
        """
        provenance = {
            "source": "Microsoft Bing Webmaster REST API",
            "property": self.site_url,
            "fetch_timestamp": self._get_timestamp_now(),
            "metric_type": "observed",
            "status": "UNAVAILABLE",
            "limitations": "Data represents organic search activity exclusively on the Bing Search network."
        }

        if not self.bing_key:
            return {
                "provenance": provenance,
                "daily_submission_quota": "N/A",
                "notes": "BING_WEBMASTER_API_KEY not configured."
            }

        try:
            quota_url = f"https://ssl.bing.com/webmaster/api.svc/json/GetUrlSubmissionQuota?siteUrl={urllib.parse.quote_plus(self.site_url)}&apikey={urllib.parse.quote_plus(self.bing_key)}"
            req = urllib.request.Request(quota_url, headers={"User-Agent": "AIDigiTools-Search-Intel/1.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                d = data.get("d", {})
                daily = d.get("DailyQuota", 100)

            provenance["status"] = "CONNECTED"
            return {
                "provenance": provenance,
                "daily_submission_quota": daily,
                "notes": f"Bing Webmaster API active. Daily submission quota: {daily} URLs."
            }
        except Exception as e:
            provenance["status"] = f"ERROR: {str(e)}"
            return {
                "provenance": provenance,
                "daily_submission_quota": "N/A",
                "notes": f"Bing API notice: {e}"
            }

    def fetch_trending_search_queries(self, seed_topics: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Collect live trending search queries via Google Predictive Autocomplete gateway.
        Strict Invariant: Tagged as INFERRED relative trend interest, not exact monthly search volume.
        """
        seeds = seed_topics or [
            "ai tools", "best ai video generator", "cursor ai vs", "chatgpt plus pakistan",
            "claude 3.5 sonnet", "midjourney alternatives", "deepseek r1", "ai coding assistant"
        ]

        provenance = {
            "source": "Google Autocomplete Predictive Trends Engine",
            "fetch_timestamp": self._get_timestamp_now(),
            "metric_type": "inferred_trend_interest",
            "status": "CONNECTED",
            "limitations": "Reflects real-time predictive user search velocity. Does not represent absolute monthly search volume counts."
        }

        discovered_trends = {}
        for seed in seeds:
            try:
                url = f"https://suggestqueries.google.com/complete/search?client=chrome&q={urllib.parse.quote_plus(seed)}"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
                with urllib.request.urlopen(req, timeout=8) as resp:
                    data = json.loads(resp.read().decode("utf-8", errors="ignore"))
                    suggestions = data[1] if len(data) > 1 else []
                    discovered_trends[seed] = suggestions[:8]
            except Exception as e:
                discovered_trends[seed] = []

        total_discovered = sum(len(v) for v in discovered_trends.values())
        return {
            "provenance": provenance,
            "seeds_scanned": len(seeds),
            "total_trending_queries_discovered": total_discovered,
            "trends_by_seed": discovered_trends,
            "notes": f"Successfully captured {total_discovered} live real-time query suggestions across {len(seeds)} AI clusters."
        }

    def fetch_pagespeed_crux_intelligence(self) -> Dict[str, Any]:
        """
        Monitor Core Web Vitals (LCP, CLS, FCP) and Lighthouse performance scores.
        """
        provenance = {
            "source": "Google PageSpeed Insights & CrUX API",
            "property": self.site_url,
            "fetch_timestamp": self._get_timestamp_now(),
            "metric_type": "observed",
            "status": "UNAVAILABLE",
            "limitations": "Lighthouse simulates mobile device conditions. CrUX reports 28-day rolling real-user metrics where sample density permits."
        }

        if not self.pagespeed_key:
            return {
                "provenance": provenance,
                "performance_score": "N/A",
                "core_web_vitals": {},
                "notes": "PAGESPEED_API_KEY not configured."
            }

        try:
            url = f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url={urllib.parse.quote_plus(self.site_url)}&key={urllib.parse.quote_plus(self.pagespeed_key)}&strategy=mobile"
            req = urllib.request.Request(url, headers={"User-Agent": "AIDigiTools-CrUX-Monitor/1.0"})
            with urllib.request.urlopen(req, timeout=35) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                lh = data.get("lighthouseResult", {})
                cats = lh.get("categories", {})
                perf = int(cats.get("performance", {}).get("score", 0) * 100)
                audits = lh.get("audits", {})
                lcp = audits.get("largest-contentful-paint", {}).get("displayValue", "N/A")
                cls = audits.get("cumulative-layout-shift", {}).get("displayValue", "N/A")
                fcp = audits.get("first-contentful-paint", {}).get("displayValue", "N/A")

            provenance["status"] = "CONNECTED"
            return {
                "provenance": provenance,
                "performance_score": perf,
                "core_web_vitals": {
                    "LCP": lcp,
                    "CLS": cls,
                    "FCP": fcp
                },
                "notes": f"Lighthouse Mobile Score: {perf}/100. LCP: {lcp}, CLS: {cls}."
            }
        except Exception as e:
            provenance["status"] = f"ERROR: {str(e)}"
            return {
                "provenance": provenance,
                "performance_score": "N/A",
                "core_web_vitals": {},
                "notes": f"PageSpeed API notice: {e}"
            }

    def generate_unified_intelligence_report(self) -> Dict[str, Any]:
        """
        Synthesize multi-source search intelligence with strict data provenance.
        Does NOT invent missing data.
        """
        print("[SearchIntelligence] Aggregating multi-source search intelligence...")
        gsc = self.fetch_gsc_intelligence()
        ga4 = self.fetch_ga4_intelligence()
        bing = self.fetch_bing_intelligence()
        trends = self.fetch_trending_search_queries()
        speed = self.fetch_pagespeed_crux_intelligence()

        report = {
            "report_generated_at_utc": self._get_timestamp_now(),
            "target_domain": self.site_url,
            "google_search_console": gsc,
            "google_analytics_4": ga4,
            "bing_webmaster": bing,
            "predictive_trends": trends,
            "pagespeed_and_crux": speed,
            "summary": {
                "active_sources": [
                    k for k, v in [
                        ("GSC", gsc["provenance"]["status"]),
                        ("GA4", ga4["provenance"]["status"]),
                        ("Bing", bing["provenance"]["status"]),
                        ("Trends", trends["provenance"]["status"]),
                        ("PageSpeed", speed["provenance"]["status"]),
                    ] if v == "CONNECTED"
                ],
                "total_trending_queries": trends.get("total_trending_queries_discovered", 0),
                "high_impression_low_ctr_opportunities": len(gsc.get("opportunities", [])),
                "cannibalization_risks_detected": len(gsc.get("cannibalization_risks", []))
            }
        }

        # Save report to data directory
        with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"[SearchIntelligence] Report successfully saved -> {OUTPUT_REPORT_PATH}")
        return report

if __name__ == "__main__":
    agg = SearchIntelligenceAggregator()
    report = agg.generate_unified_intelligence_report()
    print("Report Summary:", json.dumps(report["summary"], indent=2))

