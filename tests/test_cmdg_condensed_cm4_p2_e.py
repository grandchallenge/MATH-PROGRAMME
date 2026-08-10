from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "ci/validate_cmdg_condensed_cm4_p2_e.py"
SPEC = importlib.util.spec_from_file_location("p2e_validator", PATH)
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


class TestCMDGCondensedCM4P2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = json.loads(MOD.RECORD.read_text(encoding="utf-8"))

    def mutate(self, fn):
        data = copy.deepcopy(self.base)
        fn(data)
        return data

    def assert_rejected(self, fn):
        with self.assertRaises((AssertionError, Exception)):
            MOD.validate(self.mutate(fn))

    def test_baseline(self):
        MOD.validate(copy.deepcopy(self.base))

    def test_reject_predecessor_merge_drift(self):
        self.assert_rejected(
            lambda d: d["protected_predecessor"].__setitem__(
                "protected_merge", "0" * 40))

    def test_reject_source_blob_drift(self):
        self.assert_rejected(
            lambda d: d["exact_tree_audit"]["observed_sources"][0].__setitem__(
                "blob", "0" * 40))

    def test_reject_premature_equivalence_claim(self):
        self.assert_rejected(
            lambda d: d["stage_result"].__setitem__(
                "p2_e_natural_equivalence_established", True))

    def test_reject_premature_protected_availability(self):
        self.assert_rejected(
            lambda d: d["claim_boundary"].__setitem__(
                "p2_e_protected_available", True))

    def test_reject_premature_parent_closure(self):
        self.assert_rejected(
            lambda d: d["claim_boundary"].__setitem__("p2_closed", True))

    def test_reject_basis_dependency(self):
        self.assert_rejected(
            lambda d: d["theorem_target"].__setitem__("basis_dependency", True))

    def test_reject_loss_of_finite_obligation(self):
        self.assert_rejected(
            lambda d: d["proof_architecture"]["finite_level_comparison"].__setitem__(
                "state", "FORMALLY_AVAILABLE"))


if __name__ == "__main__":
    unittest.main()
