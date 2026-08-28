import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "automation"))

import summarize_weekly_update  # noqa: E402
import validate_data  # noqa: E402


class WeeklyUpdateTests(unittest.TestCase):
    def setUp(self):
        self.document = {
            "schemaVersion": 1,
            "publishedAt": "2026-08-28",
            "counts": {"papers": 1, "projects": 0, "datasets": 0},
            "headline": {"en": "A useful new effect paper", "zh": "本周新增一篇实用音效论文"},
            "summary": {
                "en": "This update adds one practical paper about controllable audio effects.",
                "zh": "本周新增一篇关于可控音效的实用论文。",
            },
            "highlights": [
                {
                    "type": "paper",
                    "id": "paper-1",
                    "note": {
                        "en": "The method connects a clear production task with reproducible evaluation.",
                        "zh": "这项工作把明确的制作任务与可复现评测连接起来。",
                    },
                }
            ],
        }

    def validate(self, document):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "weekly-update.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            return validate_data.validate_weekly_update(path, {"paper-1"}, {"project-1"}, {"dataset-1"})

    def test_validator_accepts_linked_highlight(self):
        self.assertEqual(self.validate(self.document), 1)

    def test_validator_rejects_unknown_highlight(self):
        invalid = copy.deepcopy(self.document)
        invalid["highlights"][0]["id"] = "invented-paper"
        with self.assertRaisesRegex(ValueError, "id is unknown"):
            self.validate(invalid)

    def test_validator_rejects_highlight_that_conflicts_with_counts(self):
        invalid = copy.deepcopy(self.document)
        invalid["counts"] = {"papers": 0, "projects": 1, "datasets": 0}
        with self.assertRaisesRegex(ValueError, "conflicts with weekly counts"):
            self.validate(invalid)

    def test_summary_builder_uses_only_verified_ids(self):
        additions = {
            "generatedAt": "2026-08-28T01:00:00+00:00",
            "addedCount": 1,
            "papers": [
                {
                    "id": "paper-1",
                    "title": "A Useful Audio Effect",
                    "areas": ["audio-effects"],
                    "summary": {"en": "A factual paper summary.", "zh": "一条事实性论文简介。"},
                    "aiAssessment": {"rating": "standard", "rationale": {"en": "", "zh": ""}},
                }
            ],
        }
        ai_summary = {
            "headline": self.document["headline"],
            "summary": self.document["summary"],
            "highlights": [{"paperId": "paper-1", "note": self.document["highlights"][0]["note"]}],
        }
        weekly = summarize_weekly_update.build_weekly_update(additions, ai_summary)
        self.assertEqual(weekly["publishedAt"], "2026-08-28")
        self.assertEqual(weekly["counts"], {"papers": 1, "projects": 0, "datasets": 0})
        self.assertEqual(weekly["highlights"][0]["id"], "paper-1")

        invalid = copy.deepcopy(ai_summary)
        invalid["highlights"][0]["paperId"] = "invented-paper"
        with self.assertRaisesRegex(ValueError, "unknown or duplicated"):
            summarize_weekly_update.build_weekly_update(additions, invalid)

    def test_formal_schema_is_valid_json(self):
        schema = json.loads((ROOT / "schemas" / "weekly-update-v1.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["properties"]["schemaVersion"]["const"], 1)


if __name__ == "__main__":
    unittest.main()
