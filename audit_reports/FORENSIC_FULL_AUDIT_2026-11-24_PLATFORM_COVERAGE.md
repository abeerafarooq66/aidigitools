# AIDigiTools — Connected Platform Audit & Coverage Register

**Audit Date:** 24 November 2026  
**Auditor:** Antigravity Forensic Architecture Suite  
**Operating Mode:** Read-Only Investigation (Authorized Sessions Inspected in Chrome)

---

## 1. Executive Platform Connectivity Summary

| Platform | Property / Account ID | Authorized User | Inspection State | Primary Findings Summary |
| :--- | :--- | :--- | :--- | :--- |
| **Google Search Console** | `https://aidigitools.tech/`<br>`sc-domain:aidigitools.tech` | Abeera Farooq (`abeerafarooq731@gmail.com`) | **COMPLETE** | 7 clicks, 307 impressions (3m). 15 indexed, 58 not indexed (44 crawled-not-indexed, 13 discovered-not-indexed, 1 canonical-alt). Top impressions dominated by domestic payment terms. |
| **Bing Webmaster Tools** | `https://aidigitools.tech/` | Authorized Session | **COMPLETE** | Site Explorer: 31 indexed, 5 excluded, 0 errors, 36 URLs. AI Performance (BETA): 7 total citations (Nov 7 & 8), 0 grounding queries. |
| **Google Analytics 4** | `AIDigiTools Production`<br>(ID: `561800932`) | Abeera Farooq (`abeerafarooq731@gmail.com`) | **COMPLETE** | 294 pageviews, 106 active users (28d). 0 key events / conversions. WhatsApp concierge checkout events not firing due to dynamic selector binding mismatch. |
| **Google Merchant Center** | `AiDigiTools`<br>(ID: `5888946609`) | Abeera Farooq (`abeerafarooq731@gmail.com`) | **COMPLETE** | "No products added yet". Notification banner states 8 products discovered by crawler scheduled for automatic addition on 11 Dec 2026. `merchant_feed.xml` not linked as Primary Data Source. |
| **PageSpeed / Lighthouse** | `https://aidigitools.tech/` | Local Headless Chrome / Node CLI | **COMPLETE** | Mobile Lab: Performance 90, Accessibility 97, Best Practices 100, SEO 100. Desktop Lab: Performance 86, Accessibility 97, Best Practices 100, SEO 100. CrUX field data: No origin data due to low traffic volume. |

---

## 2. Google Search Console Surface Breakdown

### A. Performance Report (Search Analytics)
- **Time Range Inspected:** Full 3-Month Range (25 Oct 2026 – 22 Nov 2026) and 28-Day Range.
- **Data Freshness:** Last updated 3.5 hours prior to inspection.
- **Observed Metrics:**
  - **Total Clicks:** 7
  - **Total Impressions:** 307
  - **Average CTR:** 2.3%
  - **Average Position:** 28.9
- **Query Portfolio Insights:**
  1. `"sadapay"`: 0 clicks, 30 impressions (Avg pos ~42)
  2. `"nayapay"`: 0 clicks, 27 impressions (Avg pos ~48)
  3. `"jazzcash"`: 0 clicks, 10 impressions (Avg pos ~51)
  4. `ai45813`: 0 clicks, 6 impressions (Avg pos ~38)
  5. `"easypaisa"`: 0 clicks, 5 impressions (Avg pos ~45)
  6. `spotify premium`: 0 clicks, 4 impressions (Avg pos ~12)
  7. `runway pika`: 0 clicks, 2 impressions (Avg pos ~9)
- **Forensic Diagnosis:** The site is suffering from **Payment Rail Keyword Cannibalization**. Over 70% of impression volume comes from domestic wallet queries where searchers have zero transactional intent for AI software.

### B. Page Indexing Report
- **Time Range Inspected:** As of 16 November 2026.
- **Indexed Status:** **15 pages**
- **Not Indexed Status:** **58 pages** across 3 distinct Google categories:
  1. **Crawled - currently not indexed (44 pages):** Googlebot crawled these URLs (predominantly `tools/*.html` profiles) but chose not to index them due to perceived thinness, templated repetition, and low external authority.
  2. **Discovered – currently not indexed (13 pages):** Googlebot identified the URLs from `sitemap.xml` but has not allocated crawl priority yet.
  3. **Alternative page with proper canonical tag (1 page):** `/index.html` or `deals.html` pointing to canonical destination.

### C. Experience & Enhancements
- **Core Web Vitals:** "No data" for both Mobile and Desktop (insufficient traffic volume for CrUX 28-day aggregation threshold).
- **HTTPS:** 15 Valid HTTPS URLs, 0 Non-HTTPS errors.
- **Shopping Enhancements (Extracted from Schema markup):**
  - Product Snippets: 11 Valid, 0 Invalid.
  - Merchant Listings: 11 Valid, 0 Invalid.
- **Breadcrumbs:** 13 Valid, 0 Invalid.

---

## 3. Bing Webmaster Tools Surface Breakdown

### A. Site Explorer
- **Index Status:** **31 Indexed**, **5 Excluded**, **0 Errors**, **0 Warnings**.
- **Scope:** 36 URLs tracked across root and subfolders.
- **Crawl Evidence:** Representative URLs like `blog.html` crawled on 16 Nov 2026 (HTTP 200, 33.3KB).
- **Impressions:** 7 total impressions in the 6-month folder overview.

### B. AI Performance (BETA) Report
- **Date Range Inspected:** 24 August 2026 – 23 November 2026 (Last 3 Months).
- **Citation Sources:** Microsoft Copilots and Partners.
- **Total Citations Recorded:** **7 Citations**.
- **Citation Distribution by Date:**
  - 07 November 2026: **5 citations** (Average Cited Pages: 1)
  - 08 November 2026: **2 citations** (Average Cited Pages: 1)
- **Grounding Queries:** Displayed as *"No data available"*. Bing applies minimum query volume thresholds to protect user privacy; AIDigiTools citation volume is currently beneath the individual query exposure threshold.

---

## 4. Google Analytics 4 Surface Breakdown

### A. Account & Tag Health
- **Account ID:** `a414293126`
- **Property Name:** `AIDigiTools Production` (`p561800932`)
- **Measurement Tag:** `G-NE094X2Q7H` installed on 77 HTML pages.
- **Missing Tag Flag:** `blog.html` (the primary editorial hub) and `data/previews/` files are completely missing `G-NE094X2Q7H`.

### B. Pages and Screens Report (Last 28 Days: 27 Oct – 23 Nov 2026)
- **Total Pageviews:** 294
- **Active Users:** 106
- **Top 10 Landings by Views:**
  1. `/` (root storefront): 112 views, 48 users
  2. `/index.html`: 56 views, 11 users
  3. `/tools/claude-pro.html`: 27 views, 12 users
  4. `/tools/turnitin-student.html`: 12 views, 9 users
  5. `/categories/image.html`: 10 views, 4 users
  6. `/contact.html`: 9 views, 4 users
  7. `/deals.html`: 9 views, 7 users
  8. `/categories/video.html`: 8 views, 7 users
  9. `/guides/chatgpt-vs-claude.html`: 6 views, 3 users
  10. `/policies.html`: 6 views, 4 users

### C. Conversion Funnel Status
- **Key Events / Conversions:** **0**.
- **Custom Event Tracking Failure:** `assets/analytics-events.js` attempts to bind to `a[href*="wa.me"]` on `DOMContentLoaded`. However, `assets/cart.js` dynamically builds and inserts WhatsApp checkout buttons when `openQuickOrderModal()` is triggered or catalogue cards render. As a result, 0 conversion events reach GA4.

---

## 5. Google Merchant Center Surface Breakdown

### A. Account Overview
- **Account Name:** `AiDigiTools`
- **Account ID:** `5888946609`
- **Current Active Products:** **0**.
- **Active Diagnostic Banner:**
  > *"Show customers 8 more products from aidigitools.tech. Google found additional products on your online store. They'll be automatically added on December 11, 2026 and kept updated every 24 hours in Merchant Center."*

### B. Feed & Policy Mismatch Analysis
- `merchant_feed.xml` exists in the GitHub repository (49 products formatted in Google Base RSS 2.0).
- **Root Disconnect:** The feed file was never added as a Primary Data Source inside Google Merchant Center. The 8 products referenced in the banner were discovered by Google's automatic website crawl.
- **Policy Compliance Risk:** Google Shopping requires landing pages to have direct electronic checkout (credit card, recognized payment gateway) with transparent pricing and standard merchant terms. Directing customers to a manual WhatsApp chat for bank IBFT / EasyPaisa / SadaPay transfers may trigger a Merchant Center policy disapproval or account suspension if submitted blindly.

---

## 6. PageSpeed & Core Web Vitals Coverage

| Test Environment | Strategy | Performance | Accessibility | Best Practices | SEO | FCP | LCP | TBT | CLS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Lighthouse 13.6** | Mobile Lab | **90** | **97** | **100** | **100** | 1.9s | 1.9s | 300ms | 0 |
| **Lighthouse 13.6** | Desktop Lab | **86** | **97** | **100** | **100** | 0.7s | 0.7s | 290ms | 0 |
| **CrUX Real User** | Field Data | **No Data** | — | — | — | — | — | — | — |

*Note: PageSpeed Insights public API returned daily quota limit for consumer project; verified via local Lighthouse 13.6 headless Chrome runs.*

---

## 7. Evidence Artifacts Register

Screenshots captured from live Chrome sessions and stored in `audit_reports/FORENSIC_FULL_AUDIT_2026-11-24_EVIDENCE/`:
1. `01_homepage_hero_badges.png` — Hero typography, domestic rails badges, WhatsApp CTA.
2. `02_homepage_categories_simulator.png` — Category navigation and interactive tool selector.
3. `03_homepage_pricing_table.png` — Pricing transparency matrix and warranty terms.
4. `04_homepage_guides_comparisons.png` — Editorial comparison hubs and guides list.
5. `05_compare_chatgpt_claude_stray_chars.png` — Visible `>> >> >>` text artifact above header on `/compare/chatgpt-vs-claude.html`.
6. `06_adobe_tool_page_encoding_hero.png` — Live production view of `tools/adobe-creative-cloud.html` showing `?? Orders Accepted` and `ï¿½` diamond replacement characters.
7. `07_adobe_tool_page_plans_features.png` — Plans and pricing grid showing corrupted `?` bullet icons and `?? 1 User`.
