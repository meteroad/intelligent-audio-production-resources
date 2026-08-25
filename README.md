# Intelligent Audio Production

A bilingual, research-oriented index of open projects and papers for intelligent audio effects and music production.

- **Website:** https://meteroad.github.io/intelligent-audio-production/
- **Maintainer:** [Xinlu Liu](https://meteroad.github.io/)
- **Current index:** 38 verified projects, 69 papers, and 2 reference resources

## Scope

The index currently covers:

- audio effects modeling, estimation, control, transfer, and removal;
- differentiable DSP, effect chains, and processing graphs;
- effect and production-style representation learning;
- automatic, reference-guided, and controllable mixing;
- mastering and remastering;
- benchmarks, metrics, datasets, and reproducibility tools.

Spatial audio is listed as a future extension rather than mixed into the current catalogue.

## Use the index

Open the [website](https://meteroad.github.io/intelligent-audio-production/) to browse by field, search projects and papers, and view verified paper, code, model, and DOI links. The interface is available in English and Chinese.

## Contribute

Issues and pull requests are welcome for:

- missing papers, repositories, checkpoints, or datasets;
- incorrect venues, links, licenses, or task labels;
- concise corrections to English or Chinese summaries.

Please include a primary paper or project URL and enough evidence to verify the requested change. New records must fit the production-oriented scope and pass `automation/validate_data.py`.

## Automation

The weekly paper scout searches arXiv, screens candidates with a configured language model, refreshes formal venue and DOI metadata, validates the data, and opens a reviewable pull request. It does not publish unreviewed candidates directly.

See [automation/README.md](automation/README.md) for configuration and review rules.

## Local preview

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

## License

The site code, automation, and original catalogue content in this repository are released under the [MIT License](LICENSE). Linked papers, codebases, models, datasets, and trademarks remain subject to their respective owners' terms.
