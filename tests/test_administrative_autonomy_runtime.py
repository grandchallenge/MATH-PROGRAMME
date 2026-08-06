from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
MODULE_PATH = ROOT / "ci" / "administrative_autonomy_runtime.py"
SPEC = importlib.util.spec_from_file_location(
    "administrative_autonomy_runtime",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
runtime_module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = runtime_module
SPEC.loader.exec_module(runtime_module)


class FakeChecksClient:
    def __init__(self, runs: list[dict]):
        self.runs = runs

    def get(self, path: str):
        return {"check_runs": self.runs}


class AdministrativeAutonomyRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_runtime_integration.json"
            ).read_text(encoding="utf-8")
        )
        self.activation = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_activation.json"
            ).read_text(encoding="utf-8")
        )
        self.manifest = {
            "schema_version": "1.0.0",
            "state": "CANDIDATE_PREPARED",
            "control_id": "MP-ADMIN-MAINT-001",
            "occurrence_key": "structural_sweep:2026-08-06T15:45:00Z",
            "procedure_id": "structural_sweep",
            "scheduled_due_at": "2026-08-06T15:45:00Z",
            "prepare_at": "2026-08-06T09:45:00Z",
            "freeze_at": "2026-08-06T14:15:00Z",
            "generated_at": "2026-08-06T09:45:10Z",
            "source_protected_head": "9" * 40,
            "branch": "automation/maintenance/structural_sweep-20260806T154500Z",
            "manifest_path": "governance/administrative_candidates/structural_sweep-20260806T154500Z.json",
            "issue_number": 261,
            "pull_request_number": 262,
            "evidence_digest": "a" * 64,
            "repository_state": [],
            "authority_boundary": {
                "protected_authority_created": False,
                "independent_approval_created": False,
                "human_steward_disposition_created": False,
                "merge_authorized": False,
                "merge_performed": False,
                "candidate_is_final_record": False,
            },
            "claim_boundaries": dict(self.runtime["claim_boundaries"]),
        }
        self.state = [
            {
                "repository": name,
                "default_branch": "main",
                "protected_head": str(index) * 40,
                "open_pull_requests": [],
            }
            for index, name in enumerate(
                sorted(runtime_module.ALLOWED_REPOSITORIES), start=1
            )
        ]

    def test_runtime_contract_is_valid(self) -> None:
        self.assertEqual(
            [], runtime_module.validate_runtime_contract(self.runtime)
        )

    def test_protected_activation_is_valid(self) -> None:
        self.assertEqual(
            [],
            runtime_module.validate_activation(
                self.runtime,
                self.activation,
            ),
        )

    def test_pilot_may_not_be_automated(self) -> None:
        mutated = copy.deepcopy(self.runtime)
        mutated["automated_procedures"].append("pilot_review")
        mutated["manual_procedures"].remove("pilot_review")
        self.assertTrue(runtime_module.validate_runtime_contract(mutated))

    def test_human_steward_impersonation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.runtime)
        mutated["authority_boundary"][
            "automated_human_steward_disposition"
        ] = True
        errors = runtime_module.validate_runtime_contract(mutated)
        self.assertTrue(any("Human Steward" in item for item in errors))

    def test_candidate_referee_collision_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.runtime)
        mutated["referee_identity"]["login"] = mutated[
            "candidate_identity"
        ]["login"]
        errors = runtime_module.validate_runtime_contract(mutated)
        self.assertTrue(any("collide" in item for item in errors))

    def test_activation_state_must_be_active(self) -> None:
        mutated = copy.deepcopy(self.activation)
        mutated["state"] = "ARMED_NOT_ACTIVE"
        self.assertIn(
            "activation state drift",
            runtime_module.validate_activation(self.runtime, mutated),
        )

    def test_first_record_identity_is_locked(self) -> None:
        record_id, path = runtime_module.record_path_for(
            self.runtime,
            self.manifest,
            [],
        )
        self.assertEqual(
            "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-06-008",
            record_id,
        )
        self.assertEqual(
            "governance/administrative_structural_sweeps/"
            "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-06-008.json",
            path,
        )

    def test_built_record_is_valid(self) -> None:
        record = runtime_module.build_record(
            self.runtime,
            self.activation,
            self.manifest,
            "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-06-008",
            self.state,
            datetime(2026, 8, 6, 14, 15, tzinfo=timezone.utc),
        )
        self.assertEqual([], runtime_module.validate_record(record))
        self.assertFalse(
            record["execution_contract"]["human_steward_identity_asserted"]
        )
        self.assertFalse(record["execution_contract"]["bypass_used"])

    def test_record_claim_inflation_is_rejected(self) -> None:
        record = runtime_module.build_record(
            self.runtime,
            self.activation,
            self.manifest,
            "MP-ADMIN-STRUCTURAL-SWEEP-2026-08-06-008",
            self.state,
            datetime(2026, 8, 6, 14, 15, tzinfo=timezone.utc),
        )
        record["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(runtime_module.validate_record(record))

    def test_failed_check_is_rejected(self) -> None:
        client = FakeChecksClient(
            [
                {
                    "name": "validate-json",
                    "status": "completed",
                    "conclusion": "failure",
                    "started_at": "2026-08-06T14:20:00Z",
                }
            ]
        )
        with self.assertRaises(runtime_module.AutonomyError):
            runtime_module.check_runs_state(
                client,
                "grandchallenge/MATH-PROGRAMME",
                "a" * 40,
                {"success", "neutral", "skipped"},
                {"validate-json"},
            )

    def test_pending_comment_check_prevents_merge(self) -> None:
        client = FakeChecksClient(
            [
                {
                    "name": "validate-json",
                    "status": "completed",
                    "conclusion": "success",
                    "started_at": "2026-08-06T14:20:00Z",
                },
                {
                    "name": "Administrative maintenance dispatcher",
                    "status": "in_progress",
                    "conclusion": None,
                    "started_at": "2026-08-06T14:21:00Z",
                },
            ]
        )
        settled, observed = runtime_module.check_runs_state(
            client,
            "grandchallenge/MATH-PROGRAMME",
            "a" * 40,
            {"success", "neutral", "skipped"},
            {"validate-json"},
        )
        self.assertFalse(settled)
        self.assertEqual(
            "in_progress",
            observed["Administrative maintenance dispatcher"],
        )


if __name__ == "__main__":
    unittest.main()
