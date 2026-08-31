import base64
import copy
import sys
import unittest
from pathlib import Path


AUTOMATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTOMATION_DIR))

import discover_resources  # noqa: E402
import merge_resources  # noqa: E402


class FakeGitHubClient:
    def __init__(self, responses):
        self.responses = responses

    def get(self, path, parameters=None, allow_missing=False):
        key = (path, tuple(sorted((parameters or {}).items())))
        if key in self.responses:
            return copy.deepcopy(self.responses[key])
        if path in self.responses:
            return copy.deepcopy(self.responses[path])
        if allow_missing:
            return {}
        raise AssertionError(f"Unexpected GitHub request: {key}")


def candidate():
    return {
        "sourceId": "arxiv:2608.12345",
        "title": "MethodFX: A Complete Audio Effect",
        "authors": ["First Author", "Second Author"],
        "abstract": "Method description.",
        "comment": None,
        "journalReference": None,
    }


def paper():
    return {
        "id": "arxiv-2608-12345",
        "source": {"type": "arxiv", "id": "arxiv:2608.12345"},
        "shortName": "MethodFX",
        "title": "MethodFX: A Complete Audio Effect",
        "authors": ["First Author", "Second Author"],
        "year": 2026,
        "published": "2026-08-28",
        "venue": "DAFx 2026",
        "areas": ["audio-effects"],
        "controlApproaches": [],
        "trackScopes": ["single-track"],
        "aiAssessment": {
            "rating": "standard",
            "rationale": {"en": "", "zh": ""},
            "assessor": "DeepSeek",
            "rubricVersion": "1.0",
            "assessedAt": "2026-08-28",
        },
        "impact": {
            "status": "not-assessed",
            "citationCount": None,
            "influentialCitationCount": None,
            "yearRank": None,
            "cohortSize": None,
            "sourceUrl": None,
            "measuredAt": None,
            "methodVersion": "semantic-scholar-year-cohort-v1",
        },
        "summary": {
            "en": "Introduces a complete effect method with reproducible evaluation.",
            "zh": "提出一种带有可复现评测的完整音效方法。",
        },
        "links": [{"label": "paper", "url": "https://arxiv.org/abs/2608.12345"}],
        "lastVerified": "2026-08-28",
        "curation": "agent",
    }


class ResourceDiscoveryTests(unittest.TestCase):
    def test_source_repository_is_verified_from_arxiv_id_and_tree(self):
        readme = "# MethodFX\nPaper: https://arxiv.org/abs/2608.12345\nhttps://huggingface.co/team/methodfx"
        encoded = base64.b64encode(readme.encode()).decode()
        responses = {
            (
                "/search/code",
                (("per_page", 10), ("q", '"2608.12345" in:file filename:README.md')),
            ): {"items": [{"repository": {"full_name": "team/methodfx"}}]},
            (
                "/search/repositories",
                (("order", "desc"), ("per_page", 10), ("q", '"MethodFX" in:name'), ("sort", "updated")),
            ): {"items": []},
            "/repos/team/methodfx": {
                "full_name": "team/methodfx",
                "name": "methodfx",
                "owner": {"login": "team"},
                "default_branch": "main",
                "html_url": "https://github.com/team/methodfx",
                "archived": False,
                "fork": False,
                "license": {"spdx_id": "MIT", "name": "MIT License"},
            },
            "/repos/team/methodfx/readme": {
                "content": encoded,
                "html_url": "https://github.com/team/methodfx/blob/main/README.md",
            },
            (
                "/repos/team/methodfx/git/trees/main",
                (("recursive", 1),),
            ): {"tree": [{"type": "blob", "path": "methodfx/model.py"}, {"type": "blob", "path": "LICENSE"}]},
            "/repos/team/methodfx/license": {
                "html_url": "https://github.com/team/methodfx/blob/main/LICENSE"
            },
        }
        data = {
            "generatedAt": "2026-08-28T01:00:00+00:00",
            "candidates": [candidate()],
        }
        enriched = discover_resources.enrich_candidates(data, FakeGitHubClient(responses))
        search = enriched["candidates"][0]["resourceSearch"]
        self.assertEqual(search["checkedAt"], "2026-08-28")
        self.assertEqual(search["resource"]["kind"], "source")
        self.assertEqual(search["resource"]["matchedBy"], "arxiv-id")
        self.assertEqual(search["resource"]["license"]["spdx"], "MIT")
        self.assertEqual(search["resource"]["checkpointUrls"], ["https://huggingface.co/team/methodfx"])

    def test_readme_only_repository_is_a_project_page(self):
        resource = discover_resources.source_files(
            [
                {"type": "blob", "path": "README.md"},
                {"type": "blob", "path": "assets/demo.js"},
            ]
        )
        self.assertEqual(resource, [])

    def test_method_and_author_match_supports_repository_without_readme(self):
        match = discover_resources.relation_match(
            {
                "sourceId": "arxiv:2608.24726",
                "title": "Arbitrary Polygon Oscillator: Generalizing Synthesis",
                "authors": ["Antonio Argentieri"],
            },
            {
                "full_name": "antonioargentieri1/Arbitrary_Polygon_Oscillator",
                "name": "Arbitrary_Polygon_Oscillator",
                "owner": {"login": "antonioargentieri1"},
            },
            "",
            set(),
        )
        self.assertEqual(match, (90, "method-and-author"))


class ResourceMergeTests(unittest.TestCase):
    def test_source_match_completes_paper_and_creates_project(self):
        record = paper()
        resource = {
            "kind": "source",
            "url": "https://github.com/team/methodfx",
            "fullName": "team/methodfx",
            "defaultBranch": "main",
            "readmeUrl": "https://github.com/team/methodfx/blob/main/README.md",
            "matchedBy": "arxiv-id",
            "matchScore": 110,
            "codeFileCount": 4,
            "license": {
                "en": "MIT License",
                "zh": "MIT License",
                "status": "identified",
                "spdx": "MIT",
                "evidenceUrl": "https://github.com/team/methodfx/blob/main/LICENSE",
            },
            "checkpointUrls": ["https://huggingface.co/team/methodfx"],
        }
        candidate_record = candidate()
        candidate_record["resourceSearch"] = {
            "status": "matched",
            "checkedAt": "2026-08-28",
            "provider": "github-search",
            "resource": resource,
        }
        additions = {
            "generatedAt": "2026-08-28T01:00:00+00:00",
            "addedCount": 1,
            "papers": [copy.deepcopy(record)],
        }
        papers, projects, updated_additions = merge_resources.merge_resources(
            {"generatedAt": additions["generatedAt"], "candidates": [candidate_record]},
            additions,
            {"schemaVersion": 1, "updatedAt": "2026-08-28", "papers": [record]},
            {"schemaVersion": 3, "updatedAt": "2026-08-01", "projects": []},
        )
        completed = papers["papers"][0]
        self.assertEqual(completed["templateVersion"], 1)
        self.assertEqual(completed["resourceReview"]["status"], "source")
        self.assertIn({"label": "source", "url": "https://github.com/team/methodfx"}, completed["links"])
        self.assertEqual(projects["projects"][0]["relations"]["paperIds"], [record["id"]])
        self.assertEqual(projects["projects"][0]["license"]["spdx"], "MIT")
        self.assertEqual(updated_additions["addedProjectCount"], 1)
        self.assertEqual(updated_additions["projects"][0]["id"], "team-methodfx")

    def test_not_found_is_still_a_complete_resource_review(self):
        record = paper()
        candidate_record = candidate()
        candidate_record["resourceSearch"] = {
            "status": "not-found",
            "checkedAt": "2026-08-28",
            "provider": "github-search",
            "resource": None,
        }
        papers, projects, additions = merge_resources.merge_resources(
            {"generatedAt": "2026-08-28T01:00:00+00:00", "candidates": [candidate_record]},
            {"generatedAt": "2026-08-28T01:00:00+00:00", "addedCount": 1, "papers": [copy.deepcopy(record)]},
            {"schemaVersion": 1, "updatedAt": "2026-08-28", "papers": [record]},
            {"schemaVersion": 3, "updatedAt": "2026-08-01", "projects": []},
        )
        self.assertEqual(papers["papers"][0]["resourceReview"]["status"], "not-found")
        self.assertEqual(projects["projects"], [])
        self.assertEqual(additions["addedProjectCount"], 0)


if __name__ == "__main__":
    unittest.main()
