from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from administrative_autonomy_runtime_contract import record_path_for
from administrative_autonomy_runtime_github import verify_scope
from autonomy_github import AutonomyError


class FakeFilesClient:
    def __init__(self, filenames: list[str]):
        self.filenames = filenames

    def get(self, path: str):
        if "/pulls/" not in path or "/files" not in path:
            raise AssertionError(path)
        return [
            {"filename": name, "additions": 1, "deletions": 0}
            for name in self.filenames
        ]


class AdministrativeAutonomyFinalRecordPathTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_runtime_integration.json"
            ).read_text(encoding="utf-8")
        )
        self.manifest = {
            "occurrence_key": "structural_sweep:2026-08-08T18:09:00Z",
            "procedure_id": "structural_sweep",
            "scheduled_due_at": "2026-08-08T18:09:00Z",
            "manifest_path": (
                "governance/administrative_candidates/"
                "structural_sweep-20260808T180900Z.json"
            ),
        }
        self.prefix = "MP-ADMIN-STRUCTURAL-SWEEP"

    def record(self, sequence: int, date: str = "2026-08-08") -> str:
        return f"{self.prefix}-{date}-{sequence:03d}.json"

    def test_no_same_day_record_allocates_001(self) -> None:
        record_id, _ = record_path_for(self.runtime, self.manifest, [])
        self.assertEqual(f"{self.prefix}-2026-08-08-001", record_id)

    def test_existing_001_allocates_002(self) -> None:
        record_id, _ = record_path_for(
            self.runtime,
            self.manifest,
            [self.record(1)],
        )
        self.assertEqual(f"{self.prefix}-2026-08-08-002", record_id)

    def test_existing_001_and_002_allocate_003(self) -> None:
        record_id, _ = record_path_for(
            self.runtime,
            self.manifest,
            [self.record(1), self.record(2)],
        )
        self.assertEqual(f"{self.prefix}-2026-08-08-003", record_id)

    def test_other_dates_do_not_advance_same_day_sequence(self) -> None:
        record_id, _ = record_path_for(
            self.runtime,
            self.manifest,
            [self.record(42, "2026-08-07"), self.record(1)],
        )
        self.assertEqual(f"{self.prefix}-2026-08-08-002", record_id)

    def test_malformed_names_do_not_advance_sequence(self) -> None:
        names = [
            f"{self.prefix}-2026-08-08-ABC.json",
            f"{self.prefix}-2026-08-08-002.txt",
            f"{self.prefix}-2026-08-08-0002.json",
            "UNRELATED-2026-08-08-999.json",
        ]
        record_id, _ = record_path_for(self.runtime, self.manifest, names)
        self.assertEqual(f"{self.prefix}-2026-08-08-001", record_id)

    def test_existing_same_day_record_is_not_reused(self) -> None:
        record_id, path = record_path_for(
            self.runtime,
            self.manifest,
            [self.record(1)],
        )
        self.assertNotEqual(f"{self.prefix}-2026-08-08-001", record_id)
        self.assertTrue(path.endswith("-002.json"))

    def test_scope_gate_still_rejects_manifest_only_transition(self) -> None:
        _, record_path = record_path_for(
            self.runtime,
            self.manifest,
            [self.record(1)],
        )
        client = FakeFilesClient([self.manifest["manifest_path"]])
        with self.assertRaises(AutonomyError):
            verify_scope(
                client,
                "grandchallenge/MATH-PROGRAMME",
                313,
                self.manifest["manifest_path"],
                record_path,
                self.runtime["scope"],
            )

    def test_scope_gate_accepts_exact_manifest_and_final_record_paths(self) -> None:
        _, record_path = record_path_for(
            self.runtime,
            self.manifest,
            [self.record(1)],
        )
        client = FakeFilesClient(
            sorted([self.manifest["manifest_path"], record_path])
        )
        verify_scope(
            client,
            "grandchallenge/MATH-PROGRAMME",
            313,
            self.manifest["manifest_path"],
            record_path,
            self.runtime["scope"],
        )


if __name__ == "__main__":
    unittest.main()
