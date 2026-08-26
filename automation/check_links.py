#!/usr/bin/env python3
"""Check public catalogue URLs and write a reviewable report."""

from __future__ import annotations

import argparse
import json
import socket
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener


DEFAULT_DATA_FILES = (
    Path("data/projects.json"),
    Path("data/papers.json"),
    Path("data/datasets.json"),
    Path("data/resources.json"),
)
SUCCESS = "success"
REDIRECT = "redirect"
ACCESS_BLOCKED = "access-blocked"
RATE_LIMITED = "rate-limited"
NETWORK_FAILURE = "network-failure"
BROKEN = "broken"
STATUSES = (SUCCESS, REDIRECT, ACCESS_BLOCKED, RATE_LIMITED, NETWORK_FAILURE, BROKEN)
REDIRECT_CODES = {300, 301, 302, 303, 307, 308}
GET_FALLBACK_CODES = {403, 405, 501}


class NoRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: ANN001
        return None


def classify_http_status(code: int) -> str:
    if 200 <= code < 300:
        return SUCCESS
    if code in REDIRECT_CODES:
        return REDIRECT
    if code in {401, 403}:
        return ACCESS_BLOCKED
    if code == 429:
        return RATE_LIMITED
    return BROKEN


def iter_url_sources(value: Any, file_path: Path, json_path: str = "$"):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from iter_url_sources(child, file_path, f"{json_path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_url_sources(child, file_path, f"{json_path}[{index}]")
    elif isinstance(value, str):
        parsed = urlparse(value)
        if parsed.scheme in {"http", "https"} and parsed.netloc:
            yield value, {"file": str(file_path), "path": json_path}


def collect_links(paths: list[Path]) -> dict[str, list[dict[str, str]]]:
    links: dict[str, list[dict[str, str]]] = defaultdict(list)
    for path in paths:
        data = json.loads(path.read_text(encoding="utf-8"))
        for url, source in iter_url_sources(data, path):
            if source not in links[url]:
                links[url].append(source)
    return dict(sorted(links.items()))


def make_request(url: str, method: str) -> Request:
    return Request(
        url,
        method=method,
        headers={
            "Accept": "*/*",
            "User-Agent": "intelligent-audio-production-resources-link-check/1.0",
        },
    )


def http_result(url: str, method: str, opener, timeout: float) -> dict[str, Any]:  # noqa: ANN001
    try:
        with opener.open(make_request(url, method), timeout=timeout) as response:
            code = int(response.getcode())
            return {
                "status": classify_http_status(code),
                "httpStatus": code,
                "method": method,
                "redirectLocation": response.headers.get("Location"),
                "error": None,
            }
    except HTTPError as error:
        code = int(error.code)
        return {
            "status": classify_http_status(code),
            "httpStatus": code,
            "method": method,
            "redirectLocation": error.headers.get("Location"),
            "error": str(error.reason),
        }
    except (TimeoutError, socket.timeout) as error:
        return {
            "status": NETWORK_FAILURE,
            "httpStatus": None,
            "method": method,
            "redirectLocation": None,
            "error": f"timeout: {error}",
        }
    except URLError as error:
        return {
            "status": NETWORK_FAILURE,
            "httpStatus": None,
            "method": method,
            "redirectLocation": None,
            "error": str(error.reason),
        }


def check_url(url: str, opener=None, timeout: float = 10.0) -> dict[str, Any]:
    active_opener = opener or build_opener(NoRedirectHandler)
    result = http_result(url, "HEAD", active_opener, timeout)
    if result["httpStatus"] in GET_FALLBACK_CODES:
        fallback = http_result(url, "GET", active_opener, timeout)
        fallback["headStatus"] = result["httpStatus"]
        return fallback
    return result


def build_report(paths: list[Path], timeout: float = 10.0, opener=None) -> dict[str, Any]:
    links = collect_links(paths)
    checked = []
    for url, sources in links.items():
        result = check_url(url, opener=opener, timeout=timeout)
        checked.append({"url": url, **result, "sources": sources})
    counts = Counter(item["status"] for item in checked)
    return {
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "dataFiles": [str(path) for path in paths],
        "timeoutSeconds": timeout,
        "summary": {status: counts.get(status, 0) for status in STATUSES},
        "links": checked,
    }


def write_report(report: dict[str, Any], output: Path | None) -> None:
    text = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        print(text, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"Wrote link check report to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path, default=list(DEFAULT_DATA_FILES))
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    report = build_report(args.paths, timeout=args.timeout)
    write_report(report, args.output)


if __name__ == "__main__":
    main()
