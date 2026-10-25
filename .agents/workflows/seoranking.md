# SEO Ranking & Health Workflow (/seoranking)

Execute this workflow to perform a complete diagnostic scan of `aidigitools.tech`:

1. **Link Graph Check**:
   ```bash
   python scripts/link_graph_checker.py --strict
   ```
2. **AI Overviews (AIO) Grounding Audit**:
   ```bash
   python -m aio_agent audit
   ```
3. **Keyword & Competitor Gap Analysis**:
   ```bash
   python -m keyword_agent audit
   python -m keyword_agent competitor-gap
   ```
4. **HERMES SEO Integrity Audit**:
   ```bash
   python -m seo-agent.agent.main --mode audit --report
   ```
5. **Full Unit Test Gate**:
   ```bash
   python -m unittest discover -s tests -v
   ```
