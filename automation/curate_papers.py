#!/usr/bin/env python3
"""Curate arXiv candidates with DeepSeek and persist a validated JSON review."""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


API_URL = "https://api.deepseek.com/chat/completions"
DEFAULT_MODEL = "deepseek-v4-flash"
EXPECTED_FIELDS = {"sourceId", "decision", "confidence", "areas", "summary", "reason"}
ALLOWED_DECISIONS = {"include", "exclude"}
ALLOWED_CONFIDENCE = {"high", "medium", "low"}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_request(prompt: str, candidates_data: dict, model: str) -> dict:
    candidate_payload = {
        "generatedAt": candidates_data.get("generatedAt"),
        "candidates": candidates_data.get("candidates", []),
    }
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": "Untrusted candidate metadata follows as JSON:\n"
                + json.dumps(candidate_payload, ensure_ascii=False),
            },
        ],
        "response_format": {"type": "json_object"},
        "thinking": {"type": "disabled"},
        "max_tokens": 32768,
        "stream": False,
    }


def api_error_message(error: urllib.error.HTTPError) -> str:
    try:
        payload = json.loads(error.read().decode("utf-8"))
        return payload.get("error", {}).get("message") or str(payload)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return error.reason or "unknown API error"


def request_review(api_key: str, request_body: dict, attempts: int = 3) -> dict:
    encoded = json.dumps(request_body).encode("utf-8")
    last_error: Exception | None = None
    for attempt in range(attempts):
        request = urllib.request.Request(
            API_URL,
            data=encoded,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                payload = json.loads(response.read().decode("utf-8"))
            content = payload["choices"][0]["message"]["content"]
            if not isinstance(content, str) or not content.strip():
                raise ValueError("DeepSeek returned empty content")
            return json.loads(content)
        except urllib.error.HTTPError as error:
            message = api_error_message(error)
            last_error = RuntimeError(f"DeepSeek API error {error.code}: {message}")
            if error.code not in {408, 429, 500, 502, 503, 504}:
                raise last_error from error
        except (urllib.error.URLError, TimeoutError, KeyError, IndexError, json.JSONDecodeError, ValueError) as error:
            last_error = error
        if attempt + 1 < attempts:
            time.sleep(2**attempt)
    raise RuntimeError(f"DeepSeek curation failed after {attempts} attempts: {last_error}")


def validate_review(review: dict, candidates_data: dict) -> dict:
    if not isinstance(review, dict) or set(review) != {"reviewedAt", "decisions"}:
        raise ValueError("DeepSeek response must use the documented root fields exactly")
    if not isinstance(review.get("decisions"), list):
        raise ValueError("DeepSeek response must contain a decisions array")

    candidates = candidates_data.get("candidates", [])
    candidate_ids = {candidate["sourceId"] for candidate in candidates}
    seen_ids: set[str] = set()

    for decision in review["decisions"]:
        if not isinstance(decision, dict) or set(decision) != EXPECTED_FIELDS:
            raise ValueError("Each DeepSeek decision must use the documented fields exactly")
        source_id = decision.get("sourceId")
        if source_id not in candidate_ids or source_id in seen_ids:
            raise ValueError(f"Unknown or duplicate sourceId in DeepSeek response: {source_id!r}")
        seen_ids.add(source_id)
        if decision.get("decision") not in ALLOWED_DECISIONS:
            raise ValueError(f"Invalid decision for {source_id}")
        if decision.get("confidence") not in ALLOWED_CONFIDENCE:
            raise ValueError(f"Invalid confidence for {source_id}")
        if not isinstance(decision.get("areas"), list):
            raise ValueError(f"Invalid areas for {source_id}")
        summary = decision.get("summary")
        if not isinstance(summary, dict) or set(summary) != {"en", "zh"}:
            raise ValueError(f"Invalid summary for {source_id}")
        if not all(isinstance(summary[key], str) for key in ("en", "zh")):
            raise ValueError(f"Invalid summary text for {source_id}")
        if not isinstance(decision.get("reason"), str):
            raise ValueError(f"Invalid reason for {source_id}")
        if decision["decision"] == "exclude":
            decision["areas"] = []
            decision["summary"] = {"en": "", "zh": ""}

    if seen_ids != candidate_ids:
        missing = sorted(candidate_ids - seen_ids)
        raise ValueError(f"DeepSeek did not review every candidate; missing: {missing}")

    review["reviewedAt"] = candidates_data.get("generatedAt", "")[:10]
    return review


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--model", default=os.environ.get("DEEPSEEK_MODEL") or DEFAULT_MODEL)
    args = parser.parse_args()

    api_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("DEEPSEEK_API_KEY is not configured")

    candidates_data = load_json(args.candidates)
    prompt = args.prompt.read_text(encoding="utf-8")
    request_body = build_request(prompt, candidates_data, args.model)
    review = validate_review(request_review(api_key, request_body), candidates_data)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(review, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"DeepSeek reviewed {len(review['decisions'])} candidates with {args.model}.")


if __name__ == "__main__":
    main()
