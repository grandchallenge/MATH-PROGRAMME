#!/usr/bin/env python3
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "campaigns/odd_zeta/OZ_SOURCE_REVISION_DELTA_003/validate.py"
spec = importlib.util.spec_from_file_location("ozd3", P)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class TestOZDelta003(unittest.TestCase):
    def setUp(self):
        self.d = mod.load()

    def assertRejected(self, mutate):
        d = copy.deepcopy(self.d)
        mutate(d)
        with self.assertRaises(mod.ValidationError):
            mod.validate(d)

    def test_package_valid(self):
        mod.validate(self.d)

    def test_candidate_head_drift_rejected(self):
        self.assertRejected(lambda d: d["authority"].__setitem__("candidate_source_head", "0" * 40))

    def test_sharp12_delta_inflation_rejected(self):
        self.assertRejected(lambda d: d["changed_files"].__setitem__(0, "papers_out/sharp12/fake.tex"))

    def test_depth_reopening_inflation_rejected(self):
        self.assertRejected(lambda d: d["depth_reopening_audit"][0].__setitem__("state", "SATISFIED"))

    def test_replay_inflation_rejected(self):
        self.assertRejected(lambda d: d["executable_replay"].__setitem__("state", "COMPLETE"))

    def test_theorem_promotion_rejected(self):
        self.assertRejected(lambda d: d["nonclaims"].__setitem__("t1_top_proved", True))

    def test_irrationality_promotion_rejected(self):
        self.assertRejected(lambda d: d["nonclaims"].__setitem__("new_irrationality_theorem", True))

if __name__ == "__main__":
    unittest.main()
