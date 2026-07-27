from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTARIES = ROOT / "docs" / "documentaries"

TOPIC_MARKERS = {
    "hodge": (
        r"H^{2p}(X,\mathbb Q)\cap H^{p,p}(X)",
        "The integral conjecture is false",
        "smooth projective",
        "cycle-class map",
    ),
    "navier_stokes": (
        r"viscosity \(\nu>0\)",
        r"\partial_t\omega+(u\cdot\nabla)\omega",
        r"\frac2q+\frac3p\le1",
        "Weak existence is not smooth existence",
    ),
    "yang_mills": (
        "Osterwalder",
        "positive spectral gap",
        "continuum theory",
        "finite-lattice",
    ),
    "p_vs_np": (
        r"\mathsf{P}\subseteq\mathsf{NP}",
        r"x\in A\Longleftrightarrow f(x)\in B",
        "Relativization",
        "Algebrization",
    ),
    "riemann": (
        "critical line",
        "Euler product",
        "finite zero verification",
        "universal assertion",
    ),
}


class WaveOneDocumentaryTopicTests(unittest.TestCase):
    def test_problem_specific_spines_and_guardrails(self) -> None:
        for slug, markers in TOPIC_MARKERS.items():
            page = (DOCUMENTARIES / f"{slug}.md").read_text(encoding="utf-8")
            for marker in markers:
                with self.subTest(slug=slug, marker=marker):
                    self.assertIn(marker, page)


if __name__ == "__main__":
    unittest.main()
