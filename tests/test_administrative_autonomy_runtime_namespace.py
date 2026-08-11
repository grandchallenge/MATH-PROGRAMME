from __future__ import annotations

import json
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_runtime_github as runtime_github  # noqa: E402
from autonomy_github import AutonomyError  # noqa: E402


REPO = "grandchallenge/MATH-PROGRAMME"


class FakeClient:
    def __init__(self, pulls: list[dict]):
        self.pulls = pulls

    def get(self, path: str):
        if path == f"/repos/{REPO}/pulls?state=open&per_page=100":
            return list(self.pulls)
        if "/contents/" in path:
            raise AutonomyError(f"GET {path} failed: 404 synthetic missing content")
        raise AssertionError(f"unexpected GET {path}")


def pull(branch: str, login: str, *, state: str = "open", merged: bool = False) -> dict:
    return {
        "number": 900,
        "state": state,
        "merged_at": "2026-08-10T20:00:00Z" if merged else None,
        "head": {"ref": branch},
        "user": {"login": login},
    }


class AdministrativeAutonomyRuntimeNamespaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.runtime = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_runtime_integration.json"
            ).read_text(encoding="utf-8")
        )
        self.prefix = self.runtime["scope"]["branch_prefix"]
        self.candidate_login = self.runtime["candidate_identity"]["login"]
        self.now = datetime(2026, 8, 10, 21, 0, tzinfo=timezone.utc)

    def test_historical_receipt_forms_are_excluded_before_core_scanning(self) -> None:
        branches = [
            f"{self.prefix}receipt-structural_sweep-20260810T034500Z",
            f"{self.prefix}receipt-administrative_review-20260810T203300Z",
            f"{self.prefix}receipt-",
            f"{self.prefix}receipt-pilot_review-20260810T012100Z",
        ]
        pulls = [
            pull(branches[0], "unexpected[bot]"),  # stale open receipt
            pull(branches[1], "unexpected[bot]"),  # ordinary open receipt
            pull(branches[2], "unexpected[bot]"),  # malformed receipt
            pull(branches[3], "unexpected[bot]", state="closed", merged=True),
        ]

        observed: list[dict] = []
        original = runtime_github._ordinary_eligible_candidates

        def capture(client, repo, runtime, now):
            observed.extend(
                client.get(f"/repos/{repo}/pulls?state=open&per_page=100")
            )
            return []

        runtime_github._ordinary_eligible_candidates = capture
        try:
            result = runtime_github.eligible_candidates(
                FakeClient(pulls), REPO, self.runtime, self.now
            )
        finally:
            runtime_github._ordinary_eligible_candidates = original

        self.assertEqual([], result)
        self.assertEqual([], observed)

    def test_candidate_like_receipt_name_is_not_overfiltered(self) -> None:
        branch = f"{self.prefix}receiptish-structural_sweep-20260810T203300Z"
        client = FakeClient([pull(branch, "wrong-identity[bot]")])
        with self.assertRaisesRegex(
            AutonomyError,
            "maintenance branch is not authored by Candidate Agent",
        ):
            runtime_github.eligible_candidates(
                client, REPO, self.runtime, self.now
            )

    def test_actual_candidate_missing_manifest_still_fails_closed(self) -> None:
        branch = f"{self.prefix}structural_sweep-20260810T203300Z"
        client = FakeClient([pull(branch, self.candidate_login)])
        with self.assertRaisesRegex(AutonomyError, "candidate manifest missing"):
            runtime_github.eligible_candidates(
                client, REPO, self.runtime, self.now
            )

    def test_classifier_is_explicit_and_recovery_window_is_unchanged(self) -> None:
        receipt = f"{self.prefix}receipt-structural_sweep-20260810T203300Z"
        candidate = f"{self.prefix}structural_sweep-20260810T203300Z"
        outside = "agent/407-receipt-candidate-namespace"

        self.assertEqual(
            "receipt",
            runtime_github.maintenance_branch_namespace(receipt, self.prefix),
        )
        self.assertEqual(
            "candidate",
            runtime_github.maintenance_branch_namespace(candidate, self.prefix),
        )
        self.assertEqual(
            "outside",
            runtime_github.maintenance_branch_namespace(outside, self.prefix),
        )
        self.assertEqual(
            180,
            self.runtime["scope"]["recovery_window_minutes_after_due"],
        )


if __name__ == "__main__":
    unittest.main()
