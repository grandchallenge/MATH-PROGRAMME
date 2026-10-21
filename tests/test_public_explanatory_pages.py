"""Reader-facing pages must be accurate, navigable, and distinct from proof authority."""
import json
import re
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DOCS=ROOT/"docs"


class PublicExplanatoryPagesTests(unittest.TestCase):
    def test_documentary_library_complete_and_pdf_first(self):
        text=(DOCS/"documentaries/index.md").read_text(encoding="utf8")
        manifest=json.loads((DOCS/"documentaries/ARTIFACT_MANIFEST.json").read_text())
        published=manifest["volumes"]
        self.assertEqual(len(published),9)
        self.assertIn("## Read the books",text)
        self.assertLess(text.index("## Read the books"),text.index("## Sources and publication records"))
        self.assertEqual(text.count("[Download PDF ("),8)
        self.assertIn("PDF_RELEASES.json",text)
        self.assertIn("no compiled original PDF exists",text)
        for volume in published:
            with self.subTest(volume=volume["slug"]):
                self.assertIn(f'[Source]({volume["source_record"]})',text)
                self.assertIn(f'[Edition]({volume["edition_record"]})',text)
                self.assertTrue((DOCS/"documentaries"/volume["web_page"]).is_file())
                self.assertTrue((DOCS/"documentaries"/volume["edition_record"]).is_file())
        self.assertIn("The Poincaré volume reconstructs an established theorem",text)
        self.assertIn("do **not** announce solutions",text)
        self.assertIn("The web editions and their illustrated plates are under reconstruction",text)

    def test_current_work_links_and_closed_tasks_not_misrepresented(self):
        text=(DOCS/"CURRENT_WORK.md").read_text()
        for anchor in ['id="bsd-001--literal-p2-inverse-limit-replay"',
                       'id="vgse-001--mechanical-semantics"']:
            self.assertIn(anchor,text)
        self.assertIn("WP60S*, is **closed**",text)
        self.assertIn("The larger [BSD research programme]",text)
        self.assertIn("576-dimensional space",text)
        self.assertIn("four independent ways",text)
        self.assertIn("[#662]",text)
        self.assertIn("is **complete**",text)
        self.assertIn("not necessarily a solved mathematical problem",text)
        for link in ('MATHSOLVE/issues/215','MATHSOLVE/issues/245',
                     'MATH-PROGRAMME/issues/964','MATH-PROGRAMME/issues/1179',
                     'MATH-PROGRAMME/issues/1162','MATH-PROGRAMME/issues/55'):
            self.assertIn(link,text)
        self.assertNotIn("Complete WP60S by one of",text)
        self.assertNotIn("AUTHORIZED_RESEARCH_EXECUTION",text)

    def test_estate_explains_all_eight_domains_and_provenance(self):
        text=(DOCS/"domains/index.md").read_text()
        self.assertEqual(len(re.findall(r"^\| \[",text,re.M)),8)
        for slug in ('union_closed','navier_stokes','hodge','birch_swinnerton_dyer',
                     'poincare_reconstruction','yang_mills','p_vs_np','riemann_hypothesis'):
            self.assertIn(f'({slug}.md)',text)
            self.assertTrue((DOCS/"domains"/f'{slug}.md').is_file())
        self.assertIn("**Solved**; historical reconstruction",text)
        self.assertIn("does **not** mean that GCL has solved",text)
        self.assertIn("blob/main/DOMAIN_REGISTRY.yaml",text)
        self.assertTrue((ROOT/"DOMAIN_REGISTRY.yaml").is_file())

    def test_atlas_explains_stages_before_jargon(self):
        text=(DOCS/"PROGRAMME_ATLAS.md").read_text()
        self.assertIn("# How GCL Studies a Mathematical Question",text)
        for term in ("MATHFORGE","MATHSOLVE","MATHCERT"):
            self.assertIn(term,text)
        self.assertIn("A proof begins with a clear question",text)
        self.assertIn("A formal proof and the ordinary-language claim",text)
        self.assertIn("A counterexample",text)
        self.assertIn("not mathematical implications",text)
        self.assertIn("(assets/claim-state-transition.svg)",text)
        self.assertTrue((DOCS/"assets/claim-state-transition.svg").is_file())

    def test_evidence_boundaries_across_pages(self):
        required={
          "documentaries/index.md":["not mathematical proofs","not announcements"],
          "CURRENT_WORK.md":["No proof or refutation","does **not** establish"],
          "domains/index.md":["open problems","not a proof"],
          "PROGRAMME_ATLAS.md":["do not automatically","does not prove"],
        }
        for file,fragments in required.items():
            text=(DOCS/file).read_text().lower()
            for fragment in fragments:
                self.assertIn(fragment.lower(),text,file)


if __name__=="__main__":
    unittest.main()
