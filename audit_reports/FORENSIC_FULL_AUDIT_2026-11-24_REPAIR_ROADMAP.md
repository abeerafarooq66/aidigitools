# AIDigiTools — Prioritized Repair Roadmap & Remediation Blueprint

**Document Version:** 1.0.0  
**Date:** 24 November 2026  
**Governance:** Follows `PROJECT_RULES.md` (SPEC → PLAN → EXECUTE → VERIFY → COMMIT)  
**Execution Status:** **AUDIT ONLY — PENDING OWNER APPROVAL BEFORE EXECUTION**

---

## 1. Governance & Execution Principles

Before any line of production code is changed:
1. Every fix must have an approved **SPEC** defining the exact change, affected files, expected output, and verification test.
2. Changes must be executed on a dedicated Git branch (e.g., `fix/encoding-and-analytics-remediation`), never directly on `main`.
3. Automated verification scripts must pass before opening a Pull Request.
4. **Zero production changes occur during this audit task.**

---

## 2. Horizon 1: Immediate Protection & Business Integrity (Horizon P0/P1 — Days 1–3)

### Goal: Eliminate storefront character corruption, secure admin exposure, fix conversion tracking, and quarantine fabricated metrics.

---

### Task H1.1: Automated Site-Wide UTF-8 Character & Glyph Restoration
- **Issue ID:** `P1-ENC-001`
- **Affected Scope:** All 49 files in `tools/*.html`.
- **Root Cause:** Git commit `eee2c84` rewrote all 49 HTML tool files using Windows ANSI/system default encoding instead of UTF-8, destroying 4-byte Unicode characters (emojis) and em-dashes into `??`, `?`, and `\uFFFD` (``).
- **Remediation Specification:**
  - Create a Python/Node.js script that parses the uncorrupted baseline from Git commit `eee2c84~1`.
  - For each tool file, extract clean Unicode strings: `🟢 Orders Accepted`, `Smart Tools • Bigger Possibilities`, `⚡ Quick Order`, `🛡️ 30-Day Replacement Warranty`, `⏱️ 15m Delivery`, `👤 1 User (2 Devices Active)`.
  - Re-inject clean strings into the 49 files, saving strictly with UTF-8 encoding (without BOM).
  - Add an automated pre-commit hook or CI test (`scripts/verify_utf8_clean.js`) that fails if literal `??` or `\uFFFD` are detected in any HTML file.
- **Verification Condition:** Zero instances of `\uFFFD` or accidental `??` in all HTML files. Visual verification in Chrome shows clean typography across all tool profiles.
- **Rollback Plan:** `git checkout main -- tools/`.

---

### Task H1.2: GA4 Event Delegation & Full Funnel Attribution Fix
- **Issue ID:** `P1-GA4-001`
- **Affected Scope:** `assets/analytics-events.js`, `assets/cart.js`, `blog.html`.
- **Root Cause:** Event listeners are statically bound on `DOMContentLoaded`, failing to capture WhatsApp checkout buttons rendered dynamically by `cart.js`. `blog.html` is missing the GA4 tag.
- **Remediation Specification:**
  - Replace static `querySelectorAll` in `assets/analytics-events.js` with document-level event delegation:
    ```javascript
    document.addEventListener('click', function (e) {
      // 1. WhatsApp click delegation
      var waLink = e.target.closest('a[href*="wa.me"], a[href*="api.whatsapp.com"]');
      if (waLink) {
        var toolName = waLink.getAttribute('data-tool-name') || document.title.split('|')[0].trim();
        var toolPrice = waLink.getAttribute('data-tool-price') || '0';
        if (typeof gtag === 'function') {
          gtag('event', 'wa_concierge_checkout', {
            'tool_name': toolName,
            'value': parseFloat(toolPrice) || 0,
            'currency': 'PKR',
            'link_url': waLink.href,
            'transport_type': 'beacon'
          });
        }
      }
      // 2. Quick Order button delegation
      var qoBtn = e.target.closest('button[onclick*="openQuickOrderModal"]');
      if (qoBtn) {
        var match = (qoBtn.getAttribute('onclick') || '').match(/openQuickOrderModal\('([^']+)'\)/);
        var toolSlug = match ? match[1] : 'general';
        if (typeof gtag === 'function') {
          gtag('event', 'initiate_quick_order', {
            'tool_slug': toolSlug
          });
        }
      }
    });
    ```
  - Install the Google tag (`G-NE094X2Q7H`) in the `<head>` of `blog.html`.
  - Mark `wa_concierge_checkout` and `initiate_quick_order` as Key Events in GA4 Admin.
- **Verification Condition:** Test click in Chrome triggers `wa_concierge_checkout` in GA4 Realtime / DebugView with `transport_type: beacon`.
- **Rollback Plan:** `git checkout main -- assets/analytics-events.js blog.html`.

---

### Task H1.3: Quarantine Fabricated Analytics Data & Refactor Agent
- **Issue ID:** `P0-INT-001`
- **Affected Scope:** `seo-agent/agent/conversion_analytics.py`, `data/analytics_report_*.json`.
- **Root Cause:** Lines 92–100 of `conversion_analytics.py` hardcode synthetic numbers (`base_impressions = 48500`, `base_clicks = 2650`, `base_confirmed = 98`) and multiply them across report periods.
- **Remediation Specification:**
  - Add an explicit banner to `data/analytics_report_*.json`: `"data_provenance": "SYNTHETIC_MODEL_FIXTURE_DO_NOT_CITE_AS_FACTUAL"`.
  - Refactor `conversion_analytics.py` so it requires authenticated GA4 / GSC API inputs to generate real reports; if credentials are unset, output explicitly labeled mock files (`data/mock_simulation_*.json`).
  - Purge any marketing copy, dashboard markdown, or PR text claiming 48.5k impressions or 98 verified orders.
- **Verification Condition:** Automated test asserts `data_provenance` is present and verified API credentials are required for production reports.
- **Rollback Plan:** Git branch restoration.

---

### Task H1.4: Secure Admin Dashboards & Restrict AI Crawler Directives
- **Issue ID:** `P1-SEC-001`
- **Affected Scope:** `admin/meta-integration.html`, `robots.txt`.
- **Root Cause:** `admin/meta-integration.html` is deployed publicly with `index, follow`. `robots.txt` explicitly allows AI crawlers full `/` access without admin exclusions.
- **Remediation Specification:**
  - In `admin/meta-integration.html`, replace `<meta name="robots" content="index, follow">` with `<meta name="robots" content="noindex, nofollow, noarchive">`.
  - In `robots.txt`, add `Disallow: /admin/` and `Disallow: /data/previews/` under all specific bot blocks, including `OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `GPTBot`, `ClaudeBot`, and `Applebot`.
- **Verification Condition:** `robots.txt` validator confirms `/admin/` is blocked for all 12 declared user-agents. HTTP test of `admin/meta-integration.html` returns `noindex, nofollow`.

---

### Task H1.5: Fix Stray Syntax & Broken Prices in Comparison Pages
- **Issue ID:** `P2-HTML-001`
- **Affected Scope:** `compare/chatgpt-vs-claude.html`.
- **Remediation Specification:**
  - Remove trailing `>>` characters from lines 18 and 38.
  - Correct meta description: `Detailed benchmark: ChatGPT Plus (Rs. 2,300 PKR / $8.00 USD) vs Claude Pro (Rs. 2,500 PKR / $9.00 USD). Coding speed, context window & 30-day warranty.`
- **Verification Condition:** HTML validator reports 0 unclosed or stray tags. Browser rendering verifies no text appears above navbar.

---

## 3. Horizon 2: Foundation & Unblocking Indexation (Horizon P1/P2 — Weeks 1–2)

### Goal: Address Google's 44 "Crawled - currently not indexed" pages, consolidate payment rail cannibalization, configure Merchant Center safely, and improve accessibility.

---

### Task H2.1: Payment Rail Cannibalization Elimination & Intent Consolidation
- **Issue ID:** `P1-GSC-002`
- **Affected Scope:** All 49 `tools/*.html` pages, `index.html`, `policies.html`.
- **Remediation Specification:**
  - Remove repetitive payment keywords ("EasyPaisa", "JazzCash", "SadaPay", "NayaPay") from page `<title>`, `<meta description>`, and secondary headings across tool pages.
  - Consolidate all payment rails information into a rich, dedicated pillar section on `https://aidigitools.tech/policies.html#payments`.
  - On tool pages, replace repetitive keyword blocks with a clean, unified trust chip: `Verified Domestic & International Payment Options → [View Accepted Rails](/policies.html#payments)`.
- **Verification Condition:** Internal site search and GSC crawl verify zero keyword stuffing of domestic payment gateways on individual tool pages.

---

### Task H2.2: Tool Page Content Enrichment & Unblocking Google Indexation
- **Issue ID:** `P1-GSC-001`
- **Affected Scope:** 44 "Crawled - currently not indexed" pages in `tools/`.
- **Remediation Specification:**
  - Audit reveals Google classifies these pages as thin/duplicate because they follow a rigid template with brief vendor feature summaries.
  - Select the Top 15 commercial tools (`claude-pro`, `chatgpt-plus`, `cursor-pro`, `turnitin-student`, `midjourney`, `canva-pro`, `youtube-premium`, `runway-gen3`, `capcut-pro`, `deepseek-pro`, `elevenlabs-creator`, `github-copilot`, `semrush-guru`, `nordvpn`, `surfshark-vpn`).
  - Add original, localized content to each:
    - First-hand Pakistani developer/creator workflow test notes.
    - Specific hardware/OS compatibility benchmark findings.
    - Clear distinction between official vendor retail pricing vs AIDigiTools reference concierge pricing.
    - 3 unique, non-templated FAQs addressing Pakistani billing, regional limitations, and account access.
- **Verification Condition:** Submit enriched representative URLs via GSC URL Inspection. Monitor transition from "Crawled - currently not indexed" to "Indexed".

---

### Task H2.3: Google Merchant Center Policy Alignment & Safe Feed Onboarding
- **Issue ID:** `P1-GMC-001`
- **Affected Scope:** Google Merchant Center account `5888946609`, `merchant_feed.xml`.
- **Remediation Specification:**
  - **ACTION ITEM 1:** Open GMC Products Settings and click **"Remind me later"** or pause automated website crawl product addition scheduled for 11 December 2026.
  - **ACTION ITEM 2:** Complete Merchant Center business verification (verify business name, customer service phone, Pakistani support address, and refund policy URL).
  - **ACTION ITEM 3:** Confirm whether digital subscription concierge models satisfy Google Shopping free listing policies for Pakistan. If approved, link `https://aidigitools.tech/merchant_feed.xml` as a Scheduled Fetch Primary Data Source.
- **Verification Condition:** GMC Diagnostics displays 0 critical account-level policy warnings.

---

### Task H2.4: Accessibility & Design System Remediation
- **Issue ID:** `P2-A11Y-001`
- **Affected Scope:** `assets/style.css`, `index.html`.
- **Remediation Specification:**
  - Increase contrast ratio for status badges (e.g. adjust `#ecfdf5` background and `#065f46` text to guarantee minimum 4.5:1 contrast).
  - Update `aria-label` on buttons to match visible text (`aria-label="Quick Order"` on buttons containing "Quick Order").
- **Verification Condition:** Lighthouse Accessibility score improves from 97 to 100 with zero contrast or label mismatch violations.

---

## 4. Horizon 3: Growth & Automated Engineering Quality (Horizon P2/P3 — Weeks 3–4)

### Goal: Secure CI/CD automated workflows, build topical cluster authority, track Bing AI citations, and optimize performance.

---

### Task H3.1: CI/CD Workflow Governance & Pull-Request Safety Gates
- **Issue ID:** `P2-OPS-001`
- **Affected Scope:** `.github/workflows/auto-blog-publisher.yml`, `content_intelligence_scheduler.yml`, `autonomous-seo-engineer.yml`, `aio-agent-daily.yml`.
- **Remediation Specification:**
  - Revoke direct `git push origin main` permissions from scheduled workflows.
  - Configure workflows to output changes to a new branch (e.g., `auto-content/update-YYYYMMDD`) and create a GitHub Pull Request via `peter-evans/create-pull-request@v6`.
  - Resolve overlapping cron schedule: change `auto-blog-publisher.yml` to `0 2 * * *` and `content_intelligence_scheduler.yml` to `0 4 * * *`.
- **Verification Condition:** Test workflow dispatch generates a clean Pull Request rather than writing directly to `main`.

---

### Task H3.2: Performance & Code Splitting Optimization
- **Issue ID:** `P2-PERF-001`
- **Affected Scope:** `assets/cart.js`, `assets/style.css`.
- **Remediation Specification:**
  - Split `cart.js` (2546 lines, ~100KB) into:
    1. `cart-core.js` (lightweight drawer UI, ~15KB, loaded on all pages).
    2. `tools-catalog-data.json` (asynchronous fetch when user opens the catalogue or drawer, rather than parsed synchronously).
  - Defer non-critical scripts.
- **Verification Condition:** Mobile Total Blocking Time (TBT) decreases from 300ms to <150ms. Performance score reaches 95+.

---

### Task H3.3: AI Search Visibility & GEO Measurement Cadence
- **Issue ID:** `P2-AI-001`
- **Affected Scope:** `llms.txt`, `llms-full.txt`, Bing AI Performance tracking.
- **Remediation Specification:**
  - Establish a weekly manual/semi-automated test protocol across Microsoft Copilot, Perplexity, ChatGPT Search, and Gemini for 10 commercial prompts.
  - Record date, prompt, citation presence, and grounding URL in a dedicated log (`audit_reports/AI_CITATION_TRACKING.md`).
  - Keep `llms.txt` and `llms-full.txt` updated with accurate canonical pricing and version references.
- **Verification Condition:** Reproducible citation evidence documented across multiple measurement windows.

---

## 5. Summary Approval Table for Owner

| Task ID | Description | Severity | Estimated Effort | Requires Owner Approval? | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **H1.1** | Restore UTF-8 characters across all 49 tool pages (fix `??` and ``) | P1 High | 2 Hours (M) | **YES** | Ready for execution upon approval |
| **H1.2** | Fix GA4 event delegation for WhatsApp checkout & install on blog | P1 High | 1 Hour (S) | **YES** | Ready for execution upon approval |
| **H1.3** | Quarantine fabricated analytics metrics in agent & JSON reports | P0 Critical | 1 Hour (S) | **YES** | Ready for execution upon approval |
| **H1.4** | Add noindex to admin dashboard & disallow AI bots from /admin/ in robots.txt | P1 High | 30 Mins (S) | **YES** | Ready for execution upon approval |
| **H1.5** | Clean stray `>>` characters & blanked prices in comparison metadata | P2 Medium | 15 Mins (S) | **YES** | Ready for execution upon approval |
| **H2.1** | Consolidate payment rail keywords to eliminate GSC cannibalization | P1 High | 4 Hours (M) | **YES** | Pending Horizon 1 completion |
| **H2.2** | Enrich Top 15 tool pages with original content to fix 44 unindexed pages | P1 High | 8 Hours (L) | **YES** | Pending Horizon 1 completion |
| **H2.3** | Pause Merchant Center auto-addition & audit digital goods policy | P1 High | 2 Hours (M) | **YES** | Pending Horizon 1 completion |
| **H2.4** | Fix color contrast and accessible button names for Lighthouse 100 | P2 Medium | 1 Hour (S) | **YES** | Pending Horizon 1 completion |
| **H3.1** | Convert automated workflows from direct commit to Pull Request mode | P2 Medium | 3 Hours (M) | **YES** | Pending Horizon 2 completion |
| **H3.2** | Split `cart.js` to reduce mobile Total Blocking Time (TBT) | P2 Medium | 4 Hours (M) | **YES** | Pending Horizon 2 completion |
| **H3.3** | Establish recurring GEO citation measurement ledger | P2 Medium | 2 Hours (S) | **YES** | Pending Horizon 2 completion |
