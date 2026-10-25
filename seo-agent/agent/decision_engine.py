class GrowthDecisionEngine:
    """HERMES Decision Engine: Analyzes audit results and generates automated optimization proposals."""

    def evaluate_audit(self, audit_report: dict) -> list[dict]:
        proposals = []

        if not audit_report.get("robots_txt_exists", True):
            proposals.append({
                "type": "CRITICAL_FIX",
                "component": "robots.txt",
                "action": "Generate robots.txt allowing search crawlers and AI search agents.",
                "priority": "P0"
            })

        if not audit_report.get("sitemap_xml_exists", True):
            proposals.append({
                "type": "CRITICAL_FIX",
                "component": "sitemap.xml",
                "action": "Generate canonical sitemap.xml with accurate lastmod dates.",
                "priority": "P0"
            })

        for page in audit_report.get("results", []):
            checks = page.get("checks", {})
            file_name = page.get("file", "")

            if not checks.get("title", {}).get("passed", True):
                proposals.append({
                    "type": "TITLE_OPTIMIZATION",
                    "file": file_name,
                    "action": f"Adjust title tag length (currently {checks['title']['length']} chars).",
                    "priority": "P1"
                })

            if not checks.get("meta_description", {}).get("passed", True):
                proposals.append({
                    "type": "META_DESCRIPTION_OPTIMIZATION",
                    "file": file_name,
                    "action": f"Optimize meta description length to 70-160 characters (currently {checks['meta_description']['length']} chars).",
                    "priority": "P1"
                })

            if not checks.get("single_h1", {}).get("passed", True):
                proposals.append({
                    "type": "HEADING_HIERARCHY_FIX",
                    "file": file_name,
                    "action": f"Fix H1 tag count (currently {checks['single_h1']['count']}). Exactly one H1 required.",
                    "priority": "P0"
                })

            if not checks.get("canonical", {}).get("passed", True):
                proposals.append({
                    "type": "CANONICAL_FIX",
                    "file": file_name,
                    "action": "Ensure canonical link is present and points to aidigitools.tech domain.",
                    "priority": "P0"
                })

        return proposals
