#!/usr/bin/env python3
"""Merge evidence-backed spatial datasets into the dataset catalogue."""

from __future__ import annotations

import json
from pathlib import Path


BACKFILL_DIR = Path(__file__).resolve().parent
ROOT = BACKFILL_DIR.parents[1]
CURATION_PATH = BACKFILL_DIR / "spatial-datasets.json"
DATASETS_PATH = ROOT / "data/datasets.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    curation = load(CURATION_PATH)
    current = load(DATASETS_PATH)
    ids = {dataset["id"] for dataset in current["datasets"]}
    added = 0
    for entry in curation["datasets"]:
        if entry["id"] in ids:
            continue
        current["datasets"].append({
            "id": entry["id"],
            "name": entry["name"],
            "description": entry["description"],
            "scale": entry["scale"],
            "areas": ["spatial-audio"],
            "taxonomy": {
                "tasks": entry["tasks"],
                "effects": entry["effects"],
                "contentTypes": entry["contentTypes"],
                "evidence": [entry["evidence"]],
            },
            "access": {"status": entry["accessStatus"], "evidenceUrl": entry["evidence"]},
            "license": entry["license"],
            "relations": {"papers": entry["papers"], "projects": entry["projects"]},
            "lastVerified": curation["verifiedAt"],
            "links": entry["links"],
        })
        ids.add(entry["id"])
        added += 1

    current["datasets"].sort(key=lambda dataset: dataset["name"].casefold())
    current["updatedAt"] = curation["verifiedAt"]
    DATASETS_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} spatial datasets; catalogue now contains {len(current['datasets'])} datasets.")


if __name__ == "__main__":
    main()
