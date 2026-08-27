# Contributing

Contributions that improve the accuracy, coverage, or usability of the index are welcome.

## What Belongs in the Index

A submission should make a direct contribution to intelligent audio production, including audio effects, differentiable processing, production representations, mixing, mastering, production-facing spatial audio, or task-specific evaluation.

Generic speech enhancement, audio generation, source separation, room acoustics, and spatial localization are out of scope unless the work makes a direct production, audio-effects, or spatial-rendering contribution.

## Submit Through an Issue

Use one of the structured forms for the fastest review:

- [Add a paper](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=paper.yml)
- [Add an open-source project](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=project.yml)
- [Add a dataset](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=dataset.yml)
- [Correct an entry](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=correction.yml)

Include primary evidence whenever possible: a publisher or conference page, DOI, arXiv record, official project page, source repository, model card, dataset page, or license file.

## Submit a Pull Request

Direct catalogue changes should preserve the existing JSON schema and keep English and Chinese summaries concise and factual. Do not infer a formal venue from a submission statement, label a project open source without checking its license, or reuse a software license as the license for its associated audio data.

Preview website changes through a local HTTP server so the browser can load the JSON catalogue:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`.

Before opening a pull request, run:

```bash
python3 automation/validate_data.py
python3 -m unittest discover -s automation/tests -v
node --check app.js
git diff --check
```

For a deterministic URL review report that does not edit catalogue data, run:

```bash
python3 automation/check_links.py --output /tmp/link-check-report.json
```

The maintainers may adjust wording, taxonomy, identifiers, or links so records remain consistent across the index.
