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

import affine_sweep
import lex_pivot_sweep


EXPECTED_PIVOT_SHA256 = "3c1ce5a9603bf7c59ff312d4a22da9ab1d8a68a8ac34205cb192540a871fbdfe"


class OzRtBzT3016ALexPivotSweepTests(unittest.TestCase):
    def request(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "request_id": "OZ-RT-BZ-T3-016-A-LEX-PIVOT-SWEEP-TEST",
            "enabled": False,
            "section_mode": lex_pivot_sweep.SECTION_MODE,
            "expected_pivot_sha256": None,
            "source_commit": lex_pivot_sweep.SOURCE_COMMIT,
            "source_tree": lex_pivot_sweep.SOURCE_TREE,
            "prime": 4194301,
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

    def test_source_locks_reuse_admitted_affine_sampler(self) -> None:
        self.assertEqual(lex_pivot_sweep.SOURCE_REPOSITORY, affine_sweep.SOURCE_REPOSITORY)
        self.assertEqual(lex_pivot_sweep.SOURCE_COMMIT, affine_sweep.SOURCE_COMMIT)
        self.assertEqual(lex_pivot_sweep.SOURCE_TREE, affine_sweep.SOURCE_TREE)
        self.assertEqual(lex_pivot_sweep.SOURCE_FILES, affine_sweep.SOURCE_FILES)

    def test_partition_and_reconstruction_bound(self) -> None:
        request = self.request()
        lex_pivot_sweep.validate_request(request)
        self.assertEqual(
            lex_pivot_sweep.chunk_ranges(request),
            [(3, 98), (99, 194), (195, 289), (290, 384)],
        )
        self.assertEqual(lex_pivot_sweep.max_rational_degree_bound(358), 177)
        self.assertEqual(request["rational_degree_test_bound"], 177)

    def test_enabled_request_requires_exact_pivot_digest(self) -> None:
        request = self.request()
        request["enabled"] = True
        with self.assertRaisesRegex(AssertionError, "expected pivot digest"):
            lex_pivot_sweep.validate_request(request)

        request["expected_pivot_sha256"] = "a" * 64
        lex_pivot_sweep.validate_request(request)

        request["expected_pivot_sha256"] = "not-a-digest"
        with self.assertRaisesRegex(AssertionError, "SHA-256"):
            lex_pivot_sweep.validate_request(request)

    def test_section_mode_and_claim_firewall_fail_closed(self) -> None:
        request = self.request()
        request["section_mode"] = "CANONICAL_GAUGE"
        with self.assertRaisesRegex(AssertionError, "section mode"):
            lex_pivot_sweep.validate_request(request)

        request = self.request()
        request["proof_effect"] = "PROVES_T3"
        with self.assertRaisesRegex(AssertionError, "claim firewall"):
            lex_pivot_sweep.validate_request(request)

        request = self.request()
        request["promotion_effect"] = "PROMOTE"
        with self.assertRaisesRegex(AssertionError, "claim firewall"):
            lex_pivot_sweep.validate_request(request)

    def test_pivot_digest_is_order_sensitive_and_canonical(self) -> None:
        p1 = [0, 1, 7, 11]
        p2 = [0, 1, 11, 7]
        self.assertNotEqual(
            lex_pivot_sweep._pivot_sha(p1),
            lex_pivot_sweep._pivot_sha(p2),
        )
        self.assertEqual(len(lex_pivot_sweep._pivot_sha(p1)), 64)

    def test_repository_request_binds_discovered_signature(self) -> None:
        request = lex_pivot_sweep.load_request()
        self.assertTrue(request["enabled"])
        self.assertEqual(request["expected_pivot_sha256"], EXPECTED_PIVOT_SHA256)
        self.assertEqual(request["rational_degree_test_bound"], 177)

    def test_disabled_request_cannot_execute(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            request_path = Path(temp) / "request.json"
            request_path.write_text(json.dumps(self.request()), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "disabled"):
                lex_pivot_sweep.run_chunk(
                    request_path,
                    Path(temp) / "source",
                    0,
                    Path(temp) / "output",
                )


if __name__ == "__main__":
    unittest.main()
