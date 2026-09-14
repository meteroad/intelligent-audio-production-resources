#!/usr/bin/env python3
"""Discover recent candidate papers from the public arXiv API."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

from publication_metadata import resolve_publication_venue


ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
USER_AGENT = "IntelligentAudioProductionPaperScout/1.0 (https://meteroad.github.io/intelligent-audio-production-resources/)"
API_ROOT = "https://export.arxiv.org/api/query"
RSS_ROOT = "https://rss.arxiv.org/rss"
MIN_REQUEST_INTERVAL = 3.1


def compact_text(value: str | None) -> str:
    return " ".join((value or "").split())


def display_title(value: str | None) -> str:
    title = compact_text(value)
    return re.sub(r"\$?(\d+)\^\{?\\circ\}?\$?", r"\1°", title)


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
                "title": display_title(entry.findtext(f"{ATOM}title")),
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


def split_creators(value: str) -> list[str]:
    creators = []
    start = 0
    depth = 0
    for index, character in enumerate(value):
        if character == "(":
            depth += 1
        elif character == ")":
            depth = max(0, depth - 1)
        elif character == "," and depth == 0:
            creators.append(value[start:index].strip())
            start = index + 1
    creators.append(value[start:].strip())
    return [creator for creator in creators if creator]


def parse_rss(xml_text: str, category: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    papers = []
    for item in root.findall("./channel/item"):
        announce_type = compact_text(item.findtext(f"{ARXIV}announce_type")).casefold()
        if announce_type not in {"new", "cross"}:
            continue
        entry_url = compact_text(item.findtext("link"))
        if not entry_url:
            continue
        description = compact_text(item.findtext("description"))
        abstract = description.split("Abstract:", 1)[-1].strip() if "Abstract:" in description else description
        creator = compact_text(item.findtext("{http://purl.org/dc/elements/1.1/}creator"))
        categories = sorted(set(filter(None, (compact_text(node.text) for node in item.findall("category")))))
        published_at = parsedate_to_datetime(compact_text(item.findtext("pubDate"))).astimezone(timezone.utc)
        source_id = source_id_from_url(entry_url)
        papers.append(
            {
                "sourceId": source_id,
                "title": display_title(item.findtext("title")),
                "authors": split_creators(creator),
                "abstract": abstract,
                "published": published_at.isoformat().replace("+00:00", "Z"),
                "updated": published_at.isoformat().replace("+00:00", "Z"),
                "paperUrl": https_arxiv_url(source_id),
                "doi": None,
                "journalReference": None,
                "comment": None,
                "publicationVenue": None,
                "venueEvidence": None,
                "primaryCategory": categories[0] if categories else category,
                "categories": categories or [category],
                "matchedQueries": [f"rss:{category}"],
            }
        )
    return papers


class ArxivRateLimitError(RuntimeError):
    pass


def validate_response(text: str) -> str:
    if compact_text(text).casefold().startswith("rate exceeded"):
        raise ArxivRateLimitError("arXiv rate limit exceeded")
    return text


class ArxivClient:
    def __init__(self, sleep=time.sleep, clock=time.monotonic, opener=urllib.request.urlopen):
        self.sleep = sleep
        self.clock = clock
        self.opener = opener
        self.last_request_at: float | None = None

    def _pace(self) -> None:
        if self.last_request_at is not None:
            wait = MIN_REQUEST_INTERVAL - (self.clock() - self.last_request_at)
            if wait > 0:
                self.sleep(wait)
        self.last_request_at = self.clock()

    def get(self, url: str, accept: str) -> str:
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept})
        last_error: Exception | None = None
        for retry_delay in (15, 60, None):
            self._pace()
            try:
                with self.opener(request, timeout=30) as response:
                    return validate_response(response.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                last_error = ArxivRateLimitError(f"arXiv rate limit exceeded (HTTP {error.code})") if error.code == 429 else error
            except Exception as error:  # Network failures should remain visible in the review artifact.
                last_error = error
            if retry_delay is not None:
                self.sleep(retry_delay)
        if isinstance(last_error, ArxivRateLimitError):
            raise last_error
        raise RuntimeError(f"arXiv request failed after 3 attempts: {last_error}")

    def fetch_feed(self, query: str, max_results: int) -> str:
        parameters = urllib.parse.urlencode(
            {
                "search_query": query,
                "start": 0,
                "max_results": max_results,
                "sortBy": "submittedDate",
                "sortOrder": "descending",
            }
        )
        return self.get(f"{API_ROOT}?{parameters}", "application/atom+xml")

    def fetch_rss(self, category: str) -> str:
        return self.get(f"{RSS_ROOT}/{urllib.parse.quote(category, safe='.')}", "application/rss+xml")


def fetch_feed(query: str, max_results: int) -> str:
    return ArxivClient().fetch_feed(query, max_results)


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
    client: ArxivClient | None = None,
) -> tuple[list[dict], list[dict]]:
    cutoff = now - timedelta(days=int(config["lookbackDays"]))
    candidates: dict[str, dict] = {}
    errors = []
    successful_queries = 0
    consecutive_errors = 0
    api_interrupted = False
    client = client or ArxivClient()

    def add_entries(entries: list[dict]) -> None:
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

    for query in config["queries"]:
        try:
            feed = client.fetch_feed(query["query"], int(config["maxResultsPerQuery"]))
            successful_queries += 1
            consecutive_errors = 0
            entries = parse_feed(feed, query["name"])
        except Exception as error:
            errors.append({"query": query["name"], "error": str(error)})
            consecutive_errors += 1
            if isinstance(error, ArxivRateLimitError) or consecutive_errors >= 2:
                api_interrupted = True
                break
            continue
        add_entries(entries)

    successful_rss = 0
    if api_interrupted or successful_queries == 0:
        for category in config.get("rssCategories", ["eess.AS", "cs.SD"]):
            try:
                entries = parse_rss(client.fetch_rss(category), category)
                successful_rss += 1
                add_entries(entries)
            except Exception as error:
                errors.append({"query": f"rss:{category}", "error": str(error)})

    if successful_queries == 0 and successful_rss == 0:
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
