# Google AI Optimization & Retrieval Grounding Rules

> Grounded in Google Search Central's official guide: [Optimizing your website for generative AI features on Google Search](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

## 1. Google's Official Stance on AI Search
- **AI Search is Built on Core Search**: Google AI Overviews and AI Mode are not a separate search engine. They retrieve information from the standard Google Search index using Retrieval-Augmented Generation (RAG) and core ranking/quality algorithms.
- **AEO and GEO are Modern SEO**: Answer Engine Optimization and Generative Engine Optimization are not secret "hacks". They are simply the discipline of producing crawlable, well-structured, authoritative, non-commodity content that Google's retrieval systems can easily parse and cite.

## 2. RAG & Grounding Best Practices
- **Retrieve-Friendly Architecture**: Ensure critical facts (pricing, specs, compatibility, delivery times, policies) are stated directly and clearly in HTML text, not buried in client-rendered scripts or generic banners.
- **Query Fan-Out Coverage**: When a user queries a topic, Google's AI fan-out expands the query into logical sub-questions. Anticipate and answer related sub-topics natively on the same page.
- **Source Citation Authority**: Google cites sources that provide first-hand verification, distinct points of view, and verifiable technical depth. Avoid generic recycled summaries.

## 3. The 6 Debunked AI Optimization Myths (Forbidden Tactics)
1. **Forbidden: Relying on `llms.txt` for Google Search.**
   Google Search indexing systems completely ignore `llms.txt`. All content must be rendered in standard HTML.
2. **Forbidden: Artificial Micro-Chunking.**
   Do not slice articles into disconnected, artificial fragments or mini-pages. Google prioritizes comprehensive, well-structured guides with natural semantic sections (`<section>`, `<h2>`, `<h3>`).
3. **Forbidden: Writing in Robotic / Machine Syntax.**
   Do not rewrite content into unnatural synthetic jargon. Clear, polished, human-first writing scores highest in helpfulness algorithms.
4. **Forbidden: Fake Schema & Manipulative Ratings.**
   Never add `aggregateRating` without visible on-page user reviews. Never inject hidden schema data.
5. **Forbidden: Scaled Thin Content Generation.**
   Generating dozens of near-identical low-value pages for minor keyword permutations violates Google's Scaled Content Abuse policy. Consolidate into robust pillar pages.
6. **Forbidden: Fabricating Physical Addresses or Entities.**
   Never use fictional corporate addresses. Always accurately represent the online digital operations desk.
