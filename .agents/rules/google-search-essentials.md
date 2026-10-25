# Google Search Essentials & Technical SEO Invariants

> Grounded in Google Search Central's official guide: [SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide) and [Search Essentials](https://developers.google.com/search/docs/essentials).

## 1. Technical Health & Crawlability
1. **Robots & Access**:
   - `robots.txt` must explicitly allow search crawlers and AI search bots (Googlebot, Bingbot, PerplexityBot, GPTBot, ClaudeBot).
   - Never block CSS, JavaScript, or media required for rendering page content.
2. **XML Sitemap**:
   - Maintain an automated, valid XML sitemap (`sitemap.xml`) referencing every indexable canonical URL.
   - Every URL must return HTTP 200 and include `<lastmod>` timestamps.
3. **Noindex Utility Pages**:
   - Keep internal utility pages, administrative panels, test harnesses, or staging paths flagged with `<meta name="robots" content="noindex, follow">`.
4. **Canonical Standards**:
   - Every page must contain a self-referencing canonical URL (`<link rel="canonical" href="https://aidigitools.tech/...">`).
   - Standardize on `https://aidigitools.tech` (HTTPS, non-www, trailing-slash clean).
5. **Zero Broken Links & Anchors**:
   - Maintain 100% link graph integrity. Zero 404 broken internal links and zero broken fragment `#` anchors.

## 2. Page Experience & Core Web Vitals (CWV)
1. **Mobile-First Layout**:
   - Clean, fluid viewport configuration (`<meta name="viewport" content="width=device-width, initial-scale=1.0">`).
   - Tap targets must have adequate touch padding (minimum 44x44px).
2. **Speed & Latency**:
   - Target sub-second Largest Contentful Paint (LCP < 2.5s).
   - Zero Cumulative Layout Shift (CLS < 0.1) by pre-allocating image dimensions.
   - Responsive user interaction with low Interaction to Next Paint (INP < 200ms).
3. **Typography & Readability**:
   - High contrast ratios (WCAG AA compliant) with comfortable line height and accessible font sizing.

## 3. On-Page HTML Structure
1. **Title Tag**:
   - Must be 30–65 characters (targeting 50–60 characters).
   - Unique across all site pages. Must contain Primary Keyword + Key Outcome + Brand name.
2. **Meta Description**:
   - Must be 70–165 characters (targeting 140–160 characters).
   - Accurate, enticing value summary with real pricing and natural call to action.
3. **Headings Hierarchy**:
   - Exactly one `<h1>` per page.
   - Descriptive `<h2>` headings for major content milestones.
   - Sub-points in `<h3>`. Never use empty heading tags.
4. **Image Optimization**:
   - High-fidelity WebP and PNG assets.
   - Every image must carry a non-empty, descriptive `alt` attribute.
