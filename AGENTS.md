# AGENTS.md — Master Operating System & Architecture Charter for AIDigiTools

> **Official Foundation**: Built strictly on Google Search Central Official Documentation:
> - [Google AI Optimization Guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide) ("Optimizing your website for generative AI features on Google Search")
> - [Google SEO Starter Guide](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
> - [Google Search Essentials & Spam Policies](https://developers.google.com/search/docs/essentials)

---

## 1. Platform Identity & Executive Charter

- **Domain**: `aidigitools.tech`
- **Business**: Premier localized AI software marketplace, AI video tools, creative suites, and intelligence hub serving Pakistan and worldwide.
- **Operations Model**: 100% genuine online digital marketplace desk based in Islamabad, Pakistan, serving domestic and international customers with instant WhatsApp order routing (`03326861112` / `+92 332 6861112`).
- **Core Value Proposition**: Transparent PKR & USD pricing, verified domestic payment rails (EasyPaisa, JazzCash, SadaPay, NayaPay, Raast, Bank IBFT), global settlement (Wise, Binance Pay / Crypto USDT, Payoneer), 15-minute delivery SLA, and 30-day replacement warranty.
- **Primary Goal**: Top-tier Google Search rankings + Google AI Overviews & AI Mode citations + Bing/Perplexity/ChatGPT retrieval + high-converting authentic user experience.
- **The Golden Rule**: **Human-first, original, useful, technically clean content.** Content must be created for real human beings solving real workflow problems, never written for search engine spiders or AI bots.

### Google's Official Stance on AI Search
> Generative AI experiences in Search—such as **Google AI Overviews** and **AI Mode**—are grounded directly in Google's core Search indexing, retrieval (RAG), and ranking systems. AEO and GEO are not separate "hacks" or bypasses; they are the modern, natural evolution of foundational SEO. Content must be publicly crawlable, technically indexed, and high-quality to be cited.

---

## 2. The 4 Pillars of SEO

| Pillar | Operational Agent Directives |
| :--- | :--- |
| **Technical SEO** | Ensure 100% crawlability, valid `sitemap.xml`, permissive `robots.txt`, HTTPS security, mobile-first responsive layout, sub-second latency, optimal Core Web Vitals (LCP, INP, CLS), canonical URL tags, and zero broken links/anchors. |
| **On-Page SEO** | Unique Title tags (50–60 characters), high-utility Meta Descriptions (140–160 characters), strictly one `<h1>` per page, hierarchical semantic `<h2>`/`<h3>` headings, descriptive directory URLs, rich internal linking with descriptive anchors, WebP/PNG images with descriptive `alt` text, and schema markup matching visible content. |
| **Content SEO** | In-depth, first-hand tested, original, non-commodity content that directly satisfies the user's search intent. Quantitative comparison tables, step-by-step activation workflows, real pricing figures, and visible FAQ accordions. |
| **Off-Page SEO** | Genuine brand mentions, authentic digital community authority, IndexNow protocol pings, verified social card metadata, and real customer service reputation. |

---

## 3. The 14 Keyword Types & Research Workflow

### 3.1 Keyword Taxonomy
1. **Short-tail**: Broad intent (e.g., `AI tools`, `AI video generators`). Targeted on Homepage and Hub category pages.
2. **Long-tail**: High-intent, specific queries (e.g., `best AI video generator for YouTube Shorts in Pakistan`). Targeted on Guides, Comparisons, and Blog posts.
3. **Branded**: Entity terms (e.g., `AIDigiTools AI marketplace`, `AIDigiTools WhatsApp order`). Targeted on Brand, Contact, and Policy pages.
4. **Non-branded**: Problem-oriented queries (e.g., `Canva template pack for Pakistani freelancers`). Targeted on Landing and Deal pages.
5. **Informational**: Knowledge acquisition (e.g., `What is Runway Gen-3 Alpha?`, `How does DeepSeek R1 work?`). Targeted on Guides, FAQs, and Educational hubs.
6. **Commercial Investigation**: Solution evaluation (e.g., `Best AI coding assistants compared 2026`). Targeted on Best-of listicles and Category hubs.
7. **Transactional**: High-intent purchasing (e.g., `Buy ChatGPT Plus subscription with EasyPaisa`). Targeted on Product pages and Pricing tables.
8. **Navigational**: Direct destination finding (e.g., `AIDigiTools official catalog`). Targeted on Navigation, Sitemaps, and Brand anchors.
9. **Local & Regional**: Geographic queries (e.g., `AI software subscriptions Islamabad Pakistan`). Targeted on Contact, Policies, and Localized FAQs.
10. **Question-based**: Problem solvers (e.g., `How to pay for Midjourney without international credit card?`). Targeted on Quick Answer blocks and `<details>` FAQs.
11. **Comparison**: Head-to-head evaluation (e.g., `ChatGPT Plus vs Claude Pro`). Targeted on Dedicated Comparison pages (`/compare/`).
12. **Alternative**: Substitute seekers (e.g., `Cursor Pro alternatives for Python developers`). Targeted on Alternative articles and Tool cards.
13. **Pricing**: Cost evaluation (e.g., `Adobe Creative Cloud price in Pakistan PKR`). Targeted on Product pricing tables and `#pricing` sections.
14. **Problem-based**: Pain-point queries (e.g., `fix international payment decline for AI subscriptions`). Targeted on Troubleshooting sections and Payment policies.

### 3.2 Keyword Research Workflow
1. **Seed Topics**: AI video generation, LLM coding assistants, creative assets, digital productivity, VPNs.
2. **Expansion**: Google Autocomplete, People Also Ask (PAA), Google Search Console (GSC) query data, and user intent patterns.
3. **Intent Classification**: Classify every keyword into Informational, Commercial, or Transactional before drafting.
4. **Mapping & Assignment**: Assign 1 primary keyword + 5–15 semantic variations per URL.
5. **Cannibalization Guard**: Never permit two separate URLs to compete for the exact same primary keyword.
6. **Anti-Stuffing Rule**: Strictly avoid keyword repetition. Google uses advanced language models to understand semantic meaning, synonyms, and context.

---

## 4. On-Page SEO & Content Architecture Rules

### 4.1 Titles, Headings & Descriptions
- **Title Tag**: Target 50–60 characters (hard limit 30–65 characters). Must include Primary Keyword + Key Benefit + Brand Identifier (e.g., `ChatGPT Plus Pakistan (PKR & USD) — Buy Online | AIDigiTools`).
- **Meta Description**: Target 140–160 characters (hard limit 70–165 characters). Must summarize page value, specify pricing/rail, and include a natural call to action.
- **Heading Hierarchy**:
  - Exactly **one** `<h1>` per page specifying the primary entity/tool.
  - `<h2>` for major architectural sections (Overview, Pricing Table, Features, How to Order, FAQs).
  - `<h3>` for individual features, plans, and sub-questions.
  - Never skip heading levels or leave heading tags empty.

### 4.2 Quick Answer Block (AEO / AIO Prime Extract)
- Every page must feature a `.quick-answer` paragraph immediately under the primary `<h1>`.
- Length strictly maintained between **35 and 70 words** (optimal target: **40–60 words**).
- Structure: Direct factual definition + target use-case + pricing/delivery summary.

### 4.3 Semantic Comparison Tables
- Every tool, category, and comparison page must feature a clean, semantic HTML `<table>` (`<thead>`, `<tbody>`, `<th>`, `<td>`).
- Tables must present concrete technical metrics: Plan Name, Price (PKR & USD), Key Capability, Delivery SLA, and Warranty.

### 4.4 Internal Linking Graph
- Every new page must receive at least 3–5 contextual internal links from existing relevant pages.
- Anchor text must be descriptive and natural (e.g., `explore our ChatGPT Plus review and pricing`, never `click here` or `read more`).
- Pillar pages must link down to specialized tool pages; tool pages must link back to Category hubs and parent comparisons.

### 4.5 Image & Asset Standards
- All product images stored in `assets/images/` as high-resolution (1200x630) `.png` and vector `.svg` assets.
- Every `<img>` tag must have non-empty, descriptive `alt` text explaining the exact software interface or product badge.

---

## 5. Generative Engine Optimization (GEO) & Answer Engine Optimization (AEO)

### 5.1 The GEO Content Formula
For every tool and topical guide, structure the content in this sequence:
1. **Direct Answer (40–60 words)**: `.quick-answer` block defining what it is, who it serves, and cost.
2. **Why It Matters**: Contextual breakdown of the real-world workflow bottleneck solved.
3. **Technical Specs & Features**: Bulleted, factual specifications of compute limits, models, and seats.
4. **4-Row Quantitative Comparison Table**: Structured side-by-side comparison against alternatives.
5. **First-Hand Verification Insight**: Real testing observation ("In our testing with 4K video rendering...").
6. **Visible Interactive FAQ Accordion**: 4–8 `<details><summary>` elements answering top PAA questions.
7. **Sources, Warranty & Freshness Date**: Timestamped last verified date, official provider notice, and 30-day warranty.

### 5.2 The 8 Dimensions of GEO
- **Content GEO**: Crisp definitions, structured specs, and actionable pricing.
- **Entity GEO**: Unambiguous brand identity, consistent metadata, and official knowledge graph alignment.
- **Authority GEO**: Reseller disclaimers, honest policies, and verified customer service touchpoints.
- **Freshness GEO**: Continuous updates matching current upstream software versions (e.g., GPT-4o, Claude 3.5 Sonnet, Runway Gen-3).
- **Evidence GEO**: Concrete benchmark numbers, file sizes, token limits, and verified PKR exchange conversions.
- **Conversational GEO**: Natural language phrasing matching user voice queries and chatbot prompts.
- **Multimodal GEO**: Descriptive diagrams, product preview cards, structured data, and video specifications.
- **Topical GEO**: Exhaustive 6-hub topic coverage (Coding, Video, Creative, LLMs, Audio, VPN/Security).

### 5.3 5-Branch Query Fan-Out
Every tool page must address the 5 essential branches of user intent:
1. **Pricing**: Explicit PKR price and USD equivalent.
2. **Payment Rails**: Domestic (EasyPaisa, JazzCash, SadaPay, Raast) and Global (Wise, Crypto USDT).
3. **Delivery SLA**: 15–30 minute digital delivery via WhatsApp.
4. **Warranty & Guarantee**: 30-day replacement warranty.
5. **Audience & Use-Case**: Freelancers, students, content creators, software engineers, and agencies.

---

## 6. AI Overview (AIO) Grounding & Myth Busting

### 6.1 Google Official Grounding Rules
- Google AI Overviews and AI Mode synthesize answers using Retrieval-Augmented Generation (RAG) directly from indexed web pages.
- Content must be snippet-eligible, factual, and easily parsed into key facts.

### 6.2 The 6 Debunked AIO Myths (Never Do These)
1. ❌ **Myth 1: `llms.txt` is required for Google Search.**
   *Truth*: Google Search ignores `llms.txt`. All content must be fully visible and rendered in HTML for Google's indexer.
2. ❌ **Myth 2: Content must be broken into artificial tiny chunks.**
   *Truth*: Artificial micro-chunking destroys human readability and degrades user experience. Use standard semantic sections with clear headings.
3. ❌ **Myth 3: Write in a robotic or synthetic AI style.**
   *Truth*: Google rewards clear, natural, human-written content. Robotic phrasing hurts engagement and trustworthiness.
4. ❌ **Myth 4: Fabricate fake ratings, reviews, or physical addresses.**
   *Truth*: Unverified structured data (e.g., `aggregateRating` without visible customer reviews) risks manual actions and spam penalties.
5. ❌ **Myth 5: Create special hidden AI schema tags.**
   *Truth*: Structured data must represent content visibly rendered on the page. Use standard Schema.org types (`Product`, `Offer`, `FAQPage`, `BreadcrumbList`).
6. ❌ **Myth 6: Generate bulk thin pages for every keyword variation.**
   *Truth*: Scaled low-value pages violate Google's Scaled Content Abuse policy. Group related variations into deep, comprehensive pillar pages.

---

## 7. Structured Data & Schema Standards (JSON-LD)

- **Organization & WebSite Schema**: Configured on `index.html` referencing official entity details, URL, and WhatsApp contact point.
- **BreadcrumbList Schema**: Mandatory on all category, tool, compare, and guide pages with correct hierarchic items.
- **Product & Offer Schema**: Mandatory on all 36 tool pages. Must include `name`, `description`, `image`, `sku`, `brand`, and `offers` (`price`, `priceCurrency: "PKR"`, `availability: "https://schema.org/InStock"`, `itemCondition: "https://schema.org/NewCondition"`).
- **FAQPage Schema**: Mandatory on pages with visible FAQ sections. Every Q&A in the schema must exactly match a visible `<details>` element in the DOM.
- **SpeakableSpecification Schema**: Targets `[".quick-answer", ".price-tag"]` for high-precision voice search and virtual assistant retrieval.
- **Article Schema**: Mandatory on all guide, compare, and informational pages (`@type: "TechArticle"` or `"Article"`).
- **Strict Rule**: Zero unverified `aggregateRating` or fake star reviews.

---

## 8. Google Merchant Center (GMC) & Google Ads Reseller Compliance

### 8.1 Feed Architecture (`merchant_feed.xml`)
- All 36 catalog tools must be dynamically synchronized.
- Valid XML with Google Merchant namespace: `xmlns:g="http://base.google.com/ns/1.0"`.
- Mandatory attributes per item:
  - `<g:id>`: Unique slug identifier.
  - `<g:title>`: Descriptive product title without promotional spam.
  - `<g:description>`: Clear functional description of features and subscription duration.
  - `<g:link>`: Canonical HTTPS URL.
  - `<g:image_link>`: Absolute HTTPS URL to a 1200x630 `.png` asset.
  - `<g:availability>`: `in_stock`.
  - `<g:price>`: Explicit PKR pricing (e.g., `4500 PKR`).
  - `<g:condition>`: `new`.
  - `<g:brand>`: Tool brand name.
  - `<g:google_product_category>`: Software category (e.g., `Software > Computer Software`).
  - `<g:shipping>`: Free digital email/WhatsApp delivery across target territories (`PK`, `US`, `GB`, `AE`, `CA`).

### 8.2 Google Ads Reseller & Informational Site Policy
- **Above-The-Fold Reseller Notice**: Every tool page must feature a prominent informational badge stating:
  > *"Independent Reseller & Service Desk: AIDigiTools is an independent subscription concierge and digital marketplace. All product names, logos, and trademarks belong to their respective owners. We are not directly affiliated with or endorsed by upstream tool providers."*
- **Prohibited Account-Sharing Terminology**: Zero usage of terms such as "shared slot", "profile PIN", "cracked account", or "edu pack". All items are strictly characterized as "Subscription Activation Service", "Workspace Seat", or "Verified Account Concierge".
- **Genuine Business Operations**: Never state fictional physical addresses. Represent the business honestly as an *"Online Digital Operations Desk, Islamabad & Nationwide Digital Service, Pakistan"*.

---

## 9. Continuous Quality Assurance & Testing Suite

Before any code, page, or configuration is deployed or committed, run the mandatory verification battery:

```bash
# 1. Site Integrity Test Suite (50 Unit Tests)
python -m unittest discover -s tests -v

# 2. Link Graph & Anchor Integrity (0 Broken Links, 0 Broken Anchors)
python scripts/link_graph_checker.py --strict

# 3. AI Overview Grounding & Extractability Audit (All 52 Pages)
python -m aio_agent audit

# 4. SEO & Schema Audit Engine
python -m seo-agent.agent.main --mode audit --report

# 5. Character & Word Count Metric Guard (Titles 30-65, Descs 70-165, QA 35-70 words)
python scripts/check_seo_metrics.py

# 6. Real-Time IndexNow Ping Dispatch
python scripts/submit_indexnow.py
```

### Safety Firewall (Zero-Tolerance Invariants)
1. **Never commit failing tests.**
2. **Never allow broken internal links or invalid `#` anchors.**
3. **Never deploy unverified ratings or fake reviews.**
4. **Never publish pages missing a `.quick-answer` block or single `<h1>`.**
5. **Always maintain total parity between HTML catalog, `merchant_feed.xml`, `sitemap.xml`, and `/llms.txt`.**
