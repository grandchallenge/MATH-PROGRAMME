"""Curated menus must not make archived mathematics or governance vanish."""
from pathlib import Path
import sys
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
import validate_docs as vd

class CuratedNavigationTests(unittest.TestCase):
    def test_compact_primary_navigation(self):
        cfg = yaml.safe_load((ROOT / "mkdocs.yml").read_text())
        sections = cfg["nav"]
        entries = vd.nav_leaves(sections)
        self.assertEqual(len(sections), 7)
        self.assertLessEqual(len(entries), 55)
        self.assertEqual(len(entries), len(set(entries)))
        for section in sections:
            for name, content in section.items():
                self.assertLessEqual(len(vd.nav_leaves(content)), 12, name)

    def test_all_pages_discoverable_and_no_reference_duplication(self):
        nav = vd.nav_documents()
        all_docs = vd.docs_documents()
        self.assertFalse(vd.curated_navigation_errors(nav, all_docs))
        self.assertEqual(nav | (all_docs - nav), all_docs)
        self.assertGreater(len(all_docs - nav), 150)
        for critical in vd.REQUIRED_PUBLIC_ENTRIES:
            self.assertIn(critical, nav)

    def test_high_value_sections_in_sensible_locations(self):
        cfg = yaml.safe_load((ROOT / "mkdocs.yml").read_text())
        pages = {next(iter(section)): vd.nav_leaves(section) for section in cfg["nav"]}
        self.assertIn("MILLENNIUM_PRIZE_STATUS.md", pages["Explore Mathematics"])
        self.assertIn("erdos/index.md", pages["Explore Mathematics"])
        self.assertIn("CURRENT_WORK.md", pages["Current Research"])
        self.assertIn("SHOWCASE.md", pages["Results"])
        self.assertIn("documentaries/index.md", pages["Books"])
        self.assertIn("PROGRAMME_ATLAS.md", pages["About GCL"])
        self.assertIn("REFERENCE_LIBRARY.md", pages["Reference"])

    def test_historical_links_preserved_not_promoted(self):
        nav = vd.nav_documents()
        examples = [
            "governance/ADMINISTRATIVE_MAINTENANCE_PLAN.md",
            "decisions/ADR-0002_UNION_CLOSED_AGENT_COUNCIL_PILOT.md",
            "documentaries/github_math/navier_stokes.md",
            "monographs/type-theory-series/HANDOFF_PROMPT.md",
        ]
        contents = "\n".join((ROOT/"docs"/v).read_text() for v in vd.REFERENCE_INDEXES)
        for rel in examples:
            with self.subTest(path=rel):
                self.assertTrue((ROOT / "docs" / rel).is_file())
                self.assertNotIn(rel, nav)
                self.assertIn("../"+rel, contents)

    def test_introduced_missing_page_would_fail_closed(self):
        nav = vd.nav_documents()
        all_docs = vd.docs_documents()
        example = "governance/ADMINISTRATIVE_MAINTENANCE_PLAN.md"
        original = vd.local_link_targets
        def pretend_link_removed(text):
            return [link for link in original(text) if example not in link]
        from unittest.mock import patch
        with patch.object(vd, "local_link_targets", side_effect=pretend_link_removed):
            errors=vd.curated_navigation_errors(nav,all_docs)
        self.assertTrue(any(example in issue and "neither in curated menu" in issue for issue in errors))

if __name__=="__main__":
    unittest.main()
