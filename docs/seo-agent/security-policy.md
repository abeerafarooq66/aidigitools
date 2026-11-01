# AIDigiTools Autonomous SEO Agent V2 — Credential & API Security Policy

**Document Reference**: `docs/seo-agent/security-policy.md`  
**Security Level**: High (Confidential Credential Governance)  
**Charter Date**: November 1, 2026  

---

## 1. Core Principles of Credential Governance

1. **Least-Privilege Authorization**:
   - Google Service Accounts must be granted only read-only scopes (`webmasters.readonly`, `analytics.readonly`).
   - Project Owner or Editor roles are strictly prohibited for automation service accounts.
   - GitHub Actions workflows must specify explicit read-only permissions (`permissions: contents: read`) except when automated reporting specifically requires committing audit logs (`contents: write`).
2. **Workload Identity Federation (Keyless Auth in CI/CD)**:
   - In production GitHub Actions, use Google Cloud Workload Identity Federation with GitHub's OpenID Connect (OIDC) provider.
   - Long-lived private key files (`.json`) must be avoided in GitHub Secrets wherever Workload Identity Federation is configured.
3. **Absolute Prohibition of Secret Leakage**:
   - Secret keys, API tokens, service account keys, and private certificates must **NEVER** be committed to Git, logged to console, embedded in public JSON, or included in client-side HTML or JavaScript.
   - The `.gitignore` file enforces exclusion of `.env`, `.env.*`, `*credentials*.json`, `*service_account*.json`, and `token.json`.
4. **Public Verification Keys vs. Secret API Keys**:
   - IndexNow keys (`INDEXNOW_KEY`) are public verification tokens served over HTTP (`https://aidigitools.tech/{key}.txt`) and do not grant account access.
   - Private API keys (Bing, Gemini, Google Cloud) grant account access and must remain confidential.

---

## 2. Credential Rotation Procedures

If any API key or service account credential is ever inadvertently exposed or suspected of compromise, execute the following emergency rotation protocol immediately:

### A. Google Cloud API Keys (PageSpeed / CrUX / Gemini)
1. Open [Google Cloud Console > Credentials](https://console.cloud.google.com/apis/credentials).
2. Click **Create Credentials > API Key**.
3. Apply API restrictions immediately (restrict only to target API).
4. Update GitHub Secrets (`gh secret set PAGESPEED_API_KEY`, etc.) and local `.env`.
5. Return to Google Cloud Console and **Delete** the compromised API key.

### B. Google Service Account (Search Console & GA4)
1. Open [Google Cloud Console > Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts).
2. Select `content-agent-sa@aidigitools-content-agent.iam.gserviceaccount.com`.
3. Go to the **Keys** tab and click **Add Key > Create New Key (JSON)**.
4. Update GitHub Secret `GSC_SERVICE_ACCOUNT_KEY` with the new JSON.
5. In the Service Account Keys table, delete the old compromised key.

### C. Microsoft Bing Webmaster API Key
1. Open [Bing Webmaster Tools](https://www.bing.com/webmasters).
2. Go to **Settings > API Access > API Key**.
3. Click **Generate New Key** (this automatically invalidates the prior key).
4. Update the GitHub Secret `BING_API_KEY` using `gh secret set BING_API_KEY`.

---

## 3. Secret Preflight Verification Rules

Prior to deploying any autonomous agent workflow:
1. Run `python scripts/credentials_preflight.py` to confirm format and presence.
2. Ensure the preflight checker displays only `[SET]`, `[MISSING]`, `[INVALID FORMAT]`, or `[VERIFIED]`.
3. Confirm that no secrets are echoed or logged.
