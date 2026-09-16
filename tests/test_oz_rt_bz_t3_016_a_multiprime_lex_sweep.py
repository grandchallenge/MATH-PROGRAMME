from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "campaigns" / "odd_zeta" / "OZ_RT_BZ_T3_016_A"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import multiprime_lex_pivot_sweep
import lex_pivot_sweep


EXPECTED_PIVOT_SHA256 = "3c1ce5a9603bf7c59ff312d4a22da9ab1d8a68a8ac34205cb192540a871fbdfe"
EXPECTED_PRIMES = [4194287, 4194277, 4194271]


class OzRtBzT3016AMultiprimeLexSweepTests(unittest.TestCase):
    def request(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "request_id": "OZ-RT-BZ-T3-016-A-MULTIPRIME-LEX-TEST",
            "enabled": False,
            "section_mode": multiprime_lex_pivot_sweep.SECTION_MODE,
            "expected_pivot_sha256": EXPECTED_PIVOT_SHA256,
            "reference_prime": 4194301,
            "reference_protected_head": multiprime_lex_pivot_sweep.REFERENCE_PROTECTED_HEAD,
            "reference_sweep_run_id": multiprime_lex_pivot_sweep.REFERENCE_SWEEP_RUN_ID,
            "reference_profile_report_id": multiprime_lex_pivot_sweep.REFERENCE_PROFILE_REPORT_ID,
            "reference_coordinate_map_sha256": multiprime_lex_pivot_sweep.REFERENCE_COORDINATE_MAP_SHA256,
            "primes": list(EXPECTED_PRIMES),
            "source_commit": multiprime_lex_pivot_sweep.SOURCE_COMMIT,
            "source_tree": multiprime_lex_pivot_sweep.SOURCE_TREE,
            "n_start": 3,
            "n_stop": 384,
            "chunks": 4,
            "workers_per_chunk": 4,
            "fit_extra_rows": 64,
            "fresh_rows": 16,
            "solver_block_size": 64,
            "reconstruction_fit_count": 358,
            "holdout_count": 24,
            "evidence_effect": "MODULAR_CANDIDATE_ONLY",
            "proof_effect": "NONE",
            "promotion_effect": "NONE",
        }

    def test_reuses_admitted_section_and_source_locks(self) -> None:
        self.assertEqual(multiprime_lex_pivot_sweep.SECTION_MODE, lex_pivot_sweep.SECTION_MODE)
        self.assertEqual(multiprime_lex_pivot_sweep.SOURCE_COMMIT, lex_pivot_sweep.SOURCE_COMMIT)
        self.assertEqual(multiprime_lex_pivot_sweep.SOURCE_TREE, lex_pivot_sweep.SOURCE_TREE)
        self.assertEqual(multiprime_lex_pivot_sweep.SOURCE_FILES, lex_pivot_sweep.SOURCE_FILES)

    def test_partition_and_degree_bound(self) -> None:
        request = self.request()
        multiprime_lex_pivot_sweep.validate_request(request)
        self.assertEqual(
            multiprime_lex_pivot_sweep.chunk_ranges(request),
            [(3, 98), (99, 194), (195, 289), (290, 384)],
        )
        self.assertEqual(request["rational_degree_test_bound"], 177)

    def test_additional_moduli_are_exact_distinct_primes(self) -> None:
        request = self.request()
        multiprime_lex_pivot_sweep.validate_request(request)
        self.assertEqual(request["primes"], EXPECTED_PRIMES)
        for p in EXPECTED_PRIMES:
            self.assertTrue(multiprime_lex_pivot_sweep._is_prime(p))

        bad = self.request()
        bad["primes"] = [4194301, 4194277, 4194271]
        with self.assertRaisesRegex(AssertionError, "reference prime"):
            multiprime_lex_pivot_sweep.validate_request(bad)

        bad = self.request()
        bad["primes"] = [4194287, 4194287, 4194271]
        with self.assertRaisesRegex(AssertionError, "distinct"):
            multiprime_lex_pivot_sweep.validate_request(bad)

        bad = self.request()
        bad["primes"] = [4194286, 4194277, 4194271]
        with self.assertRaisesRegex(AssertionError, "non-prime"):
            multiprime_lex_pivot_sweep.validate_request(bad)

    def test_claim_firewall_fails_closed(self) -> None:
        request = self.request()
        request["proof_effect"] = "PROVES_T3"
        with self.assertRaisesRegex(AssertionError, "claim firewall"):
            multiprime_lex_pivot_sweep.validate_request(request)

        request = self.request()
        request["promotion_effect"] = "PROMOTE"
        with self.assertRaisesRegex(AssertionError, "claim firewall"):
            multiprime_lex_pivot_sweep.validate_request(request)

    def test_repository_request_is_separate_from_admitted_reference_request(self) -> None:
        request = multiprime_lex_pivot_sweep.load_request()
        admitted = lex_pivot_sweep.load_request()
        self.assertTrue(request["enabled"])
        self.assertEqual(request["reference_prime"], admitted["prime"])
        self.assertEqual(
            request["reference_coordinate_map_sha256"],
            multiprime_lex_pivot_sweep.REFERENCE_COORDINATE_MAP_SHA256,
        )
        self.assertNotIn(admitted["prime"], request["primes"])
        self.assertEqual(request["expected_pivot_sha256"], admitted["expected_pivot_sha256"])
        self.assertEqual(request["primes"], EXPECTED_PRIMES)

    def test_disabled_request_cannot_execute(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            request_path = Path(temp) / "request.json"
            request_path.write_text(json.dumps(self.request()), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "disabled"):
                multiprime_lex_pivot_sweep.run_chunk(
                    request_path,
                    Path(temp) / "source",
                    0,
                    0,
                    Path(temp) / "output",
                )


if __name__ == "__main__":
    unittest.main()
