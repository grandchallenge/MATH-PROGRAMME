from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
UTC = timezone.utc


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


queue = load_module(
    "administrative_autonomy_runtime_queue_starvation_test",
    ROOT / "ci" / "administrative_autonomy_runtime_queue_starvation.py",
)
continuation = load_module(
    "administrative_autonomy_runtime_transition_continuation_test",
    ROOT / "ci" / "administrative_autonomy_runtime_transition_continuation.py",
)

CONTROL = ROOT / "governance" / "administrative_recovery_queue_starvation_control.json"
SCHEMA = ROOT / "schemas" / "administrative_recovery_queue_starvation_control.schema.json"
RUNTIME = ROOT / "governance" / "administrative_autonomy_runtime_integration.json"
SOURCE = "de8e30dc6c23eca5ff2a0607b179c67a6a90eecc"


def exact_candidate(issue: int = 384, pr: int = 385, source: str = SOURCE):
    manifest = {
        "occurrence_key": "structural_sweep:2026-08-10T03:45:00Z",
        "issue_number": issue,
        "pull_request_number": pr,
        "source_protected_head": source,
    }
    pull = {"number": pr}
    return pull, manifest


class RecordingBase:
    def __init__(self, ordinary, widened):
        self.ordinary = ordinary
        self.widened = widened
        self.calls = []

    def __call__(self, candidate, repo, runtime, now):
        self.calls.append(copy.deepcopy(runtime))
        return self.ordinary if len(self.calls) == 1 else self.widened


def incomplete_completion():
    return {
        "procedures": {
            "structural_sweep": {
                "completed_through_utc": "2026-08-09T10:57:00Z",
                "receipts": [],
            }
        }
    }


class AdministrativeAutonomyQueueStarvationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = json.loads(RUNTIME.read_text(encoding="utf-8"))
        self.control = json.loads(CONTROL.read_text(encoding="utf-8"))
        self.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.load_completion = lambda candidate, repo: incomplete_completion()
        self.ancestral = lambda candidate, repo, source: source == SOURCE

    def test_control_schema_and_nonclaims(self):
        jsonschema.validate(self.control, self.schema)
        self.assertEqual(self.control["status"], "ACTIVE_ON_PROTECTED_MERGE")
        self.assertEqual(
            self.control["correction"]["ordinary_recovery_window_minutes_unchanged"],
            180,
        )
        self.assertFalse(self.control["correction"]["cadence_anchor_reset"])
        self.assertFalse(self.control["correction"]["deadline_reset"])
        self.assertFalse(
            self.control["correction"]["eventual_recovery_relabels_on_time"]
        )
        self.assertTrue(all(value is False for value in self.control["claim_boundaries"].values()))

    def test_control_mutations_fail_schema(self):
        for section, field, value in (
            ("correction", "ordinary_recovery_window_minutes_unchanged", 1008),
            ("correction", "cadence_anchor_reset", True),
            ("correction", "deadline_reset", True),
            ("correction", "eventual_recovery_relabels_on_time", True),
            ("authority_boundary", "bypass_created", True),
            ("authority_boundary", "required_checks_weakened", True),
            ("claim_boundaries", "external_claim_authorized", True),
        ):
            mutated = copy.deepcopy(self.control)
            mutated[section][field] = value
            with self.assertRaises(jsonschema.ValidationError):
                jsonschema.validate(mutated, self.schema)

    def test_receipt_complete_closure_is_quarantined(self):
        blocking = {"pull_request": 385, "receipt_present": False}
        completed = {"pull_request": 362, "receipt_present": True}
        self.assertEqual(
            [blocking],
            queue.filter_receipt_complete_closures([completed, blocking]),
        )

    def test_missing_receipt_evidence_fails_closed(self):
        with self.assertRaises(queue.AutonomyError):
            queue.filter_receipt_complete_closures([{"pull_request": 362}])

    def test_invalid_receipt_evidence_fails_closed(self):
        with self.assertRaises(queue.AutonomyError):
            queue.filter_receipt_complete_closures(
                [{"pull_request": 362, "receipt_present": "yes"}]
            )

    def test_ordinary_candidate_wins_without_continuation(self):
        ordinary = [exact_candidate()]
        base = RecordingBase(ordinary, [])
        result = continuation.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 10, 7, 0, tzinfo=UTC),
            base=base,
            completion_loader=self.load_completion,
            ancestry_checker=self.ancestral,
        )
        self.assertEqual(ordinary, result)
        self.assertEqual(1, len(base.calls))
        self.assertEqual(
            180,
            base.calls[0]["scope"]["recovery_window_minutes_after_due"],
        )

    def test_exact_385_is_admitted_after_starved_window(self):
        base = RecordingBase([], [exact_candidate()])
        original = copy.deepcopy(self.runtime)
        result = continuation.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 10, 7, 0, tzinfo=UTC),
            base=base,
            completion_loader=self.load_completion,
            ancestry_checker=self.ancestral,
        )
        self.assertEqual([exact_candidate()], result)
        self.assertEqual(2, len(base.calls))
        self.assertEqual(
            180,
            base.calls[0]["scope"]["recovery_window_minutes_after_due"],
        )
        self.assertEqual(
            1008,
            base.calls[1]["scope"]["recovery_window_minutes_after_due"],
        )
        self.assertEqual(original, self.runtime)

    def test_continuation_is_not_used_inside_original_window(self):
        base = RecordingBase([], [exact_candidate()])
        result = continuation.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 10, 6, 44, tzinfo=UTC),
            base=base,
            completion_loader=self.load_completion,
            ancestry_checker=self.ancestral,
        )
        self.assertEqual([], result)
        self.assertEqual(1, len(base.calls))

    def test_continuation_expires_at_next_structural_locus(self):
        base = RecordingBase([], [exact_candidate()])
        result = continuation.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 10, 20, 33, tzinfo=UTC),
            base=base,
            completion_loader=self.load_completion,
            ancestry_checker=self.ancestral,
        )
        self.assertEqual([], result)
        self.assertEqual(1, len(base.calls))

    def test_protected_completion_disables_continuation(self):
        completion = incomplete_completion()
        completion["procedures"]["structural_sweep"]["completed_through_utc"] = (
            "2026-08-10T03:45:00Z"
        )
        base = RecordingBase([], [exact_candidate()])
        result = continuation.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 10, 7, 0, tzinfo=UTC),
            base=base,
            completion_loader=lambda candidate, repo: completion,
            ancestry_checker=self.ancestral,
        )
        self.assertEqual([], result)
        self.assertEqual(1, len(base.calls))

    def test_nonancestral_source_fails_closed(self):
        base = RecordingBase([], [exact_candidate()])
        with self.assertRaises(continuation.AutonomyError):
            continuation.eligible_candidates(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime,
                datetime(2026, 8, 10, 7, 0, tzinfo=UTC),
                base=base,
                completion_loader=self.load_completion,
                ancestry_checker=lambda candidate, repo, source: False,
            )

    def test_identity_drift_fails_closed(self):
        for candidate in (
            exact_candidate(issue=999),
            exact_candidate(pr=999),
            exact_candidate(source="f" * 40),
        ):
            base = RecordingBase([], [candidate])
            with self.assertRaises(continuation.AutonomyError):
                continuation.eligible_candidates(
                    object(),
                    "grandchallenge/MATH-PROGRAMME",
                    self.runtime,
                    datetime(2026, 8, 10, 7, 0, tzinfo=UTC),
                    base=base,
                    completion_loader=self.load_completion,
                    ancestry_checker=self.ancestral,
                )

    def test_naive_time_fails_closed(self):
        base = RecordingBase([], [exact_candidate()])
        with self.assertRaises(continuation.AutonomyError):
            continuation.eligible_candidates(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime,
                datetime(2026, 8, 10, 7, 0),
                base=base,
                completion_loader=self.load_completion,
                ancestry_checker=self.ancestral,
            )


if __name__ == "__main__":
    unittest.main()
