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

import lex_pivot_multiprime
import lex_pivot_sweep


class OzRtBzT3016ALexPivotMultiprimeTests(unittest.TestCase):
    def request(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "request_id": "OZ-RT-BZ-T3-016-A-LEX-PIVOT-MULTIPRIME-TEST",
            "enabled": False,
            "section_mode": lex_pivot_multiprime.SECTION_MODE,
            "expected_pivot_sha256": lex_pivot_multiprime.ANCHOR_PIVOT_SHA256,
            "anchor_profile": {
                "report_id": lex_pivot_multiprime.ANCHOR_PROFILE_REPORT_ID,
                "protected_head": lex_pivot_multiprime.ANCHOR_PROFILE_PROTECTED_HEAD,
                "profile_blob_sha": lex_pivot_multiprime.ANCHOR_PROFILE_BLOB_SHA,
                "prime": lex_pivot_multiprime.ANCHOR_PRIME,
                "normalized_dataset_sha256": lex_pivot_multiprime.ANCHOR_NORMALIZED_DATASET_SHA256,
            },
            "source_commit": lex_pivot_multiprime.SOURCE_COMMIT,
            "source_tree": lex_pivot_multiprime.SOURCE_TREE,
            "replay_primes": [4194271, 4194277, 4194287],
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

    def test_reuses_exact_lex_section_and_source_lock(self) -> None:
        self.assertEqual(lex_pivot_multiprime.SECTION_MODE, lex_pivot_sweep.SECTION_MODE)
        self.assertEqual(lex_pivot_multiprime.SOURCE_COMMIT, lex_pivot_sweep.SOURCE_COMMIT)
        self.assertEqual(lex_pivot_multiprime.SOURCE_TREE, lex_pivot_sweep.SOURCE_TREE)
        self.assertEqual(lex_pivot_multiprime.SOURCE_FILES, lex_pivot_sweep.SOURCE_FILES)

    def test_request_binds_independent_primes_and_anchor(self) -> None:
        request = self.request()
        lex_pivot_multiprime.validate_request(request)
        self.assertEqual(
            lex_pivot_multiprime.chunk_ranges(request),
            [(3, 98), (99, 194), (195, 289), (290, 384)],
        )
        self.assertEqual(request["rational_degree_test_bound"], 177)
        self.assertNotIn(lex_pivot_multiprime.ANCHOR_PRIME, request["replay_primes"])
        self.assertTrue(all(lex_pivot_multiprime._is_prime(p) for p in request["replay_primes"]))

    def test_bad_prime_duplicate_order_and_float_bound_fail_closed(self) -> None:
        request = self.request()
        request["replay_primes"] = [4194271, 4194271]
        with self.assertRaisesRegex(AssertionError, "strictly increasing"):
            lex_pivot_multiprime.validate_request(request)

        request = self.request()
        request["replay_primes"] = [4194277, 4194271]
        with self.assertRaisesRegex(AssertionError, "strictly increasing"):
            lex_pivot_multiprime.validate_request(request)

        request = self.request()
        request["replay_primes"] = [4194271, 4194273]
        with self.assertRaisesRegex(AssertionError, "not prime"):
            lex_pivot_multiprime.validate_request(request)

        request = self.request()
        request["replay_primes"] = [4194271, 11863289]
        with self.assertRaisesRegex(AssertionError, "exactness bound"):
            lex_pivot_multiprime.validate_request(request)

    def test_anchor_prime_and_anchor_identity_fail_closed(self) -> None:
        request = self.request()
        request["replay_primes"] = [4194271, 4194301]
        with self.assertRaisesRegex(AssertionError, "independent"):
            lex_pivot_multiprime.validate_request(request)

        request = self.request()
        request["anchor_profile"]["profile_blob_sha"] = "0" * 40
        with self.assertRaisesRegex(AssertionError, "anchor profile drift"):
            lex_pivot_multiprime.validate_request(request)

        request = self.request()
        request["expected_pivot_sha256"] = "0" * 64
        with self.assertRaisesRegex(AssertionError, "pivot identity drift"):
            lex_pivot_multiprime.validate_request(request)

    def test_range_partition_and_claim_firewall_fail_closed(self) -> None:
        request = self.request()
        request["n_stop"] = 383
        with self.assertRaisesRegex(AssertionError, "n=3..384"):
            lex_pivot_multiprime.validate_request(request)

        request = self.request()
        request["holdout_count"] = 23
        with self.assertRaisesRegex(AssertionError, "358 fit / 24 holdout"):
            lex_pivot_multiprime.validate_request(request)

        request = self.request()
        request["proof_effect"] = "PROVES_T3"
        with self.assertRaisesRegex(AssertionError, "claim firewall"):
            lex_pivot_multiprime.validate_request(request)

    def test_repository_request_is_enabled_and_exact(self) -> None:
        request = lex_pivot_multiprime.load_request()
        self.assertTrue(request["enabled"])
        self.assertEqual(request["replay_primes"], [4194271, 4194277, 4194287])
        self.assertEqual(request["expected_pivot_sha256"], lex_pivot_multiprime.ANCHOR_PIVOT_SHA256)
        self.assertEqual(request["anchor_profile"]["profile_blob_sha"], lex_pivot_multiprime.ANCHOR_PROFILE_BLOB_SHA)

    def test_runtime_recovery_receipt_binds_failed_request(self) -> None:
        recovery = json.loads(
            (HERE / "LEX_PIVOT_MULTIPRIME_RECOVERY_002.json").read_text(encoding="utf-8")
        )
        request = lex_pivot_multiprime.load_request()
        self.assertEqual(
            recovery["predecessor_request_id"],
            "OZ-RT-BZ-T3-016-A-LEX-PIVOT-MULTIPRIME-SWEEP-001",
        )
        self.assertEqual(recovery["predecessor_run_id"], 34945709508)
        self.assertEqual(recovery["replacement_request_id"], request["request_id"])
        self.assertEqual(recovery["replacement_replay_primes"], request["replay_primes"])
        self.assertEqual(recovery["preserved_artifact_count"], 0)
        self.assertEqual(recovery["proof_effect"], "NONE")
        self.assertEqual(recovery["promotion_effect"], "NONE")

    def test_disabled_request_cannot_execute(self) -> None:
        request = self.request()
        with tempfile.TemporaryDirectory() as temp:
            request_path = Path(temp) / "request.json"
            request_path.write_text(json.dumps(request), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "disabled"):
                lex_pivot_multiprime.run_chunk(
                    request_path,
                    Path(temp) / "source",
                    request["replay_primes"][0],
                    0,
                    Path(temp) / "output",
                )

    def test_unauthorized_prime_rejected_before_source_access(self) -> None:
        request = self.request()
        request["enabled"] = True
        with tempfile.TemporaryDirectory() as temp:
            request_path = Path(temp) / "request.json"
            request_path.write_text(json.dumps(request), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "not authorized"):
                lex_pivot_multiprime.run_chunk(
                    request_path,
                    Path(temp) / "missing-source",
                    4194371,
                    0,
                    Path(temp) / "output",
                )


if __name__ == "__main__":
    unittest.main()
