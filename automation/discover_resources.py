#!/usr/bin/env python3
"""Find evidence-backed GitHub resources for newly discovered papers."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date
from pathlib import Path


API_ROOT = "https://api.github.com"
SOURCE_EXTENSIONS = {
    ".c",
    ".cc",
    ".cpp",
    ".cs",
    ".cu",
    ".cxx",
    ".h",
    ".hpp",
    ".ipynb",
    ".java",
    ".jl",
    ".js",
    ".m",
    ".matlab",
    ".maxpat",
    ".mm",
    ".py",
    ".r",
    ".rnbopat",
    ".rs",
    ".sh",
    ".swift",
    ".ts",
}
IGNORED_SOURCE_PREFIXES = ("assets/", "docs/", "images/", "static/")
GITHUB_URL = re.compile(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")
HUGGING_FACE_URL = re.compile(r"https://huggingface\.co/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)")


def normalized(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.casefold())


def index_name_seed(title: str) -> str:
    prefix = title.split(":", 1)[0].strip()
    if ":" in title and 2 <= len(prefix) <= 60:
        return prefix
    words = title.split()
    return " ".join(words[: min(8, len(words))])


def repository_name(url: str) -> str | None:
    match = GITHUB_URL.match(url)
    if not match:
        return None
    return f"{match.group(1)}/{match.group(2).removesuffix('.git')}"


def explicit_repositories(candidate: dict) -> set[str]:
    text = " ".join(
        str(candidate.get(field) or "")
        for field in ("abstract", "comment", "journalReference")
    )
    return {
        f"{owner}/{repository.removesuffix('.git')}"
        for owner, repository in GITHUB_URL.findall(text)
    }


def source_files(tree: list[dict]) -> list[str]:
    paths = []
    for item in tree:
        path = str(item.get("path") or "")
        lowered = path.casefold()
        if item.get("type") != "blob" or lowered.startswith(IGNORED_SOURCE_PREFIXES):
            continue
        if Path(lowered).suffix in SOURCE_EXTENSIONS:
            paths.append(path)
    return paths


def checkpoint_urls(readme: str) -> list[str]:
    urls = {
        f"https://huggingface.co/{owner}/{repository.rstrip('.,;:')}"
        for owner, repository in HUGGING_FACE_URL.findall(readme)
        if owner not in {"datasets", "spaces"}
    }
    return sorted(urls)


def detected_license(text: str) -> tuple[str, str] | None:
    lowered = text.casefold()
    if "polyform noncommercial license 1.0.0" in lowered:
        return "PolyForm-Noncommercial-1.0.0", "PolyForm Noncommercial License 1.0.0"
    if "apache license" in lowered and "version 2.0" in lowered:
        return "Apache-2.0", "Apache License 2.0"
    if "permission is hereby granted, free of charge" in lowered:
        return "MIT", "MIT"
    return None


class GitHubClient:
    def __init__(self, token: str):
        self.token = token

    def get(self, path: str, parameters: dict | None = None, allow_missing: bool = False) -> dict:
        query = f"?{urllib.parse.urlencode(parameters)}" if parameters else ""
        request = urllib.request.Request(
            f"{API_ROOT}{path}{query}",
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": f"Bearer {self.token}",
                "User-Agent": "IntelligentAudioProductionResourceScout/1.0",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
        last_error: Exception | None = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(request, timeout=60) as response:
                    return json.loads(response.read().decode("utf-8"))
            except urllib.error.HTTPError as error:
                if allow_missing and error.code == 404:
                    return {}
                last_error = error
                if error.code not in {403, 408, 429, 500, 502, 503, 504}:
                    break
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
                last_error = error
            if attempt < 2:
                time.sleep(2**attempt)
        raise RuntimeError(f"GitHub API request failed for {path}: {last_error}")


def readme_for(client: GitHubClient, full_name: str) -> tuple[str, str | None]:
    payload = client.get(f"/repos/{full_name}/readme", allow_missing=True)
    content = payload.get("content")
    if not isinstance(content, str):
        return "", None
    return base64.b64decode(content).decode("utf-8", errors="replace"), payload.get("html_url")


def relation_match(candidate: dict, repo: dict, readme: str, explicit: set[str]) -> tuple[int, str] | None:
    full_name = repo["full_name"]
    if full_name.casefold() in {item.casefold() for item in explicit}:
        return 120, "explicit-url"

    identifier = candidate["sourceId"].removeprefix("arxiv:")
    if identifier in readme or f"arxiv.org/abs/{identifier}" in readme.casefold():
        return 110, "arxiv-id"

    title = normalized(candidate["title"])
    readme_text = normalized(readme)
    if len(title) >= 24 and title in readme_text:
        return 100, "exact-title"

    seed = normalized(index_name_seed(candidate["title"]))
    repo_slug = normalized(repo["name"])
    first_author = normalized(candidate.get("authors", [""])[0])
    owner = normalized(repo["owner"]["login"])
    name_matches = len(seed) >= 5 and (seed in repo_slug or repo_slug in seed)
    author_matches = len(first_author) >= 6 and (first_author in owner or owner in first_author)
    if name_matches and author_matches:
        return 90, "method-and-author"
    return None


def repository_candidates(client: GitHubClient, candidate: dict) -> list[str]:
    identifier = candidate["sourceId"].removeprefix("arxiv:")
    seed = index_name_seed(candidate["title"])
    repositories = set(explicit_repositories(candidate))

    code_results = client.get(
        "/search/code",
        {"q": f'"{identifier}" in:file filename:README.md', "per_page": 10},
    )
    repositories.update(
        item["repository"]["full_name"]
        for item in code_results.get("items", [])
        if item.get("repository", {}).get("full_name")
    )

    repository_results = client.get(
        "/search/repositories",
        {"q": f'"{seed}" in:name', "per_page": 10, "sort": "updated", "order": "desc"},
    )
    repositories.update(
        item["full_name"]
        for item in repository_results.get("items", [])
        if item.get("full_name")
    )
    return sorted(repositories, key=str.casefold)


def license_metadata(
    client: GitHubClient,
    repo: dict,
    tree: list[dict],
) -> dict:
    full_name = repo["full_name"]
    branch = repo["default_branch"]
    license_payload = client.get(f"/repos/{full_name}/license", allow_missing=True)
    repository_license = repo.get("license") or {}
    spdx = repository_license.get("spdx_id")
    if isinstance(spdx, str) and spdx not in {"", "NOASSERTION", "OTHER"}:
        return {
            "en": repository_license.get("name") or spdx,
            "zh": repository_license.get("name") or spdx,
            "status": "identified",
            "spdx": spdx,
            "evidenceUrl": license_payload.get("html_url"),
        }

    license_paths = sorted(
        (
            item["path"]
            for item in tree
            if item.get("type") == "blob"
            and re.search(r"(?:^|/)(?:licen[cs]e|copying)(?:\.[a-z0-9]+)?$", item.get("path", ""), re.IGNORECASE)
        ),
        key=lambda path: (path.count("/"), len(path), path.casefold()),
    )
    if not license_paths:
        return {
            "en": "No repository license file verified",
            "zh": "未核验到仓库许可证文件",
            "status": "not-verified",
            "spdx": None,
            "evidenceUrl": None,
        }

    path = license_paths[0]
    payload = client.get(f"/repos/{full_name}/contents/{urllib.parse.quote(path)}")
    content = base64.b64decode(payload.get("content", "")).decode("utf-8", errors="replace")
    evidence_url = f"https://github.com/{full_name}/blob/{branch}/{path}"
    detected = detected_license(content)
    if detected:
        detected_spdx, name = detected
        return {
            "en": name,
            "zh": name,
            "status": "identified",
            "spdx": detected_spdx,
            "evidenceUrl": evidence_url,
        }
    return {
        "en": "Custom or non-standard terms; see repository license text",
        "zh": "自定义或非标准条款；详见仓库许可证原文",
        "status": "custom",
        "spdx": None,
        "evidenceUrl": evidence_url,
    }


def inspect_repository(client: GitHubClient, candidate: dict, full_name: str) -> dict | None:
    repo = client.get(f"/repos/{full_name}")
    if repo.get("archived") or repo.get("fork"):
        return None
    readme, readme_url = readme_for(client, full_name)
    match = relation_match(candidate, repo, readme, explicit_repositories(candidate))
    if not match:
        return None
    branch = repo["default_branch"]
    tree_payload = client.get(
        f"/repos/{full_name}/git/trees/{urllib.parse.quote(branch, safe='')}",
        {"recursive": 1},
    )
    tree = tree_payload.get("tree", [])
    if not isinstance(tree, list):
        raise RuntimeError(f"GitHub returned no tree for {full_name}")
    code = source_files(tree)
    score, matched_by = match
    return {
        "kind": "source" if code else "project-page",
        "url": repo["html_url"],
        "fullName": full_name,
        "defaultBranch": branch,
        "readmeUrl": readme_url,
        "matchedBy": matched_by,
        "matchScore": score,
        "codeFileCount": len(code),
        "license": license_metadata(client, repo, tree) if code else None,
        "checkpointUrls": checkpoint_urls(readme) if code else [],
    }


def discover_for_candidate(client: GitHubClient, candidate: dict, checked_at: str) -> dict:
    inspected = []
    for full_name in repository_candidates(client, candidate)[:15]:
        resource = inspect_repository(client, candidate, full_name)
        if resource:
            inspected.append(resource)
    if not inspected:
        return {
            "status": "not-found",
            "checkedAt": checked_at,
            "provider": "github-search",
            "resource": None,
        }
    inspected.sort(
        key=lambda item: (item["matchScore"], item["kind"] == "source", item["codeFileCount"]),
        reverse=True,
    )
    return {
        "status": "matched",
        "checkedAt": checked_at,
        "provider": "github-search",
        "resource": inspected[0],
    }


def enrich_candidates(data: dict, client: GitHubClient) -> dict:
    checked_at = str(data.get("generatedAt") or date.today().isoformat())[:10]
    for candidate in data.get("candidates", []):
        candidate["resourceSearch"] = discover_for_candidate(client, candidate, checked_at)
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if not token:
        raise SystemExit("GITHUB_TOKEN is required for evidence-backed repository search")
    data = json.loads(args.candidates.read_text(encoding="utf-8"))
    enriched = enrich_candidates(data, GitHubClient(token))
    args.output.write_text(json.dumps(enriched, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    matched = sum(candidate["resourceSearch"]["status"] == "matched" for candidate in enriched.get("candidates", []))
    print(f"Verified GitHub resources for {matched}/{len(enriched.get('candidates', []))} candidates.")


if __name__ == "__main__":
    main()
