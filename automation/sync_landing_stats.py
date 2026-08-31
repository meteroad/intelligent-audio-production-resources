#!/usr/bin/env python3
"""Keep website and README catalogue counts aligned with data files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


COUNT_IDS = {
    "projects": "hero-project-count",
    "datasets": "hero-dataset-count",
    "papers": "hero-paper-count",
}


def record_count(path: Path, collection: str) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    records = data.get(collection)
    if not isinstance(records, list):
        raise ValueError(f"{path} does not contain a {collection} list")
    return len(records)


def sync_counts(html: str, counts: dict[str, int]) -> str:
    updated = html
    for collection, element_id in COUNT_IDS.items():
        pattern = rf'(<strong id="{re.escape(element_id)}">)\d+(</strong>)'
        updated, replacements = re.subn(
            pattern,
            lambda match: f"{match.group(1)}{counts[collection]}{match.group(2)}",
            updated,
        )
        if replacements != 1:
            raise ValueError(f"Expected exactly one #{element_id} count in index.html")
    return updated


def sync_readme_counts(readme: str, counts: dict[str, int]) -> str:
    pattern = (
        r"\*\*\d+ papers · \d+ verified projects · \d+ datasets · "
        r"\d+ reference collections\*\*"
    )
    replacement = (
        f"**{counts['papers']} papers · {counts['projects']} verified projects · "
        f"{counts['datasets']} datasets · {counts['resources']} reference collections**"
    )
    updated, replacements = re.subn(pattern, replacement, readme)
    if replacements != 1:
        raise ValueError("Expected exactly one catalogue count line in README.md")
    return updated


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projects", type=Path, default=Path("data/projects.json"))
    parser.add_argument("--datasets", type=Path, default=Path("data/datasets.json"))
    parser.add_argument("--papers", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--resources", type=Path, default=Path("data/resources.json"))
    parser.add_argument("--html", type=Path, default=Path("index.html"))
    parser.add_argument("--readme", type=Path, default=Path("README.md"))
    args = parser.parse_args()

    counts = {
        "projects": record_count(args.projects, "projects"),
        "datasets": record_count(args.datasets, "datasets"),
        "papers": record_count(args.papers, "papers"),
        "resources": record_count(args.resources, "resources"),
    }
    html = args.html.read_text(encoding="utf-8")
    args.html.write_text(sync_counts(html, counts), encoding="utf-8")
    readme = args.readme.read_text(encoding="utf-8")
    args.readme.write_text(sync_readme_counts(readme, counts), encoding="utf-8")
    print(
        "Synchronized catalogue counts: "
        f"{counts['projects']} projects, {counts['datasets']} datasets, "
        f"{counts['papers']} papers, {counts['resources']} reference resources."
    )


if __name__ == "__main__":
    main()
