"""Dated official prize status must not silently promote unrelated GCL claims."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOMAINS = {
    "navier_stokes": "Active",
    "poincare_reconstruction": "Solved",
    "riemann_hypothesis": "Unsolved",
    "hodge": "Unsolved",
    "birch_swinnerton_dyer": "Unsolved",
    "p_vs_np": "Unsolved",
    "yang_mills": "Unsolved",
}


class MillenniumPublicStatusTests(unittest.TestCase):
    def test_all_seven_have_attributed_dated_classifications(self):
        page = (DOCS / "MILLENNIUM_PRIZE_STATUS.md").read_text()
        self.assertIn("Last checked against primary sources: 20 October 2026", page)
        for name, status in DOMAINS.items():
            with self.subTest(domain=name):
                self.assertIn(f"(domains/{name}.md)", page)
                text = (DOCS / "domains" / f"{name}.md").read_text()
                self.assertIn("**Millennium status, 20 October 2026:**", text)
                self.assertIn(f"**{status}**", text)
                self.assertIn("../MILLENNIUM_PRIZE_STATUS.md", text)
        self.assertEqual(sum(1 for line in page.splitlines() if line.startswith("| **") and "(domains/" in line), 7)

    def test_clay_authority_not_confused_with_announced_proof(self):
        page = (DOCS / "MILLENNIUM_PRIZE_STATUS.md").read_text()
        for source in (
            "https://www.claymath.org/Millennium%20Problems/",
            "https://www.claymath.org/news/navier-stokes-announcement/",
            "https://openai.com/index/navier-stokes-solution/",
        ):
            self.assertIn(source, page)
        self.assertIn("8 September 2026", page)
        self.assertIn("11 September", page)
        self.assertIn("Active; announced resolution under evaluation", page)
        self.assertIn("has **not** yet changed to", page)
        self.assertIn("GCL has not independently certified", page)
        self.assertIn("NS-CI-001", page)
        self.assertIn("separate", page)

    def test_announced_partial_results_do_not_promote_millennium_conjectures(self):
        page = (DOCS / "MILLENNIUM_PRIZE_STATUS.md").read_text()
        self.assertIn("Re(s) > 7/8", page)
        self.assertIn("Re(s) = 1/2", page)
        self.assertIn("complex multiplication", page)
        self.assertIn("restricted class", page)
        self.assertIn("https://github.com/openai/math", page)
        self.assertIn("Unsolved", page)

    def test_public_entry_points_and_navier_historical_reading_edition(self):
        nav = (ROOT / "mkdocs.yml").read_text()
        self.assertIn("Millennium Prize Problems (October 2026): MILLENNIUM_PRIZE_STATUS.md", nav)
        for p in ("index.md", "SHOWCASE.md", "PROGRAMME_ATLAS.md"):
            self.assertIn("MILLENNIUM_PRIZE_STATUS", (DOCS / p).read_text())
        for p in ("domains/index.md", "documentaries/index.md"):
            self.assertIn("../MILLENNIUM_PRIZE_STATUS.md", (DOCS / p).read_text())
        book = (DOCS / "documentaries/navier_stokes.md").read_text()
        self.assertIn("Important update · 20 October 2026", book)
        self.assertIn("its separate unforced critical-integrability investigation remains open", book)
        self.assertIn("Older references to an", book)
        self.assertIn("../MILLENNIUM_PRIZE_STATUS/", book)
        self.assertIn("Clay", book)
        assert "NS-CI-001" in (DOCS / "domains/navier_stokes.md").read_text()


if __name__ == "__main__":
    unittest.main()
