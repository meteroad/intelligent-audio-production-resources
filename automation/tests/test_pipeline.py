import json
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


AUTOMATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTOMATION_DIR))

import discover_papers  # noqa: E402
import curate_papers  # noqa: E402
import merge_papers  # noqa: E402
import publication_metadata  # noqa: E402
import refresh_impact  # noqa: E402
import refresh_publication_metadata  # noqa: E402


ARXIV_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2608.12345v2</id>
    <updated>2026-08-24T12:00:00Z</updated>
    <published>2026-08-20T12:00:00Z</published>
    <title>  A Neural Audio Effect for Music Production  </title>
    <summary> We introduce a production-oriented audio effect. </summary>
    <author><name>First Author</name></author>
    <author><name>Second Author</name></author>
    <category term="eess.AS" />
    <arxiv:primary_category term="eess.AS" />
    <arxiv:doi>10.1234/example</arxiv:doi>
    <arxiv:comment>Accepted at ISMIR 2026. 8 pages.</arxiv:comment>
  </entry>
</feed>
"""


class DiscoveryTests(unittest.TestCase):
    def test_parse_feed_normalizes_authoritative_metadata(self):
        papers = discover_papers.parse_feed(ARXIV_FEED, "audio-effects")
        self.assertEqual(len(papers), 1)
        paper = papers[0]
        self.assertEqual(paper["sourceId"], "arxiv:2608.12345")
        self.assertEqual(paper["title"], "A Neural Audio Effect for Music Production")
        self.assertEqual(paper["authors"], ["First Author", "Second Author"])
        self.assertEqual(paper["paperUrl"], "https://arxiv.org/abs/2608.12345")
        self.assertEqual(paper["matchedQueries"], ["audio-effects"])
        self.assertEqual(paper["publicationVenue"], "ISMIR 2026")
        self.assertEqual(paper["venueEvidence"], "comment")

    def test_existing_records_include_title_level_deduplication(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "papers.json"
            path.write_text(
                json.dumps(
                    {
                        "papers": [
                            {
                                "title": "Beyond Dry References: Learning Relative Audio Effects",
                                "source": {"type": "manual", "id": "local-paper"},
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            source_ids, titles = discover_papers.existing_records(path)
            self.assertEqual(source_ids, {"local-paper"})
            self.assertIn("beyonddryreferenceslearningrelativeaudioeffects", titles)


class CurationTests(unittest.TestCase):
    def test_deepseek_request_uses_non_thinking_json_mode(self):
        candidate = discover_papers.parse_feed(ARXIV_FEED, "audio-effects")[0]
        request = curate_papers.build_request(
            "Return JSON.",
            {"generatedAt": "2026-08-25T10:00:00", "candidates": [candidate]},
            "deepseek-v4-flash",
        )
        self.assertEqual(request["model"], "deepseek-v4-flash")
        self.assertEqual(request["response_format"], {"type": "json_object"})
        self.assertEqual(request["thinking"], {"type": "disabled"})
        self.assertIn("arxiv:2608.12345", request["messages"][1]["content"])

    def test_review_validation_covers_every_candidate(self):
        candidate = discover_papers.parse_feed(ARXIV_FEED, "audio-effects")[0]
        candidates = {"generatedAt": "2026-08-25T10:00:00", "candidates": [candidate]}
        review = {
            "reviewedAt": "model-generated-value-is-ignored",
            "decisions": [
                {
                    "sourceId": "arxiv:2608.12345",
                    "decision": "exclude",
                    "confidence": "high",
                    "areas": ["audio-effects"],
                    "controlApproaches": ["direct-prediction"],
                    "trackScopes": ["single-track"],
                    "aiAssessment": {
                        "rating": "highlighted",
                        "rationale": {
                            "en": "A rationale that will be cleared for an excluded candidate.",
                            "zh": "这是一条会在候选论文被排除后清空的评价依据。",
                        },
                    },
                    "summary": {"en": "Ignored summary", "zh": "忽略的摘要"},
                    "reason": "Not directly relevant.",
                }
            ],
        }
        validated = curate_papers.validate_review(review, candidates)
        self.assertEqual(validated["reviewedAt"], "2026-08-25")
        self.assertEqual(validated["decisions"][0]["areas"], [])
        self.assertEqual(validated["decisions"][0]["controlApproaches"], [])
        self.assertEqual(validated["decisions"][0]["trackScopes"], [])
        self.assertEqual(
            validated["decisions"][0]["aiAssessment"],
            {"rating": "standard", "rationale": {"en": "", "zh": ""}},
        )
        self.assertEqual(validated["decisions"][0]["summary"], {"en": "", "zh": ""})

    def test_review_rejects_unknown_control_approach(self):
        candidate = discover_papers.parse_feed(ARXIV_FEED, "audio-effects")[0]
        candidates = {"generatedAt": "2026-08-25T10:00:00", "candidates": [candidate]}
        review = {
            "reviewedAt": "model-generated-value-is-ignored",
            "decisions": [
                {
                    "sourceId": "arxiv:2608.12345",
                    "decision": "include",
                    "confidence": "high",
                    "areas": ["audio-effects"],
                    "controlApproaches": ["ordinary-training"],
                    "trackScopes": ["single-track"],
                    "aiAssessment": {"rating": "standard", "rationale": {"en": "", "zh": ""}},
                    "summary": {
                        "en": "Introduces a neural audio effect intended for music production workflows.",
                        "zh": "提出一种面向音乐制作流程的神经音频效果器。",
                    },
                    "reason": "The abstract states a direct production contribution.",
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "Invalid control approaches"):
            curate_papers.validate_review(review, candidates)

    def test_review_rejects_unknown_track_scope(self):
        candidate = discover_papers.parse_feed(ARXIV_FEED, "audio-effects")[0]
        candidates = {"generatedAt": "2026-08-25T10:00:00", "candidates": [candidate]}
        review = {
            "reviewedAt": "model-generated-value-is-ignored",
            "decisions": [
                {
                    "sourceId": "arxiv:2608.12345",
                    "decision": "include",
                    "confidence": "high",
                    "areas": ["audio-effects"],
                    "controlApproaches": ["direct-prediction"],
                    "trackScopes": ["stereo"],
                    "aiAssessment": {"rating": "standard", "rationale": {"en": "", "zh": ""}},
                    "summary": {
                        "en": "Introduces a neural audio effect intended for music production workflows.",
                        "zh": "提出一种面向音乐制作流程的神经音频效果器。",
                    },
                    "reason": "The abstract states a direct production contribution.",
                }
            ],
        }
        with self.assertRaisesRegex(ValueError, "Invalid track scopes"):
            curate_papers.validate_review(review, candidates)


class PublicationMetadataTests(unittest.TestCase):
    def test_submission_comment_is_not_treated_as_acceptance(self):
        venue, evidence = publication_metadata.resolve_publication_venue(
            None,
            "Submitted to ICASSP 2027; under review.",
        )
        self.assertIsNone(venue)
        self.assertIsNone(evidence)

    def test_bare_arxiv_venue_comment_is_accepted(self):
        venue, evidence = publication_metadata.resolve_publication_venue(None, "ISMIR 2025")
        self.assertEqual(venue, "ISMIR 2025")
        self.assertEqual(evidence, "comment")

    def test_bare_journal_target_is_not_treated_as_acceptance(self):
        venue, evidence = publication_metadata.resolve_publication_venue(
            None,
            "JAES, extension of an earlier conference paper.",
        )
        self.assertIsNone(venue)
        self.assertIsNone(evidence)

    def test_comment_without_known_venue_is_ignored(self):
        venue, evidence = publication_metadata.resolve_publication_venue(None, "8 pages and 4 figures")
        self.assertIsNone(venue)
        self.assertIsNone(evidence)

    def test_journal_reference_takes_priority(self):
        venue, evidence = publication_metadata.resolve_publication_venue(
            "Proceedings of ICML, 2026, Seoul, South Korea",
            "Earlier version submitted elsewhere.",
        )
        self.assertEqual(venue, "ICML 2026")
        self.assertEqual(evidence, "journalReference")

    def test_known_doi_resolves_journal(self):
        venue, evidence = publication_metadata.resolve_publication_venue(
            None,
            None,
            "10.17743/jaes.2026.0273",
        )
        self.assertEqual(venue, "JAES")
        self.assertEqual(evidence, "doi")

    def test_semantic_scholar_venue_uses_doi_year(self):
        venue, evidence = publication_metadata.semantic_scholar_venue(
            {
                "venue": "IEEE International Conference on Acoustics, Speech, and Signal Processing",
                "year": 2024,
                "publicationVenue": {
                    "name": "IEEE International Conference on Acoustics, Speech, and Signal Processing",
                    "type": "conference"
                },
                "externalIds": {"DOI": "10.1109/ICASSP49660.2025.10888532"},
            }
        )
        self.assertEqual(venue, "ICASSP 2025")
        self.assertEqual(evidence, "semanticScholar")

    def test_semantic_scholar_journal_uses_record_year(self):
        venue, evidence = publication_metadata.semantic_scholar_venue(
            {
                "venue": "Journal of The Audio Engineering Society",
                "year": 2025,
                "publicationVenue": {
                    "name": "Journal of The Audio Engineering Society",
                    "type": "journal",
                },
                "externalIds": {"DOI": "10.17743/jaes.2022.0212"},
            }
        )
        self.assertEqual(venue, "JAES 2025")
        self.assertEqual(evidence, "semanticScholar")

    def test_semantic_scholar_arxiv_is_not_a_formal_venue(self):
        venue, evidence = publication_metadata.semantic_scholar_venue(
            {"venue": "arXiv.org", "publicationVenue": {"name": "arXiv.org"}, "year": 2025}
        )
        self.assertIsNone(venue)
        self.assertIsNone(evidence)


class MergeTests(unittest.TestCase):
    def test_empty_week_is_a_valid_no_op(self):
        papers = {"schemaVersion": 1, "updatedAt": "2026-08-01", "papers": []}
        merged, added = merge_papers.merge_records(
            {"generatedAt": "2026-08-25T10:00:00", "candidates": []},
            {"reviewedAt": "2026-08-25", "decisions": []},
            papers,
        )
        self.assertEqual(added, 0)
        self.assertEqual(merged, papers)

    def test_only_high_confidence_includes_are_merged(self):
        candidate = discover_papers.parse_feed(ARXIV_FEED, "audio-effects")[0]
        candidates = {"candidates": [candidate]}
        review = {
            "reviewedAt": "2026-08-25",
            "decisions": [
                {
                    "sourceId": "arxiv:2608.12345",
                    "decision": "include",
                    "confidence": "high",
                    "areas": ["audio-effects"],
                    "controlApproaches": ["direct-prediction"],
                    "trackScopes": ["single-track"],
                    "aiAssessment": {
                        "rating": "highlighted",
                        "rationale": {
                            "en": "The method combines a clear contribution with substantive validation and practical value.",
                            "zh": "该方法兼具明确贡献、充分验证与实际使用价值。",
                        },
                    },
                    "summary": {
                        "en": "Introduces a neural audio effect intended for music production workflows.",
                        "zh": "提出一种面向音乐制作流程的神经音频效果器。",
                    },
                    "reason": "The abstract states a direct production contribution.",
                }
            ],
        }
        papers = {"schemaVersion": 1, "updatedAt": "2026-08-01", "papers": []}
        merged, added = merge_papers.merge_records(candidates, review, papers)
        self.assertEqual(added, 1)
        self.assertEqual(merged["papers"][0]["title"], candidate["title"])
        self.assertEqual(merged["papers"][0]["authors"], candidate["authors"])
        self.assertEqual(merged["papers"][0]["curation"], "agent")
        self.assertEqual(merged["papers"][0]["controlApproaches"], ["direct-prediction"])
        self.assertEqual(merged["papers"][0]["trackScopes"], ["single-track"])
        self.assertEqual(merged["papers"][0]["aiAssessment"]["rating"], "highlighted")
        self.assertEqual(merged["papers"][0]["impact"]["status"], "not-assessed")
        self.assertEqual(merged["papers"][0]["venue"], "ISMIR 2026")
        self.assertEqual(merged["papers"][0]["links"][1]["url"], "https://doi.org/10.1234/example")
        additions = merge_papers.build_additions(
            {"generatedAt": "2026-08-25T10:00:00", **candidates},
            merged,
            set(),
        )
        self.assertEqual(additions["addedCount"], 1)
        self.assertEqual(additions["papers"][0]["id"], "arxiv-2608-12345")

    def test_unknown_source_id_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "unknown sourceId"):
            merge_papers.merge_records(
                {"candidates": []},
                {
                    "reviewedAt": "2026-08-25",
                    "decisions": [
                        {
                            "sourceId": "arxiv:invented",
                            "decision": "exclude",
                            "confidence": "high",
                            "areas": [],
                            "controlApproaches": [],
                            "trackScopes": [],
                            "aiAssessment": {"rating": "standard", "rationale": {"en": "", "zh": ""}},
                            "summary": {"en": "", "zh": ""},
                            "reason": "Not relevant.",
                        }
                    ],
                },
                {"schemaVersion": 1, "updatedAt": "2026-08-01", "papers": []},
            )

    def test_duplicate_areas_are_rejected(self):
        candidate = discover_papers.parse_feed(ARXIV_FEED, "audio-effects")[0]
        review = {
            "decisions": [
                {
                    "sourceId": "arxiv:2608.12345",
                    "decision": "include",
                    "confidence": "high",
                    "areas": ["audio-effects", "audio-effects"],
                    "controlApproaches": [],
                    "trackScopes": ["single-track"],
                    "aiAssessment": {"rating": "standard", "rationale": {"en": "", "zh": ""}},
                    "summary": {
                        "en": "Introduces a neural audio effect intended for music production workflows.",
                        "zh": "提出一种面向音乐制作流程的神经音频效果器。",
                    },
                    "reason": "The abstract states a direct production contribution.",
                }
            ]
        }
        with self.assertRaisesRegex(ValueError, "Invalid areas"):
            merge_papers.merge_records(
                {"candidates": [candidate]},
                review,
                {"schemaVersion": 1, "updatedAt": "2026-08-01", "papers": []},
            )

    def test_missing_candidate_decision_is_rejected(self):
        candidate = discover_papers.parse_feed(ARXIV_FEED, "audio-effects")[0]
        with self.assertRaisesRegex(ValueError, "did not review every candidate"):
            merge_papers.merge_records(
                {"candidates": [candidate]},
                {"reviewedAt": "2026-08-25", "decisions": []},
                {"schemaVersion": 1, "updatedAt": "2026-08-01", "papers": []},
            )


class PublicationRefreshTests(unittest.TestCase):
    def test_refresh_upgrades_arxiv_venue_and_adds_doi(self):
        papers = {
            "schemaVersion": 1,
            "updatedAt": "2026-08-01",
            "papers": [
                {
                    "id": "arxiv-2608-12345",
                    "source": {"type": "arxiv", "id": "arxiv:2608.12345"},
                    "venue": "arXiv",
                    "links": [{"label": "paper", "url": "https://arxiv.org/abs/2608.12345"}],
                    "lastVerified": "2026-08-01",
                }
            ],
        }
        metadata = [
            {
                "sourceId": "arxiv:2608.12345",
                "publicationVenue": "ISMIR 2026",
                "doi": "10.1234/example",
            }
        ]
        refreshed, changed = refresh_publication_metadata.refresh_records(papers, metadata, "2026-08-25")
        self.assertEqual(changed, 1)
        self.assertEqual(refreshed["papers"][0]["venue"], "ISMIR 2026")
        self.assertEqual(refreshed["papers"][0]["links"][-1]["label"], "doi")
        self.assertEqual(refreshed["updatedAt"], "2026-08-25")


class ImpactRefreshTests(unittest.TestCase):
    def test_identifier_prefers_arxiv_and_supports_doi(self):
        self.assertEqual(
            refresh_impact.paper_identifier({"source": {"type": "arxiv", "id": "arxiv:2401.12345"}}),
            "ARXIV:2401.12345",
        )
        self.assertEqual(
            refresh_impact.paper_identifier(
                {
                    "source": {"type": "manual", "id": "manual"},
                    "links": [{"label": "doi", "url": "https://doi.org/10.1234%2Fexample"}],
                }
            ),
            "DOI:10.1234/example",
        )

    def test_year_cohort_marks_top_twenty_percent_with_minimum(self):
        papers = {
            "schemaVersion": 1,
            "updatedAt": "2026-08-01",
            "papers": [
                {"id": f"paper-{index}", "year": 2024, "source": {"type": "arxiv", "id": f"arxiv:2401.0000{index}"}}
                for index in range(1, 6)
            ],
        }
        records = {
            f"ARXIV:2401.0000{index}": {
                "paperId": str(index),
                "citationCount": citations,
                "influentialCitationCount": index,
                "url": f"https://www.semanticscholar.org/paper/{index}",
            }
            for index, citations in enumerate([20, 10, 5, 3, 1], start=1)
        }
        refreshed, changed = refresh_impact.refresh_records(papers, records, "2026-08-27")
        self.assertEqual(changed, 5)
        self.assertEqual(refreshed["papers"][0]["impact"]["status"], "high-impact")
        self.assertEqual(refreshed["papers"][1]["impact"]["status"], "standard")
        self.assertEqual(refreshed["papers"][0]["impact"]["yearRank"], 1)
        self.assertEqual(refreshed["papers"][0]["impact"]["cohortSize"], 5)

    def test_current_year_is_too_recent_and_missing_record_is_not_assessed(self):
        papers = {
            "papers": [
                {"id": "new", "year": 2026, "source": {"type": "arxiv", "id": "arxiv:2601.00001"}},
                {"id": "old", "year": 2020, "source": {"type": "manual", "id": "manual"}, "links": []},
            ]
        }
        refreshed, _ = refresh_impact.refresh_records(papers, {}, "2026-08-27")
        self.assertEqual(refreshed["papers"][0]["impact"]["status"], "too-recent")
        self.assertEqual(refreshed["papers"][1]["impact"]["status"], "not-assessed")

    def test_refresh_is_requested_only_when_measurement_is_old(self):
        papers = {"papers": [{"impact": {"measuredAt": "2026-08-10"}}]}
        self.assertFalse(refresh_impact.impact_is_stale(papers, date(2026, 8, 27), 28))
        self.assertTrue(refresh_impact.impact_is_stale(papers, date(2026, 9, 7), 28))


if __name__ == "__main__":
    unittest.main()
