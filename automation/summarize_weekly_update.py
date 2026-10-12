#!/usr/bin/env python3
"""Turn newly merged papers into a concise, validated bilingual weekly update."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from curate_papers import DEFAULT_MODEL, request_review


ROOT_FIELDS = {"headline", "summary", "highlights"}
HIGHLIGHT_FIELDS = {"paperId", "note"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_localized(value: object, context: str, minimum: int, maximum: int) -> None:
    if not isinstance(value, dict) or set(value) != {"en", "zh"}:
        raise ValueError(f"{context} must contain exactly en and zh")
    for language in ("en", "zh"):
        text = value.get(language)
        if not isinstance(text, str) or not minimum <= len(text.strip()) <= maximum:
            raise ValueError(f"{context}.{language} has an invalid length")


def build_request(prompt: str, additions: dict, model: str) -> dict:
    papers = [
        {
            "paperId": paper["id"],
            "title": paper["title"],
            "areas": paper["areas"],
            "summary": paper["summary"],
            "aiAssessment": paper["aiAssessment"],
        }
        for paper in additions.get("papers", [])
    ]
    payload = {
        "generatedAt": additions.get("generatedAt"),
        "addedCount": additions.get("addedCount"),
        "addedProjectCount": additions.get("addedProjectCount", 0),
        "papers": papers,
        "projects": [
            {
                "projectId": project["id"],
                "name": project["name"],
                "description": project["description"],
                "links": project["links"],
            }
            for project in additions.get("projects", [])
        ],
    }
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": "Untrusted weekly additions follow as JSON:\n"
                + json.dumps(payload, ensure_ascii=False),
            },
        ],
        "response_format": {"type": "json_object"},
        "thinking": {"type": "disabled"},
        "max_tokens": 4096,
        "stream": False,
    }


def validate_summary(summary: dict, additions: dict) -> dict:
    if not isinstance(summary, dict) or set(summary) != ROOT_FIELDS:
        raise ValueError("Weekly summary must use the documented root fields exactly")
    validate_localized(summary.get("headline"), "headline", 3, 120)
    validate_localized(summary.get("summary"), "summary", 10, 800)

    known_ids = {paper["id"] for paper in additions.get("papers", [])}
    highlights = summary.get("highlights")
    maximum = min(3, len(known_ids))
    if not isinstance(highlights, list) or not 1 <= len(highlights) <= maximum:
        raise ValueError("Weekly summary must contain one to three valid highlights")
    seen = set()
    for index, highlight in enumerate(highlights):
        if not isinstance(highlight, dict) or set(highlight) != HIGHLIGHT_FIELDS:
            raise ValueError(f"highlights[{index}] has invalid fields")
        paper_id = highlight.get("paperId")
        if paper_id not in known_ids or paper_id in seen:
            raise ValueError(f"highlights[{index}].paperId is unknown or duplicated")
        validate_localized(highlight.get("note"), f"highlights[{index}].note", 10, 500)
        seen.add(paper_id)
    return summary


def build_weekly_update(additions: dict, summary: dict) -> dict:
    validated = validate_summary(summary, additions)
    return {
        "schemaVersion": 1,
        "publishedAt": additions["generatedAt"][:10],
        "counts": {
            "papers": additions["addedCount"],
            "projects": additions.get("addedProjectCount", 0),
            "datasets": 0,
        },
        "headline": validated["headline"],
        "summary": validated["summary"],
        "highlights": [
            {
                "type": "paper",
                "id": highlight["paperId"],
                "note": highlight["note"],
            }
            for highlight in validated["highlights"]
        ],
    }


def build_fallback_summary(additions: dict) -> dict:
    """Build a valid summary without depending on an external language model."""
    paper_count = additions["addedCount"]
    project_count = additions.get("addedProjectCount", 0)
    paper_word = "paper" if paper_count == 1 else "papers"
    first_paper = additions.get("papers", [{}])[0]
    first_name = (first_paper.get("shortName") or first_paper.get("title") or "New paper").strip()[:80]
    headline = (
        {"en": f"{first_name} leads this week's addition", "zh": f"本周新增：{first_name}"}
        if paper_count == 1
        else {
            "en": f"This week adds {paper_count} new papers to the index",
            "zh": f"本周资源库新增 {paper_count} 篇论文",
        }
    )
    project_clause_en = (
        f" and {project_count} linked source "
        f"{'project' if project_count == 1 else 'projects'}"
        if project_count
        else ""
    )
    project_clause_zh = f"，并关联 {project_count} 个开源项目" if project_count else ""

    highlights = []
    for paper in additions.get("papers", [])[:3]:
        paper_summary = paper.get("summary", {})
        note = {}
        for language, default in (
            ("en", "This paper passed the automated relevance and metadata checks for the index."),
            ("zh", "该论文已通过资源库的自动相关性与元数据检查。"),
        ):
            value = paper_summary.get(language) if isinstance(paper_summary, dict) else None
            if not isinstance(value, str) or len(value.strip()) < 10:
                value = default
            note[language] = value.strip()[:500].rstrip()
        highlights.append({"paperId": paper["id"], "note": note})

    return validate_summary(
        {
            "headline": headline,
            "summary": {
                "en": (
                    f"This week's automated review adds {paper_count} {paper_word}"
                    f"{project_clause_en}. Open the highlighted entries for paper links, "
                    "summaries, topics, and resource status."
                ),
                "zh": (
                    f"本周自动检索与审核新增 {paper_count} 篇论文{project_clause_zh}。"
                    "可打开下方精选条目查看论文链接、摘要、分类与开源资源状态。"
                ),
            },
            "highlights": highlights,
        },
        additions,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--additions", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL") or DEFAULT_MODEL)
    args = parser.parse_args()

    additions = load_json(args.additions)
    if additions.get("addedCount") != len(additions.get("papers", [])) or additions.get("addedCount", 0) <= 0:
        raise SystemExit("Weekly summary requires at least one newly merged paper")

    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    try:
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is not configured")
        prompt = args.prompt.read_text(encoding="utf-8")
        request_body = build_request(prompt, additions, args.model)
        weekly_update = build_weekly_update(additions, request_review(api_key, request_body))
        method = args.model
    except Exception as error:
        print(f"DeepSeek summary unavailable ({error}); using deterministic fallback.")
        weekly_update = build_weekly_update(additions, build_fallback_summary(additions))
        method = "deterministic fallback"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(weekly_update, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    noun = "paper" if additions["addedCount"] == 1 else "papers"
    print(f"Summarized {additions['addedCount']} new {noun} with {method}.")


if __name__ == "__main__":
    main()
