# SEO Ranking & Health Workflow (/seoranking)

Execute this workflow to perform a complete diagnostic scan of `aidigitools.tech`:

1. **Link Graph & Anchor Integrity Check**:
   ```bash
   python scripts/link_graph_checker.py --strict
   ```

2. **AI Overviews (AIO) Grounding Audit**:
   ```bash
   python -m aio_agent audit
   ```

3. **SEO Character & Word Count Metric Guard**:
   ```bash
   python scripts/check_seo_metrics.py
   ```

4. **Keyword & Competitor Gap Analysis**:
   ```bash
   python -m keyword_agent audit
   python -m keyword_agent competitor-gap
   ```

5. **HERMES SEO Integrity Audit**:
   ```bash
   python -m seo-agent.agent.main --mode audit --report
   ```

6. **Site Integrity Test Suite (50 Tests)**:
   ```bash
   python -m unittest discover -s tests -v
   ```

7. **IndexNow Real-Time Protocol Ping**:
   ```bash
   python scripts/submit_indexnow.py
   ```
