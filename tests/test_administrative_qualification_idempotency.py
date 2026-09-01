from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from administrative_protected_receipt_live import (
    IDEMPOTENCY_IGNORED_ADVISORY_FIELDS,
    _mergeability_advisory,
    _stable_snapshot_digest,
    _stable_snapshot_projection,
)


class QualificationIdempotencyTests(unittest.TestCase):
    def snapshot(self):
        return {
            "protected_head": "a" * 40,
            "configuration": {
                "state": "CONVERGED",
                "observed_digest": "1" * 64,
            },
            "receipt_pull": {
                "number": 596,
                "head_sha": "b" * 40,
                "declared_base_sha": "c" * 40,
                "state": "open",
                "facts": {
                    "current_base_sha": "a" * 40,
                    "candidate_head_sha": "b" * 40,
                    "candidate_recorded_base_sha": "c" * 40,
                    "branch_state": "BEHIND_CURRENT_BASE",
                    "conflict_state": "UNKNOWN",
                    "check_state": "PASSING",
                    "update_branch_state": "NOT_PERMITTED_BY_POLICY",
                    "raw_advisory": {
                        "mergeable": None,
                        "mergeable_state": "unknown",
                    },
                },
                "review_state": "PRESENT_FOR_HEAD",
            },
            "authoritative_frontier": {
                "completed_through_utc": "2026-08-10T01:21:00Z",
                "receipt_count": 3,
                "ledger_digest": "2" * 64,
            },
            "mirror_results": [
                {"state": "MIRROR_CONFLICTED", "derived_frontier": "2026-08-16T01:21:00Z"}
            ],
            "safety": {
                "mutation_performed": False,
                "bypass_exercised": False,
                "direct_protected_push": False,
                "reactivation_authorized": False,
            },
        }

    def test_mergeability_advisory_transition_is_digest_stable(self):
        first = self.snapshot()
        second = copy.deepcopy(first)
        second["receipt_pull"]["facts"]["conflict_state"] = "CONFLICTED"
        second["receipt_pull"]["facts"]["raw_advisory"] = {
            "mergeable": False,
            "mergeable_state": "dirty",
        }
        self.assertEqual(_stable_snapshot_digest(first), _stable_snapshot_digest(second))
        self.assertNotEqual(_mergeability_advisory(first), _mergeability_advisory(second))

    def test_projection_removes_only_declared_advisory_fields(self):
        value = self.snapshot()
        projected = _stable_snapshot_projection(value)
        facts = projected["receipt_pull"]["facts"]
        self.assertNotIn("conflict_state", facts)
        self.assertNotIn("raw_advisory", facts)
        self.assertEqual("PASSING", facts["check_state"])
        self.assertEqual("BEHIND_CURRENT_BASE", facts["branch_state"])
        self.assertEqual(
            (
                "receipt_pull.facts.conflict_state",
                "receipt_pull.facts.raw_advisory",
            ),
            IDEMPOTENCY_IGNORED_ADVISORY_FIELDS,
        )

    def test_authoritative_receipt_head_change_breaks_idempotency(self):
        first = self.snapshot()
        second = copy.deepcopy(first)
        second["receipt_pull"]["head_sha"] = "d" * 40
        self.assertNotEqual(_stable_snapshot_digest(first), _stable_snapshot_digest(second))

    def test_authoritative_ledger_change_breaks_idempotency(self):
        first = self.snapshot()
        second = copy.deepcopy(first)
        second["authoritative_frontier"]["receipt_count"] = 4
        self.assertNotEqual(_stable_snapshot_digest(first), _stable_snapshot_digest(second))

    def test_ruleset_digest_change_breaks_idempotency(self):
        first = self.snapshot()
        second = copy.deepcopy(first)
        second["configuration"]["observed_digest"] = "3" * 64
        self.assertNotEqual(_stable_snapshot_digest(first), _stable_snapshot_digest(second))

    def test_branch_state_change_breaks_idempotency(self):
        first = self.snapshot()
        second = copy.deepcopy(first)
        second["receipt_pull"]["facts"]["branch_state"] = "AT_CURRENT_BASE"
        self.assertNotEqual(_stable_snapshot_digest(first), _stable_snapshot_digest(second))


if __name__ == "__main__":
    unittest.main()
