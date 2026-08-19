import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "governance" / "visual_pedagogy" / "garden_correction_r2.json"
CANDIDATE = ROOT / "governance" / "visual_pedagogy" / "review_candidates" / "union_closed" / "plate_garden_successor_r2.svg"
LIVE_R1 = ROOT / "docs" / "assets" / "visual_pedagogy" / "batch1" / "union_closed" / "plate_garden.svg"
RENDERER = ROOT / "tools" / "render_visual_pedagogy_garden_correction.py"
RUNTIME = ROOT / "docs" / "javascripts" / "documentary.js"


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def as_set(xs):
    return frozenset(xs)


class GardenCorrectionR2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = json.loads(MANIFEST.read_text(encoding="utf-8"))
        cls.svg = CANDIDATE.read_text(encoding="utf-8")

    def test_candidate_is_distinct_non_live_identity(self):
        self.assertEqual(
            "2931b423942ac079002b37233e4a42a1f4a6da462f096938393b2715dd71d296",
            sha256(CANDIDATE),
        )
        self.assertEqual(
            "a70b8af6df46589d0df3d2c5c508e54933dd8c01259711e75640821f2188cef7",
            sha256(LIVE_R1),
        )
        self.assertNotEqual(sha256(CANDIDATE), sha256(LIVE_R1))
        self.assertFalse(self.data["correction_candidate"]["live_switch_authorized"])
        self.assertTrue(self.data["batch2_paused"])
        self.assertNotIn("plate_garden_successor_r2.svg", RUNTIME.read_text(encoding="utf-8"))

    def test_renderer_reproduces_candidate_bytes(self):
        spec = importlib.util.spec_from_file_location("garden_r2_renderer", RENDERER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.SVG.encode("utf-8"), CANDIDATE.read_bytes())

    def test_exact_family_is_union_closed_and_counts_are_correct(self):
        family = {as_set(s) for s in self.data["exact_family"]}
        for a in family:
            for b in family:
                self.assertIn(a | b, family)
        frequencies = {
            x: sum(x in s for s in family)
            for x in ("a", "b", "c")
        }
        self.assertEqual({"a": 4, "b": 3, "c": 2}, frequencies)
        self.assertEqual(3, self.data["half_threshold"])

    def test_manifest_edges_are_exact_hasse_covers(self):
        family = {as_set(s) for s in self.data["exact_family"]}
        expected = set()
        for lower in family:
            for upper in family:
                if not lower < upper:
                    continue
                if not any(lower < middle < upper for middle in family):
                    expected.add((lower, upper))
        actual = {
            (as_set(lower), as_set(upper))
            for lower, upper in self.data["cover_edges"]
        }
        self.assertEqual(expected, actual)
        self.assertNotIn((frozenset({"b"}), frozenset({"a", "b", "c"})), actual)
        self.assertEqual(7, self.svg.count('class="line"'))

    def test_presentation_defects_are_cured(self):
        self.assertIn('aria-label="empty set"', self.svg)
        self.assertIn("strict Hasse-style inclusion diagram", self.svg)
        self.assertIn("a exceeds and b meets", self.svg)
        self.assertIn("Selected unions", self.svg)
        self.assertIn("the full six-set family is checked separately as union-closed", self.svg)
        self.assertIn("with at least one nonempty member", self.svg)
        self.assertNotIn("a and b meet", self.svg)
        self.assertNotIn("every finite nonempty union-closed family", self.svg)
        self.assertIn("visual_is_evidence: false", self.svg)
        self.assertFalse(self.data["visual_is_evidence"])


if __name__ == "__main__":
    unittest.main()
