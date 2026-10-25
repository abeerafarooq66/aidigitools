# Master Agent QA & Verification Workflow

Execute this comprehensive Quality Assurance checklist prior to pushing changes or adding pages:

## Phase 1: Pre-Build Validation
- [ ] Has the Content Brief been completed?
- [ ] Is the primary keyword mapped without cannibalizing existing URLs?
- [ ] Is the search intent classified (Informational, Commercial, Transactional)?
- [ ] Is the primary CTA linked to WhatsApp helpline `03326861112`?

## Phase 2: On-Page Architecture Check
- [ ] Title tag length between 30 and 65 characters (targeting 50–60).
- [ ] Meta description length between 70 and 165 characters (targeting 140–160).
- [ ] Exactly one `<h1>` tag defining the primary topic or tool.
- [ ] Quick Answer block (`.quick-answer`) immediately under `<h1>` with 35–70 words.
- [ ] Semantic HTML `<table>` for plan and price comparison.
- [ ] Visible `<details><summary>` FAQ accordion with real questions.
- [ ] Above-the-fold Reseller Notice present on tool pages.
- [ ] Non-empty, descriptive `alt` tags on all images.
- [ ] Zero unverified ratings or fake star reviews.

## Phase 3: Technical SEO & Feed Integrity
- [ ] Self-referencing canonical tag present and HTTPS formatted.
- [ ] Page URL listed in `sitemap.xml`.
- [ ] Product item listed in `merchant_feed.xml` with 1200x630 `.png` image link.
- [ ] Tool entry listed in `llms.txt` and `llms-full.txt`.
- [ ] Valid JSON-LD schema matching visible content only (`Product` + `Offer` + `FAQPage` + `BreadcrumbList`).

## Phase 4: Automated Execution Verification
Execute the automated test suite:
```bash
python -m unittest discover -s tests -v
python scripts/link_graph_checker.py --strict
python -m aio_agent audit
python scripts/check_seo_metrics.py
python scripts/submit_indexnow.py
```
All tests must pass with 100% green status.
