#!/usr/bin/env python3
"""Merge the reviewed spatial-production backfill into the paper catalogue."""

from __future__ import annotations

import json
import re
from pathlib import Path


BACKFILL_DIR = Path(__file__).resolve().parent
ROOT = BACKFILL_DIR.parents[1]
METADATA_PATH = BACKFILL_DIR / "spatial-arxiv-metadata.json"
CURATION_PATH = BACKFILL_DIR / "spatial-curation.json"
MANUAL_PATH = BACKFILL_DIR / "spatial-manual-papers.json"
PAPERS_PATH = ROOT / "data/papers.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def build_record(metadata: dict, curation: dict, verified_at: str) -> dict:
    arxiv_id = metadata["sourceId"].removeprefix("arxiv:")
    published = metadata["published"][:10]
    links = [{"label": "paper", "url": metadata["paperUrl"]}]
    if metadata.get("doi"):
        links.append({"label": "doi", "url": f"https://doi.org/{metadata['doi']}"})
    if curation.get("sourceUrl"):
        links.append({"label": "source", "url": curation["sourceUrl"]})
    if curation.get("projectUrl"):
        links.append({"label": "project", "url": curation["projectUrl"]})

    return {
        "id": f"arxiv-{arxiv_id.replace('.', '-')}",
        "source": {"type": "arxiv", "id": metadata["sourceId"]},
        "shortName": curation["shortName"],
        "title": metadata["title"],
        "authors": metadata["authors"],
        "year": int(published[:4]),
        "published": published,
        "venue": metadata.get("publicationVenue") or metadata.get("journalReference") or "arXiv",
        "areas": curation["areas"],
        "controlApproaches": curation["controlApproaches"],
        "trackScopes": curation["trackScopes"],
        "summary": curation["summary"],
        "links": links,
        "lastVerified": verified_at,
        "curation": "manual",
        "aiAssessment": {
            "rating": "standard",
            "rationale": {"en": "", "zh": ""},
            "assessor": "Codex",
            "rubricVersion": "1.0",
            "assessedAt": verified_at,
        },
        "impact": {
            "status": "not-assessed",
            "citationCount": None,
            "influentialCitationCount": None,
            "yearRank": None,
            "cohortSize": None,
            "sourceUrl": None,
            "measuredAt": None,
            "methodVersion": "semantic-scholar-year-cohort-v1",
        },
    }


def main() -> None:
    metadata = {
        item["sourceId"].removeprefix("arxiv:"): item
        for item in load(METADATA_PATH)["papers"]
    }
    curation_data = load(CURATION_PATH)
    curated = curation_data["papers"]
    if set(metadata) != set(curated):
        raise ValueError("Spatial metadata and curation identifiers differ")

    current = load(PAPERS_PATH)
    current_sources = {paper["source"]["id"] for paper in current["papers"]}
    current_titles = {normalized_title(paper["title"]) for paper in current["papers"]}
    added = 0
    for arxiv_id, curation in curated.items():
        record = build_record(metadata[arxiv_id], curation, curation_data["verifiedAt"])
        if record["source"]["id"] in current_sources or normalized_title(record["title"]) in current_titles:
            continue
        current["papers"].append(record)
        current_sources.add(record["source"]["id"])
        current_titles.add(normalized_title(record["title"]))
        added += 1

    for record in load(MANUAL_PATH)["papers"]:
        if record["source"]["id"] in current_sources or normalized_title(record["title"]) in current_titles:
            continue
        current["papers"].append(record)
        current_sources.add(record["source"]["id"])
        current_titles.add(normalized_title(record["title"]))
        added += 1

    current["papers"].sort(key=lambda paper: (paper["published"], paper["id"]), reverse=True)
    current["updatedAt"] = curation_data["verifiedAt"]
    PAPERS_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} spatial-production papers; catalogue now contains {len(current['papers'])} papers.")


if __name__ == "__main__":
    main()
