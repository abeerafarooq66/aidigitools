# AIDigiTools Production Deployment Verification Protocol
**Repository:** `abeerafarooq66/aidigitools`  
**Production URL:** `https://aidigitools.tech/`  
**Standard:** *Universal Web Search & SEO Master Book V2*

---

## 1. Post-Push GitHub Pages Deployment Verification
After pushing commits to `origin/main`, GitHub Pages automatically triggers a build via the deployment pipeline.

### Verification Checklist:
1. **GitHub Actions / Pages Build Status:**
   - Confirm successful completion of the GitHub Pages workflow at `https://github.com/abeerafarooq66/aidigitools/actions`.
2. **Live Cache Invalidation:**
   - Confirm edge CDN (GitHub Pages Fastly / Cloudflare) returns updated headers:
     `curl -I https://aidigitools.tech/robots.txt`
3. **Live UTF-8 Glyph Verification:**
   - Inspect live product routes (`https://aidigitools.tech/tools/claude-pro.html`, `chatgpt-plus.html`, `turnitin-student.html`) in an active browser session.
   - Verify that all currency symbols (`Rs.`, `$`), checklist checkmarks (`✓`), and contact phone numbers (`+92 332 6861112`) render cleanly without `??` or replacement characters (``).
4. **Live Payment Policy Consolidation:**
   - Confirm footer links point to `https://aidigitools.tech/policies.html#payments`.
   - Confirm product meta descriptions do not contain repeated wallet keyword stuffing.
5. **GA4 Realtime Event Verification:**
   - Trigger a test WhatsApp click and Quick Order modal open.
   - Confirm events (`whatsapp_click`, `quick_order_click`) fire via navigator.sendBeacon in GA4 Realtime DebugView.

---

## 2. Deployment Status Transition Ledger
Upon executing `git push origin main`, update statuses across this register from `VERIFIED LOCALLY` to `PUSHED TO GITHUB`, then to `DEPLOYED TO PRODUCTION`, and finally to `VERIFIED LIVE`.
