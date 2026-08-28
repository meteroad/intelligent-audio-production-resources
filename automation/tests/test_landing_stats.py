import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class LandingStatsTests(unittest.TestCase):
    def test_static_landing_counts_match_catalogue_data(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        projects = json.loads((ROOT / "data/projects.json").read_text(encoding="utf-8"))
        datasets = json.loads((ROOT / "data/datasets.json").read_text(encoding="utf-8"))
        papers = json.loads((ROOT / "data/papers.json").read_text(encoding="utf-8"))
        expected = {
            "hero-project-count": len(projects["projects"]),
            "hero-dataset-count": len(datasets["datasets"]),
            "hero-paper-count": len(papers["papers"]),
        }

        for element_id, count in expected.items():
            match = re.search(rf'id="{element_id}">(\d+)<', html)
            self.assertIsNotNone(match, f"missing static count: {element_id}")
            self.assertEqual(int(match.group(1)), count, f"stale static count: {element_id}")

    def test_spatial_field_map_links_to_filtered_papers(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertRegex(
            html,
            r'<a class="field-map-link" href="#papers" data-paper-area="spatial-audio">',
        )

    def test_weekly_update_appears_before_field_map(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertLess(html.index('id="weekly-update"'), html.index('id="scope"'))
        weekly = json.loads((ROOT / "data" / "weekly-update.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(weekly["highlights"]), 1)


if __name__ == "__main__":
    unittest.main()
