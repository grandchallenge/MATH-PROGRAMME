from __future__ import annotations
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "campaigns/odd_zeta/OZ_RT_BZ_T3_001/validate.py"
spec = importlib.util.spec_from_file_location("oz_t3_validate", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

class OZT3Tests(unittest.TestCase):
    def setUp(self):
        self.record = mod.load_record()

    def test_package_valid(self):
        self.assertEqual(mod.errors(self.record), [])

    def test_proof_inflation_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["disposition"]["proof_found"] = True
        bad["disposition"]["claim_boundaries"]["T3_proved"] = True
        self.assertTrue(mod.errors(bad))

    def test_finite_evidence_promotion_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["finite_evidence"]["theorem_effect"] = "PROOF"
        bad["finite_evidence"]["finite_agreement_is_proof"] = True
        self.assertTrue(mod.errors(bad))

    def test_counterexample_fabrication_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["certificate_status"]["counterexample_certificate"]["present"] = True
        bad["certificate_status"]["may_claim_refutation"] = True
        self.assertTrue(mod.errors(bad))

    def test_source_drift_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["target_lock"]["source"]["bridge_blob"] = "0" * 40
        self.assertTrue(mod.errors(bad))

    def test_sharp12_gate_inflation_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["disposition"]["route_effect"]["sharp_12_may_advance"] = True
        self.assertTrue(mod.errors(bad))

if __name__ == "__main__":
    unittest.main()
