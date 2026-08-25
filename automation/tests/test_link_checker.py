import json
import socket
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.response import addinfourl


AUTOMATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTOMATION_DIR))

import check_links  # noqa: E402


class FakeHeaders(dict):
    def get(self, key, default=None):
        return super().get(key, default)


class FakeResponse:
    def __init__(self, code, headers=None):
        self.code = code
        self.headers = FakeHeaders(headers or {})

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def getcode(self):
        return self.code


class FakeOpener:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.requests = []

    def open(self, request, timeout):
        self.requests.append((request.full_url, request.get_method(), timeout))
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, BaseException):
            raise outcome
        return outcome


def http_error(url, code, message="error", headers=None):
    return HTTPError(url, code, message, FakeHeaders(headers or {}), addinfourl(None, {}, url))


class LinkCheckerTests(unittest.TestCase):
    def test_collect_links_finds_nested_urls_and_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(
                json.dumps(
                    {
                        "projects": [
                            {
                                "links": [{"url": "https://example.test/project"}],
                                "availability": {"source": {"evidence": ["https://example.test/project"]}},
                                "ignored": "mailto:test@example.test",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            links = check_links.collect_links([path])
        self.assertEqual(list(links), ["https://example.test/project"])
        self.assertEqual(len(links["https://example.test/project"]), 2)

    def test_successful_link(self):
        result = check_links.check_url("https://example.test", opener=FakeOpener([FakeResponse(200)]))
        self.assertEqual(result["status"], check_links.SUCCESS)
        self.assertEqual(result["httpStatus"], 200)
        self.assertEqual(result["method"], "HEAD")

    def test_redirect_is_reported_without_following(self):
        opener = FakeOpener([http_error("https://example.test", 302, headers={"Location": "https://example.test/new"})])
        result = check_links.check_url("https://example.test", opener=opener)
        self.assertEqual(result["status"], check_links.REDIRECT)
        self.assertEqual(result["httpStatus"], 302)
        self.assertEqual(result["redirectLocation"], "https://example.test/new")

    def test_access_block_after_get_fallback(self):
        opener = FakeOpener([http_error("https://example.test", 403), http_error("https://example.test", 403)])
        result = check_links.check_url("https://example.test", opener=opener)
        self.assertEqual(result["status"], check_links.ACCESS_BLOCKED)
        self.assertEqual(result["httpStatus"], 403)
        self.assertEqual(result["method"], "GET")
        self.assertEqual(result["headStatus"], 403)

    def test_head_403_can_recover_with_get(self):
        opener = FakeOpener([http_error("https://example.test", 403), FakeResponse(200)])
        result = check_links.check_url("https://example.test", opener=opener)
        self.assertEqual(result["status"], check_links.SUCCESS)
        self.assertEqual(result["method"], "GET")

    def test_rate_limit(self):
        result = check_links.check_url("https://example.test", opener=FakeOpener([http_error("https://example.test", 429)]))
        self.assertEqual(result["status"], check_links.RATE_LIMITED)

    def test_timeout_network_failure(self):
        result = check_links.check_url("https://example.test", opener=FakeOpener([socket.timeout("slow")]))
        self.assertEqual(result["status"], check_links.NETWORK_FAILURE)
        self.assertIn("timeout", result["error"])

    def test_url_error_network_failure(self):
        result = check_links.check_url("https://example.test", opener=FakeOpener([URLError("dns")]))
        self.assertEqual(result["status"], check_links.NETWORK_FAILURE)

    def test_missing_link_is_broken(self):
        result = check_links.check_url("https://example.test", opener=FakeOpener([http_error("https://example.test", 404)]))
        self.assertEqual(result["status"], check_links.BROKEN)
        self.assertEqual(result["httpStatus"], 404)

    def test_method_not_allowed_falls_back_to_get(self):
        opener = FakeOpener([http_error("https://example.test", 405), FakeResponse(204)])
        result = check_links.check_url("https://example.test", opener=opener)
        self.assertEqual(result["status"], check_links.SUCCESS)
        self.assertEqual(result["method"], "GET")
        self.assertEqual([request[1] for request in opener.requests], ["HEAD", "GET"])


if __name__ == "__main__":
    unittest.main()
