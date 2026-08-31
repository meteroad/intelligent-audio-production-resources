#!/usr/bin/env python3
"""Attach verified resources and create complete project records for new papers."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical_url(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.rstrip("/").casefold()
    if path.endswith(".git"):
        path = path[:-4]
    return f"{parsed.netloc.casefold().removeprefix('www.')}{path}"


def project_id(full_name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", full_name.casefold()).strip("-")


def resource_review(search: dict) -> dict:
    resource = search.get("resource")
    if search.get("status") == "not-found":
        return {
            "status": "not-found",
            "checkedAt": search["checkedAt"],
            "provider": search["provider"],
            "url": None,
        }
    if search.get("status") != "matched" or not isinstance(resource, dict):
        raise ValueError("Candidate resource search is incomplete")
    return {
        "status": resource["kind"],
        "checkedAt": search["checkedAt"],
        "provider": search["provider"],
        "url": resource["url"],
    }


def add_link(links: list[dict], label: str, url: str) -> None:
    if not any(item["label"] == label and canonical_url(item["url"]) == canonical_url(url) for item in links):
        links.append({"label": label, "url": url})


def project_description(paper: dict) -> dict:
    name = paper["shortName"]
    return {
        "en": f"Public implementation associated with {name}. {paper['summary']['en']}",
        "zh": f"与 {name} 关联的公开实现。{paper['summary']['zh']}",
    }


def build_project(paper: dict, resource: dict, checked_at: str) -> dict:
    source_url = resource["url"]
    checkpoint_urls = resource.get("checkpointUrls", [])
    links = [{"label": "source", "url": source_url}]
    links.extend({"label": "checkpoint", "url": url} for url in checkpoint_urls)
    return {
        "id": project_id(resource["fullName"]),
        "name": paper["shortName"],
        "description": project_description(paper),
        "areas": paper["areas"],
        "taxonomy": {
            "tasks": paper.get("topics", []),
            "effects": [],
            "reviewStatus": "reviewed" if paper.get("topics") else "not-reviewed",
            "evidence": [resource.get("readmeUrl") or source_url] if paper.get("topics") else [],
        },
        "license": resource["license"],
        "availability": {
            "source": {"status": "linked", "evidence": [source_url]},
            "checkpoint": {
                "status": "linked" if checkpoint_urls else "not-reviewed",
                "evidence": checkpoint_urls,
            },
            "inference": {"status": "not-reviewed", "evidence": []},
            "training": {"status": "not-reviewed", "evidence": []},
            "dataset": {"status": "not-reviewed", "evidence": []},
        },
        "relations": {
            "paperIds": [paper["id"]],
            "reviewStatus": "exact-link-match",
        },
        "lastVerified": checked_at,
        "links": links,
    }


def attach_existing_project(project: dict, paper_id: str, checked_at: str) -> None:
    if paper_id not in project["relations"]["paperIds"]:
        project["relations"]["paperIds"].append(paper_id)
        project["relations"]["paperIds"].sort()
    if project["relations"]["reviewStatus"] == "not-reviewed":
        project["relations"]["reviewStatus"] = "exact-link-match"
    project["lastVerified"] = checked_at


def merge_resources(
    candidates_data: dict,
    additions_data: dict,
    papers_data: dict,
    projects_data: dict,
) -> tuple[dict, dict, dict]:
    candidates = {candidate["sourceId"]: candidate for candidate in candidates_data.get("candidates", [])}
    papers = {paper["id"]: paper for paper in papers_data.get("papers", [])}
    existing_projects = {
        canonical_url(link["url"]): project
        for project in projects_data.get("projects", [])
        for link in project.get("links", [])
        if link.get("label") in {"source", "project"}
    }
    new_projects = []

    for addition in additions_data.get("papers", []):
        paper = papers[addition["id"]]
        candidate = candidates.get(paper["source"]["id"])
        if not candidate or "resourceSearch" not in candidate:
            raise ValueError(f"Missing resource search for {paper['id']}")
        search = candidate["resourceSearch"]
        review = resource_review(search)
        paper["templateVersion"] = 1
        paper["resourceReview"] = review
        resource = search.get("resource")
        if not resource:
            continue

        label = "source" if resource["kind"] == "source" else "project"
        add_link(paper["links"], label, resource["url"])
        for checkpoint_url in resource.get("checkpointUrls", []):
            add_link(paper["links"], "checkpoint", checkpoint_url)
        if resource["kind"] != "source":
            continue

        key = canonical_url(resource["url"])
        existing = existing_projects.get(key)
        if existing:
            attach_existing_project(existing, paper["id"], search["checkedAt"])
            continue
        project = build_project(paper, resource, search["checkedAt"])
        projects_data["projects"].append(project)
        existing_projects[key] = project
        new_projects.append(project)

    if additions_data.get("papers"):
        checked_at = candidates_data.get("generatedAt", "")[:10]
        projects_data["updatedAt"] = checked_at
    projects_data["projects"].sort(key=lambda project: project["name"].casefold())
    addition_ids = {paper["id"] for paper in additions_data.get("papers", [])}
    additions_data["papers"] = [paper for paper in papers_data["papers"] if paper["id"] in addition_ids]
    additions_data["addedProjectCount"] = len(new_projects)
    additions_data["projects"] = new_projects
    return papers_data, projects_data, additions_data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--additions", type=Path, required=True)
    parser.add_argument("--papers", type=Path, required=True)
    parser.add_argument("--projects", type=Path, required=True)
    args = parser.parse_args()

    papers, projects, additions = merge_resources(
        load_json(args.candidates),
        load_json(args.additions),
        load_json(args.papers),
        load_json(args.projects),
    )
    args.papers.write_text(json.dumps(papers, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.projects.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    args.additions.write_text(json.dumps(additions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"Completed resource reviews for {additions['addedCount']} papers; "
        f"added {additions['addedProjectCount']} projects."
    )


if __name__ == "__main__":
    main()
