from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "campaigns/odd_zeta/OZ_RT_SHARP12_DEPTH_001/validate.py"
spec = importlib.util.spec_from_file_location("oz_depth_validate", VALIDATOR)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

class OZSharp12DepthBlockerTests(unittest.TestCase):
    def setUp(self):
        self.record = mod.load_record()

    def test_package_valid(self):
        self.assertEqual(mod.errors(self.record), [])

    def test_exact_source_commit_drift_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["target_lock"]["upstream_commit"] = "0" * 40
        self.assertTrue(mod.errors(bad))

    def test_exact_source_tree_drift_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["target_lock"]["upstream_tree"] = "0" * 40
        self.assertTrue(mod.errors(bad))

    def test_missing_producer_artifact_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["unrecoverable_producer_order_artifacts"] = bad["unrecoverable_producer_order_artifacts"][1:]
        self.assertTrue(mod.errors(bad))

    def test_variable_order_recovery_cannot_be_silently_asserted(self):
        bad = copy.deepcopy(self.record)
        bad["unrecoverable_producer_order_artifacts"][1]["absence_effect"] = ""
        self.assertTrue(mod.errors(bad))

    def test_modular_evidence_cannot_be_promoted_to_rational_certificate(self):
        bad = copy.deepcopy(self.record)
        bad["source_observations"]["rational_certificate_independently_replayable"] = True
        self.assertTrue(mod.errors(bad))

    def test_missing_reopening_requirement_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["reopening_requirements"] = bad["reopening_requirements"][:-1]
        self.assertTrue(mod.errors(bad))

    def test_depth_promotion_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["nonclaims"]["depth_certified"] = True
        self.assertTrue(mod.errors(bad))

    def test_sharp12_promotion_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["nonclaims"]["sharp12_gate_open"] = True
        self.assertTrue(mod.errors(bad))

    def test_t3_inference_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["nonclaims"]["t3_proved"] = True
        self.assertTrue(mod.errors(bad))

    def test_terminal_disposition_drift_rejected(self):
        bad = copy.deepcopy(self.record)
        bad["terminal_disposition"] = "DEPTH_CERTIFIED"
        bad["disposition"]["status"] = "DEPTH_CERTIFIED"
        self.assertTrue(mod.errors(bad))

if __name__ == "__main__":
    unittest.main()
