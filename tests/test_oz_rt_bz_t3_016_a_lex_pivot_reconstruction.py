from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_016_A"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import lex_pivot_reconstruction


class OzRtBzT3016ALexPivotReconstructionTests(unittest.TestCase):
    def test_report_claim_firewall_and_bound(self) -> None:
        report = lex_pivot_reconstruction.load_report()
        self.assertEqual(report["evidence_effect"], "MODULAR_CANDIDATE_ONLY")
        self.assertEqual(report["proof_effect"], "NONE")
        self.assertEqual(report["promotion_effect"], "NONE")
        self.assertFalse(report["t3_proved"])
        self.assertFalse(report["t3_refuted"])
        self.assertFalse(report["global_certificate_constructed"])
        self.assertEqual(report["sweep_contract"]["fit_count"], 358)
        self.assertEqual(report["sweep_contract"]["holdout_count"], 24)
        self.assertEqual(report["sweep_contract"]["balanced_degree_ceiling"], 177)
        self.assertEqual(report["rational_profile_mod_p"]["common_monic_denominator_degree"], 85)
        self.assertEqual(report["rational_profile_mod_p"]["common_numerator_degree_max_before_cancellation"], 157)

    def test_common_denominator_profile_accepts_rational_holdouts(self) -> None:
        p = 101
        ns = np.arange(3, 23, dtype=np.int64)
        denominator = np.asarray([7, 1], dtype=np.int64)
        values = []
        for n in ns:
            den = (int(n) + 7) % p
            num = (3 * int(n) ** 4 + 2 * int(n) + 5) % p
            values.append(num * pow(den, p - 2, p) % p)
        normalized = np.asarray(values, dtype=np.int64)[:, None]
        result = lex_pivot_reconstruction._newton_common_denominator_profile(
            normalized,
            ns,
            fit_count=15,
            degree_ceiling=6,
            denominator=denominator,
            p=p,
        )
        self.assertEqual(result["fit_pass_count"], 1)
        self.assertEqual(result["holdout_pass_count"], 1)
        self.assertEqual(result["common_numerator_degree_max"], 4)

    def test_common_denominator_profile_rejects_holdout_drift(self) -> None:
        p = 101
        ns = np.arange(3, 23, dtype=np.int64)
        denominator = np.asarray([7, 1], dtype=np.int64)
        values = []
        for n in ns:
            den = (int(n) + 7) % p
            num = (int(n) ** 2 + 1) % p
            values.append(num * pow(den, p - 2, p) % p)
        normalized = np.asarray(values, dtype=np.int64)[:, None]
        normalized[-1, 0] = (normalized[-1, 0] + 1) % p
        with self.assertRaisesRegex(AssertionError, "holdout failure"):
            lex_pivot_reconstruction._newton_common_denominator_profile(
                normalized,
                ns,
                fit_count=15,
                degree_ceiling=6,
                denominator=denominator,
                p=p,
            )

    def test_common_denominator_profile_rejects_fit_degree_overrun(self) -> None:
        p = 101
        ns = np.arange(3, 23, dtype=np.int64)
        denominator = np.asarray([1], dtype=np.int64)
        normalized = np.asarray([(int(n) ** 8) % p for n in ns], dtype=np.int64)[:, None]
        with self.assertRaisesRegex(AssertionError, "degree exceeds governed ceiling"):
            lex_pivot_reconstruction._newton_common_denominator_profile(
                normalized,
                ns,
                fit_count=15,
                degree_ceiling=6,
                denominator=denominator,
                p=p,
            )


if __name__ == "__main__":
    unittest.main()
