#!/usr/bin/env python3
"""Build the verified project index from GitHub evidence and curation."""

from __future__ import annotations

import json
import re
from pathlib import Path


BACKFILL_DIR = Path(__file__).resolve().parent
REPOSITORY_ROOT = BACKFILL_DIR.parents[1]
METADATA_PATH = BACKFILL_DIR / "project-github-metadata.json"
CURATION_PATH = BACKFILL_DIR / "project-curation.json"
TAXONOMY_PATH = BACKFILL_DIR / "taxonomy-tags.json"
PROJECTS_PATH = REPOSITORY_ROOT / "data/projects.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def project_id(repository: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", repository.casefold()).strip("-")


def localized_license(identifier: str | None) -> dict[str, str]:
    if identifier is None:
        return {
            "en": "No license file verified",
            "zh": "未核验到许可证文件",
        }
    if identifier == "Custom/other":
        return {
            "en": "Custom/other; see repository terms",
            "zh": "自定义或其他条款；请查看仓库",
        }
    return {"en": identifier, "zh": identifier}


def main() -> None:
    metadata = {project["fullName"]: project for project in load_json(METADATA_PATH)["projects"]}
    curation_data = load_json(CURATION_PATH)
    curated = curation_data["projects"]
    method_tags = load_json(TAXONOMY_PATH)["projects"]
    if set(metadata) != set(curated):
        missing_curation = sorted(set(metadata) - set(curated))
        missing_metadata = sorted(set(curated) - set(metadata))
        raise ValueError(
            f"Project sets differ; missing curation={missing_curation}, missing metadata={missing_metadata}"
        )

    projects = []
    for repository, entry in curated.items():
        evidence = metadata[repository]
        links = [{"label": "source", "url": evidence["url"]}]
        links.extend(entry.get("extraLinks", []))
        projects.append(
            {
                "id": project_id(repository),
                "name": entry["name"],
                "description": entry["description"],
                "areas": list(
                    dict.fromkeys(
                        [
                            *entry["areas"],
                            *[area for area, repositories in method_tags.items() if repository in repositories],
                        ]
                    )
                ),
                "license": localized_license(evidence["license"]),
                "lastVerified": curation_data["verifiedAt"],
                "links": links,
            }
        )

    projects.sort(key=lambda project: project["name"].casefold())
    output = {"schemaVersion": 2, "projects": projects}
    PROJECTS_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Built {len(projects)} verified project records.")


if __name__ == "__main__":
    main()
