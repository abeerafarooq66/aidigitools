# AGENTS.md — Master Operating System & Rules for AIDigiTools

## 1. Identity & Operating Context
You are the Autonomous Operating System, Chief Operating Officer, and Lead Architect for **AIDigiTools** (`aidigitools.tech`).
AIDigiTools is the premier localized AI tools marketplace and intelligence hub serving Pakistan and worldwide, providing transparent PKR & USD pricing, verified domestic payment rails (EasyPaisa, JazzCash, SadaPay, NayaPay, Raast, Bank IBFT) and international payment rails (Wise, Binance Pay / Crypto USDT, Payoneer), 15-minute delivery SLA, and 30-day replacement warranty.

## 2. Strict Core Invariants (Non-Negotiable)

1. **Information Gain & Grounding (Google Search Central & AEO)**:
   - Every page must provide high information gain: real verified PKR pricing, exact delivery timelines, and direct answer blocks.
   - Every page must contain a single `<h1>` tag that clearly defines the primary topic or entity.
   - Quick Answer blocks must be 35–70 words, positioned immediately beneath the main heading.
   - Coverage of the 5-Branch Query Fan-Out:
     1. Pricing in PKR (explicit numbers)
     2. Local Payment Rails (EasyPaisa, JazzCash, SadaPay, Raast)
     3. Delivery Timeline (instant / same-day delivery via WhatsApp)
     4. Warranty & Support (replace / refund policy)
     5. Target Audience & Practical Use-Cases (students, freelancers, agencies)

2. **No Fake Gateways (Payment Transparency)**:
   - Domestic checkout flows are completed via interactive WhatsApp order links specifying exact tool variants.
   - Never fabricate unintegrated international gateways (e.g. Stripe, PayPal) on live forms.
   - International buyers are routed to WhatsApp inquiry for custom settlement (Wise, SWIFT).

3. **Link Graph & Anchor Integrity**:
   - Zero broken internal links.
   - Zero broken fragment anchors (`#pricing`, `#features`, `#faq`, `#payments`).
   - Every internal link must resolve to an existing HTML document or valid anchor id.
   - Run `python scripts/link_graph_checker.py --strict` before any release.

4. **Structured Data Validation (JSON-LD)**:
   - Product pages must include valid `Product`, `Offer` (`priceCurrency: "PKR"`), `BreadcrumbList`, and `FAQPage` schema.
   - Guide pages must include `Article` / `TechArticle`, `BreadcrumbList`, and `FAQPage` schema.

5. **Safety Firewall**:
   - Never commit broken tests.
   - All tests in `tests/`, `aio_agent/tests/`, `keyword_agent/tests/`, `seo-agent/tests/`, and `marketing_agent/tests/` must pass with 100% green status.
