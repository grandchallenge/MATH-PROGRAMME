from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"
MOD=HERE/"residual_canonical.py"
spec=importlib.util.spec_from_file_location("t3_009_residual_canonical",MOD)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load T3-009 residual canonicalizer")
rc=importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)


class T3009ResidualCanonicalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result, cls.deltas = rc.build_all()
        print("T3-009 residual canonical summary:", cls.result)

    def test_all_five_certificate_shifts_are_canonicalized(self):
        self.assertEqual(set(self.result["shifts"]),{"n1","n2","n3","k1","l1"})
        self.assertTrue(all(x["canonical_monomials"]>0 for x in self.result["shifts"].values()))

    def test_independent_exact_replay_executed(self):
        self.assertGreaterEqual(self.result["exact_independent_checks"],200)

    def test_no_theorem_promotion(self):
        self.assertEqual(self.result["proof_effect"],"NONE")
        self.assertEqual(self.result["promotion_effect"],"NONE")
        self.assertEqual(self.result["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_closure_extension_is_explicit(self):
        self.assertIsInstance(self.result["closure_only_atoms"],list)
        self.assertEqual(len(self.result["protected_atoms"]),self.result["protected_atom_count"])


if __name__ == "__main__":
    unittest.main()
