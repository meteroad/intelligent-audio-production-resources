import sys
import unittest
from pathlib import Path


AUTOMATION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AUTOMATION_DIR))

import sync_landing_stats  # noqa: E402


class SyncLandingStatsTests(unittest.TestCase):
    def test_sync_counts_updates_each_fallback_value(self):
        html = """
<strong id="hero-project-count">1</strong>
<strong id="hero-dataset-count">2</strong>
<strong id="hero-paper-count">3</strong>
"""
        updated = sync_landing_stats.sync_counts(
            html,
            {"projects": 72, "datasets": 23, "papers": 115},
        )
        self.assertIn('id="hero-project-count">72<', updated)
        self.assertIn('id="hero-dataset-count">23<', updated)
        self.assertIn('id="hero-paper-count">115<', updated)

    def test_sync_counts_rejects_missing_element(self):
        with self.assertRaisesRegex(ValueError, "hero-project-count"):
            sync_landing_stats.sync_counts(
                '<strong id="hero-paper-count">3</strong>',
                {"projects": 1, "datasets": 2, "papers": 3},
            )

    def test_sync_readme_counts_updates_catalogue_line(self):
        readme = "**1 papers · 2 verified projects · 3 datasets · 4 reference collections**"
        updated = sync_landing_stats.sync_readme_counts(
            readme,
            {"projects": 73, "datasets": 23, "papers": 119, "resources": 3},
        )
        self.assertEqual(
            updated,
            "**119 papers · 73 verified projects · 23 datasets · 3 reference collections**",
        )

    def test_sync_readme_counts_rejects_missing_line(self):
        with self.assertRaisesRegex(ValueError, "README.md"):
            sync_landing_stats.sync_readme_counts(
                "No catalogue counts here.",
                {"projects": 1, "datasets": 2, "papers": 3, "resources": 4},
            )


if __name__ == "__main__":
    unittest.main()
