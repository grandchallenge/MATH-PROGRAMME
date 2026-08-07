from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
MODULE_PATH = ROOT / "ci" / "administrative_autonomy_receipt_stage.py"
SPEC = importlib.util.spec_from_file_location("administrative_autonomy_receipt_stage", MODULE_PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class PullHeadClient:
    def __init__(self) -> None:
        self.calls = 0

    def get(self, path: str):
        self.calls += 1
        sha = "1" * 40 if self.calls == 1 else "2" * 40
        return {"head": {"sha": sha}}


class ReceiptStageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.current = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_maintenance_completion_state.json"
            ).read_text(encoding="utf-8")
        )
        self.current = copy.deepcopy(self.current)
        structural = self.current["procedures"]["structural_sweep"]
        structural["receipts"] = structural["receipts"][:-1]
        structural["receipt_count"] = len(structural["receipts"])
        structural["completed_through_utc"] = "2026-08-05T22:57:00Z"
        self.current["derived_from_protected_head"] = "a" * 40
        self.receipt = {
            "procedure_id": "structural_sweep",
            "scheduled_due_at": "2026-08-06T15:45:00Z",
            "record_path": (
                "governance/administrative_structural_sweeps/"
                "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-06-008.json"
            ),
            "record_sha256": "b" * 64,
            "merge_commit": "c" * 40,
            "reviewed_head": "d" * 40,
            "pull_request": 263,
            "disposition": module.DISPOSITION,
            "receipt_state": "PROTECTED_COMPLETE",
        }

    def test_receipt_advances_completion_state(self) -> None:
        value = module.advance_completion_state(
            self.current, self.receipt, "c" * 40
        )
        structural = value["procedures"]["structural_sweep"]
        self.assertEqual("2026-08-06T15:45:00Z", structural["completed_through_utc"])
        self.assertEqual(3, structural["receipt_count"])
        self.assertTrue(module.completion_has_receipt(value, self.receipt))
        self.assertEqual("c" * 40, value["derived_from_protected_head"])

    def test_duplicate_receipt_is_idempotent(self) -> None:
        first = module.advance_completion_state(
            self.current, self.receipt, "c" * 40
        )
        second = module.advance_completion_state(
            first, self.receipt, "c" * 40
        )
        self.assertEqual(first, second)

    def test_non_advancing_receipt_is_rejected(self) -> None:
        stale = copy.deepcopy(self.receipt)
        stale["scheduled_due_at"] = "2026-08-05T06:09:00Z"
        with self.assertRaises(module.AutonomyError):
            module.advance_completion_state(
                self.current, stale, "c" * 40
            )

    def test_eventual_head_readback_is_polled(self) -> None:
        client = PullHeadClient()
        pull = module.wait_pull_head(
            client,
            "grandchallenge/MATH-PROGRAMME",
            263,
            "2" * 40,
            1,
            0,
        )
        self.assertEqual("2" * 40, pull["head"]["sha"])
        self.assertEqual(2, client.calls)

    def test_first_live_receipt_is_bound(self) -> None:
        protected = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_maintenance_completion_state.json"
            ).read_text(encoding="utf-8")
        )
        receipts = protected["procedures"]["structural_sweep"]["receipts"]
        target = [item for item in receipts if item["pull_request"] == 263]
        self.assertEqual(1, len(target))
        self.assertEqual(
            "REFEREE_AGENT_AUTHORIZED_EXACT_HEAD_PROTECTED_MERGE",
            target[0]["disposition"],
        )


if __name__ == "__main__":
    unittest.main()
