#!/usr/bin/env python3
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "campaigns/odd_zeta/OZ_RT_SHARP12_T1TOP_001/validate.py"
spec = importlib.util.spec_from_file_location("ozt1", P)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TestOZT1Top(unittest.TestCase):
    def setUp(self):
        self.d = mod.load()

    def reject(self, mutate):
        d = copy.deepcopy(self.d)
        mutate(d)
        with self.assertRaises(mod.ValidationError):
            mod.validate(d)

    def test_package_valid(self):
        mod.validate(self.d)

    def test_source_drift_rejected(self):
        self.reject(lambda d: d["authority"].__setitem__("source_commit", "0" * 40))

    def test_representative_substitution_rejected(self):
        self.reject(lambda d: d["target_lock"].__setitem__("representative", "w5_sym"))

    def test_finite_evidence_promotion_rejected(self):
        self.reject(lambda d: d["certificate_search"].__setitem__("finite_evidence_is_proof", True))

    def test_t3_substitution_rejected(self):
        self.reject(lambda d: d["certificate_search"].__setitem__("t3_is_substitute", True))

    def test_missing_certificate_inflation_rejected(self):
        self.reject(lambda d: d["missing_objects"][0].__setitem__("state", "PRESENT"))

    def test_t1_proof_inflation_rejected(self):
        self.reject(lambda d: d["nonclaims"].__setitem__("t1_top_proved", True))

    def test_sharp12_inflation_rejected(self):
        self.reject(lambda d: d["nonclaims"].__setitem__("sharp12_proved", True))

    def test_terminal_disposition_drift_rejected(self):
        self.reject(lambda d: d.__setitem__("terminal_disposition", "T1_TOP_PROVED"))

if __name__ == "__main__":
    unittest.main()
