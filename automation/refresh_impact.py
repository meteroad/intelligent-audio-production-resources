#!/usr/bin/env python3
"""Refresh year-normalized paper impact metadata from Semantic Scholar."""

from __future__ import annotations

import argparse
import json
import math
import os
import time
import urllib.parse
import urllib.request
from datetime import date, timedelta
from pathlib import Path

import discover_papers


METHOD_VERSION = "semantic-scholar-year-cohort-v1"
MIN_HIGH_IMPACT_CITATIONS = 5
HIGH_IMPACT_FRACTION = 0.20


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def paper_identifier(paper: dict) -> str | None:
    source = paper.get("source", {})
    if source.get("type") == "arxiv" and source.get("id"):
        return f"ARXIV:{source['id'].removeprefix('arxiv:')}"
    for link in paper.get("links", []):
        if link.get("label") != "doi":
            continue
        parsed = urllib.parse.urlparse(link.get("url", ""))
        if parsed.netloc.lower() in {"doi.org", "www.doi.org"} and parsed.path.strip("/"):
            return f"DOI:{urllib.parse.unquote(parsed.path.strip('/'))}"
    return None


def fetch_semantic_scholar(identifiers: list[str], batch_size: int = 500) -> dict[str, dict]:
    fields = "title,year,citationCount,influentialCitationCount,url,externalIds"
    records: dict[str, dict] = {}
    for offset in range(0, len(identifiers), batch_size):
        batch = identifiers[offset : offset + batch_size]
        request = urllib.request.Request(
            f"https://api.semanticscholar.org/graph/v1/paper/batch?fields={fields}",
            data=json.dumps({"ids": batch}).encode("utf-8"),
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
                    payload = json.loads(response.read().decode("utf-8"))
                for identifier, record in zip(batch, payload, strict=True):
                    if record and record.get("paperId"):
                        records[identifier] = record
                break
            except Exception as error:
                last_error = error
                if attempt < 2:
                    time.sleep(2**attempt)
        else:
            raise RuntimeError(f"Semantic Scholar impact refresh failed after 3 attempts: {last_error}")
    return records


def impact_is_stale(papers_data: dict, today: date, max_age_days: int) -> bool:
    cutoff = today - timedelta(days=max_age_days)
    for paper in papers_data.get("papers", []):
        impact = paper.get("impact")
        if not isinstance(impact, dict) or not impact.get("measuredAt"):
            return True
        try:
            if date.fromisoformat(impact["measuredAt"]) <= cutoff:
                return True
        except (TypeError, ValueError):
            return True
    return False


def empty_impact(status: str, measured_date: str) -> dict:
    return {
        "status": status,
        "citationCount": None,
        "influentialCitationCount": None,
        "yearRank": None,
        "cohortSize": None,
        "sourceUrl": None,
        "measuredAt": measured_date,
        "methodVersion": METHOD_VERSION,
    }


def refresh_records(
    papers_data: dict,
    semantic_records: dict[str, dict],
    measured_date: str,
) -> tuple[dict, int]:
    current_year = date.fromisoformat(measured_date).year
    eligible_by_year: dict[int, list[tuple[dict, dict]]] = {}
    changed = 0

    for paper in papers_data.get("papers", []):
        identifier = paper_identifier(paper)
        record = semantic_records.get(identifier) if identifier else None
        if paper.get("year") >= current_year:
            impact = empty_impact("too-recent", measured_date)
            if record:
                impact.update(
                    citationCount=int(record.get("citationCount") or 0),
                    influentialCitationCount=int(record.get("influentialCitationCount") or 0),
                    sourceUrl=record.get("url"),
                )
            if paper.get("impact") != impact:
                paper["impact"] = impact
                changed += 1
            continue
        if not record:
            impact = empty_impact("not-assessed", measured_date)
            if paper.get("impact") != impact:
                paper["impact"] = impact
                changed += 1
            continue
        eligible_by_year.setdefault(paper["year"], []).append((paper, record))

    for cohort in eligible_by_year.values():
        citation_counts = sorted((int(record.get("citationCount") or 0) for _, record in cohort), reverse=True)
        cutoff_index = max(0, math.ceil(len(cohort) * HIGH_IMPACT_FRACTION) - 1)
        citation_threshold = max(MIN_HIGH_IMPACT_CITATIONS, citation_counts[cutoff_index])
        for paper, record in cohort:
            citation_count = int(record.get("citationCount") or 0)
            impact = {
                "status": "high-impact" if citation_count >= citation_threshold else "standard",
                "citationCount": citation_count,
                "influentialCitationCount": int(record.get("influentialCitationCount") or 0),
                "yearRank": 1 + sum(value > citation_count for value in citation_counts),
                "cohortSize": len(cohort),
                "sourceUrl": record.get("url"),
                "measuredAt": measured_date,
                "methodVersion": METHOD_VERSION,
            }
            if paper.get("impact") != impact:
                paper["impact"] = impact
                changed += 1

    if changed:
        papers_data["updatedAt"] = measured_date
    return papers_data, changed


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--papers", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--measured-date", default=date.today().isoformat())
    parser.add_argument("--max-age-days", type=int, default=28)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    papers_data = load_json(args.papers)
    today = date.fromisoformat(args.measured_date)
    if not args.force and not impact_is_stale(papers_data, today, args.max_age_days):
        print("Citation impact metadata is still fresh; no refresh needed.")
        return

    identifiers = sorted(
        identifier
        for paper in papers_data.get("papers", [])
        if (identifier := paper_identifier(paper))
    )
    try:
        semantic_records = fetch_semantic_scholar(identifiers)
    except Exception as error:
        print(f"Warning: {error}; keeping existing impact metadata.")
        return

    refreshed, changed = refresh_records(papers_data, semantic_records, args.measured_date)
    output = args.output or args.papers
    output.write_text(json.dumps(refreshed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Resolved {len(semantic_records)} of {len(identifiers)} papers; updated {changed} impact entries.")


if __name__ == "__main__":
    main()
