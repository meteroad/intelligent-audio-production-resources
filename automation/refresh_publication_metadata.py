#!/usr/bin/env python3
"""Refresh formal publication venues and DOI links for indexed arXiv papers."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path

import discover_papers
from publication_metadata import semantic_scholar_doi, semantic_scholar_venue


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fetch_arxiv_ids(
    arxiv_ids: list[str],
    batch_size: int = 40,
    client: discover_papers.ArxivClient | None = None,
) -> list[dict]:
    records = []
    client = client or discover_papers.ArxivClient()
    for offset in range(0, len(arxiv_ids), batch_size):
        batch = arxiv_ids[offset : offset + batch_size]
        parameters = urllib.parse.urlencode({"id_list": ",".join(batch), "max_results": len(batch)})
        response = client.get(
            f"{discover_papers.API_ROOT}?{parameters}",
            "application/atom+xml",
        )
        records.extend(discover_papers.parse_feed(response, "venue-refresh"))
    return records


def fetch_semantic_scholar(arxiv_ids: list[str]) -> dict[str, dict]:
    fields = "title,venue,year,publicationVenue,externalIds"
    request = urllib.request.Request(
        f"https://api.semanticscholar.org/graph/v1/paper/batch?fields={fields}",
        data=json.dumps({"ids": [f"ARXIV:{identifier}" for identifier in arxiv_ids]}).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "User-Agent": discover_papers.USER_AGENT,
            **(
                {"x-api-key": os.environ["SEMANTIC_SCHOLAR_API_KEY"]}
                if os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
                else {}
            ),
        },
        method="POST",
    )
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                records = json.loads(response.read().decode("utf-8"))
            return {
                f"arxiv:{identifier}": record
                for identifier, record in zip(arxiv_ids, records, strict=True)
                if record
            }
        except Exception as error:
            last_error = error
            if attempt < 2:
                time.sleep(2**attempt)
    raise RuntimeError(f"Semantic Scholar venue refresh failed after 3 attempts: {last_error}")


def enrich_with_semantic_scholar(metadata: list[dict], semantic_records: dict[str, dict]) -> list[dict]:
    for record in metadata:
        semantic = semantic_records.get(record["sourceId"])
        if not record.get("publicationVenue"):
            venue, evidence = semantic_scholar_venue(semantic)
            if venue:
                record["publicationVenue"] = venue
                record["venueEvidence"] = evidence
        if not record.get("doi"):
            record["doi"] = semantic_scholar_doi(semantic)
    return metadata


def collect_metadata(
    arxiv_ids: list[str],
    arxiv_fetcher=fetch_arxiv_ids,
    semantic_fetcher=fetch_semantic_scholar,
) -> tuple[list[dict], list[str]]:
    warnings = []
    try:
        metadata = arxiv_fetcher(arxiv_ids)
    except Exception as error:
        warnings.append(f"{error}; continuing without an arXiv metadata refresh")
        metadata = [
            {
                "sourceId": f"arxiv:{identifier}",
                "publicationVenue": None,
                "doi": None,
            }
            for identifier in arxiv_ids
        ]

    try:
        semantic_records = semantic_fetcher(arxiv_ids)
        metadata = enrich_with_semantic_scholar(metadata, semantic_records)
    except Exception as error:
        warnings.append(f"{error}; continuing without a Semantic Scholar metadata refresh")
    return metadata, warnings


def refresh_records(papers_data: dict, metadata: list[dict], verified_date: str) -> tuple[dict, int]:
    evidence = {record["sourceId"]: record for record in metadata}
    changed = 0

    for paper in papers_data.get("papers", []):
        source = paper.get("source", {})
        if source.get("type") != "arxiv":
            continue
        record = evidence.get(source.get("id"))
        if not record:
            continue

        paper_changed = False
        formal_venue = record.get("publicationVenue")
        if formal_venue and paper.get("venue") == "arXiv":
            paper["venue"] = formal_venue
            paper_changed = True

        doi = record.get("doi")
        if doi and not any(link.get("label") == "doi" for link in paper.get("links", [])):
            paper.setdefault("links", []).append({"label": "doi", "url": f"https://doi.org/{doi}"})
            paper_changed = True

        if paper_changed:
            paper["lastVerified"] = verified_date
            changed += 1

    if changed:
        papers_data["updatedAt"] = verified_date
    return papers_data, changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--papers", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--verified-date", default=date.today().isoformat())
    args = parser.parse_args()

    papers_data = load_json(args.papers)
    arxiv_ids = sorted(
        paper["source"]["id"].removeprefix("arxiv:")
        for paper in papers_data.get("papers", [])
        if paper.get("source", {}).get("type") == "arxiv"
    )
    metadata, warnings = collect_metadata(arxiv_ids)
    for warning in warnings:
        print(f"Warning: {warning}.")
    refreshed, changed = refresh_records(papers_data, metadata, args.verified_date)
    output = args.output or args.papers
    output.write_text(json.dumps(refreshed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Processed {len(metadata)} indexed arXiv records; updated {changed} publication entries.")


if __name__ == "__main__":
    main()
