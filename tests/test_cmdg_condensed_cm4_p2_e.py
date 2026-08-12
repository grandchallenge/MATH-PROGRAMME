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
        self.assert_rejected(lambda d: d["protected_predecessor"].__setitem__("protected_merge", "0" * 40))

    def test_reject_source_blob_drift(self):
        self.assert_rejected(lambda d: d["exact_tree_audit"]["observed_sources"][0].__setitem__("blob", "0" * 40))

    def test_reject_loss_of_terminal_equivalence(self):
        self.assert_rejected(lambda d: d["stage_result"].__setitem__("p2_e_natural_equivalence_established", False))

    def test_reject_premature_protected_availability(self):
        self.assert_rejected(lambda d: d["claim_boundary"].__setitem__("p2_e_protected_available", True))

    def test_reject_premature_parent_closure(self):
        self.assert_rejected(lambda d: d["claim_boundary"].__setitem__("p2_closed", True))

    def test_reject_basis_dependency(self):
        self.assert_rejected(lambda d: d["theorem_target"].__setitem__("basis_dependency", True))

    def test_reject_loss_of_e1_certification(self):
        self.assert_rejected(lambda d: d["proof_architecture"]["finite_level_comparison"].__setitem__("state", "FORMALLY_AVAILABLE"))

    def test_reject_loss_of_e2_certification(self):
        self.assert_rejected(lambda d: d["proof_architecture"]["measure_right_kan_extension"].__setitem__("state", "OPEN_CONSTRUCTION"))

    def test_reject_e2_exact_head_drift(self):
        self.assert_rejected(lambda d: d["proof_architecture"]["measure_right_kan_extension"].__setitem__("requirement", "E2 CLOSED_MACHINE_CERTIFIED"))

    def test_reject_loss_of_e3_certification(self):
        self.assert_rejected(lambda d: d["proof_architecture"]["kan_extension_uniqueness"].__setitem__("state", "FORMALLY_AVAILABLE"))

    def test_reject_e3_exact_head_drift(self):
        self.assert_rejected(lambda d: d["proof_architecture"]["kan_extension_uniqueness"].__setitem__("requirement", "E3 CLOSED_MACHINE_CERTIFIED"))

    def test_reject_duality_implies_reconstruction_scope_drift(self):
        self.assert_rejected(lambda d: d.__setitem__("scope", "CM4-P2-E only: natural equivalence between measureFunctor and profiniteSolid"))

    def test_reject_p2d_role_promotion(self):
        def mutate_role(d):
            for row in d["exact_tree_audit"]["observed_sources"]:
                if row["path"].endswith("CMDGCondensedCM4P2D.lean"):
                    row["role"] = "protected P2-D functor already sufficient for equivalence"
                    return
            raise AssertionError("P2-D source row missing")
        self.assert_rejected(mutate_role)


if __name__ == "__main__":
    unittest.main()
