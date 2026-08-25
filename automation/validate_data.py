#!/usr/bin/env python3
"""Validate website data before it can be proposed for publication."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


ALLOWED_AREAS = {
    "audio-effects",
    "differentiable-processing",
    "representation",
    "mixing",
    "mastering",
    "evaluation",
    "spatial-audio",
}
ALLOWED_LINK_LABELS = {"paper", "project", "source", "checkpoint", "doi"}
ALLOWED_RESOURCE_KINDS = {"bibliography"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_localized(value: object, context: str) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    for language in ("en", "zh"):
        require(isinstance(value.get(language), str) and value[language].strip(), f"{context}.{language} is required")


def validate_areas(areas: object, context: str) -> None:
    require(isinstance(areas, list) and areas, f"{context} must have at least one area")
    require(len(areas) == len(set(areas)), f"{context} contains duplicate areas")
    require(set(areas).issubset(ALLOWED_AREAS), f"{context} contains unknown areas")


def validate_links(links: object, context: str) -> None:
    require(isinstance(links, list) and links, f"{context} must have at least one link")
    for index, link in enumerate(links):
        require(link.get("label") in ALLOWED_LINK_LABELS, f"{context}[{index}] has an unknown label")
        parsed = urlparse(link.get("url", ""))
        require(parsed.scheme == "https" and parsed.netloc, f"{context}[{index}] must use a valid HTTPS URL")


def validate_projects(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schemaVersion") == 2, "projects.json schemaVersion must be 2")
    projects = data.get("projects")
    require(isinstance(projects, list), "projects must be a list")
    ids = set()
    for project in projects:
        project_id = project.get("id")
        require(isinstance(project_id, str) and project_id not in ids, f"duplicate or invalid project id: {project_id}")
        ids.add(project_id)
        require(isinstance(project.get("name"), str) and project["name"].strip(), f"{project_id}.name is required")
        validate_localized(project.get("description"), f"{project_id}.description")
        validate_localized(project.get("license"), f"{project_id}.license")
        validate_areas(project.get("areas"), f"{project_id}.areas")
        validate_links(project.get("links"), f"{project_id}.links")
        require(isinstance(project.get("lastVerified"), str), f"{project_id}.lastVerified is required")
    return len(projects)


def validate_papers(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schemaVersion") == 1, "papers.json schemaVersion must be 1")
    papers = data.get("papers")
    require(isinstance(papers, list), "papers must be a list")
    ids = set()
    sources = set()
    for paper in papers:
        paper_id = paper.get("id")
        require(isinstance(paper_id, str) and paper_id not in ids, f"duplicate or invalid paper id: {paper_id}")
        ids.add(paper_id)
        source = paper.get("source", {})
        source_key = (source.get("type"), source.get("id"))
        require(all(isinstance(value, str) and value for value in source_key), f"{paper_id}.source is invalid")
        require(source_key not in sources, f"duplicate paper source: {source_key}")
        sources.add(source_key)
        short_name = paper.get("shortName")
        if short_name is not None:
            require(isinstance(short_name, str) and 1 <= len(short_name.strip()) <= 40, f"{paper_id}.shortName is invalid")
        require(isinstance(paper.get("title"), str) and paper["title"].strip(), f"{paper_id}.title is required")
        require(isinstance(paper.get("authors"), list) and all(isinstance(author, str) and author for author in paper["authors"]), f"{paper_id}.authors is invalid")
        require(isinstance(paper.get("year"), int), f"{paper_id}.year must be an integer")
        require(isinstance(paper.get("published"), str) and paper["published"], f"{paper_id}.published is required")
        require(isinstance(paper.get("venue"), str) and paper["venue"], f"{paper_id}.venue is required")
        validate_areas(paper.get("areas"), f"{paper_id}.areas")
        validate_localized(paper.get("summary"), f"{paper_id}.summary")
        validate_links(paper.get("links"), f"{paper_id}.links")
        require(
            any(link.get("label") in {"paper", "doi"} for link in paper["links"]),
            f"{paper_id}.links must include a paper or DOI link",
        )
        require(paper.get("curation") in {"manual", "agent"}, f"{paper_id}.curation is invalid")
        require(isinstance(paper.get("lastVerified"), str), f"{paper_id}.lastVerified is required")
    return len(papers)


def validate_resources(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(data.get("schemaVersion") == 1, "resources.json schemaVersion must be 1")
    resources = data.get("resources")
    require(isinstance(resources, list), "resources must be a list")
    ids = set()
    for resource in resources:
        resource_id = resource.get("id")
        require(isinstance(resource_id, str) and resource_id not in ids, f"duplicate or invalid resource id: {resource_id}")
        ids.add(resource_id)
        require(isinstance(resource.get("name"), str) and resource["name"].strip(), f"{resource_id}.name is required")
        require(resource.get("kind") in ALLOWED_RESOURCE_KINDS, f"{resource_id}.kind is invalid")
        validate_localized(resource.get("description"), f"{resource_id}.description")
        validate_areas(resource.get("areas"), f"{resource_id}.areas")
        validate_links(resource.get("links"), f"{resource_id}.links")
        require(isinstance(resource.get("lastVerified"), str), f"{resource_id}.lastVerified is required")
    return len(resources)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projects", type=Path, default=Path("data/projects.json"))
    parser.add_argument("--papers", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--resources", type=Path, default=Path("data/resources.json"))
    args = parser.parse_args()
    project_count = validate_projects(args.projects)
    paper_count = validate_papers(args.papers)
    resource_count = validate_resources(args.resources)
    print(f"Validated {project_count} projects, {paper_count} papers, and {resource_count} reference resources.")


if __name__ == "__main__":
    main()
