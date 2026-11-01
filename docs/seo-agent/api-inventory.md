# AIDigiTools Autonomous SEO Agent V2 — Complete API & Integration Inventory

**Document Reference**: `docs/seo-agent/api-inventory.md`  
**Platform**: `aidigitools.tech`  
**Charter**: Phase 0 — Credentials, Authentication, & Identity Architecture  
**Audit Date**: November 1, 2026  

---

## 1. Master Service Matrix

| Service Name | Already Configured? | Credential Type | Authentication Method | Required Scope / Permissions | Connection Status | Next Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **IndexNow Protocol** | ✅ **YES** | 32-char Hex Key | Public Key File Verification (`/{KEY}.txt`) | Public Read HTTP | **VERIFIED** (Live HTTP 200) | None (Active on Bing, Yandex, IndexNow Central) |
| **Microsoft Bing Webmaster API** | 🟡 **PARTIAL** | API Key (in GitHub Secrets as `BING_API_KEY`) | REST JSON API Header (`apikey`) | Webmaster read-only analytics | **READY IN CI / PENDING LOCAL** | Export to local `.env` if local runs needed |
| **Google PageSpeed Insights** | 🟡 **PARTIAL** | Google Cloud API Key (in GitHub Secrets as `PAGESPEED_API_KEY`) | Query parameter (`key=...`) | PageSpeed Insights API | **READY IN CI / PENDING LOCAL** | Restrict in GCP Console to PageSpeed API only |
| **Chrome UX Report (CrUX) API** | 🟡 **PARTIAL** | Google Cloud API Key | Query parameter (`key=...`) | Chrome UX Report API | **READY IN CI / PENDING LOCAL** | Enable CrUX API in GCP; restrict key |
| **Google Gemini API** | 🟡 **PARTIAL** | Google AI Studio API Key (in GitHub Secrets as `GEMINI_API_KEY`) | Query param / Bearer token | Generative Language API | **READY IN CI / PENDING LOCAL** | Verify quota; restrict to `generativelanguage.googleapis.com` |
| **Google Search Console (GSC) API** | 🟡 **PARTIAL** | Service Account JSON / Workload Identity (in GitHub Secrets as `GSC_SERVICE_ACCOUNT_KEY`) | OAuth 2.0 Bearer Token | `webmasters.readonly` | **READY IN CI / PENDING PROPERTY CONFIRMATION** | Add Service Account email to Search Console as Restricted User |
| **Google Analytics 4 (GA4) Data API** | 🔴 **PENDING** | Service Account / Workload Identity | OAuth 2.0 Bearer Token (`analytics.readonly`) | GA4 Viewer permission on Property ID | **PENDING USER ACTION** | Add SA email as GA4 Viewer; set `GA4_PROPERTY_ID` |
| **Google Ads API (Keyword Planner)** | ⚪ **OPTIONAL / PENDING** | OAuth 2.0 Client ID + Refresh Token (Developer tokens sunset Sept 2026) | OAuth 2.0 Bearer Token | Keyword Planner read-only | **PENDING APPROVAL / OPTIONAL** | Apply for Explorer access if production Ads account exists; otherwise use search data fallback |
| **Google Trends API** | ⚪ **FALLBACK** | Private Alpha (Google Trends API) | N/A (Private Access) | N/A | **PENDING APPROVAL** | Official alpha application pending; use GSC autocomplete fallback |
| **GitHub Actions Authentication** | ✅ **YES** | `GITHUB_TOKEN` + Workload Identity Federation | OIDC (Token exchange) | `contents: write`, `pull-requests: write` | **VERIFIED** | Enforce least-privilege token permissions per workflow |

---

## 2. Environment Variables Specification

### Non-Secret Environment Variables
* `GOOGLE_CLOUD_PROJECT_ID`: Name/ID of Google Cloud project (`aidigitools-content-agent`).
* `GCP_SERVICE_ACCOUNT_EMAIL`: Dedicated IAM Service Account email (`content-agent-sa@aidigitools-content-agent.iam.gserviceaccount.com`).
* `GCP_WORKLOAD_IDENTITY_PROVIDER`: Workload Identity Provider resource string for GitHub Actions keyless authentication.
* `GSC_SITE_URL`: Verified Search Console property root (`https://aidigitools.tech/`).
* `GA4_PROPERTY_ID`: Numeric Google Analytics 4 property ID (e.g., `123456789`). Note: Never use the `G-XXXXXX` Measurement ID.
* `INDEXNOW_KEY`: Standard 32-character hexadecimal string (`89d63ab53a63527b12a199a3096e51ad`).

### Secret Credentials (Stored in GitHub Secrets & Local .env)
* `BING_WEBMASTER_API_KEY`: Bing Webmaster API token.
* `PAGESPEED_API_KEY`: Restricted Google Cloud API key for Lighthouse performance audits.
* `CRUX_API_KEY`: Restricted Google Cloud API key for Chrome User Experience Report real-user metrics.
* `GEMINI_API_KEY`: Google AI Studio API key for content intelligence and autonomous reasoning.
* `GSC_SERVICE_ACCOUNT_KEY`: Service Account JSON key (for local execution fallback when not using Workload Identity Federation).
