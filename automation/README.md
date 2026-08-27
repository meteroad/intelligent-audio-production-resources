# AI paper scout

The paper scout follows a reviewable pipeline:

1. A scheduled GitHub Action retrieves recent metadata from the public arXiv API.
2. DeepSeek classifies direct relevance, production-control approaches, input track scope, short English and Chinese summaries, and a conservative AI Highlight assessment under the website taxonomy.
3. A deterministic refresh rechecks every indexed arXiv record for DOI and formal publication information, using Semantic Scholar as a secondary bibliographic fallback.
4. Citation counts are refreshed from exact arXiv or DOI matches when the stored measurement is at least 28 days old. High Impact is derived within each pre-current-year index cohort; current-year papers are not ranked.
5. Titles, authors, dates, and paper URLs remain anchored to arXiv. Formal venues prioritize arXiv `journal_ref`, recognized DOI metadata, and arXiv comments; Semantic Scholar is used only when those fields do not identify a venue. Submission or under-review comments are never treated as acceptance evidence.
6. Only high-confidence new records and verified metadata changes that pass deterministic validation and unit tests are proposed in a pull request.
7. Merging the pull request updates `main`; the Pages workflow then deploys the validated static site.

The active scope covers audio effects, differentiable production processing, effect and production representations, mixing, mastering, and task-specific evaluation. Spatial audio remains deferred. Bibliography repositories are maintained under `data/resources.json`; they are not treated as runnable projects. Dataset records and their paper/project usage relations are maintained under `data/datasets.json` and pass deterministic cross-reference validation, but the paper scout does not infer dataset usage automatically.

## Repository setup

In GitHub, open **Settings → Secrets and variables → Actions**:

- Add a repository secret named `DEEPSEEK_API_KEY`.
- Optionally add `SEMANTIC_SCHOLAR_API_KEY` to increase the bibliographic refresh rate limit. The public batch API is used when this secret is absent.
- Under **Actions → General → Workflow permissions**, allow read and write permissions and allow GitHub Actions to create pull requests.

The workflow runs every Monday at 01:00 UTC (09:00 Asia/Shanghai) and can also be started manually from **Actions → Weekly paper scout → Run workflow**. The publication refresh runs even when no new candidate paper is found.

For unattended publication after validation, add the repository variable `PAPER_SCOUT_AUTO_MERGE` with the value `true`. The safer default is to review and merge the generated pull request manually.

Never commit an API key or place it in workflow-level environment variables.

The curation step uses `deepseek-v4-flash` in non-thinking JSON mode. Set the optional repository or job environment variable `DEEPSEEK_MODEL` only when intentionally testing another compatible model.

AI Highlight is an editorial model assessment, not peer review. It requires evidence for contribution, methodological coherence, empirical validation, and practical or reproducibility value. The `standard` state is not displayed as a negative label. Citation impact is kept independent and never combined with this assessment into a single score. See [`DATA.md`](../DATA.md#recognition-metadata) for the exact impact threshold and field contract.

## Local checks

```bash
python3 automation/validate_data.py
python3 -m unittest discover -s automation/tests -v
node --check app.js
```

Force a local citation refresh when needed:

```bash
python3 automation/refresh_impact.py --force
```

Build a review-only URL report with:

```bash
python3 automation/check_links.py --output /tmp/link-check-report.json
```

The checker reads public JSON files, distinguishes successful links, redirects, 401/403 access blocks, 429 rate limits, network failures/timeouts, and broken HTTP responses, and never edits catalogue data. The `Link check report` GitHub workflow can run weekly or manually and uploads the JSON report as an artifact.

## Project catalogue migration

The project catalogue uses an evidence-oriented v3 schema. Upgrade a v2 catalogue with:

```bash
python3 automation/migrate_projects_v3.py \
  --direction upgrade \
  --input data/projects.json \
  --output data/projects.json \
  --papers data/papers.json
```

The migration records existing source and checkpoint links as `linked`, matches paper relations only through identical canonical resource URLs, and leaves all unsupported capability and taxonomy claims as `not-reviewed`. It also supports a deterministic `downgrade` direction for compatibility checks. See [`DATA.md`](../DATA.md) for the complete interface contract.
