"""Hostile and positive tests for pre-admission mathematical Markdown syntax."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
from math_markdown_gate import issues, newly_introduced


class MathematicalMarkdownGateTests(unittest.TestCase):
    def kinds(self, text):
        return {row[0] for row in issues(text)}

    def test_valid_display_and_inline(self):
        text = "Prose with $x+y$.\n\n$$\n\\frac{a}{b}=c\n$$\n\nNext paragraph.\n"
        self.assertEqual([], issues(text))

    def test_blank_line_before_display_required(self):
        self.assertIn("display-opening-needs-blank-line",
                      self.kinds("Prose.\n$$\nx=y\n$$\n\nEnd.\n"))

    def test_blank_line_after_display_required(self):
        self.assertIn("display-closing-needs-blank-line",
                      self.kinds("Prose.\n\n$$\nx=y\n$$\nNext.\n"))

    def test_inline_double_dollar_rejected(self):
        self.assertIn("display-delimiter-not-on-own-line",
                      self.kinds("Formula $$x+y$$ embedded in prose."))

    def test_unpaired_dollar_rejected(self):
        self.assertIn("unpaired-inline-dollar",
                      self.kinds("A broken $x+y expression"))

    def test_prose_adjacency_rejected(self):
        self.assertIn("inline-math-touching-prose",
                      self.kinds("The fixed-$u$ regime.\n"))

    def test_disallowed_operator_in_display(self):
        self.assertIn("unsupported-operatorname",
                      self.kinds("\n$$\n\\operatorname{Var}(X)\n$$\n"))

    def test_legacy_delimiter(self):
        self.assertIn("legacy-inline-delimiter",
                      self.kinds(r"Legacy \(x+y\)."))

    def test_unclosed_display(self):
        self.assertIn("unclosed-display", self.kinds("Before\n\n$$\na=b\n"))

    def test_fenced_and_inline_code_are_ignored(self):
        source = (
            "Example:\n\n"
            "~~~markdown\n"
            "$$\n"
            "\\operatorname{Var}\n"
            "~~~\n\n"
            "Literal code: " + chr(96) + r"\operatorname{Var}" + chr(96) + ".\n"
        )
        self.assertEqual([], issues(source))

    def test_unchanged_historical_error_not_promoted_to_new_error(self):
        old = "Old issue:\n$$\nx=y\n$$\n\n"
        new = "Introduction.\n\n" + old
        self.assertEqual([], newly_introduced(old, new))

    def test_new_error_fails_even_with_historical_debt(self):
        old = "Old issue:\n$$\nx=y\n$$\n\n"
        new = old + "A fresh bad-$x$ line.\n"
        self.assertIn("inline-math-touching-prose",
                      {x[0] for x in newly_introduced(old, new)})

    def test_fixed_historical_error_is_accepted(self):
        old = "Old issue:\n$$\nx=y\n$$\n"
        new = "Old issue:\n\n$$\nx=y\n$$\n"
        self.assertEqual([], newly_introduced(old, new))

    def test_blank_document_no_math_passes(self):
        self.assertEqual([], issues("# Ordinary prose\n\nNothing special.\n"))


if __name__ == "__main__":
    unittest.main()
