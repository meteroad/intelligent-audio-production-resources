# Intelligent Audio Production Resources

A curated, bilingual research index covering audio effects, differentiable processing, representation learning, automatic mixing, mastering, and evaluation.

[Browse the index](https://meteroad.github.io/intelligent-audio-production-resources/) · [Submit a resource](https://github.com/meteroad/intelligent-audio-production-resources/issues/new/choose) · [Report an issue](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=correction.yml)

**69 papers · 38 verified projects · 2 reference collections**

[![Intelligent Audio Production: papers, code, models, datasets, and benchmarks](assets/social-preview.jpg)](https://meteroad.github.io/intelligent-audio-production-resources/)

## What You Can Find

| Collection | Included information |
| --- | --- |
| Papers | Formal venues, paper and DOI links, concise English and Chinese summaries, and associated open resources |
| Projects | Source, checkpoint, inference, training, dataset, license, taxonomy, related-paper evidence, and last-verification dates |
| Reference resources | Field bibliographies and research guides kept separate from runnable implementations |

The index is organized by production task rather than publication year. It currently covers:

- audio effects modeling, estimation, control, transfer, and removal;
- differentiable DSP, effect chains, and processing graphs;
- effect and production-style representation learning;
- automatic, reference-guided, and controllable mixing;
- mastering and remastering;
- benchmarks, metrics, datasets, and reproducibility tools.

Spatial audio is listed as a future extension rather than mixed into the current catalogue.

## Curation Principles

- Paper titles, authors, dates, and links are anchored to primary publication sources where available.
- Formal venues are shown only when publication evidence can be verified.
- Project source, checkpoint, dataset, taxonomy, and license claims are recorded with first-party repository or official-documentation evidence.
- The weekly paper scout proposes reviewable changes; AI-screened candidates are never published directly.
- Every public entry remains open to correction through a structured issue or pull request.

## Contribute

The quickest route is to open a structured request:

- [Add a paper](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=paper.yml)
- [Add an open-source project](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=project.yml)
- [Correct metadata or report a broken link](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=correction.yml)

Please include a primary paper or project URL and enough evidence to verify the requested change. See [CONTRIBUTING.md](CONTRIBUTING.md) before editing catalogue data directly.

## Data

The catalogue is available as version-controlled JSON:

- [`data/papers.json`](data/papers.json)
- [`data/projects.json`](data/projects.json)
- [`data/resources.json`](data/resources.json)

These files drive the public website and can also be used for research tooling or downstream analysis under the repository license.

See [DATA.md](DATA.md) for endpoint URLs, schema versions, field semantics, and migration guidance. The formal projects v3 contract is available at [`schemas/projects-v3.schema.json`](schemas/projects-v3.schema.json).

## Automation

The weekly paper scout searches arXiv, screens candidates with a configured language model, refreshes formal venue and DOI metadata, validates the data, and opens a reviewable pull request. It does not publish unreviewed candidates directly.

See [automation/README.md](automation/README.md) for configuration and review rules.

## Local Preview

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

Run the checks with:

```bash
python3 automation/validate_data.py
python3 -m unittest discover -s automation/tests -v
node --check app.js
```

Generate a deterministic URL review report without editing data:

```bash
python3 automation/check_links.py --output /tmp/link-check-report.json
```

## License

The site code, automation, and original catalogue content in this repository are released under the [MIT License](LICENSE). Linked papers, codebases, models, datasets, and trademarks remain subject to their respective owners' terms.
