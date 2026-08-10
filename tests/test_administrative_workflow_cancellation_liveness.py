from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import dispatch_administrative_maintenance as legacy
import dispatch_administrative_maintenance_v2 as dispatcher
import dispatch_administrative_maintenance_v3 as dispatcher_v3

UTC = timezone.utc
NOW = datetime(2026, 8, 10, 12, 15, 23, tzinfo=UTC)
OLD_HEAD = "d80f5ed7c49730aa6d11f9ae3a80c203511c0637"
NEW_HEAD = "696a89ed5675e275d74ab69929ac31b698e389f2"


def workflow_event(
    conclusion: str,
    *,
    run_head: str = OLD_HEAD,
    pr_heads: tuple[str, ...] = (NEW_HEAD,),
    run_id: int = 31386125203,
) -> dict:
    return {
        "workflow_run": {
            "id": run_id,
            "name": "Programme policy checks",
            "conclusion": conclusion,
            "head_sha": run_head,
            "pull_requests": [
                {"number": 376 + index, "head": {"sha": head}}
                for index, head in enumerate(pr_heads)
            ],
        }
    }


def reconciled(event: dict) -> list[legacy.Dispatch]:
    initial = legacy.event_dispatches("workflow_run", event, NOW)
    return dispatcher.reconcile_workflow_run_liveness("workflow_run", event, initial, NOW)


class AdministrativeWorkflowCancellationLivenessTests(unittest.TestCase):
    def test_superseded_cancelled_pr_run_becomes_p3_evidence(self) -> None:
        dispatches = reconciled(workflow_event("cancelled"))
        self.assertEqual(len(dispatches), 1)
        self.assertEqual(dispatches[0].severity, "P3")
        self.assertEqual(
            dispatches[0].key,
            "event:workflow-superseded-cancellation:31386125203",
        )
        self.assertNotIn("event:workflow-failure:31386125203", {item.key for item in dispatches})

    def test_cancelled_current_head_remains_p1(self) -> None:
        dispatches = reconciled(
            workflow_event("cancelled", run_head=NEW_HEAD, pr_heads=(NEW_HEAD,))
        )
        self.assertEqual([item.severity for item in dispatches], ["P1"])

    def test_cancelled_without_pr_head_evidence_remains_p1(self) -> None:
        dispatches = reconciled(workflow_event("cancelled", pr_heads=()))
        self.assertEqual([item.severity for item in dispatches], ["P1"])

    def test_non_cancelled_failure_remains_p1_even_if_pr_advanced(self) -> None:
        dispatches = reconciled(workflow_event("failure"))
        self.assertEqual([item.severity for item in dispatches], ["P1"])

    def test_success_emits_no_workflow_failure_dispatch(self) -> None:
        self.assertEqual(reconciled(workflow_event("success")), [])

    def test_any_current_head_match_blocks_supersession(self) -> None:
        dispatches = reconciled(
            workflow_event("cancelled", pr_heads=(NEW_HEAD, OLD_HEAD))
        )
        self.assertEqual([item.severity for item in dispatches], ["P1"])

    def test_v3_production_binding_reports_zero_p1_for_reproduced_case(self) -> None:
        self.assertIs(dispatcher_v3.implementation, dispatcher)
        event = workflow_event("cancelled")
        initial = legacy.event_dispatches("workflow_run", event, NOW)
        dispatches = dispatcher_v3.implementation.reconcile_workflow_run_liveness(
            "workflow_run", event, initial, NOW
        )
        severity_counts = {
            severity: sum(item.severity == severity for item in dispatches)
            for severity in ("P1", "P2", "P3")
        }
        self.assertEqual(severity_counts, {"P1": 0, "P2": 0, "P3": 1})


if __name__ == "__main__":
    unittest.main()