#!/usr/bin/env python3
"""Fetch authoritative arXiv metadata for the spatial-production backfill."""

from __future__ import annotations

import json
import sys
from pathlib import Path


AUTOMATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTOMATION_DIR))

import discover_papers  # noqa: E402


# The list is intentionally limited to generation, upmixing, rendering, and
# production-facing HRTF work. SELD-only and separation-only papers are out of scope.
ARXIV_IDS = [
    "1809.02587",
    "1812.04204",
    "2007.09902",
    "2104.06162",
    "2105.00708",
    "2106.10801",
    "2109.00748",
    "2111.08046",
    "2111.10882",
    "2111.11882",
    "2203.12053",
    "2204.02637",
    "2205.14807",
    "2207.03697",
    "2207.10967",
    "2210.15196",
    "2211.00878",
    "2211.02301",
    "2212.07000",
    "2302.02088",
    "2302.02809",
    "2306.05812",
    "2307.14650",
    "2308.09514",
    "2309.08290",
    "2310.13430",
    "2311.07630",
    "2402.17907",
    "2404.15107",
    "2405.13428",
    "2406.06612",
    "2410.10676",
    "2410.11299",
    "2410.14945",
    "2501.02786",
    "2502.18952",
    "2504.14906",
    "2504.20630",
    "2506.12199",
    "2507.07318",
    "2507.05053",
    "2601.12950",
]


def main() -> None:
    query = " OR ".join(f"id:{identifier}" for identifier in ARXIV_IDS)
    feed = discover_papers.fetch_feed(query, len(ARXIV_IDS))
    papers = discover_papers.parse_feed(feed, "spatial-production-backfill")
    found = {paper["sourceId"].removeprefix("arxiv:") for paper in papers}
    missing = sorted(set(ARXIV_IDS) - found)
    if missing:
        raise RuntimeError(f"arXiv did not return metadata for: {', '.join(missing)}")

    output = Path(__file__).with_name("spatial-arxiv-metadata.json")
    output.write_text(json.dumps({"papers": papers}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Fetched {len(papers)} spatial-production records into {output}.")


if __name__ == "__main__":
    main()
