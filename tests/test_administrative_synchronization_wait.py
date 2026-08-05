from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import synchronize_administrative_completion_v3 as synchronization


class FakeClient:
    def __init__(self, runs: list[dict]) -> None:
        self.runs = runs

    def get(self, path: str) -> dict:
        self.path = path
        return {"workflow_runs": self.runs}


class AdministrativeSynchronizationWaitTests(unittest.TestCase):
    def test_single_success_is_not_full_gate(self) -> None:
        client = FakeClient([
            {"id": 1, "name": "Programme policy checks", "status": "completed", "conclusion": "success"},
            {"id": 2, "name": "GCL conformance", "status": "in_progress", "conclusion": None},
        ])
        observed = synchronization.successful_workflows(client, "grandchallenge/MATH-PROGRAMME", "a" * 40)
        self.assertEqual(observed, {"Programme policy checks": 1})
        self.assertEqual(synchronization.REQUIRED - set(observed), {"GCL conformance"})

    def test_both_successes_open_synchronization_gate(self) -> None:
        client = FakeClient([
            {"id": 1, "name": "Programme policy checks", "status": "completed", "conclusion": "success"},
            {"id": 2, "name": "GCL conformance", "status": "completed", "conclusion": "success"},
        ])
        observed = synchronization.successful_workflows(client, "grandchallenge/MATH-PROGRAMME", "a" * 40)
        self.assertEqual(set(observed), synchronization.REQUIRED)


if __name__ == "__main__":
    unittest.main()
