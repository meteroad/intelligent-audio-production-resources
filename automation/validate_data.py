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
    "symbolic-performance",
    "production-program",
}
ALLOWED_LINK_LABELS = {"paper", "project", "source", "checkpoint", "doi"}
ALLOWED_DATASET_LINK_LABELS = {"dataset", "paper", "project", "source", "doi"}
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
    "spatial-generation",
    "spatial-mixing",
    "spatial-rendering",
    "hrtf-personalization",
    "spatial-evaluation",
    "symbolic-performance",
    "performance-rendering",
    "production-program",
    "production-graph",
    "daw-interaction",
    "agentic-production",
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
ALLOWED_CONTROL_APPROACHES = {
    "gradient-based-optimization",
    "derivative-free-optimization",
    "direct-prediction",
}
ALLOWED_TRACK_SCOPES = {"single-track", "multitrack"}
ALLOWED_PAPER_TOPICS = {
    "symbolic-performance",
    "performance-rendering",
    "production-program",
    "production-graph",
    "daw-interaction",
    "agentic-production",
}
ALLOWED_PRODUCTION_STAGES = {"score", "performance", "synthesis", "track", "mix", "project"}
ALLOWED_OUTPUT_TYPES = {"audio", "parameter", "graph", "edit", "project"}
AI_ASSESSMENT_RATINGS = {"highlighted", "standard"}
IMPACT_STATUSES = {"high-impact", "standard", "too-recent", "not-assessed"}
RESOURCE_REVIEW_STATUSES = {"source", "project-page", "not-found"}
RESOURCE_REVIEW_PROVIDERS = {"github-search", "manual-web-review"}
ALLOWED_DATASET_CONTENT_TYPES = {
    "multitrack",
    "stems",
    "dry-audio",
    "processed-audio",
    "dry-wet-pairs",
    "effect-parameters",
    "impulse-responses",
    "reference-mixes",
    "annotations",
    "text-prompts",
    "synthetic-audio",
    "binaural-audio",
    "ambisonics",
    "hrtf",
    "spatial-metadata",
    "video",
}
DATASET_ACCESS_STATUSES = {
    "direct-download",
    "request",
    "registration",
    "restricted",
    "unavailable",
    "not-reviewed",
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
DATASET_V1_FIELDS = {
    "id",
    "name",
    "description",
    "scale",
    "areas",
    "taxonomy",
    "access",
    "license",
    "relations",
    "lastVerified",
    "links",
}
WEEKLY_UPDATE_FIELDS = {"schemaVersion", "publishedAt", "counts", "headline", "summary", "highlights"}
WEEKLY_HIGHLIGHT_FIELDS = {"type", "id", "note"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_localized(value: object, context: str) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    for language in ("en", "zh"):
        require(isinstance(value.get(language), str) and value[language].strip(), f"{context}.{language} is required")


def validate_ai_assessment(value: object, context: str) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    require(
        set(value) == {"rating", "rationale", "assessor", "rubricVersion", "assessedAt"},
        f"{context} has invalid fields",
    )
    require(value.get("rating") in AI_ASSESSMENT_RATINGS, f"{context}.rating is invalid")
    rationale = value.get("rationale")
    require(isinstance(rationale, dict) and set(rationale) == {"en", "zh"}, f"{context}.rationale is invalid")
    require(all(isinstance(rationale.get(language), str) for language in ("en", "zh")), f"{context}.rationale is invalid")
    if value["rating"] == "highlighted":
        for language in ("en", "zh"):
            require(20 <= len(rationale[language].strip()) <= 500, f"{context}.rationale.{language} is invalid")
    else:
        require(not rationale["en"].strip() and not rationale["zh"].strip(), f"{context}.rationale must be empty")
    require(value.get("assessor") in {"Codex", "DeepSeek"}, f"{context}.assessor is invalid")
    require(value.get("rubricVersion") == "1.0", f"{context}.rubricVersion is invalid")
    validate_date(value.get("assessedAt"), f"{context}.assessedAt")


def validate_impact(value: object, context: str) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    require(
        set(value)
        == {
            "status",
            "citationCount",
            "influentialCitationCount",
            "yearRank",
            "cohortSize",
            "sourceUrl",
            "measuredAt",
            "methodVersion",
        },
        f"{context} has invalid fields",
    )
    require(value.get("status") in IMPACT_STATUSES, f"{context}.status is invalid")
    for field in ("citationCount", "influentialCitationCount", "yearRank", "cohortSize"):
        number = value.get(field)
        require(number is None or isinstance(number, int) and number >= 0, f"{context}.{field} is invalid")
    source_url = value.get("sourceUrl")
    require(source_url is None or isinstance(source_url, str), f"{context}.sourceUrl is invalid")
    if source_url is not None:
        validate_https_url(source_url, f"{context}.sourceUrl")
    measured_at = value.get("measuredAt")
    require(measured_at is None or isinstance(measured_at, str), f"{context}.measuredAt is invalid")
    if measured_at is not None:
        validate_date(measured_at, f"{context}.measuredAt")
    require(value.get("methodVersion") == "semantic-scholar-year-cohort-v1", f"{context}.methodVersion is invalid")
    if value["status"] in {"high-impact", "standard"}:
        require(value["citationCount"] is not None, f"{context}.citationCount is required")
        require(value["yearRank"] is not None and value["yearRank"] >= 1, f"{context}.yearRank is required")
        require(value["cohortSize"] is not None and value["cohortSize"] >= 1, f"{context}.cohortSize is required")
        require(value["sourceUrl"] is not None and value["measuredAt"] is not None, f"{context} evidence is required")


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


def validate_dataset_links(links: object, context: str) -> None:
    require(isinstance(links, list) and links, f"{context} must have at least one link")
    seen = set()
    for index, link in enumerate(links):
        require(isinstance(link, dict) and set(link) == {"label", "url"}, f"{context}[{index}] has invalid fields")
        require(link.get("label") in ALLOWED_DATASET_LINK_LABELS, f"{context}[{index}] has an unknown label")
        validate_https_url(link.get("url"), f"{context}[{index}].url")
        key = (link["label"], link["url"])
        require(key not in seen, f"{context} contains duplicate links")
        seen.add(key)


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
    require(set(value) == {"tasks", "effects", "reviewStatus", "evidence"}, f"{context} has invalid fields")
    tasks = value.get("tasks")
    effects = value.get("effects")
    evidence = value.get("evidence")
    require(isinstance(tasks, list) and len(tasks) == len(set(tasks)), f"{context}.tasks is invalid")
    require(set(tasks).issubset(ALLOWED_PROJECT_TASKS), f"{context}.tasks contains unknown values")
    require(isinstance(effects, list) and len(effects) == len(set(effects)), f"{context}.effects is invalid")
    require(set(effects).issubset(ALLOWED_EFFECTS), f"{context}.effects contains unknown values")
    require(isinstance(evidence, list) and len(evidence) == len(set(evidence)), f"{context}.evidence is invalid")
    for index, url in enumerate(evidence):
        validate_https_url(url, f"{context}.evidence[{index}]")
    require(value.get("reviewStatus") in {"not-reviewed", "reviewed"}, f"{context}.reviewStatus is invalid")
    if value["reviewStatus"] == "not-reviewed":
        require(not tasks and not effects, f"{context} cannot contain unreviewed taxonomy claims")
        require(not evidence, f"{context} cannot attach evidence before review")
    else:
        require(tasks or effects, f"{context} reviewed taxonomy requires at least one tag")
        require(evidence, f"{context} reviewed taxonomy requires evidence")


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
        control_approaches = paper.get("controlApproaches")
        require(isinstance(control_approaches, list), f"{paper_id}.controlApproaches must be a list")
        require(len(control_approaches) == len(set(control_approaches)), f"{paper_id}.controlApproaches contains duplicates")
        require(
            set(control_approaches).issubset(ALLOWED_CONTROL_APPROACHES),
            f"{paper_id}.controlApproaches contains unknown values",
        )
        track_scopes = paper.get("trackScopes")
        require(isinstance(track_scopes, list), f"{paper_id}.trackScopes must be a list")
        require(len(track_scopes) == len(set(track_scopes)), f"{paper_id}.trackScopes contains duplicates")
        require(set(track_scopes).issubset(ALLOWED_TRACK_SCOPES), f"{paper_id}.trackScopes contains unknown values")
        topics = paper.get("topics", [])
        require(isinstance(topics, list), f"{paper_id}.topics must be a list")
        require(len(topics) == len(set(topics)), f"{paper_id}.topics contains duplicates")
        require(set(topics).issubset(ALLOWED_PAPER_TOPICS), f"{paper_id}.topics contains unknown values")
        production_stages = paper.get("productionStages", [])
        require(isinstance(production_stages, list), f"{paper_id}.productionStages must be a list")
        require(
            len(production_stages) == len(set(production_stages)),
            f"{paper_id}.productionStages contains duplicates",
        )
        require(
            set(production_stages).issubset(ALLOWED_PRODUCTION_STAGES),
            f"{paper_id}.productionStages contains unknown values",
        )
        output_types = paper.get("outputTypes", [])
        require(isinstance(output_types, list), f"{paper_id}.outputTypes must be a list")
        require(len(output_types) == len(set(output_types)), f"{paper_id}.outputTypes contains duplicates")
        require(set(output_types).issubset(ALLOWED_OUTPUT_TYPES), f"{paper_id}.outputTypes contains unknown values")
        validate_ai_assessment(paper.get("aiAssessment"), f"{paper_id}.aiAssessment")
        validate_impact(paper.get("impact"), f"{paper_id}.impact")
        validate_localized(paper.get("summary"), f"{paper_id}.summary")
        validate_links(paper.get("links"), f"{paper_id}.links")
        require(
            any(link.get("label") in {"paper", "doi"} for link in paper["links"]),
            f"{paper_id}.links must include a paper or DOI link",
        )
        require(paper.get("curation") in {"manual", "agent"}, f"{paper_id}.curation is invalid")
        require(isinstance(paper.get("lastVerified"), str), f"{paper_id}.lastVerified is required")
        template_version = paper.get("templateVersion")
        if template_version is not None:
            require(template_version == 1, f"{paper_id}.templateVersion is invalid")
            require("topics" in paper, f"{paper_id}.topics is required by templateVersion 1")
            require(
                "productionStages" in paper,
                f"{paper_id}.productionStages is required by templateVersion 1",
            )
            require("outputTypes" in paper, f"{paper_id}.outputTypes is required by templateVersion 1")
            require(paper.get("curation") == "agent", f"{paper_id} complete template requires agent curation")
            require(isinstance(short_name, str) and short_name.strip(), f"{paper_id} complete template requires shortName")
            review = paper.get("resourceReview")
            require(isinstance(review, dict), f"{paper_id}.resourceReview must be an object")
            require(
                set(review) == {"status", "checkedAt", "provider", "url"},
                f"{paper_id}.resourceReview has invalid fields",
            )
            status = review.get("status")
            require(status in RESOURCE_REVIEW_STATUSES, f"{paper_id}.resourceReview.status is invalid")
            validate_date(review.get("checkedAt"), f"{paper_id}.resourceReview.checkedAt")
            require(review.get("provider") in RESOURCE_REVIEW_PROVIDERS, f"{paper_id}.resourceReview.provider is invalid")
            resource_url = review.get("url")
            if status == "not-found":
                require(resource_url is None, f"{paper_id}.resourceReview.url must be null")
            else:
                validate_https_url(resource_url, f"{paper_id}.resourceReview.url")
                expected_label = "source" if status == "source" else "project"
                require(
                    any(
                        link["label"] == expected_label
                        and canonical_resource_url(link["url"]) == canonical_resource_url(resource_url)
                        for link in paper["links"]
                    ),
                    f"{paper_id}.resourceReview has no matching {expected_label} link",
                )
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


def validate_weekly_update(
    path: Path,
    paper_ids: set[str],
    project_ids: set[str],
    dataset_ids: set[str],
) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(set(data) == WEEKLY_UPDATE_FIELDS, "weekly-update.json has invalid top-level fields")
    require(data.get("schemaVersion") == 1, "weekly-update.json schemaVersion must be 1")
    validate_date(data.get("publishedAt"), "weekly-update.json.publishedAt")
    validate_localized(data.get("headline"), "weekly-update.json.headline")
    validate_localized(data.get("summary"), "weekly-update.json.summary")

    counts = data.get("counts")
    require(isinstance(counts, dict) and set(counts) == {"papers", "projects", "datasets"}, "weekly-update.json.counts is invalid")
    require(
        all(isinstance(counts.get(key), int) and counts[key] >= 0 for key in ("papers", "projects", "datasets")),
        "weekly-update.json.counts must contain non-negative integers",
    )
    require(sum(counts.values()) > 0, "weekly-update.json must describe at least one addition")

    known_ids = {"paper": paper_ids, "project": project_ids, "dataset": dataset_ids}
    highlights = data.get("highlights")
    require(isinstance(highlights, list) and 1 <= len(highlights) <= 3, "weekly-update.json.highlights must contain 1 to 3 entries")
    seen = set()
    for index, highlight in enumerate(highlights):
        context = f"weekly-update.json.highlights[{index}]"
        require(isinstance(highlight, dict) and set(highlight) == WEEKLY_HIGHLIGHT_FIELDS, f"{context} has invalid fields")
        resource_type = highlight.get("type")
        resource_id = highlight.get("id")
        require(resource_type in known_ids, f"{context}.type is invalid")
        require(isinstance(resource_id, str) and resource_id in known_ids[resource_type], f"{context}.id is unknown")
        require((resource_type, resource_id) not in seen, f"{context} is duplicated")
        require(counts[f"{resource_type}s"] > 0, f"{context}.type conflicts with weekly counts")
        validate_localized(highlight.get("note"), f"{context}.note")
        seen.add((resource_type, resource_id))
    return len(highlights)


def validate_dataset_taxonomy(value: object, context: str) -> None:
    require(isinstance(value, dict), f"{context} must be an object")
    require(set(value) == {"tasks", "effects", "contentTypes", "evidence"}, f"{context} has invalid fields")
    tasks = value.get("tasks")
    effects = value.get("effects")
    content_types = value.get("contentTypes")
    evidence = value.get("evidence")
    require(isinstance(tasks, list) and tasks, f"{context}.tasks must not be empty")
    require(len(tasks) == len(set(tasks)), f"{context}.tasks contains duplicates")
    require(set(tasks).issubset(ALLOWED_PROJECT_TASKS), f"{context}.tasks contains unknown values")
    require(isinstance(effects, list), f"{context}.effects must be a list")
    require(len(effects) == len(set(effects)), f"{context}.effects contains duplicates")
    require(set(effects).issubset(ALLOWED_EFFECTS), f"{context}.effects contains unknown values")
    require(isinstance(content_types, list) and content_types, f"{context}.contentTypes must not be empty")
    require(len(content_types) == len(set(content_types)), f"{context}.contentTypes contains duplicates")
    require(
        set(content_types).issubset(ALLOWED_DATASET_CONTENT_TYPES),
        f"{context}.contentTypes contains unknown values",
    )
    require(isinstance(evidence, list) and evidence, f"{context}.evidence must not be empty")
    require(len(evidence) == len(set(evidence)), f"{context}.evidence contains duplicates")
    for index, url in enumerate(evidence):
        validate_https_url(url, f"{context}.evidence[{index}]")


def validate_dataset_access(value: object, context: str) -> None:
    require(isinstance(value, dict) and set(value) == {"status", "evidenceUrl"}, f"{context} has invalid fields")
    status = value.get("status")
    evidence_url = value.get("evidenceUrl")
    require(status in DATASET_ACCESS_STATUSES, f"{context}.status is invalid")
    if status == "not-reviewed":
        require(evidence_url is None, f"{context}.evidenceUrl must be null before review")
    else:
        validate_https_url(evidence_url, f"{context}.evidenceUrl")


def validate_dataset_license(value: object, context: str) -> None:
    validate_project_license(value, context)
    if value["status"] in {"identified", "custom"}:
        require(value["evidenceUrl"] is not None, f"{context}.evidenceUrl is required")


def validate_dataset_relations(
    value: object,
    paper_ids: set[str],
    project_ids: set[str],
    context: str,
) -> None:
    require(isinstance(value, dict) and set(value) == {"papers", "projects"}, f"{context} has invalid fields")
    for relation_type, known_ids in (("papers", paper_ids), ("projects", project_ids)):
        relations = value.get(relation_type)
        require(isinstance(relations, list), f"{context}.{relation_type} must be a list")
        ids = []
        for index, relation in enumerate(relations):
            relation_context = f"{context}.{relation_type}[{index}]"
            require(
                isinstance(relation, dict) and set(relation) == {"id", "evidenceUrl"},
                f"{relation_context} has invalid fields",
            )
            relation_id = relation.get("id")
            require(isinstance(relation_id, str) and relation_id, f"{relation_context}.id is invalid")
            require(relation_id in known_ids, f"{relation_context}.id is unknown")
            validate_https_url(relation.get("evidenceUrl"), f"{relation_context}.evidenceUrl")
            ids.append(relation_id)
        require(len(ids) == len(set(ids)), f"{context}.{relation_type} contains duplicate relations")


def validate_datasets(path: Path, paper_ids: set[str], project_ids: set[str]) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(set(data) == {"schemaVersion", "updatedAt", "datasets"}, "datasets.json has invalid top-level fields")
    require(data.get("schemaVersion") == 1, "datasets.json schemaVersion must be 1")
    validate_date(data.get("updatedAt"), "datasets.json.updatedAt")
    datasets = data.get("datasets")
    require(isinstance(datasets, list), "datasets must be a list")
    ids = set()
    for dataset in datasets:
        dataset_id = dataset.get("id")
        require(isinstance(dataset_id, str) and dataset_id not in ids, f"duplicate or invalid dataset id: {dataset_id}")
        ids.add(dataset_id)
        require(set(dataset) == DATASET_V1_FIELDS, f"{dataset_id} has invalid fields")
        require(isinstance(dataset.get("name"), str) and dataset["name"].strip(), f"{dataset_id}.name is required")
        validate_localized(dataset.get("description"), f"{dataset_id}.description")
        validate_localized(dataset.get("scale"), f"{dataset_id}.scale")
        validate_areas(dataset.get("areas"), f"{dataset_id}.areas")
        validate_dataset_taxonomy(dataset.get("taxonomy"), f"{dataset_id}.taxonomy")
        validate_dataset_access(dataset.get("access"), f"{dataset_id}.access")
        validate_dataset_license(dataset.get("license"), f"{dataset_id}.license")
        validate_dataset_relations(dataset.get("relations"), paper_ids, project_ids, f"{dataset_id}.relations")
        validate_date(dataset.get("lastVerified"), f"{dataset_id}.lastVerified")
        validate_dataset_links(dataset.get("links"), f"{dataset_id}.links")
    return len(datasets)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--projects", type=Path, default=Path("data/projects.json"))
    parser.add_argument("--papers", type=Path, default=Path("data/papers.json"))
    parser.add_argument("--resources", type=Path, default=Path("data/resources.json"))
    parser.add_argument("--datasets", type=Path, default=Path("data/datasets.json"))
    parser.add_argument("--weekly-update", type=Path, default=Path("data/weekly-update.json"))
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
    project_data = json.loads(args.projects.read_text(encoding="utf-8"))
    project_ids = {project["id"] for project in project_data["projects"]}
    linked_project_papers = {
        paper_id
        for project in project_data["projects"]
        for paper_id in project["relations"]["paperIds"]
    }
    complete_source_papers = {
        paper["id"]
        for paper in paper_data["papers"]
        if paper.get("templateVersion") == 1
        and paper.get("resourceReview", {}).get("status") == "source"
    }
    require(
        complete_source_papers.issubset(linked_project_papers),
        "complete source papers must have a project catalogue relation",
    )
    dataset_count = validate_datasets(args.datasets, paper_ids, project_ids)
    dataset_data = json.loads(args.datasets.read_text(encoding="utf-8"))
    dataset_ids = {dataset["id"] for dataset in dataset_data["datasets"]}
    resource_count = validate_resources(args.resources)
    weekly_highlight_count = validate_weekly_update(args.weekly_update, paper_ids, project_ids, dataset_ids)
    print(
        f"Validated {project_count} projects, {paper_count} papers, "
        f"{dataset_count} datasets, {resource_count} reference resources, "
        f"and {weekly_highlight_count} weekly highlights."
    )


if __name__ == "__main__":
    main()
