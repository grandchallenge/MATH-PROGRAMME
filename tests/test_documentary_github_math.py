"""Source-locked seven-documentary GitHub mathematics reader regression."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from ci.generate_documentary_github_math import NAMES, generate
from ci.math_markdown_gate import issues

class GitHubDocumentaryMath(unittest.TestCase):
    def test_exact_source_math_parity_and_generator_freshness(self):
        for name in NAMES:
            with self.subTest(documentary=name):
                src,s,dest,text,n=generate(name)
                self.assertEqual(src.read_text(encoding="utf-8"),s)
                self.assertEqual(dest.read_text(encoding="utf-8"),text)
                self.assertGreater(n,5)
                self.assertTrue(text.startswith("# "))
                self.assertIn("illustrated documentary",text)
                self.assertIn("No solution claimed" if name=="riemann" else "Source status:",text)
                self.assertNotIn("<div",text)
                self.assertNotIn("<script",text)

    def test_strict_github_math_source_syntax(self):
        for name in NAMES:
            with self.subTest(documentary=name):
                _,_,_,text,_=generate(name)
                self.assertEqual(issues(text),[],name)

    def test_github_parser_adversarial_tex_and_link_boundaries(self):
        # GitHub's Markdown layer consumes cardinality escapes and norm bars;
        # unsupported math inside links or at word boundaries renders as text.
        bsd=generate("bsd")[3]
        hodge=generate("hodge")[3]
        ns=generate("navier_stokes")[3]
        self.assertIn(r"\\#E(",bsd)
        self.assertIn(r"\\#E_5(",bsd)
        self.assertIn(r"\\#\mathop",bsd)
        self.assertIn(r"\Vert{}u",ns)
        self.assertNotIn(r"\|",ns)
        self.assertIn("codimension- $p$",hodge)
        self.assertNotIn("codimension-\u200b$p$",hodge)
        self.assertIn("([source](https://doi.org/10.1007/BF01388809))",bsd)
        for name in NAMES:
            text=generate(name)[3]
            self.assertNotIn("\u200b$",text)
            self.assertNotIn("$\u200b",text)

    def test_every_public_documentary_links_to_its_reader(self):
        for name in NAMES:
            with self.subTest(documentary=name):
                path=ROOT/"docs"/"documentaries"/f"{name}.md"
                source=path.read_text(encoding="utf-8")
                self.assertEqual(source.count(f"github_math/{name}.md"),1)
                self.assertIn("gcl-monograph",source)
                self.assertIn("data-reader-section",source)

    def test_math_reader_has_all_sections_and_figures(self):
        for name in NAMES:
            with self.subTest(documentary=name):
                src,_,dest,text,_=generate(name)
                self.assertGreaterEqual(text.count("\n## "),7)
                self.assertGreaterEqual(text.count("[Illustration]("),4)
                self.assertIn("not independent mathematical",text.lower())
                # Exact source stays canonical. Generated text is deliberately
                # distinct from the figure-heavy raw HTML manuscript.
                self.assertNotEqual(src.read_bytes(),dest.read_bytes())

if __name__=="__main__":
    unittest.main()
