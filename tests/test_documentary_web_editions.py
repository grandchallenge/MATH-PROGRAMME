from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "documentaries" / "bsd.md"


class BSDDocumentaryTopicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PAGE.read_text(encoding="utf-8")
        cls.normalized = re.sub(r"\s+", " ", cls.page)

    def test_arithmetic_and_analytic_spine(self) -> None:
        for marker in (
            r"\operatorname{rank}E(\mathbb{Q})",
            r"\operatorname{ord}_{s=1}L(E,s)",
            r"\operatorname{Reg}(E/\mathbb{Q})",
            r"\operatorname{Sel}_n(E/\mathbb{Q})",
            r"\operatorname{Sha}(E/\mathbb{Q})",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, self.normalized)

    def test_logically_distinct_obligations_remain_separate(self) -> None:
        for phrase in (
            "Rank equality, finiteness",
            "Three obligations, not one slogan",
            "Numerical agreement, parity, Selmer bounds",
            "does not prove BSD",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.page)

    def test_low_rank_theorem_boundary_is_present(self) -> None:
        self.assertIn("analytic rank zero or one", self.page)
        self.assertIn("higher-rank", self.page)
        self.assertIn("universal leading-term frontier", self.page)


if __name__ == "__main__":
    unittest.main()
