# Contributing

Contributions that improve the accuracy, coverage, or usability of the index are welcome.

## What Belongs in the Index

A submission should make a direct contribution to intelligent audio production, including audio effects, differentiable processing, production representations, mixing, mastering, or task-specific evaluation.

Generic speech enhancement, audio generation, source separation, room acoustics, and spatial localization are out of scope unless the work makes a direct production or audio-effects contribution.

## Submit Through an Issue

Use one of the structured forms for the fastest review:

- [Add a paper](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=paper.yml)
- [Add an open-source project](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=project.yml)
- [Correct an entry](https://github.com/meteroad/intelligent-audio-production-resources/issues/new?template=correction.yml)

Include primary evidence whenever possible: a publisher or conference page, DOI, arXiv record, official project page, source repository, model card, dataset page, or license file.

## Submit a Pull Request

Direct catalogue changes should preserve the existing JSON schema and keep English and Chinese summaries concise and factual. Do not infer a formal venue from a submission statement or label a project open source without checking its license.

Before opening a pull request, run:

```bash
python3 automation/validate_data.py
python3 -m unittest discover -s automation/tests -v
node --check app.js
git diff --check
```

The maintainers may adjust wording, taxonomy, identifiers, or links so records remain consistent across the index.
