#!/usr/bin/env python3
"""Merge reviewed spatial-production repositories into the project catalogue."""

from __future__ import annotations

import json
import re
from pathlib import Path


BACKFILL_DIR = Path(__file__).resolve().parent
ROOT = BACKFILL_DIR.parents[1]
METADATA_PATH = BACKFILL_DIR / "spatial-project-github-metadata.json"
CURATION_PATH = BACKFILL_DIR / "spatial-project-curation.json"
PROJECTS_PATH = ROOT / "data/projects.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def project_id(repository: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", repository.casefold()).strip("-")


def license_record(repository: str, metadata: dict) -> dict:
    detected = metadata.get("license")
    evidence = metadata.get("licenseUrl")
    if detected in {"MIT", "Apache-2.0"}:
        return {"en": detected, "zh": detected, "status": "identified", "spdx": detected, "evidenceUrl": evidence}
    if repository == "videolabs/libspatialaudio":
        return {"en": "LGPL-2.1-or-later or commercial license", "zh": "LGPL-2.1-or-later 或商业许可证", "status": "identified", "spdx": "LGPL-2.1-or-later", "evidenceUrl": evidence}
    if detected:
        labels = {
            "GPL": "GNU GPL terms; see repository license text",
            "AGPL": "GNU AGPL terms; see repository license text",
            "Custom/other": "Custom or non-standard terms; see repository license text",
        }
        zh = {
            "GPL": "GNU GPL 条款；详见仓库许可证原文",
            "AGPL": "GNU AGPL 条款；详见仓库许可证原文",
            "Custom/other": "自定义或非标准条款；详见仓库许可证原文",
        }
        return {"en": labels.get(detected, detected), "zh": zh.get(detected, detected), "status": "custom", "spdx": None, "evidenceUrl": evidence}
    return {"en": "No repository license file verified", "zh": "未核验到仓库许可证文件", "status": "not-verified", "spdx": None, "evidenceUrl": None}


def availability(source_url: str, repository: str, kind: str | None) -> dict:
    readme = f"https://github.com/{repository}/blob/HEAD/README.md"
    toolkit = kind == "toolkit"
    return {
        "source": {"status": "linked", "evidence": [source_url]},
        "checkpoint": {"status": "not-applicable" if toolkit else "not-reviewed", "evidence": []},
        "inference": {"status": "documented" if toolkit else "not-reviewed", "evidence": [readme] if toolkit else []},
        "training": {"status": "not-applicable" if toolkit else "not-reviewed", "evidence": []},
        "dataset": {"status": "not-applicable" if toolkit else "not-reviewed", "evidence": []},
    }


def main() -> None:
    metadata = {item["fullName"]: item for item in load(METADATA_PATH)["projects"]}
    curation_data = load(CURATION_PATH)
    curated = curation_data["projects"]
    if set(metadata) != set(curated):
        raise ValueError("Spatial project metadata and curation identifiers differ")

    current = load(PROJECTS_PATH)
    ids = {project["id"] for project in current["projects"]}
    added = 0
    for repository, entry in curated.items():
        identifier = project_id(repository)
        if identifier in ids:
            continue
        source_url = entry.get("sourceUrl", metadata[repository]["url"])
        taxonomy_evidence = entry.get("evidenceUrl", f"https://github.com/{repository}/blob/HEAD/README.md")
        paper_ids = entry["paperIds"]
        current["projects"].append({
            "id": identifier,
            "name": entry["name"],
            "description": entry["description"],
            "areas": entry["areas"],
            "taxonomy": {
                "tasks": entry["tasks"],
                "effects": entry["effects"],
                "reviewStatus": "reviewed",
                "evidence": [taxonomy_evidence],
            },
            "license": license_record(repository, metadata[repository]),
            "availability": availability(source_url, repository, entry.get("kind")),
            "relations": {
                "paperIds": paper_ids,
                "reviewStatus": "exact-link-match" if paper_ids else "not-reviewed",
            },
            "lastVerified": curation_data["verifiedAt"],
            "links": [{"label": "source", "url": source_url}],
        })
        ids.add(identifier)
        added += 1

    current["projects"].sort(key=lambda project: project["name"].casefold())
    current["updatedAt"] = curation_data["verifiedAt"]
    PROJECTS_PATH.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Added {added} spatial projects; catalogue now contains {len(current['projects'])} projects.")


if __name__ == "__main__":
    main()
