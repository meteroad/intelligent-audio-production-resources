import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "automation"))

import validate_data  # noqa: E402


class DatasetSchemaTests(unittest.TestCase):
    def setUp(self):
        self.document = {
            "schemaVersion": 1,
            "updatedAt": "2026-08-26",
            "datasets": [
                {
                    "id": "example-dataset",
                    "name": "Example Dataset",
                    "description": {"en": "Example audio data.", "zh": "示例音频数据。"},
                    "scale": {"en": "Ten paired clips.", "zh": "十组配对片段。"},
                    "areas": ["audio-effects"],
                    "taxonomy": {
                        "tasks": ["effect-modeling"],
                        "effects": ["distortion"],
                        "contentTypes": ["dry-wet-pairs"],
                        "evidence": ["https://example.com/dataset"],
                    },
                    "access": {
                        "status": "direct-download",
                        "evidenceUrl": "https://example.com/dataset",
                    },
                    "license": {
                        "en": "CC-BY-4.0",
                        "zh": "CC-BY-4.0",
                        "status": "identified",
                        "spdx": "CC-BY-4.0",
                        "evidenceUrl": "https://example.com/license",
                    },
                    "relations": {
                        "papers": [{"id": "example-paper", "evidenceUrl": "https://example.com/paper"}],
                        "projects": [{"id": "example-project", "evidenceUrl": "https://example.com/project"}],
                    },
                    "lastVerified": "2026-08-26",
                    "links": [{"label": "dataset", "url": "https://example.com/dataset"}],
                }
            ],
        }

    def validate(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "datasets.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            return validate_data.validate_datasets(path, {"example-paper"}, {"example-project"})

    def test_validator_accepts_dataset_document(self):
        self.assertEqual(self.validate(self.document), 1)

    def test_validator_rejects_unknown_relation(self):
        invalid = copy.deepcopy(self.document)
        invalid["datasets"][0]["relations"]["projects"][0]["id"] = "missing-project"
        with self.assertRaisesRegex(ValueError, "id is unknown"):
            self.validate(invalid)

    def test_validator_requires_relation_evidence(self):
        invalid = copy.deepcopy(self.document)
        invalid["datasets"][0]["relations"]["papers"][0]["evidenceUrl"] = None
        with self.assertRaisesRegex(ValueError, "valid HTTPS URL"):
            self.validate(invalid)

    def test_validator_requires_reviewed_access_evidence(self):
        invalid = copy.deepcopy(self.document)
        invalid["datasets"][0]["access"]["evidenceUrl"] = None
        with self.assertRaisesRegex(ValueError, "valid HTTPS URL"):
            self.validate(invalid)

    def test_validator_rejects_identified_license_without_evidence(self):
        invalid = copy.deepcopy(self.document)
        invalid["datasets"][0]["license"]["evidenceUrl"] = None
        with self.assertRaisesRegex(ValueError, "evidenceUrl is required"):
            self.validate(invalid)

    def test_formal_schema_is_valid_json(self):
        schema = json.loads((ROOT / "schemas" / "datasets-v1.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["properties"]["schemaVersion"]["const"], 1)


if __name__ == "__main__":
    unittest.main()
