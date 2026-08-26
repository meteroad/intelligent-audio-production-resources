#!/usr/bin/env python3
"""Merge only high-confidence agent decisions using authoritative candidate metadata."""

from __future__ import annotations

import argparse
import json
import re
from datetime import date
from pathlib import Path


ALLOWED_AREAS = {
    "audio-effects",
    "differentiable-processing",
    "representation",
    "mixing",
    "mastering",
    "evaluation",
    "spatial-audio",
}
ALLOWED_CONTROL_APPROACHES = {
    "gradient-based-optimization",
    "derivative-free-optimization",
    "direct-prediction",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def paper_id(source_id: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", source_id.lower()).strip("-")


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def validate_decision(decision: dict, candidate_ids: set[str]) -> None:
    source_id = decision.get("sourceId")
    if source_id not in candidate_ids:
        raise ValueError(f"Agent returned an unknown sourceId: {source_id!r}")
    areas = decision.get("areas", [])
    if decision.get("decision") == "include":
        if not areas or len(areas) != len(set(areas)) or not set(areas).issubset(ALLOWED_AREAS):
            raise ValueError(f"Invalid areas for {source_id}: {areas}")
        control_approaches = decision.get("controlApproaches", [])
        if (
            not isinstance(control_approaches, list)
            or len(control_approaches) != len(set(control_approaches))
            or not set(control_approaches).issubset(ALLOWED_CONTROL_APPROACHES)
        ):
            raise ValueError(f"Invalid control approaches for {source_id}: {control_approaches}")
        summary = decision.get("summary", {})
        for language in ("en", "zh"):
            value = summary.get(language, "").strip()
            if not 20 <= len(value) <= 500:
                raise ValueError(f"Invalid {language} summary length for {source_id}")


def merge_records(candidates_data: dict, review_data: dict, papers_data: dict) -> tuple[dict, int]:
    candidates = {paper["sourceId"]: paper for paper in candidates_data.get("candidates", [])}
    decisions = review_data.get("decisions", [])
    seen_decisions = set()
    for decision in decisions:
        source_id = decision.get("sourceId")
        if source_id in seen_decisions:
            raise ValueError(f"Duplicate agent decision for {source_id}")
        seen_decisions.add(source_id)
        validate_decision(decision, set(candidates))
    if seen_decisions != set(candidates):
        missing = sorted(set(candidates) - seen_decisions)
        raise ValueError(f"Agent did not review every candidate; missing: {missing}")

    existing_sources = {
        paper.get("source", {}).get("id")
        for paper in papers_data.get("papers", [])
        if paper.get("source", {}).get("id")
    }
    existing_titles = {
        normalized_title(paper["title"])
        for paper in papers_data.get("papers", [])
        if isinstance(paper.get("title"), str)
    }
    added = 0
    verified_date = candidates_data.get("generatedAt", date.today().isoformat())[:10]

    for decision in decisions:
        if decision.get("decision") != "include" or decision.get("confidence") != "high":
            continue
        source_id = decision["sourceId"]
        candidate = candidates[source_id]
        if source_id in existing_sources or normalized_title(candidate["title"]) in existing_titles:
            continue
        links = [{"label": "paper", "url": candidate["paperUrl"]}]
        if candidate.get("doi"):
            links.append({"label": "doi", "url": f"https://doi.org/{candidate['doi']}"})
        published = candidate["published"][:10]
        papers_data["papers"].append(
            {
                "id": paper_id(source_id),
                "source": {"type": "arxiv", "id": source_id},
                "title": candidate["title"],
                "authors": candidate["authors"],
                "year": int(published[:4]),
                "published": published,
                "venue": candidate.get("publicationVenue") or candidate.get("journalReference") or "arXiv",
                "areas": decision["areas"],
                "controlApproaches": decision["controlApproaches"],
                "summary": decision["summary"],
                "links": links,
                "lastVerified": verified_date,
                "curation": "agent",
            }
        )
        existing_sources.add(source_id)
        existing_titles.add(normalized_title(candidate["title"]))
        added += 1

    papers_data["papers"].sort(key=lambda paper: (paper["published"], paper["id"]), reverse=True)
    if added:
        papers_data["updatedAt"] = verified_date
    return papers_data, added


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--review", type=Path, required=True)
    parser.add_argument("--papers", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    merged, added = merge_records(
        load_json(args.candidates),
        load_json(args.review),
        load_json(args.papers),
    )
    args.output.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} high-confidence papers.")


if __name__ == "__main__":
    main()
