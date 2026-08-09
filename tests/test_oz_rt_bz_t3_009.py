from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_009"
VALIDATOR = HERE / "validate.py"

spec = importlib.util.spec_from_file_location("t3_009_validate", VALIDATOR)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-009 validator")
val = importlib.util.module_from_spec(spec)
spec.loader.exec_module(val)


class T3009Tests(unittest.TestCase):
    def test_baseline_validates(self):
        val.validate()

    def test_nonvacuity_is_explicit(self):
        d = json.loads((HERE / "BASELINE_RESULT.json").read_text())
        self.assertTrue(d["nonvacuity"]["scalar_D_recurrence_fitting_forbidden"])
        self.assertFalse(d["nonvacuity"]["finite_residuals_are_proof"])
        self.assertNotEqual(d["finite_component_baseline"][1]["P5"], [0,1])

    def test_operator_normalization_is_locked(self):
        d = json.loads((HERE / "RECURRENCE_LOCK.json").read_text())
        self.assertEqual(d["coefficients"]["c3"], "2*(n+3)^5*(2*n+5)*a0(n)")
        self.assertFalse(d["normalization_drift_allowed"])

    def test_moving_support_not_prematurely_certified(self):
        d = json.loads((HERE / "BASELINE_RESULT.json").read_text())
        self.assertFalse(d["moving_support"]["uniform_support_proof_complete"])

    def test_middle_row_checkpoint_is_not_t3_certificate(self):
        d = json.loads((HERE / "BASELINE_RESULT.json").read_text())
        self.assertEqual(d["source_artifact_audit"]["RFD_ann.m"]["relevance"], "NOT_A_T3_CERTIFICATE")

    def test_no_proof_promotion(self):
        d = json.loads((HERE / "BASELINE_RESULT.json").read_text())
        self.assertEqual(d["proof_effect"], "NONE")
        self.assertEqual(d["promotion_effect"], "NONE")
        self.assertEqual(d["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")


if __name__ == "__main__":
    unittest.main()
