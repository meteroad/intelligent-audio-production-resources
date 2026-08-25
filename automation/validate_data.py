#!/usr/bin/env python3
"""Validate website data before it can be proposed for publication."""

from __future__ import annotations

import argparse
import json
from datetime import date
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
ALLOWED_PROJECT_TASKS = {
    "effect-modeling",
    "parameter-estimation",
    "effect-control",
    "effect-transfer",
    "effect-removal",
    "representation-learning",
    "automatic-mixing",
    "mastering",
    "evaluation",
    "differentiable-processing",
}
ALLOWED_EFFECTS = {
    "gain",
    "equalization",
    "compression",
    "distortion",
    "reverberation",
    "delay",
    "modulation",
    "stereo",
    "filtering",
    "multi-effect",
    "other",
}
AVAILABILITY_CAPABILITIES = {"source", "checkpoint", "inference", "training", "dataset"}
AVAILABILITY_STATUSES = {
    "not-reviewed",
    "linked",
    "documented",
    "tested",
    "gated",
    "restricted",
    "not-found",
    "not-applicable",
}
EVIDENCE_REQUIRED_STATUSES = {"linked", "documented", "tested", "gated", "restricted"}
LICENSE_STATUSES = {"identified", "custom", "not-verified"}
RELATION_REVIEW_STATUSES = {"not-reviewed", "exact-link-match", "verified"}
RELATION_LINK_LABELS = {"project", "source", "checkpoint"}
PROJECT_V3_FIELDS = {
    "id",
    "name",
    "description",
    "areas",
    "taxonomy",
    "license",
    "availability",
    "relations",
    "lastVerified",
    "links",
}


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


def validate_date(value: object, context: str) -> None:
    require(isinstance(value, str), f"{context} must be an ISO date")
    try:
        date.fromisoformat(value)
    except ValueError as error:
        raise ValueError(f"{context} must be an ISO date") from error


def validate_https_url(value: object, context: str) -> None:
    parsed = urlparse(value if isinstance(value, str) else "")
    require(parsed.scheme == "https" and parsed.netloc, f"{context} must use a valid HTTPS URL")


def canonical_resource_url(url: str) -> str:
    parsed = urlparse(url)
    host = parsed.netloc.lower().removeprefix("www.")
    path = parsed.path.rstrip("/")
    if host == "github.com":
        path = path.lower()
        if path.endswith(".git"):
            path = path[:-4]
    return f"{host}{path}"


def validate_project_taxonomy(value: object, context: str) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    require(set(value) == {"tasks", "effects", "reviewStatus"}, f"{context} has invalid fields")
    tasks = value.get("tasks")
    effects = value.get("effects")
    require(isinstance(tasks, list) and len(tasks) == len(set(tasks)), f"{context}.tasks is invalid")
    require(set(tasks).issubset(ALLOWED_PROJECT_TASKS), f"{context}.tasks contains unknown values")
    require(isinstance(effects, list) and len(effects) == len(set(effects)), f"{context}.effects is invalid")
    require(set(effects).issubset(ALLOWED_EFFECTS), f"{context}.effects contains unknown values")
    require(value.get("reviewStatus") in {"not-reviewed", "reviewed"}, f"{context}.reviewStatus is invalid")
    if value["reviewStatus"] == "not-reviewed":
        require(not tasks and not effects, f"{context} cannot contain unreviewed taxonomy claims")


def validate_project_license(value: object, context: str) -> None:
    validate_localized(value, context)
    require(
        set(value) == {"en", "zh", "status", "spdx", "evidenceUrl"},
        f"{context} has invalid fields",
    )
    require(value.get("status") in LICENSE_STATUSES, f"{context}.status is invalid")
    require(value.get("spdx") is None or isinstance(value["spdx"], str), f"{context}.spdx is invalid")
    if isinstance(value["spdx"], str):
        require(value["spdx"].strip(), f"{context}.spdx cannot be empty")
    if value["status"] != "identified":
        require(value["spdx"] is None, f"{context}.spdx requires an identified license")
    evidence_url = value.get("evidenceUrl")
    if evidence_url is not None:
        validate_https_url(evidence_url, f"{context}.evidenceUrl")


def validate_project_availability(value: object, links: list[dict[str, str]], context: str) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    require(set(value) == AVAILABILITY_CAPABILITIES, f"{context} has invalid capabilities")
    for capability in sorted(AVAILABILITY_CAPABILITIES):
        entry = value[capability]
        entry_context = f"{context}.{capability}"
        require(isinstance(entry, dict), f"{entry_context} must be an object")
        require(set(entry) == {"status", "evidence"}, f"{entry_context} has invalid fields")
        status = entry.get("status")
        evidence = entry.get("evidence")
        require(status in AVAILABILITY_STATUSES, f"{entry_context}.status is invalid")
        require(isinstance(evidence, list), f"{entry_context}.evidence must be a list")
        require(len(evidence) == len(set(evidence)), f"{entry_context}.evidence contains duplicates")
        for index, url in enumerate(evidence):
            validate_https_url(url, f"{entry_context}.evidence[{index}]")
        if status in EVIDENCE_REQUIRED_STATUSES:
            require(evidence, f"{entry_context} requires evidence")
        if status == "not-reviewed":
            require(not evidence, f"{entry_context} cannot attach evidence before review")
        if status == "linked" and capability in {"source", "checkpoint"}:
            recorded = {link["url"] for link in links if link["label"] == capability}
            require(set(evidence).issubset(recorded), f"{entry_context} evidence is not a recorded {capability} link")


def validate_project_relations(
    value: object,
    paper_ids: set[str],
    project_links: list[dict[str, str]],
    paper_resource_urls: dict[str, set[str]],
    context: str,
) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    require(set(value) == {"paperIds", "reviewStatus"}, f"{context} has invalid fields")
    related_ids = value.get("paperIds")
    require(isinstance(related_ids, list), f"{context}.paperIds must be a list")
    require(len(related_ids) == len(set(related_ids)), f"{context}.paperIds contains duplicates")
    require(all(isinstance(item, str) and item for item in related_ids), f"{context}.paperIds is invalid")
    require(set(related_ids).issubset(paper_ids), f"{context}.paperIds contains unknown papers")
    review_status = value.get("reviewStatus")
    require(review_status in RELATION_REVIEW_STATUSES, f"{context}.reviewStatus is invalid")
    if review_status == "not-reviewed":
        require(not related_ids, f"{context} cannot contain unreviewed relations")
    if review_status == "exact-link-match":
        require(related_ids, f"{context} exact-link-match requires at least one paper")
        project_urls = {
            canonical_resource_url(link["url"])
            for link in project_links
            if link["label"] in RELATION_LINK_LABELS
        }
        for paper_id in related_ids:
            require(
                project_urls & paper_resource_urls.get(paper_id, set()),
                f"{context} has no exact resource URL match for {paper_id}",
            )


def validate_projects(
    path: Path,
    paper_ids: set[str] | None = None,
    paper_resource_urls: dict[str, set[str]] | None = None,
) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(set(data) == {"schemaVersion", "updatedAt", "projects"}, "projects.json has invalid top-level fields")
    require(data.get("schemaVersion") == 3, "projects.json schemaVersion must be 3")
    validate_date(data.get("updatedAt"), "projects.json.updatedAt")
    projects = data.get("projects")
    require(isinstance(projects, list), "projects must be a list")
    known_paper_ids = paper_ids or set()
    known_paper_urls = paper_resource_urls or {}
    ids = set()
    for project in projects:
        project_id = project.get("id")
        require(isinstance(project_id, str) and project_id not in ids, f"duplicate or invalid project id: {project_id}")
        ids.add(project_id)
        require(set(project) == PROJECT_V3_FIELDS, f"{project_id} has invalid fields")
        require(isinstance(project.get("name"), str) and project["name"].strip(), f"{project_id}.name is required")
        validate_localized(project.get("description"), f"{project_id}.description")
        validate_areas(project.get("areas"), f"{project_id}.areas")
        validate_project_taxonomy(project.get("taxonomy"), f"{project_id}.taxonomy")
        validate_project_license(project.get("license"), f"{project_id}.license")
        validate_links(project.get("links"), f"{project_id}.links")
        validate_project_availability(project.get("availability"), project["links"], f"{project_id}.availability")
        validate_project_relations(
            project.get("relations"),
            known_paper_ids,
            project["links"],
            known_paper_urls,
            f"{project_id}.relations",
        )
        validate_date(project.get("lastVerified"), f"{project_id}.lastVerified")
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
    paper_count = validate_papers(args.papers)
    paper_data = json.loads(args.papers.read_text(encoding="utf-8"))
    paper_ids = {paper["id"] for paper in paper_data["papers"]}
    paper_resource_urls = {
        paper["id"]: {
            canonical_resource_url(link["url"])
            for link in paper["links"]
            if link["label"] in RELATION_LINK_LABELS
        }
        for paper in paper_data["papers"]
    }
    project_count = validate_projects(args.projects, paper_ids, paper_resource_urls)
    resource_count = validate_resources(args.resources)
    print(f"Validated {project_count} projects, {paper_count} papers, and {resource_count} reference resources.")


if __name__ == "__main__":
    main()
