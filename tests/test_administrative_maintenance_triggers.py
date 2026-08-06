from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "governance" / "administrative_maintenance_trigger_registry.json"
SCHEMA_PATH = ROOT / "schemas" / "administrative_maintenance_trigger_registry.schema.json"
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "administrative-maintenance-dispatch.yml"
SCRIPT_PATH = ROOT / "ci" / "dispatch_administrative_maintenance.py"

SPEC = importlib.util.spec_from_file_location("maintenance_dispatcher", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
dispatcher = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = dispatcher
SPEC.loader.exec_module(dispatcher)


class AdministrativeMaintenanceTriggerTests(unittest.TestCase):
    def load_registry(self) -> dict:
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def errors_for(self, registry: dict) -> list[str]:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        return [error.message for error in validator.iter_errors(registry)]

    def procedure(self, name: str) -> dict:
        return next(item for item in self.load_registry()["procedures"] if item["id"] == name)

    def test_registry_is_schema_valid(self) -> None:
        self.assertEqual(self.errors_for(self.load_registry()), [])

    def test_first_completed_sweep_is_not_redispatched(self) -> None:
        procedure = self.procedure("structural_sweep")
        now = dispatcher.parse_datetime("2026-08-01T18:09:00Z")
        self.assertEqual(dispatcher.due_occurrences(procedure, now), [])

    def test_second_structural_sweep_is_due_at_exact_anchor(self) -> None:
        procedure = self.procedure("structural_sweep")
        before = dispatcher.parse_datetime("2026-08-02T10:56:59Z")
        due = dispatcher.parse_datetime("2026-08-02T10:57:00Z")
        self.assertEqual(dispatcher.due_occurrences(procedure, before), [])
        self.assertEqual(
            [dispatcher.iso_z(value) for value in dispatcher.due_occurrences(procedure, due)],
            ["2026-08-02T10:57:00Z"],
        )

    def test_exact_schedule_dispatches_due_procedure(self) -> None:
        registry = self.load_registry()
        now = dispatcher.parse_datetime("2026-08-02T10:57:00Z")
        dispatches = dispatcher.build_dispatches(
            registry,
            "schedule",
            {"schedule": "57 10 2 8 *"},
            now,
            "auto",
        )
        self.assertEqual([item.key for item in dispatches], [
            "scheduled:structural_sweep:2026-08-02T10:57:00Z"
        ])

    def test_watchdog_recovers_recent_missed_dispatch(self) -> None:
        registry = self.load_registry()
        now = dispatcher.parse_datetime("2026-08-02T11:47:00Z")
        dispatches = dispatcher.build_dispatches(
            registry,
            "schedule",
            {"schedule": "47 * * * *"},
            now,
            "auto",
        )
        self.assertEqual(len(dispatches), 1)
        self.assertEqual(dispatches[0].due_at, "2026-08-02T10:57:00Z")

    def test_watchdog_does_not_repeat_old_dispatch(self) -> None:
        registry = self.load_registry()
        now = dispatcher.parse_datetime("2026-08-02T11:58:00Z")
        dispatches = dispatcher.build_dispatches(
            registry,
            "schedule",
            {"schedule": "47 * * * *"},
            now,
            "auto",
        )
        self.assertEqual(dispatches, [])

    def test_three_day_review_is_anchored(self) -> None:
        procedure = self.procedure("administrative_review")
        due = dispatcher.parse_datetime("2026-08-04T01:21:00Z")
        self.assertEqual(
            [dispatcher.iso_z(value) for value in dispatcher.due_occurrences(procedure, due)],
            ["2026-08-04T01:21:00Z"],
        )

    def test_pilot_close_dispatches_three_distinct_procedures(self) -> None:
        registry = self.load_registry()
        now = dispatcher.parse_datetime("2026-08-10T01:21:00Z")
        dispatches = dispatcher.build_dispatches(
            registry,
            "schedule",
            {"schedule": "21 1 4,7,10 8 *"},
            now,
            "auto",
        )
        keys = {item.key for item in dispatches}
        self.assertIn("scheduled:administrative_review:2026-08-10T01:21:00Z", keys)
        self.assertIn("scheduled:deep_conformance_review:2026-08-10T01:21:00Z", keys)
        self.assertIn("scheduled:pilot_review:2026-08-10T01:21:00Z", keys)

    def test_constitutional_review_due_is_preserved(self) -> None:
        procedure = self.procedure("constitutional_review")
        due = dispatcher.parse_datetime("2026-09-06T13:21:00Z")
        self.assertEqual(dispatcher.due_occurrences(procedure, due), [due])

    def test_governed_push_creates_material_sync_triage(self) -> None:
        now = dispatcher.parse_datetime("2026-08-02T04:45:00Z")
        dispatches = dispatcher.event_dispatches("push", {"after": "a" * 40}, now)
        self.assertEqual(len(dispatches), 1)
        self.assertEqual(dispatches[0].severity, "P2")
        self.assertIn("2026-08-02T11:57:00Z", dispatches[0].body)
        self.assertIn("evidence only", dispatches[0].body)

    def test_pull_request_lifecycle_emits_interference_evidence(self) -> None:
        now = dispatcher.parse_datetime("2026-08-02T04:45:00Z")
        event = {
            "action": "synchronize",
            "number": 203,
            "pull_request": {
                "number": 203,
                "draft": True,
                "head": {"sha": "a" * 40},
                "base": {"sha": "b" * 40},
            },
        }
        dispatches = dispatcher.event_dispatches("pull_request", event, now)
        self.assertEqual(len(dispatches), 1)
        self.assertEqual(dispatches[0].severity, "P3")
        self.assertIn("does not authorize merge", dispatches[0].body)

    def test_required_workflow_failure_is_p1(self) -> None:
        now = dispatcher.parse_datetime("2026-08-02T04:45:00Z")
        dispatches = dispatcher.event_dispatches(
            "workflow_run",
            {"workflow_run": {"id": 123, "name": "Programme policy checks", "conclusion": "failure"}},
            now,
        )
        self.assertEqual(len(dispatches), 1)
        self.assertEqual(dispatches[0].severity, "P1")

    def test_successful_required_workflow_does_not_emit_failure(self) -> None:
        now = dispatcher.parse_datetime("2026-08-02T04:45:00Z")
        dispatches = dispatcher.event_dispatches(
            "workflow_run",
            {"workflow_run": {"id": 123, "name": "Programme policy checks", "conclusion": "success"}},
            now,
        )
        self.assertEqual(dispatches, [])

    def test_dispatcher_ignores_its_own_issue_mirror(self) -> None:
        now = dispatcher.parse_datetime("2026-08-02T04:45:00Z")
        event = {
            "action": "opened",
            "issue": {
                "number": 999,
                "title": "[maintenance-dispatch] test",
                "body": "<!-- maintenance-dispatch:test --> may_adjudicate: true",
            },
        }
        self.assertEqual(dispatcher.event_dispatches("issues", event, now), [])

    def test_issue_authority_inflation_is_p1(self) -> None:
        now = dispatcher.parse_datetime("2026-08-02T04:45:00Z")
        event = {
            "action": "edited",
            "issue": {
                "number": 77,
                "title": "Mutable authority attempt",
                "body": "may_adjudicate: true",
            },
        }
        dispatches = dispatcher.event_dispatches("issues", event, now)
        self.assertEqual(len(dispatches), 1)
        self.assertEqual(dispatches[0].severity, "P1")

    def test_workflow_has_exact_read_only_and_event_triggers(self) -> None:
        workflow = WORKFLOW_PATH.read_text(encoding="utf-8")
        for fragment in (
            "cron: '57 10 2 8 *'",
            "cron: '21 1 4,7,10 8 *'",
            "cron: '47 * * * *'",
            "workflow_dispatch:",
            "branch_protection_rule:",
            "workflow_run:",
            "pull_request:",
            "issues:",
            "push:",
            "permissions:\n  contents: read\n",
            "Enforce P1 fail-closed signal",
        ):
            self.assertIn(fragment, workflow)
        self.assertNotIn("issues: write", workflow)
        self.assertNotIn("actions: read", workflow)

        pins = self.load_registry()["workflow"]["pinned_actions"]
        expected_actions = {
            "checkout": "actions/checkout",
            "setup_python": "actions/setup-python",
            "upload_artifact": "actions/upload-artifact",
        }
        for key, action in expected_actions.items():
            self.assertIn(f"{action}@{pins[key]}", workflow)

    def test_mutation_rejects_anchor_reset(self) -> None:
        registry = self.load_registry()
        registry["schedule"]["anchor_utc"] = "2026-08-02T00:00:00Z"
        self.assertTrue(self.errors_for(registry))

    def test_mutation_rejects_disabled_branch_protection_trigger(self) -> None:
        registry = self.load_registry()
        registry["event_triggers"]["branch_protection_rule"]["enabled"] = False
        self.assertTrue(self.errors_for(registry))

    def test_mutation_rejects_issue_creation_authority(self) -> None:
        registry = self.load_registry()
        registry["dispatch"]["may_create_issue"] = True
        self.assertTrue(self.errors_for(registry))

    def test_main_dry_run_writes_non_authoritative_report(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            event_path = Path(temporary) / "event.json"
            report_path = Path(temporary) / "report.json"
            event_path.write_text(json.dumps({"schedule": "57 10 2 8 *"}), encoding="utf-8")
            with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "schedule"}, clear=False):
                result = dispatcher.main(
                    [
                        "--event-path",
                        str(event_path),
                        "--procedure",
                        "auto",
                        "--now",
                        "2026-08-02T10:57:00Z",
                        "--dry-run",
                        "--report",
                        str(report_path),
                    ]
                )
            self.assertEqual(result, 0)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["dispatch_count"], 1)
            self.assertFalse(report["authority_boundary"]["issue_creation_allowed"])
            self.assertFalse(report["authority_boundary"]["claim_promotion"])
            self.assertFalse(report["authority_boundary"]["schedule_anchor_reset"])

    def test_main_operational_report_uses_read_only_delivery(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            event_path = Path(temporary) / "event.json"
            report_path = Path(temporary) / "report.json"
            event_path.write_text(json.dumps({"action": "opened", "number": 10, "pull_request": {"number": 10, "head": {"sha": "a" * 40}, "base": {"sha": "b" * 40}}}), encoding="utf-8")
            with patch.dict(os.environ, {"GITHUB_EVENT_NAME": "pull_request"}, clear=False):
                result = dispatcher.main([
                    "--event-path", str(event_path),
                    "--procedure", "auto",
                    "--now", "2026-08-02T04:45:00Z",
                    "--report", str(report_path),
                ])
            self.assertEqual(result, 0)
            report = json.loads(report_path.read_text(encoding="utf-8"))
            self.assertEqual(report["dispatches"][0]["disposition"], "emitted")
            self.assertIn("retained_json_artifact", report["delivery_channels"])
            self.assertFalse(report["authority_boundary"]["issue_creation_allowed"])


if __name__ == "__main__":
    unittest.main()
