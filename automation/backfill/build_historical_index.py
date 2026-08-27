#!/usr/bin/env python3
"""Build website paper records from verified arXiv metadata and curation."""

from __future__ import annotations

import json
import re
from pathlib import Path


BACKFILL_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = BACKFILL_DIR.parents[1]
METADATA_PATH = BACKFILL_DIR / "historical-arxiv-metadata.json"
CURATION_PATH = BACKFILL_DIR / "historical-curation.json"
SHORT_NAMES_PATH = BACKFILL_DIR / "historical-short-names.json"
TAXONOMY_PATH = BACKFILL_DIR / "taxonomy-tags.json"
MANUAL_PAPERS_PATH = BACKFILL_DIR / "historical-manual-papers.json"
PAPERS_PATH = REPOSITORY_ROOT / "data/papers.json"


def default_ai_assessment(verified_at: str) -> dict:
    return {
        "rating": "standard",
        "rationale": {"en": "", "zh": ""},
        "assessor": "Codex",
        "rubricVersion": "1.0",
        "assessedAt": verified_at,
    }


def default_impact() -> dict:
    return {
        "status": "not-assessed",
        "citationCount": None,
        "influentialCitationCount": None,
        "yearRank": None,
        "cohortSize": None,
        "sourceUrl": None,
        "measuredAt": None,
        "methodVersion": "semantic-scholar-year-cohort-v1",
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def build_record(
    metadata: dict,
    curation: dict,
    short_name: str,
    method_areas: list[str],
    verified_at: str,
) -> dict:
    arxiv_id = metadata["sourceId"].removeprefix("arxiv:")
    source = curation.get("source", {"type": "arxiv", "id": metadata["sourceId"]})
    record_id = source["id"] if source["type"] == "manual" else f"arxiv-{arxiv_id.replace('.', '-')}"
    published = curation.get("published", metadata["published"][:10])
    links = [{"label": "paper", "url": metadata["paperUrl"]}]
    if metadata.get("doi"):
        links.append({"label": "doi", "url": f"https://doi.org/{metadata['doi']}"})
    links.extend(curation.get("extraLinks", []))

    return {
        "id": record_id,
        "source": source,
        "shortName": short_name,
        "title": metadata["title"],
        "authors": curation.get("authors", metadata["authors"]),
        "year": int(curation.get("year", published[:4])),
        "published": published,
        "venue": curation.get(
            "venue",
            metadata.get("publicationVenue") or metadata.get("journalReference") or "arXiv",
        ),
        "areas": list(dict.fromkeys([*curation["areas"], *method_areas])),
        "controlApproaches": curation.get("controlApproaches", []),
        "trackScopes": curation.get("trackScopes", []),
        "summary": curation["summary"],
        "links": links,
        "lastVerified": verified_at,
        "curation": curation.get("curation", "manual"),
    }


def main() -> None:
    metadata = {
        paper["sourceId"].removeprefix("arxiv:"): paper
        for paper in load_json(METADATA_PATH)["papers"]
    }
    curation_data = load_json(CURATION_PATH)
    curated = curation_data["papers"]
    short_names = load_json(SHORT_NAMES_PATH)
    method_tags = load_json(TAXONOMY_PATH)["papers"]
    if set(metadata) != set(curated):
        missing_curation = sorted(set(metadata) - set(curated))
        missing_metadata = sorted(set(curated) - set(metadata))
        raise ValueError(
            f"Backfill sets differ; missing curation={missing_curation}, missing metadata={missing_metadata}"
        )
    if set(metadata) != set(short_names):
        raise ValueError("Every historical paper must have one index short name")

    current = load_json(PAPERS_PATH)
    current_by_source = {
        paper.get("source", {}).get("id"): paper
        for paper in current["papers"]
        if paper.get("source", {}).get("id")
    }
    current_by_title = {normalized_title(paper["title"]): paper for paper in current["papers"]}
    records = [
        build_record(
            metadata[arxiv_id],
            curated[arxiv_id],
            short_names[arxiv_id],
            [area for area, identifiers in method_tags.items() if arxiv_id in identifiers],
            curation_data["verifiedAt"],
        )
        for arxiv_id in curated
    ]
    manual_records = load_json(MANUAL_PAPERS_PATH)["papers"]
    records.extend(manual_records)
    for record in records:
        previous = current_by_source.get(record.get("source", {}).get("id")) or current_by_title.get(
            normalized_title(record["title"])
        )
        record["aiAssessment"] = (
            previous.get("aiAssessment", default_ai_assessment(curation_data["verifiedAt"]))
            if previous
            else default_ai_assessment(curation_data["verifiedAt"])
        )
        record["impact"] = previous.get("impact", default_impact()) if previous else default_impact()
    built_sources = {record["source"]["id"] for record in records}
    built_titles = {normalized_title(record["title"]) for record in records}
    preserved = [
        paper
        for paper in current["papers"]
        if paper.get("source", {}).get("id") not in built_sources
        and normalized_title(paper["title"]) not in built_titles
    ]
    records.extend(preserved)
    records.sort(key=lambda paper: (paper["published"], paper["id"]), reverse=True)

    output = {
        "schemaVersion": 1,
        "updatedAt": curation_data["verifiedAt"],
        "papers": records,
    }
    PAPERS_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Built {len(records)} paper records "
        f"({len(manual_records)} manual, {len(preserved)} preserved outside the backfill)."
    )


if __name__ == "__main__":
    main()
