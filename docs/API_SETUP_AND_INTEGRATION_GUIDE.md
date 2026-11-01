# AIDigiTools — Official API Setup & Credential Integration Guide

> **Charter Alignment**: Strictly implements **Part 21 (Security & API Access)** and **Part 23 (Implementation Order & Setup Guide)** of the Master Operating System & Architecture Charter for `aidigitools.tech`.
> 
> **Zero-Leak Invariant**: Never paste raw API keys, private tokens, refresh tokens, or service-account JSON into chat, public files, or GitHub commits. All credentials must be stored strictly in environment variables or GitHub Actions Secrets.

---

## Executive Overview: The 2-Phase Operational Model

| Operational Phase | Status | Rules & Constraints |
| :--- | :--- | :--- |
| **Phase 1: Supervised Mode** | **Active** | The first **3 publishing cycles** must be prepared with a rendered preview in `data/previews/{slug}.html` and require explicit human review and sign-off by Abeera Farooq before publication. |
| **Phase 2: Autonomous Low-Risk** | *Unlocks after 3 approved cycles* | Automatic publication is enabled **strictly for eligible, low-risk content** that passes 100% of the 20 Quality Gates. High-risk claims (licensing, pricing exceptions, legal terms, warranty changes) continue to halt for human review. |

---

## Step-by-Step API Integration Walkthrough

The following guide walks the owner through connecting each API service **one integration at a time**.

```
[Integration 1: IndexNow] ──► [Integration 2: Google Gemini] ──► [Integration 3: Bing Webmaster]
         │
         ▼
[Integration 4: Search Console] ──► [Integration 5: GA4 Data API] ──► [Integration 6: PageSpeed]
         │
         ▼
[Integration 7: Google Ads & Trends Fallback]
```

---

### Integration 1: IndexNow (Bing & Search Central)
- **Status**: **CONNECTED & VERIFIED**
- **Purpose**: Instant crawl discovery notification to Microsoft Bing, Yandex, and Naver upon publishing or modifying canonical URLs.
- **Exact Console URL**: [Bing Webmaster Tools — IndexNow](https://www.bing.com/webmasters/indexnow)
- **Required Permissions**: Domain ownership verification via root `.txt` file.
- **Environment Variable**: `INDEXNOW_KEY=89d63ab53a63527b12a199a3096e51ad`
- **Root Verification File**: [`89d63ab53a63527b12a199a3096e51ad.txt`](file:///c:/Users/Dell/Desktop/aidigitools/89d63ab53a63527b12a199a3096e51ad.txt)
- **One-Line Verification Command**:
  ```bash
  python -m seo-agent.agent.indexing_notifier --notify-indexnow --dry-run
  ```
- **Expected Output**:
  ```
  [INDEXNOW DISPATCH] Submitted: 65 URLs | Success: True
  [DISCLAIMER] Notice: Neither sitemap submission, search console inspection, nor IndexNow notification guarantees that a URL will be crawled, indexed, or ranked...
  ```

---

### Integration 2: Google Gemini API (Generative Language)
- **Purpose**: Powers semantic keyword classification, topic clustering, and synthesis of research briefs.
- **Exact Console URL**: [Google AI Studio — API Keys](https://aistudio.google.com/app/apikey)
- **Required Scope**: Dedicated Generative Language API (`https://www.googleapis.com/auth/generative-language`).
- **Setup Instructions**:
  1. Open Google AI Studio and click **Create API Key**.
  2. Select your Google Cloud project (`aidigitools-content-agent`).
  3. Copy the generated key.
  4. In your local `.env` file (or GitHub Actions Repository Secrets), add:
     ```env
     GEMINI_API_KEY=AIzaSy...your-gemini-key
     ```
- **One-Line Verification Command**:
  ```bash
  python -m seo-agent.agent.security_access_manager --audit-integrations
  ```
- **Expected Output**:
  `gemini_api: CONNECTED (Authorized test request to Gemini returned verified tokens.)`

---

### Integration 3: Microsoft Bing Webmaster Tools REST API
- **Purpose**: Multi-source search intelligence: queries, impressions, clicks, and crawl telemetry from Bing search.
- **Exact Console URL**: [Bing Webmaster Tools — API Access](https://www.bing.com/webmasters/api)
- **Required Permissions**: Read-only access to `aidigitools.tech` webmaster data.
- **Setup Instructions**:
  1. Navigate to **Settings** > **API Access** > **API Key**.
  2. Click **Generate API Key**.
  3. Copy the key and add to your local `.env` or GitHub Secrets:
     ```env
     BING_WEBMASTER_API_KEY=your-bing-api-key
     ```
- **One-Line Verification Command**:
  ```bash
  python -m seo-agent.agent.search_intelligence
  ```

---

### Integration 4: Google Search Console (Service Account / Least-Privilege)
- **Purpose**: Real search performance tracking, average position, impressions, and indexation status.
- **Exact Console URL**: [Google Cloud Console — IAM & Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts?project=aidigitools-content-agent)
- **Required Least-Privilege Scope**:
  `https://www.googleapis.com/auth/webmasters.readonly` *(Strictly read-only; never request full write access).*
- **Setup Instructions**:
  1. In Cloud Console, click **Create Service Account**:
     - Name: `gsc-reader-sa`
     - Email: `gsc-reader-sa@aidigitools-content-agent.iam.gserviceaccount.com`
  2. Click **Manage Keys** > **Add Key** > **Create new JSON key**.
  3. Base64-encode or store the JSON string in GitHub Actions Secrets as `GSC_SERVICE_ACCOUNT_KEY`.
  4. Open [Google Search Console](https://search.google.com/search-console) > **Settings** > **Users and Permissions**.
  5. Click **Add User**, enter the service account email, and grant **Read-Only** permission.
- **One-Line Verification Command**:
  ```bash
  python -c "import os; os.environ['GSC_SITE_URL']='https://aidigitools.tech/'; from seo_agent.agent.security_access_manager import SecurityAccessManager; m = SecurityAccessManager(); print(m.verify_integration('google_search_console'))"
  ```

---

### Integration 5: Google Analytics 4 (GA4 Data API)
- **Purpose**: Track user engagement, article views, Quick Order conversions, and topic cluster performance over 7, 14, 28, and 56 days.
- **Exact Console URL**: [Google Cloud Console — Enabled APIs (Google Analytics Data API)](https://console.cloud.google.com/apis/library/analyticsdata.googleapis.com?project=aidigitools-content-agent)
- **Required Least-Privilege Scope**:
  `https://www.googleapis.com/auth/analytics.readonly`
- **Setup Instructions**:
  1. Enable the **Google Analytics Data API** in Google Cloud Console.
  2. Open [Google Analytics Admin](https://analytics.google.com/) > **Property Access Management**.
  3. Add the service account email (`gsc-reader-sa@aidigitools-content-agent.iam.gserviceaccount.com`) with **Viewer** role.
  4. Copy your numeric **Property ID** (found in GA4 Property Settings) and set:
     ```env
     GA4_PROPERTY_ID=your-numeric-property-id
     ```
- **One-Line Verification Command**:
  ```bash
  python -m seo-agent.agent.conversion_analytics --audit-events
  ```

---

### Integration 6: Google PageSpeed Insights & Chrome UX Report (CruX)
- **Purpose**: Automated Core Web Vitals (LCP, INP, CLS) and page speed monitoring for all 66 HTML templates.
- **Exact Console URL**: [Google Cloud Console — Credentials](https://console.cloud.google.com/apis/credentials?project=aidigitools-content-agent)
- **Setup Instructions**:
  1. Click **Create Credentials** > **API Key**.
  2. Under **API Restrictions**, restrict the key to **PageSpeed Insights API**.
  3. Set in your `.env` or GitHub Secrets:
     ```env
     PAGESPEED_API_KEY=your-restricted-key
     CRUX_API_KEY=your-restricted-key
     ```
- **One-Line Verification Command**:
  ```bash
  python scripts/credentials_preflight.py --test
  ```

---

### Integration 7: Google Ads API & Trends Fallback
- **Purpose**: Search query volume, seasonal trends, and commercial CPC estimates.
- **Fallback Architecture**: When Google Ads API credentials are not provisioned, the agent automatically falls back to the **Real-Time Google Autocomplete & Trends Engine**, extracting search query suggestions without requiring paid developer tokens.
- **Environment Variables**:
  ```env
  GOOGLE_ADS_CUSTOMER_ID=2913849282
  GOOGLE_ADS_MANAGER_ID=1826247360
  GOOGLE_ADS_DEVELOPER_TOKEN=
  GOOGLE_TRENDS_FALLBACK=active
  ```

---

## Summary of Truthful Connection Rules

1. **Never Pretend**: If a credential is not present, the agent reports `NOT_CONFIGURED` or `OPTIONAL / NOT CONFIGURED`.
2. **Real Data Required**: No integration is ever marked `CONNECTED` until a live authorized request returns verified non-empty data.
3. **Least Privilege**: Always restrict service accounts to `readonly` scopes.
4. **No Secrets in Git**: Maintain `.env` in `.gitignore` and ensure `.env.example` contains variable names only.

---

## The Final Mission

> *"Build AIDigiTools into a trusted, research-driven AI software information and product discovery platform.*
> 
> *Every published article must earn its place on the website by helping readers, accurately explaining products, answering search intent, and contributing meaningful original value.*
> 
> *Prioritize reader trust, evidence, accurate product information, sustainable organic visibility, and qualified business outcomes over publishing volume.*
> 
> *Never guarantee Google rankings, indexing, AI Overview inclusion, or traffic results."*

