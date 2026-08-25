#!/usr/bin/env python3
"""Fetch authoritative arXiv metadata for the curated historical backfill."""

from __future__ import annotations

import json
import sys
from pathlib import Path


AUTOMATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTOMATION_DIR))

import discover_papers  # noqa: E402


ARXIV_IDS = [
    "2001.04643",
    "2010.10291",
    "2012.03216",
    "2103.08709",
    "2105.04752",
    "2105.13940",
    "2110.03691",
    "2110.06525",
    "2202.01664",
    "2202.08520",
    "2207.08759",
    "2208.11428",
    "2211.02247",
    "2303.08610",
    "2306.00860",
    "2306.01332",
    "2308.15422",
    "2308.16177",
    "2310.11364",
    "2310.11781",
    "2402.11216",
    "2403.08559",
    "2403.16331",
    "2404.00082",
    "2404.07970",
    "2406.01049",
    "2407.08889",
    "2407.10646",
    "2407.16691",
    "2408.03204",
    "2409.08723",
    "2409.18847",
    "2410.21233",
    "2411.14972",
    "2502.11668",
    "2502.14405",
    "2504.14735",
    "2505.11315",
    "2506.16889",
    "2507.02273",
    "2508.03448",
    "2509.15948",
    "2511.08040",
    "2511.20380",
    "2512.01559",
    "2601.04867",
    "2606.22005",
    "2607.19645",
    "2608.00656",
    "2608.00667",
    "2608.05442",
    "2608.05506",
    "2608.05513",
    "2608.10573",
]


def main() -> None:
    query = " OR ".join(f"id:{identifier}" for identifier in ARXIV_IDS)
    feed = discover_papers.fetch_feed(query, len(ARXIV_IDS))
    papers = discover_papers.parse_feed(feed, "historical-backfill")
    found = {paper["sourceId"].removeprefix("arxiv:") for paper in papers}
    missing = sorted(set(ARXIV_IDS) - found)
    if missing:
        raise RuntimeError(f"arXiv did not return metadata for: {', '.join(missing)}")

    output = Path(__file__).with_name("historical-arxiv-metadata.json")
    output.write_text(json.dumps({"papers": papers}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Fetched {len(papers)} arXiv records into {output}.")


if __name__ == "__main__":
    main()
