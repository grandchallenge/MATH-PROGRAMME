from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/"campaigns"/"odd_zeta"/"OZ_RT_BZ_T3_009"


class T3009SearchTests(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((HERE/"SEARCH_RESULT.json").read_text())

    def test_declared_bounded_negative(self):
        self.assertEqual([(x["coefficient_rank"],x["augmented_rank"]) for x in self.r["stages"]],[(198,199),(792,793)])
        self.assertEqual([x["unknowns"] for x in self.r["stages"]],[198,792])

    def test_common_support_has_no_shell_omission(self):
        self.assertEqual(self.r["common_support"]["square"],"0<=k,l<=n+3")
        self.assertFalse(self.r["common_support"]["shell_omission"])

    def test_denominators_are_rank_prime_safe(self):
        self.assertTrue(self.r["denominator_condition"]["all_nonzero_mod_prime"])
        self.assertLess(self.r["denominator_condition"]["max_harmonic_argument_on_strongest_grid"],self.r["prime"])
        self.assertLess(self.r["denominator_condition"]["max_flux_linear_factor"],self.r["prime"])

    def test_bounded_negative_is_not_t3_negative(self):
        self.assertEqual(self.r["proof_effect"],"NONE")
        self.assertEqual(self.r["promotion_effect"],"NONE")
        self.assertEqual(self.r["t3_status"],"OPEN_WITH_CHARACTERIZED_BLOCKER")
        self.assertIn("component recurrence certificate for P5",self.r["remaining_routes"])


if __name__ == "__main__":
    unittest.main()
