# Data Interface

The website is backed by versioned static JSON. No API key or server-side API is required.

## Endpoints

- Papers: <https://meteroad.github.io/intelligent-audio-production-resources/data/papers.json>
- Projects: <https://meteroad.github.io/intelligent-audio-production-resources/data/projects.json>
- Datasets: <https://meteroad.github.io/intelligent-audio-production-resources/data/datasets.json>
- Reference resources: <https://meteroad.github.io/intelligent-audio-production-resources/data/resources.json>
- Projects v3 schema: <https://meteroad.github.io/intelligent-audio-production-resources/schemas/projects-v3.schema.json>
- Datasets v1 schema: <https://meteroad.github.io/intelligent-audio-production-resources/schemas/datasets-v1.schema.json>

Consumers should inspect the top-level `schemaVersion` before processing a catalogue. Additive fields may be introduced within a schema version. A breaking field or semantic change requires a new schema version and a migration path.

## Papers v1

Paper records include a `controlApproaches` array when the method obtains effect or production-control parameters at inference or target-matching time:

| Identifier | Meaning |
| --- | --- |
| `gradient-based-optimization` | Target-specific iterative optimization through a differentiable processor or processing graph. |
| `derivative-free-optimization` | Target-specific black-box, evolutionary, population-based, or other derivative-free search. |
| `direct-prediction` | A trained model predicts controls or a processing graph without target-specific iterative optimization. |

A paper may combine approaches, for example direct prediction followed by differentiable refinement. Ordinary gradient-based model training alone does not qualify as `gradient-based-optimization`. An empty array means that no listed approach applies or that the available evidence is not sufficiently clear.

Paper records also include a `trackScopes` array:

| Identifier | Meaning |
| --- | --- |
| `single-track` | The method processes, models, estimates, or controls one audio stream at a time. The stream may be an isolated stem, completed mix, or mastered stereo signal. |
| `multitrack` | The method jointly consumes or processes multiple separately available tracks or stems. |

A mixing-related method is not automatically `multitrack`: the paper must explicitly use separately available tracks or stems. Both identifiers may be present when both operating modes are supported; an empty array means the scope is not applicable or not sufficiently clear.

### Recognition metadata

Paper recognition uses two independent signals. Neither is an aggregate score or a ranking of research quality.

`aiAssessment` records a conservative editorial assessment made from public paper metadata. `highlighted` is assigned only when the available evidence supports all four rubric dimensions: a meaningful contribution, coherent methodology, substantive empirical validation, and practical or reproducibility value. `standard` is the default and is not a negative judgment. Only highlighted records carry a public bilingual rationale. `assessor`, `rubricVersion`, and `assessedAt` make each assessment traceable. AI Highlight is not peer review.

`impact` records citation metadata obtained through an exact arXiv or DOI lookup in Semantic Scholar. For each publication year before the current year, `high-impact` means that the paper is in the top `ceil(20%)` of citation counts among exactly matched papers from that year in this index, including ties, and has at least five citations. `yearRank` and `cohortSize` expose the comparison cohort. Current-year papers are `too-recent`; papers without an exact identifier match are `not-assessed`. Citation metadata is refreshed when it is at least 28 days old and every automated change remains subject to pull-request review.

The method is intentionally scoped to this catalogue. `high-impact` does not claim a field-wide percentile, citation counts are time-dependent, and citation impact is not a substitute for technical assessment. GitHub stars are not used as a scholarly impact signal.

## Projects v3

Each project retains the existing bilingual description, areas, links, license label, and verification date. Version 3 adds four evidence-oriented sections:

- `taxonomy`: reviewed task and effect tags plus the evidence URLs used for review;
- `license`: the preserved display label plus identification status, SPDX identifier when unambiguous, and an optional direct evidence URL;
- `availability`: evidence for source, checkpoint, inference, training, and dataset capabilities;
- `relations`: paper IDs associated with the project and how that association was established.

### Availability status

| Status | Meaning |
| --- | --- |
| `not-reviewed` | This capability has not been assessed. It must not be interpreted as unavailable. |
| `linked` | The catalogue records a direct resource URL. This does not mean the resource has been executed or reproduced. |
| `documented` | Public documentation for the capability has been reviewed. |
| `tested` | A curator has executed the documented path and recorded supporting evidence. |
| `gated` | The resource exists but requires an application or approval. |
| `restricted` | Access is limited by terms, credentials, or another explicit restriction. |
| `not-found` | A review did not find the capability. |
| `not-applicable` | The capability does not apply to the project. |

Statuses `linked`, `documented`, `tested`, `gated`, and `restricted` require at least one HTTPS URL in `evidence`. `not-reviewed` requires an empty evidence list so that unreviewed claims cannot enter the index accidentally.

Availability, license, relation, and reviewed taxonomy claims must be backed by first-party public repositories or official documentation. Paper abstracts alone are not enough to mark a project capability as available. When evidence is ambiguous, leave the capability or taxonomy `not-reviewed`; use `not-found` only when a review looked for that capability and did not find it.

### License status

| Status | Meaning |
| --- | --- |
| `identified` | A license label was identified during curation. `spdx` is populated only when the label is unambiguous. |
| `custom` | The repository uses custom or other terms that require reading the linked project. |
| `not-verified` | No license file was verified during the last review. |

An `identified` status is metadata, not legal advice. `BSD` remains without an SPDX identifier because the existing record does not distinguish a specific BSD variant.

### Taxonomy review

Reviewed taxonomy entries use:

- `tasks`: production or research capabilities such as automatic mixing, effect transfer, mastering, or differentiable processing;
- `effects`: processor families explicitly supported by the first-party project evidence;
- `reviewStatus`: `reviewed` only when at least one task or effect tag is supported by evidence;
- `evidence`: direct HTTPS evidence URLs for the reviewed taxonomy claim.

`not-reviewed` taxonomy entries must keep `tasks`, `effects`, and `evidence` empty.

### Relation status

| Status | Meaning |
| --- | --- |
| `not-reviewed` | No paper relation has been assessed. |
| `exact-link-match` | The project and paper records share the same canonical public resource URL. |
| `verified` | A curator has manually confirmed the relation. |

Only `paperIds` are stored on projects. Paper-to-project links should be derived at read time to avoid maintaining the same relation in two places.

## Datasets v1

Each dataset record separates factual dataset metadata from usage relations:

- `taxonomy`: reviewed task, effect, and content-type tags plus first-party evidence;
- `access`: the current access mode and an official URL supporting that status;
- `license`: the data license or terms, kept distinct from licenses for accompanying software;
- `relations`: paper and project IDs that use the dataset, with an evidence URL on every relation;
- `scale`: a concise bilingual description of the public collection's size or composition.

Access statuses are `direct-download`, `request`, `registration`, `restricted`, `unavailable`, and `not-reviewed`. Every reviewed status requires an HTTPS evidence URL. Identified and custom data licenses also require direct evidence; an unknown license remains `not-verified` and must not inherit a repository's software license.

Dataset relations are stored only in `datasets.json`; paper-to-dataset and project-to-dataset views are derived at read time. Each referenced ID must exist in the paper or project catalogue, relation IDs must be unique within a dataset, and every relation must cite primary paper text, an official repository, or official documentation that demonstrates use.

## Website behavior

The project table supports compound filtering by text, area, linked control approach, linked track scope, license identity (SPDX, reviewed custom terms, or unverified), availability capability, availability status, and reviewed taxonomy tags. Task and effect filters are shown only when reviewed taxonomy tags exist in the loaded data. The dataset table supports text, area, task, content-type, and access filtering. The paper index supports text, area, control-approach, track-scope, AI Highlight, and High Impact filtering. The three primary indexes paginate filtered results in groups of ten. Reset buttons clear their respective filters.

Each project and dataset row contains a keyboard-focusable details button. Dataset details show access and license evidence, taxonomy, official links, and evidence-backed paper/project usage relations. Dataset, paper, and project dialogs expose the relation in both directions while keeping one canonical data record. Interface labels are localized in English and Chinese.

## Link checks

Build a no-model-API link report with:

```bash
python3 automation/check_links.py --output /tmp/link-check-report.json
```

Without `--output`, the report is written to stdout. The checker reads public JSON data, sends deterministic HTTP requests, and classifies URLs as `success`, `redirect`, `access-blocked`, `rate-limited`, `network-failure`, or `broken`. It never edits paper, project, or resource data. The scheduled/manual **Link check report** workflow uploads the JSON report as an artifact and does not commit changes.

## Migration

Upgrade a projects v2 document using the paper catalogue as deterministic relation evidence:

```bash
python3 automation/migrate_projects_v3.py \
  --direction upgrade \
  --input data/projects.json \
  --output data/projects.json \
  --papers data/papers.json
```

Downgrade a v3 document to the original v2 surface fields:

```bash
python3 automation/migrate_projects_v3.py \
  --direction downgrade \
  --input data/projects.json \
  --output /tmp/projects-v2.json
```

The migration is deterministic. It does not infer task tags, effect tags, training support, inference support, or dataset access from project descriptions.
