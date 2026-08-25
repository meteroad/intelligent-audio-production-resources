#!/usr/bin/env python3
"""Discover recent candidate papers from the public arXiv API."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

from publication_metadata import resolve_publication_venue


ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
USER_AGENT = "IntelligentAudioProductionPaperScout/1.0 (https://meteroad.github.io/intelligent-audio-production/)"


def compact_text(value: str | None) -> str:
    return " ".join((value or "").split())


def normalized_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def source_id_from_url(url: str) -> str:
    identifier = urllib.parse.urlparse(url).path.rsplit("/", 1)[-1]
    identifier = re.sub(r"v\d+$", "", identifier)
    if not identifier:
        raise ValueError(f"Could not parse arXiv identifier from {url!r}")
    return f"arxiv:{identifier}"


def https_arxiv_url(source_id: str) -> str:
    return f"https://arxiv.org/abs/{source_id.removeprefix('arxiv:')}"


def parse_feed(xml_text: str, query_name: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    papers = []
    for entry in root.findall(f"{ATOM}entry"):
        entry_url = compact_text(entry.findtext(f"{ATOM}id"))
        source_id = source_id_from_url(entry_url)
        authors = [compact_text(author.findtext(f"{ATOM}name")) for author in entry.findall(f"{ATOM}author")]
        categories = [category.attrib.get("term", "") for category in entry.findall(f"{ATOM}category")]
        primary = entry.find(f"{ARXIV}primary_category")
        doi = compact_text(entry.findtext(f"{ARXIV}doi")) or None
        journal_reference = compact_text(entry.findtext(f"{ARXIV}journal_ref")) or None
        comment = compact_text(entry.findtext(f"{ARXIV}comment")) or None
        publication_venue, venue_evidence = resolve_publication_venue(journal_reference, comment, doi)
        published = compact_text(entry.findtext(f"{ATOM}published"))
        updated = compact_text(entry.findtext(f"{ATOM}updated"))
        if not published or not updated:
            continue
        papers.append(
            {
                "sourceId": source_id,
                "title": compact_text(entry.findtext(f"{ATOM}title")),
                "authors": [author for author in authors if author],
                "abstract": compact_text(entry.findtext(f"{ATOM}summary")),
                "published": published,
                "updated": updated,
                "paperUrl": https_arxiv_url(source_id),
                "doi": doi,
                "journalReference": journal_reference,
                "comment": comment,
                "publicationVenue": publication_venue,
                "venueEvidence": venue_evidence,
                "primaryCategory": primary.attrib.get("term") if primary is not None else None,
                "categories": sorted(set(filter(None, categories))),
                "matchedQueries": [query_name],
            }
        )
    return papers


def fetch_feed(query: str, max_results: int) -> str:
    parameters = urllib.parse.urlencode(
        {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
    )
    request = urllib.request.Request(
        f"https://export.arxiv.org/api/query?{parameters}",
        headers={"User-Agent": USER_AGENT, "Accept": "application/atom+xml"},
    )
    last_error = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=45) as response:
                return response.read().decode("utf-8")
        except Exception as error:  # Network failures should be reported with the query name.
            last_error = error
            if attempt < 2:
                time.sleep(2 ** attempt)
    raise RuntimeError(f"arXiv request failed after 3 attempts: {last_error}")


def existing_records(path: Path) -> tuple[set[str], set[str]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    source_ids = {
        paper.get("source", {}).get("id")
        for paper in data.get("papers", [])
        if paper.get("source", {}).get("id")
    }
    titles = {
        normalized_title(paper["title"])
        for paper in data.get("papers", [])
        if isinstance(paper.get("title"), str)
    }
    return source_ids, titles


def discover(
    config: dict,
    existing_ids: set[str],
    existing_titles: set[str],
    now: datetime,
) -> tuple[list[dict], list[dict]]:
    cutoff = now - timedelta(days=int(config["lookbackDays"]))
    candidates: dict[str, dict] = {}
    errors = []
    successful_queries = 0

    for query in config["queries"]:
        try:
            feed = fetch_feed(query["query"], int(config["maxResultsPerQuery"]))
            successful_queries += 1
            entries = parse_feed(feed, query["name"])
        except Exception as error:
            errors.append({"query": query["name"], "error": str(error)})
            continue

        for paper in entries:
            published_date = parse_datetime(paper["published"])
            if (
                published_date < cutoff
                or paper["sourceId"] in existing_ids
                or normalized_title(paper["title"]) in existing_titles
            ):
                continue
            if paper["sourceId"] in candidates:
                matches = candidates[paper["sourceId"]]["matchedQueries"]
                matches.extend(paper["matchedQueries"])
                candidates[paper["sourceId"]]["matchedQueries"] = sorted(set(matches))
            else:
                candidates[paper["sourceId"]] = paper

    if successful_queries == 0:
        raise RuntimeError(f"All arXiv queries failed: {errors}")

    ordered = sorted(candidates.values(), key=lambda paper: (paper["published"], paper["sourceId"]), reverse=True)
    ordered = ordered[: int(config.get("maxCandidates", 60))]
    return ordered, errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("automation/config.json"))
    parser.add_argument("--existing", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--output", type=Path, default=Path("automation/candidates.json"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    now = datetime.now(timezone.utc)
    existing_ids, existing_titles = existing_records(args.existing)
    candidates, errors = discover(config, existing_ids, existing_titles, now)
    output = {
        "schemaVersion": 1,
        "generatedAt": now.isoformat(timespec="seconds"),
        "lookbackDays": config["lookbackDays"],
        "candidateCount": len(candidates),
        "errors": errors,
        "candidates": candidates,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Discovered {len(candidates)} new candidate papers; {len(errors)} queries reported errors.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"paper discovery failed: {error}", file=sys.stderr)
        raise SystemExit(1)
