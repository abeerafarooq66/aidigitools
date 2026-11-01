"""
AIDigiTools — Blog Website Architecture & Routing Engine
Strictly implements Section 14 of Master Architecture Charter:
BLOG WEBSITE ARCHITECTURE
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
from email.utils import format_datetime

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
BLOG_REGISTRY_PATH = ROOT_DIR / "data" / "blog_articles_registry.json"
FEED_PATH = ROOT_DIR / "feed.xml"

THIN_TAG_PATTERNS = [
    r"/tags?/",
    r"/date/\d{4}/",
    r"/archives?/",
    r"/author/page/\d+/",
    r"/tag-[a-z0-9-]+"
]

DATE_BASED_URL_PATTERN = r"/\d{4}/\d{2}(?:/\d{2})?/"

class BlogArchitectureEngine:
    def __init__(self, registry_path: Optional[Path] = None):
        self.registry_path = registry_path or BLOG_REGISTRY_PATH
        self.registry = self._load_registry()

    def _load_registry(self) -> Dict[str, Any]:
        if not self.registry_path.exists():
            return {"articles": []}
        try:
            with open(self.registry_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"articles": []}

    def validate_article_url(self, url: str) -> Tuple[bool, List[str]]:
        """
        Enforce clean evergreen URLs:
        - No date-based paths (e.g. /2026/11/01/slug)
        - No thin tag, archive, or duplicate pagination paths
        - No query parameters or fragment identifiers in canonical URL
        """
        violations = []

        # 1. Date-based check
        if re.search(DATE_BASED_URL_PATTERN, url):
            violations.append(f"URL Violation: '{url}' contains date-based path. Ever-green URLs are required.")

        # 2. Thin tag / archive check
        for pattern in THIN_TAG_PATTERNS:
            if re.search(pattern, url.lower()):
                violations.append(f"URL Violation: '{url}' matches thin tag/archive pattern '{pattern}'. Thin tag pages are prohibited.")

        # 3. Query string / fragment check
        if "?" in url or "#" in url:
            violations.append(f"URL Violation: Canonical URL '{url}' must not contain query parameters or fragments.")

        # 4. Trailing whitespace or uppercase
        if any(c.isupper() for c in url):
            violations.append(f"URL Violation: Canonical URL '{url}' must be strictly lowercase.")

        return len(violations) == 0, violations

    def validate_breadcrumbs(self, breadcrumbs: List[Dict[str, str]]) -> Tuple[bool, List[str]]:
        """
        Verify Breadcrumbs hierarchy:
        - Must begin with Home
        - Must have at least 2 items (Home > Section/Category > Page)
        - Each item must have non-empty 'name' and valid 'url'
        """
        violations = []
        if not breadcrumbs or len(breadcrumbs) < 2:
            violations.append("Breadcrumb Violation: Hierarchy must contain at least 2 levels (e.g. Home > Article).")
            return False, violations

        first = breadcrumbs[0]
        if first.get("name", "").lower() not in ["home", "aidigitools"]:
            violations.append(f"Breadcrumb Violation: Root item must be 'Home', found '{first.get('name')}'.")

        for idx, item in enumerate(breadcrumbs):
            if not item.get("name"):
                violations.append(f"Breadcrumb Violation: Item {idx+1} is missing 'name'.")
            if not item.get("url"):
                violations.append(f"Breadcrumb Violation: Item {idx+1} is missing 'url'.")

        return len(violations) == 0, violations

    def validate_related_entities(self, article_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Enforce strong interlinking graph:
        - Every article must map to at least 2 related tools
        - Every article must map to at least 2 related articles
        """
        violations = []
        related_tools = article_data.get("related_tools", [])
        related_articles = article_data.get("related_articles", [])

        if len(related_tools) < 2:
            violations.append(
                f"Interlinking Violation: Article has {len(related_tools)} related tools (minimum 2 required)."
            )

        if len(related_articles) < 2:
            violations.append(
                f"Interlinking Violation: Article has {len(related_articles)} related articles (minimum 2 required)."
            )

        return len(violations) == 0, violations

    def generate_rss_item(self, article: Dict[str, Any]) -> str:
        """Generate valid RSS 2.0 item element."""
        title = article.get("title", "")
        link = article.get("canonical_url", "")
        desc = article.get("description", title)
        pub_date = article.get("date_published", "2026-10-25T12:00:00+05:00")

        try:
            dt = datetime.fromisoformat(pub_date)
            formatted_date = format_datetime(dt)
        except Exception:
            formatted_date = "Sun, 25 Oct 2026 12:00:00 +0500"

        return f"""    <item>
      <title>{title}</title>
      <link>{link}</link>
      <guid>{link}</guid>
      <description>{desc}</description>
      <pubDate>{formatted_date}</pubDate>
    </item>"""

    def validate_article_architecture_compliance(
        self,
        html_content: str,
        article_data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Full audit of an article page against Section 14 Blog Architecture standards.
        """
        violations = []
        warnings = []
        article_data = article_data or {}

        # 1. Canonical URL check
        canonical_match = re.search(r'<link\s+[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']', html_content, re.I)
        if not canonical_match:
            violations.append("Missing Canonical Link: Article must have a canonical tag.")
        else:
            url_ok, url_viols = self.validate_article_url(canonical_match.group(1))
            violations.extend(url_viols)

        # 2. Breadcrumbs in DOM
        has_breadcrumbs = bool(re.search(r'<nav\s+[^>]*class=["\'][^"\']*breadcrumb[^"\']*["\']', html_content, re.I))
        if not has_breadcrumbs:
            violations.append("Missing Breadcrumb Navigation: Article lacks semantic <nav class='breadcrumbs'> element.")

        # 3. Responsive layout
        has_viewport = '<meta name="viewport"' in html_content
        if not has_viewport:
            violations.append("Responsive Layout Violation: Missing <meta name='viewport'> tag.")

        # 4. Related entities in DOM
        if article_data:
            ent_ok, ent_viols = self.validate_related_entities(article_data)
            violations.extend(ent_viols)

            # Check if related tools are linked in HTML
            for tool_slug in article_data.get("related_tools", []):
                if f"/tools/{tool_slug}.html" not in html_content and f"tools/{tool_slug}.html" not in html_content:
                    warnings.append(f"Interlinking Notice: Related tool '{tool_slug}' is declared but not linked in DOM.")

        passed = len(violations) == 0

        return {
            "passed": passed,
            "violations": violations,
            "warnings": warnings
        }

if __name__ == "__main__":
    engine = BlogArchitectureEngine()
    print("Testing BlogArchitectureEngine...")

    # Test clean evergreen URL
    ok, viols = engine.validate_article_url("https://aidigitools.tech/compare/chatgpt-vs-claude.html")
    print(f"Clean URL valid: {ok}")
    assert ok

    # Test date-based URL rejection
    bad_url_ok, bad_viols = engine.validate_article_url("https://aidigitools.tech/2026/11/01/chatgpt-vs-claude/")
    print(f"Date-based URL rejected: {not bad_url_ok}")
    assert not bad_url_ok

    # Test thin tag URL rejection
    tag_ok, tag_viols = engine.validate_article_url("https://aidigitools.tech/tags/ai-tools/")
    print(f"Thin tag URL rejected: {not tag_ok}")
    assert not tag_ok

    # Test breadcrumb validation
    crumbs = [
        {"name": "Home", "url": "https://aidigitools.tech/"},
        {"name": "Comparisons", "url": "https://aidigitools.tech/#products"},
        {"name": "ChatGPT vs Claude", "url": "https://aidigitools.tech/compare/chatgpt-vs-claude.html"}
    ]
    crumb_ok, _ = engine.validate_breadcrumbs(crumbs)
    print(f"Breadcrumbs valid: {crumb_ok}")
    assert crumb_ok

    # Test related entities
    article_sample = {
        "related_tools": ["chatgpt-plus", "claude-pro"],
        "related_articles": ["guides/chatgpt-vs-claude.html", "best/best-ai-coding-tools.html"]
    }
    rel_ok, _ = engine.validate_related_entities(article_sample)
    print(f"Related entities valid: {rel_ok}")
    assert rel_ok

    # Test RSS item generator
    rss_item = engine.generate_rss_item({
        "title": "ChatGPT vs Claude",
        "canonical_url": "https://aidigitools.tech/compare/chatgpt-vs-claude.html",
        "description": "Benchmark comparison.",
        "date_published": "2026-10-25T12:00:00+05:00"
    })
    print(f"RSS Item generated: {rss_item[:60]}...")
    assert "<item>" in rss_item and "<title>ChatGPT vs Claude</title>" in rss_item

    print("BlogArchitectureEngine self-test PASSED!")

