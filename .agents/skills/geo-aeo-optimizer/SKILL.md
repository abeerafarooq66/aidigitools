---
name: geo-aeo-optimizer
description: Audits web pages for Generative Engine Optimization (GEO) and Answer Engine Optimization (AEO) grounding invariants.
---

# GEO & AEO Optimizer Skill

Use this skill to audit and optimize HTML pages on `aidigitools.tech` for AI search engines (Google AI Overviews, Perplexity, Claude Search, ChatGPT).

## Workflow Steps:
1. **H1 & Structure Audit**: Ensure exactly one semantic `<h1>` exists and encapsulates the primary search entity.
2. **Quick-Answer Verification**: Extract the paragraph immediately following H1/H2; verify word count falls between 35 and 70 words.
3. **Query Fan-Out Coverage**: Check for presence of the 5 canonical branches:
   - Pricing in PKR (`Rs.` or `PKR`)
   - Local Payment rails (`EasyPaisa`, `JazzCash`, `SadaPay`, `Raast`)
   - Delivery SLA (`Instant` / `Minutes`)
   - Guarantee / Warranty policy
   - Audience / Practical applications
4. **JSON-LD Schema Verification**: Ensure schemas for `Product`, `Offer`, `BreadcrumbList`, and `FAQPage` are well-formed and valid.
