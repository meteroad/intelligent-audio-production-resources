#!/usr/bin/env python3
"""Fetch current GitHub metadata for verified intelligent-audio projects."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import Request, urlopen


BACKFILL_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = BACKFILL_DIR.parents[1]
PAPERS_PATH = REPOSITORY_ROOT / "data/papers.json"

ADDITIONAL_REPOSITORIES = {
    "csteinmetz1/dasp-pytorch",
    "DiffAPF/torchcomp",
    "f90/Mix-Wave-U-Net",
    "int0thewind/s4-dynamic-range-compressor",
    "mcomunita/tonetwist-afx-dataset",
    "mhrice/RemFx",
    "sh-lee97/grafx-prune",
    "ytsrt66589/diffFx-pytorch",
    "zys711/Diff2Mix",
}


def source_repositories() -> set[str]:
    papers = json.loads(PAPERS_PATH.read_text(encoding="utf-8"))["papers"]
    repositories = set(ADDITIONAL_REPOSITORIES)
    for paper in papers:
        for link in paper["links"]:
            parsed = urlparse(link["url"])
            if link["label"] == "source" and parsed.netloc.lower() == "github.com":
                path = parsed.path.strip("/").removesuffix(".git")
                if len(path.split("/")) == 2:
                    repositories.add(path)
    return repositories


LICENSE_FILENAMES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING")


def fetch_text(url: str) -> str | None:
    request = Request(
        url,
        headers={
            "User-Agent": "IntelligentAudioProductionIndex/1.0",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except HTTPError as error:
        if error.code == 404:
            return None
        raise


def detect_license(text: str) -> str:
    normalized = " ".join(text.casefold().split())
    primary = normalized[:3000]
    if "permission is hereby granted, free of charge" in primary:
        return "MIT"
    if "apache license version 2.0" in primary:
        return "Apache-2.0"
    if "gnu affero general public license" in primary:
        return "AGPL"
    if "gnu lesser general public license" in primary:
        return "LGPL"
    if "gnu general public license" in primary:
        return "GPL"
    if "redistribution and use in source and binary forms" in primary:
        return "BSD"
    if "creative commons attribution-noncommercial-sharealike 4.0" in primary:
        return "CC-BY-NC-SA-4.0"
    if "mozilla public license version 2.0" in primary:
        return "MPL-2.0"
    if "the unlicense" in primary:
        return "Unlicense"
    return "Custom/other"


def fetch_repository(repository: str) -> dict:
    license_name = None
    license_url = None
    for filename in LICENSE_FILENAMES:
        raw_url = f"https://raw.githubusercontent.com/{repository}/HEAD/{filename}"
        text = fetch_text(raw_url)
        if text is not None:
            license_name = detect_license(text)
            license_url = f"https://github.com/{repository}/blob/HEAD/{filename}"
            break
    return {
        "fullName": repository,
        "url": f"https://github.com/{repository}",
        "license": license_name,
        "licenseUrl": license_url,
    }


def main() -> None:
    repositories = sorted(source_repositories(), key=str.casefold)
    metadata = [fetch_repository(repository) for repository in repositories]
    output = BACKFILL_DIR / "project-github-metadata.json"
    output.write_text(json.dumps({"projects": metadata}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Fetched {len(metadata)} GitHub projects into {output}.")


if __name__ == "__main__":
    main()
