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

import affine_probe
import affine_sweep


class OzRtBzT3016AAffineSweepTests(unittest.TestCase):
    def request(self) -> dict:
        return {
            "schema_version": "1.0.0",
            "request_id": "OZ-RT-BZ-T3-016-A-AFFINE-SWEEP-TEST",
            "enabled": False,
            "source_commit": affine_sweep.SOURCE_COMMIT,
            "source_tree": affine_sweep.SOURCE_TREE,
            "prime": 4194301,
            "n_start": 1,
            "n_stop": 384,
            "chunks": 4,
            "workers_per_chunk": 4,
            "fit_extra_rows": 64,
            "fresh_rows": 16,
            "solver_block_size": 64,
            "reconstruction_fit_count": 360,
            "holdout_count": 24,
            "evidence_effect": "MODULAR_CANDIDATE_ONLY",
            "proof_effect": "NONE",
            "promotion_effect": "NONE",
        }

    def test_source_locks_reuse_admitted_affine_probe(self) -> None:
        self.assertEqual(affine_sweep.SOURCE_REPOSITORY, affine_probe.SOURCE_REPOSITORY)
        self.assertEqual(affine_sweep.SOURCE_COMMIT, affine_probe.SOURCE_COMMIT)
        self.assertEqual(affine_sweep.SOURCE_FILES, affine_probe.SOURCE_FILES)
        self.assertEqual(
            affine_sweep.SOURCE_TREE,
            "be780558454b704bdd016a3070d698c2e106e2b8",
        )

    def test_partition_and_reconstruction_bound(self) -> None:
        request = self.request()
        affine_sweep.validate_request(request)
        self.assertEqual(
            affine_sweep.chunk_ranges(request),
            [(1, 96), (97, 192), (193, 288), (289, 384)],
        )
        self.assertEqual(affine_sweep.max_rational_degree_bound(360), 178)
        self.assertEqual(request["rational_degree_test_bound"], 178)

    def test_claim_firewall_rejects_promotion_or_proof(self) -> None:
        request = self.request()
        request["proof_effect"] = "PROVES_T3"
        with self.assertRaisesRegex(AssertionError, "claim firewall"):
            affine_sweep.validate_request(request)

        request = self.request()
        request["promotion_effect"] = "PROMOTE"
        with self.assertRaisesRegex(AssertionError, "claim firewall"):
            affine_sweep.validate_request(request)

    def test_source_and_numeric_guardrails_fail_closed(self) -> None:
        request = self.request()
        request["source_commit"] = "0" * 40
        with self.assertRaisesRegex(AssertionError, "source commit drift"):
            affine_sweep.validate_request(request)

        request = self.request()
        request["solver_block_size"] = 1000
        with self.assertRaisesRegex(AssertionError, "solver block size"):
            affine_sweep.validate_request(request)

        request = self.request()
        request["reconstruction_fit_count"] = 359
        with self.assertRaisesRegex(AssertionError, "partition"):
            affine_sweep.validate_request(request)

    def test_disabled_request_cannot_execute(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            request_path = Path(temp) / "request.json"
            request_path.write_text(json.dumps(self.request()), encoding="utf-8")
            with self.assertRaisesRegex(AssertionError, "disabled"):
                affine_sweep.run_chunk(
                    request_path,
                    Path(temp) / "source",
                    0,
                    Path(temp) / "output",
                )


if __name__ == "__main__":
    unittest.main()
