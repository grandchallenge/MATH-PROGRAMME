from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"


class T3009SearchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=json.loads((HERE/"SEARCH_RESULT.json").read_text())

    def test_exact_rank_search_replays(self):
        cp=subprocess.run([sys.executable,str(HERE/"search.py")],check=True,capture_output=True,text=True,timeout=300)
        for rank in (199,793,1981):
            self.assertIn(str(rank),cp.stdout)

    def test_declared_bounded_negative_for_all_three_rhs(self):
        for kind in ("D","P5","W"):
            stages=self.r["target_results"][kind]["stages"]
            self.assertEqual([(x["coefficient_rank"],x["augmented_rank"]) for x in stages],[(198,199),(792,793),(1980,1981)])
            self.assertEqual([x["unknowns"] for x in stages],[198,792,1980])

    def test_common_support_has_no_shell_omission(self):
        self.assertEqual(self.r["common_support"]["square"],"0<=k,l<=n+3")
        self.assertTrue(self.r["common_support"]["uniform_zero_extension_lemma"])
        self.assertFalse(self.r["common_support"]["shell_omission"])

    def test_denominators_are_rank_prime_safe(self):
        self.assertTrue(self.r["denominator_condition"]["all_nonzero_mod_prime"])
        self.assertEqual(self.r["denominator_condition"]["max_harmonic_argument_on_strongest_grid"],63)
        self.assertEqual(self.r["denominator_condition"]["max_flux_linear_factor"],43)
        self.assertLess(63,self.r["prime"])

    def test_bounded_negative_is_not_t3_negative(self):
        self.assertEqual(self.r["proof_effect"],"NONE")
        self.assertEqual(self.r["promotion_effect"],"NONE")
        self.assertEqual(self.r["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")
        self.assertIn("Q-row product-rule reduction using the exact unweighted kernel recurrence certificate",self.r["remaining_routes"])


if __name__ == "__main__":
    unittest.main()
