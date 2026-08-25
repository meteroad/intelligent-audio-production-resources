# Data Interface

The website is backed by versioned static JSON. No API key or server-side API is required.

## Endpoints

- Papers: <https://meteroad.github.io/intelligent-audio-production-resources/data/papers.json>
- Projects: <https://meteroad.github.io/intelligent-audio-production-resources/data/projects.json>
- Reference resources: <https://meteroad.github.io/intelligent-audio-production-resources/data/resources.json>
- Projects v3 schema: <https://meteroad.github.io/intelligent-audio-production-resources/schemas/projects-v3.schema.json>

Consumers should inspect the top-level `schemaVersion` before processing a catalogue. Additive fields may be introduced within a schema version. A breaking field or semantic change requires a new schema version and a migration path.

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

## Website behavior

The project table supports compound filtering by text, area, license identity (SPDX, reviewed custom terms, or unverified), availability capability, availability status, and reviewed taxonomy tags. Task and effect filters are shown only when reviewed taxonomy tags exist in the loaded data. The reset button clears all project filters.

Each project row contains a keyboard-focusable details button. The details dialog shows related papers, license metadata and evidence, source/checkpoint/inference/training/dataset status and evidence, taxonomy tags and evidence, project links, and the verification date. Interface labels are localized in English and Chinese.

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
