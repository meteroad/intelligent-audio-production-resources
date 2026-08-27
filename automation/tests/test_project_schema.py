import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "automation"))

import migrate_projects_v3  # noqa: E402
import validate_data  # noqa: E402


class ProjectSchemaMigrationTests(unittest.TestCase):
    def setUp(self):
        self.v2 = {
            "schemaVersion": 2,
            "projects": [
                {
                    "id": "example-project",
                    "name": "Example Project",
                    "description": {"en": "Example project.", "zh": "示例项目。"},
                    "areas": ["audio-effects"],
                    "license": {"en": "MIT", "zh": "MIT"},
                    "lastVerified": "2026-08-25",
                    "links": [
                        {"label": "source", "url": "https://github.com/example/Project.git"},
                        {"label": "checkpoint", "url": "https://example.com/checkpoint"},
                    ],
                }
            ],
        }
        self.papers = {
            "schemaVersion": 1,
            "updatedAt": "2026-08-25",
            "papers": [
                {
                    "id": "example-paper",
                    "links": [{"label": "source", "url": "https://github.com/Example/project"}],
                }
            ],
        }
        self.paper_resource_urls = {
            "example-paper": {"github.com/example/project"},
        }

    def test_upgrade_is_deterministic(self):
        first = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        second = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        self.assertEqual(first, second)
        self.assertEqual(first["schemaVersion"], 3)
        self.assertEqual(first["updatedAt"], "2026-08-25")

    def test_upgrade_and_downgrade_round_trip(self):
        upgraded = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        self.assertEqual(migrate_projects_v3.downgrade_document(upgraded), self.v2)

    def test_upgrade_records_only_link_evidence(self):
        project = migrate_projects_v3.upgrade_document(self.v2, self.papers)["projects"][0]
        self.assertEqual(project["taxonomy"], {"tasks": [], "effects": [], "reviewStatus": "not-reviewed", "evidence": []})
        self.assertEqual(project["availability"]["source"]["status"], "linked")
        self.assertEqual(project["availability"]["checkpoint"]["status"], "linked")
        self.assertEqual(project["availability"]["inference"], {"status": "not-reviewed", "evidence": []})
        self.assertEqual(project["availability"]["training"], {"status": "not-reviewed", "evidence": []})
        self.assertEqual(project["availability"]["dataset"], {"status": "not-reviewed", "evidence": []})

    def test_exact_github_url_match_creates_relation(self):
        project = migrate_projects_v3.upgrade_document(self.v2, self.papers)["projects"][0]
        self.assertEqual(project["relations"]["paperIds"], ["example-paper"])
        self.assertEqual(project["relations"]["reviewStatus"], "exact-link-match")

    def test_license_migration_does_not_guess_ambiguous_spdx(self):
        cases = {
            "MIT": ("identified", "MIT"),
            "BSD": ("identified", None),
            "Custom/other; see repository terms": ("custom", None),
            "No license file verified": ("not-verified", None),
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                result = migrate_projects_v3.license_metadata({"en": name, "zh": name})
                self.assertEqual((result["status"], result["spdx"]), expected)

    def test_validator_accepts_migrated_document(self):
        migrated = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(json.dumps(migrated), encoding="utf-8")
            self.assertEqual(
                validate_data.validate_projects(path, {"example-paper"}, self.paper_resource_urls),
                1,
            )

    def test_validator_accepts_spatial_taxonomy(self):
        migrated = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        migrated["projects"][0]["areas"] = ["spatial-audio"]
        migrated["projects"][0]["taxonomy"] = {
            "tasks": ["spatial-rendering", "hrtf-personalization"],
            "effects": ["filtering", "stereo"],
            "reviewStatus": "reviewed",
            "evidence": ["https://example.com/project"],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(json.dumps(migrated), encoding="utf-8")
            self.assertEqual(
                validate_data.validate_projects(path, {"example-paper"}, self.paper_resource_urls),
                1,
            )

    def test_validator_rejects_claim_without_evidence(self):
        migrated = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        migrated["projects"][0]["availability"]["training"] = {
            "status": "documented",
            "evidence": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(json.dumps(migrated), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "requires evidence"):
                validate_data.validate_projects(path, {"example-paper"}, self.paper_resource_urls)

    def test_validator_rejects_taxonomy_without_evidence(self):
        migrated = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        migrated["projects"][0]["taxonomy"] = {
            "tasks": ["effect-modeling"],
            "effects": ["distortion"],
            "reviewStatus": "reviewed",
            "evidence": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(json.dumps(migrated), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "reviewed taxonomy requires evidence"):
                validate_data.validate_projects(path, {"example-paper"}, self.paper_resource_urls)

    def test_validator_rejects_unknown_paper_relation(self):
        migrated = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        invalid = copy.deepcopy(migrated)
        invalid["projects"][0]["relations"]["paperIds"] = ["missing-paper"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(json.dumps(invalid), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unknown papers"):
                validate_data.validate_projects(path, {"example-paper"}, self.paper_resource_urls)

    def test_validator_rechecks_exact_link_relation(self):
        migrated = migrate_projects_v3.upgrade_document(self.v2, self.papers)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "projects.json"
            path.write_text(json.dumps(migrated), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "no exact resource URL match"):
                validate_data.validate_projects(
                    path,
                    {"example-paper"},
                    {"example-paper": {"github.com/unrelated/project"}},
                )

    def test_formal_schema_is_valid_json(self):
        schema = json.loads((ROOT / "schemas" / "projects-v3.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["properties"]["schemaVersion"]["const"], 3)


if __name__ == "__main__":
    unittest.main()
