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
| **Microsoft Bing Webmaster API** | ✅ **YES** | API Key (in GitHub Secrets as `BING_API_KEY`) | REST JSON API Header (`apikey`) | Webmaster read-only analytics | **VERIFIED** (Live HTTP 200 / Quota OK) | Fully integrated |
| **Google PageSpeed Insights** | ✅ **YES** | Google Cloud API Key (in GitHub Secrets as `PAGESPEED_API_KEY`) | Query parameter (`key=...`) | PageSpeed Insights API | **VERIFIED** (Live Lighthouse OK) | Fully integrated |
| **Chrome UX Report (CrUX) API** | ✅ **YES** | Google Cloud API Key (in GitHub Secrets as `CRUX_API_KEY`) | Query parameter (`key=...`) | Chrome UX Report API | **VERIFIED** (Live API Authenticated) | Fully integrated |
| **Google Gemini API** | ✅ **YES** | Google AI Studio API Key (in GitHub Secrets as `GEMINI_API_KEY`) | Query param / Bearer token | Generative Language API | **VERIFIED** (50 Models Discovered) | Fully integrated |
| **Google Search Console (GSC) API** | ✅ **YES** | Service Account JSON (`content-agent-sa@...`) in GitHub Secrets | OAuth 2.0 Bearer Token | `webmasters.readonly` | **VERIFIED** (Live Property Access Confirmed) | Fully integrated |
| **Google Analytics 4 (GA4) Data API** | ✅ **YES** | Service Account JSON (`content-agent-sa@...`) in GitHub Secrets | OAuth 2.0 Bearer Token (`analytics.readonly`) | GA4 Viewer on Property `561800932` | **VERIFIED** (Live GA4 Data API Confirmed) | Fully integrated |
| **Google Ads API (Keyword Planner)** | ✅ **YES** | GCP Enabled + Customer IDs in GitHub Secrets | Google Cloud Managed API | Client CID: `2913849282`, Manager MCC: `1826247360` | **VERIFIED** (API Enabled in GCP) | Fully configured |
| **Google Trends Discovery Engine** | ✅ **YES** | Google Search Autocomplete Gateway | HTTP Real-time predictive stream | Query trend volume extraction | **VERIFIED** (Live Trends Autocomplete Active) | Fully integrated |
| **GitHub Actions Authentication** | ✅ **YES** | `GITHUB_TOKEN` + Workload Identity Federation | OIDC (Token exchange) | `contents: write`, `pull-requests: write` | **VERIFIED** | Enforce least-privilege token permissions per workflow |

---

## 2. Environment Variables Specification

### Non-Secret Environment Variables
* `GOOGLE_CLOUD_PROJECT_ID`: Name/ID of Google Cloud project (`aidigitools-content-agent`).
* `GCP_SERVICE_ACCOUNT_EMAIL`: Dedicated IAM Service Account email (`content-agent-sa@aidigitools-content-agent.iam.gserviceaccount.com`).
* `GCP_WORKLOAD_IDENTITY_PROVIDER`: Workload Identity Provider resource string for GitHub Actions keyless authentication.
* `GSC_SITE_URL`: Verified Search Console property root (`https://aidigitools.tech/`).
* `GA4_PROPERTY_ID`: Numeric Google Analytics 4 property ID (`561800932`).
* `GA4_MEASUREMENT_ID`: Web Stream Measurement ID (`G-NE094X2Q7H`) installed on all 66 HTML pages.
* `INDEXNOW_KEY`: Standard 32-character hexadecimal string (`89d63ab53a63527b12a199a3096e51ad`).

### Secret Credentials (Stored in GitHub Secrets & Local .env)
* `BING_WEBMASTER_API_KEY`: Bing Webmaster API token.
* `PAGESPEED_API_KEY`: Restricted Google Cloud API key for Lighthouse performance audits.
* `CRUX_API_KEY`: Restricted Google Cloud API key for Chrome User Experience Report real-user metrics.
* `GEMINI_API_KEY`: Google AI Studio API key for content intelligence and autonomous reasoning.
* `GSC_SERVICE_ACCOUNT_KEY`: Service Account JSON key (for local execution fallback when not using Workload Identity Federation).

