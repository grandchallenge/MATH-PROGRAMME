"""Curated menus must not make archived mathematics or governance vanish."""
from pathlib import Path
import sys
import re
import subprocess
import tempfile
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

    def test_header_tabs_suppression_preserves_pages_and_mobile_navigation(self):
        # Exercise the real pinned Material template in a tiny site with the
        # actual navigation tree, rather than testing only the YAML flag.
        cfg = yaml.safe_load((ROOT / "mkdocs.yml").read_text())
        self.assertEqual(cfg["extra"]["hidden_header_tabs"], ["Results", "Books"])
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            docs = base / "docs"
            for relative in vd.nav_leaves(cfg["nav"]):
                path = docs / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# Sample page\n")
            config = {
                "site_name": "Navigation test",
                "nav": cfg["nav"],
                "theme": {
                    "name": cfg["theme"]["name"],
                    "custom_dir": str(ROOT / cfg["theme"]["custom_dir"]),
                    "features": cfg["theme"]["features"],
                },
                "extra": cfg["extra"],
            }
            (base / "mkdocs.yml").write_text(yaml.safe_dump(config))
            subprocess.run([sys.executable, "-m", "mkdocs", "build", "--quiet"],
                           cwd=base, check=True, capture_output=True, text=True)
            for rel in ["index.html", "SHOWCASE/index.html", "documentaries/index.html",
                        "pnp_above/primer/index.html"]:
                html = (base / "site" / rel).read_text()
                tabs = re.search(r'<nav class="md-tabs"[^>]*>(.*?)</nav>', html, re.S)
                self.assertIsNotNone(tabs, rel)
                titles = [re.sub(r"<[^>]*>", "", item).strip() for item in
                          re.findall(r'<a[^>]*class="md-tabs__link"[^>]*>(.*?)</a>',
                                     tabs.group(1), re.S)]
                self.assertEqual(titles, ["Home", "Explore Mathematics", "Current Research",
                                          "About GCL", "Reference"], rel)
                # The sidebar/mobile tree still contains both sections.
                self.assertRegex(html, r">\s*Results\s*<")
                self.assertRegex(html, r">\s*Books\s*<")

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
