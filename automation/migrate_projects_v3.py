#!/usr/bin/env python3
"""Upgrade or downgrade the project catalogue without inventing evidence."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from urllib.parse import urlsplit


V2_PROJECT_KEYS = {
    "id",
    "name",
    "description",
    "areas",
    "license",
    "lastVerified",
    "links",
}
RELATION_LINK_LABELS = {"project", "source", "checkpoint"}
AVAILABILITY_LINK_LABELS = {
    "source": "source",
    "checkpoint": "checkpoint",
}
LICENSE_SPDX = {
    "Apache-2.0": "Apache-2.0",
    "CC-BY-NC-SA-4.0": "CC-BY-NC-SA-4.0",
    "MIT": "MIT",
}


def canonical_url(url: str) -> str:
    """Return a conservative URL key for exact cross-record matching."""

    parsed = urlsplit(url)
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.rstrip("/")
    if host == "github.com":
        path = path.lower()
        if path.endswith(".git"):
            path = path[:-4]
    return f"{host}{path}"


def license_metadata(legacy: dict[str, str]) -> dict[str, object]:
    name = legacy["en"]
    if name == "No license file verified":
        status = "not-verified"
    elif name == "Custom/other; see repository terms":
        status = "custom"
    else:
        status = "identified"

    return {
        "en": legacy["en"],
        "zh": legacy["zh"],
        "status": status,
        "spdx": LICENSE_SPDX.get(name),
        "evidenceUrl": None,
    }


def availability_from_links(links: list[dict[str, str]]) -> dict[str, dict[str, object]]:
    by_label: dict[str, list[str]] = {}
    for link in links:
        by_label.setdefault(link["label"], []).append(link["url"])

    availability: dict[str, dict[str, object]] = {}
    for capability in ("source", "checkpoint", "inference", "training", "dataset"):
        label = AVAILABILITY_LINK_LABELS.get(capability)
        evidence = sorted(set(by_label.get(label, []))) if label else []
        availability[capability] = {
            "status": "linked" if evidence else "not-reviewed",
            "evidence": evidence,
        }
    return availability


def paper_link_index(papers: list[dict[str, object]]) -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}
    for paper in papers:
        for link in paper.get("links", []):
            if link.get("label") not in RELATION_LINK_LABELS:
                continue
            index.setdefault(canonical_url(link["url"]), set()).add(paper["id"])
    return index


def matched_paper_ids(project: dict[str, object], link_index: dict[str, set[str]]) -> list[str]:
    matches: set[str] = set()
    for link in project["links"]:
        if link["label"] in RELATION_LINK_LABELS:
            matches.update(link_index.get(canonical_url(link["url"]), set()))
    return sorted(matches)


def upgrade_document(project_data: dict[str, object], paper_data: dict[str, object]) -> dict[str, object]:
    if project_data.get("schemaVersion") != 2:
        raise ValueError("upgrade input must use projects schemaVersion 2")
    if paper_data.get("schemaVersion") != 1:
        raise ValueError("paper catalogue must use schemaVersion 1")

    links_to_papers = paper_link_index(paper_data["papers"])
    migrated = []
    for project in project_data["projects"]:
        unexpected = set(project) - V2_PROJECT_KEYS
        missing = V2_PROJECT_KEYS - set(project)
        if unexpected or missing:
            raise ValueError(
                f"{project.get('id', '<unknown>')} does not match the v2 contract; "
                f"missing={sorted(missing)}, unexpected={sorted(unexpected)}"
            )

        links = copy.deepcopy(project["links"])
        paper_ids = matched_paper_ids(project, links_to_papers)
        migrated.append(
            {
                "id": project["id"],
                "name": project["name"],
                "description": copy.deepcopy(project["description"]),
                "areas": copy.deepcopy(project["areas"]),
                "taxonomy": {
                    "tasks": [],
                    "effects": [],
                    "reviewStatus": "not-reviewed",
                },
                "license": license_metadata(project["license"]),
                "availability": availability_from_links(links),
                "relations": {
                    "paperIds": paper_ids,
                    "reviewStatus": "exact-link-match" if paper_ids else "not-reviewed",
                },
                "lastVerified": project["lastVerified"],
                "links": links,
            }
        )

    updated_at = max((project["lastVerified"] for project in project_data["projects"]), default="")
    return {
        "schemaVersion": 3,
        "updatedAt": updated_at,
        "projects": migrated,
    }


def downgrade_document(project_data: dict[str, object]) -> dict[str, object]:
    if project_data.get("schemaVersion") != 3:
        raise ValueError("downgrade input must use projects schemaVersion 3")

    projects = []
    for project in project_data["projects"]:
        projects.append(
            {
                "id": project["id"],
                "name": project["name"],
                "description": copy.deepcopy(project["description"]),
                "areas": copy.deepcopy(project["areas"]),
                "license": {
                    "en": project["license"]["en"],
                    "zh": project["license"]["zh"],
                },
                "lastVerified": project["lastVerified"],
                "links": copy.deepcopy(project["links"]),
            }
        )
    return {"schemaVersion": 2, "projects": projects}


def write_json(path: Path, value: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=Path("data/projects.json"))
    parser.add_argument("--output", type=Path, default=Path("data/projects.json"))
    parser.add_argument("--papers", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--direction", choices=("upgrade", "downgrade"), default="upgrade")
    args = parser.parse_args()

    project_data = json.loads(args.input.read_text(encoding="utf-8"))
    if args.direction == "upgrade":
        paper_data = json.loads(args.papers.read_text(encoding="utf-8"))
        result = upgrade_document(project_data, paper_data)
    else:
        result = downgrade_document(project_data)
    write_json(args.output, result)
    print(f"Wrote projects schemaVersion {result['schemaVersion']} to {args.output}")


if __name__ == "__main__":
    main()
