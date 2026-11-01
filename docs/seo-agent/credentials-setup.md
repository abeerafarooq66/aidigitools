# AIDigiTools Autonomous SEO Agent V2 — Step-by-Step Credentials & Integration Setup Guide

**Document Reference**: `docs/seo-agent/credentials-setup.md`  
**Platform**: `aidigitools.tech`  
**Target Project**: `AIDigiTools-Content-Agent`  

This guide provides beginner-friendly, click-by-click instructions to configure all required cloud APIs, service accounts, and authentication credentials for the AIDigiTools Autonomous SEO Content Agent V2.

---

## 1. Google Cloud Project Setup (`AIDigiTools-Content-Agent`)

### Step 1.1: Create Dedicated GCP Project
1. Navigate to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown in the top header and select **New Project**.
3. **Project Name**: Enter `AIDigiTools-Content-Agent`.
4. **Project ID**: Accept or specify `aidigitools-content-agent` (record your exact Project ID).
5. Click **Create** and ensure this project is actively selected.

### Step 1.2: Enable Required Google APIs
Go to **APIs & Services > Library** and enable each of the following:
* **Google Search Console API** (`searchconsole.googleapis.com`)
* **Google Analytics Data API** (`analyticsdata.googleapis.com`)
* **Google Analytics Admin API** (`analyticsadmin.googleapis.com`)
* **PageSpeed Insights API** (`pagespeedonline.googleapis.com`)
* **Chrome UX Report API** (`chromeuxreport.googleapis.com`)
* **Google Ads API** (`googleads.googleapis.com`)
* **IAM Service Account Credentials API** (`iamcredentials.googleapis.com`)
* **Security Token Service API** (`sts.googleapis.com`)

---

## 2. Google Search Console & GA4 Service Account Setup

### Step 2.1: Create Dedicated Service Account
1. In Google Cloud Console, navigate to **IAM & Admin > Service Accounts**.
2. Click **+ Create Service Account**.
3. **Service account name**: `content-agent-sa`
4. **Service account ID**: `content-agent-sa`
5. **Description**: `AIDigiTools Autonomous SEO Agent V2 read-only reporting`
6. Click **Create and Continue**. (Do not assign project-wide Owner/Editor roles; leave Project Access blank).
7. Click **Done**.
8. Copy the generated email address:
   `content-agent-sa@<your-project-id>.iam.gserviceaccount.com`

### Step 2.2: Add Service Account to Google Search Console
1. Open [Google Search Console](https://search.google.com/search-console).
2. Select the verified property for `https://aidigitools.tech/`.
3. In the left sidebar, click **Settings** (gear icon) at the bottom.
4. Click **Users and permissions**.
5. Click **Add user** (top right).
6. **Email address**: Paste your service account email (`content-agent-sa@...`).
7. **Permission**: Select **Restricted** (read-only queries and search analytics).
8. Click **Add**.

### Step 2.3: Add Service Account to Google Analytics 4 (GA4)
1. Open [Google Analytics](https://analytics.google.com/).
2. Select your AIDigiTools GA4 property.
3. In the bottom-left corner, click **Admin** (gear icon).
4. Under the *Property* column, click **Property Access Management**.
5. Click the blue **+** button (top right) and select **Add users**.
6. **Email addresses**: Paste your service account email (`content-agent-sa@...`).
7. **Direct roles**: Select **Viewer** (read-only reporting; zero administrative or edit rights).
8. Click **Add**.
9. Under *Property Settings > Property Details*, copy the numeric **Property ID** (e.g., `123456789`).  
   *(IMPORTANT: Do not confuse this with the Measurement ID starting with `G-`)*.

---

## 3. Microsoft Bing Webmaster Tools API Setup

1. Open [Bing Webmaster Tools](https://www.bing.com/webmasters) and sign in.
2. Select your verified site `https://aidigitools.tech`.
3. Click the gear icon (**Settings**) in the top right.
4. Under the **API Access** section, click **API Key**.
5. Click **Generate API Key** (or copy your existing key).
6. Store this key securely as `BING_WEBMASTER_API_KEY`.

---

## 4. Google PageSpeed Insights & CrUX API Keys Setup

1. In Google Cloud Console, go to **APIs & Services > Credentials**.
2. Click **+ Create Credentials > API Key**.
3. Rename the key to `PageSpeed Insights Key`.
4. Click **Edit API Key** under API Restrictions:
   - Select **Restrict key**.
   - Check **PageSpeed Insights API**.
   - Click **Save**.
5. Create a second key:
   - Rename to `Chrome UX Report Key`.
   - Select **Restrict key**.
   - Check **Chrome UX Report API**.
   - Click **Save**.

---

## 5. Google Gemini API Setup (Google AI Studio)

1. Open [Google AI Studio](https://aistudio.google.com/).
2. Sign in and click **Get API key** in the top navigation.
3. Click **Create API key in new project** (or link to `AIDigiTools-Content-Agent`).
4. Copy the API key and store it as `GEMINI_API_KEY`.
5. (Note: Free tier accommodates 15 requests per minute, sufficient for autonomous SEO reasoning with zero billing required).

---

## 6. Storing Secrets in GitHub Actions & Local Environment

### In GitHub Actions (via GitHub CLI):
```bash
# Set secrets
gh secret set BING_WEBMASTER_API_KEY
gh secret set PAGESPEED_API_KEY
gh secret set CRUX_API_KEY
gh secret set GEMINI_API_KEY
gh secret set GSC_SERVICE_ACCOUNT_KEY

# Set repository variables (non-secret IDs)
gh variable set GOOGLE_CLOUD_PROJECT_ID --body "aidigitools-content-agent"
gh variable set GCP_SERVICE_ACCOUNT_EMAIL --body "content-agent-sa@aidigitools-content-agent.iam.gserviceaccount.com"
gh variable set GSC_SITE_URL --body "https://aidigitools.tech/"
gh variable set GA4_PROPERTY_ID --body "<YOUR_NUMERIC_GA4_PROPERTY_ID>"
```

### In Local Development (`.env`):
1. Copy template: `cp .env.example .env`
2. Populate the keys into `.env`.
3. Run preflight verification: `python scripts/credentials_preflight.py --test`

