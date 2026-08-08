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
MODULE_PATH = ROOT / "ci" / "administrative_autonomy_runtime_late_recovery.py"
SPEC = importlib.util.spec_from_file_location(
    "administrative_autonomy_runtime_late_recovery",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
late = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = late
SPEC.loader.exec_module(late)

UTC = timezone.utc


def exact_candidate(issue: int = 312, pr: int = 313):
    manifest = {
        "occurrence_key": "structural_sweep:2026-08-08T18:09:00Z",
        "issue_number": issue,
        "pull_request_number": pr,
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
        if len(self.calls) == 1:
            return self.ordinary
        return self.widened


class AdministrativeAutonomyLateRecoveryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_runtime_integration.json"
            ).read_text(encoding="utf-8")
        )

    def test_ordinary_candidate_wins_without_override(self) -> None:
        ordinary = [exact_candidate()]
        base = RecordingBase(ordinary, [])
        result = late.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 8, 20, 0, tzinfo=UTC),
            base=base,
        )
        self.assertEqual(ordinary, result)
        self.assertEqual(1, len(base.calls))
        self.assertEqual(
            180,
            base.calls[0]["scope"]["recovery_window_minutes_after_due"],
        )

    def test_exact_occurrence_is_admitted_after_ordinary_window(self) -> None:
        base = RecordingBase([], [exact_candidate()])
        original = copy.deepcopy(self.runtime)
        result = late.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 8, 23, 0, tzinfo=UTC),
            base=base,
        )
        self.assertEqual([exact_candidate()], result)
        self.assertEqual(2, len(base.calls))
        self.assertEqual(
            180,
            base.calls[0]["scope"]["recovery_window_minutes_after_due"],
        )
        self.assertGreater(
            base.calls[1]["scope"]["recovery_window_minutes_after_due"],
            180,
        )
        self.assertEqual(original, self.runtime)

    def test_override_expires_at_pilot_boundary(self) -> None:
        base = RecordingBase([], [exact_candidate()])
        result = late.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 10, 1, 21, 1, tzinfo=UTC),
            base=base,
        )
        self.assertEqual([], result)
        self.assertEqual(1, len(base.calls))

    def test_nonmatching_occurrence_is_not_admitted(self) -> None:
        pull, manifest = exact_candidate()
        manifest = dict(manifest)
        manifest["occurrence_key"] = "structural_sweep:2026-08-09T10:57:00Z"
        base = RecordingBase([], [(pull, manifest)])
        result = late.eligible_candidates(
            object(),
            "grandchallenge/MATH-PROGRAMME",
            self.runtime,
            datetime(2026, 8, 8, 23, 0, tzinfo=UTC),
            base=base,
        )
        self.assertEqual([], result)

    def test_issue_identity_drift_fails_closed(self) -> None:
        base = RecordingBase([], [exact_candidate(issue=999)])
        with self.assertRaises(late.AutonomyError):
            late.eligible_candidates(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime,
                datetime(2026, 8, 8, 23, 0, tzinfo=UTC),
                base=base,
            )

    def test_pull_request_identity_drift_fails_closed(self) -> None:
        pull, manifest = exact_candidate()
        pull = {"number": 999}
        base = RecordingBase([], [(pull, manifest)])
        with self.assertRaises(late.AutonomyError):
            late.eligible_candidates(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime,
                datetime(2026, 8, 8, 23, 0, tzinfo=UTC),
                base=base,
            )

    def test_naive_time_fails_closed(self) -> None:
        base = RecordingBase([], [exact_candidate()])
        with self.assertRaises(late.AutonomyError):
            late.eligible_candidates(
                object(),
                "grandchallenge/MATH-PROGRAMME",
                self.runtime,
                datetime(2026, 8, 8, 23, 0),
                base=base,
            )


if __name__ == "__main__":
    unittest.main()
