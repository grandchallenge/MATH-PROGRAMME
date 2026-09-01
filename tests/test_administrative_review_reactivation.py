from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AdministrativeReviewReactivationTests(unittest.TestCase):
    def test_production_runtime_uses_generic_receipt_path_without_suspension_wrappers(self):
        text = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(encoding="utf-8")

        for forbidden in (
            "suspended_eligible_candidates",
            "suspended_pending_closures",
            "suspended_stage_completion_receipt",
        ):
            self.assertNotIn(forbidden, text)

        for required in (
            "runtime_github.eligible_candidates = RECOVERY_ELIGIBILITY_CHAIN[-1]",
            "receipt_stage.pending_closures = current_frontier_post_receipt_pending_closures",
            "receipt_stage.stage_completion_receipt = current_frontier_post_receipt_stage_completion_receipt",
            "behind_sync.synchronize_eligible_candidate = partial(",
            "structural_1809_synchronize_eligible_candidate",
        ):
            self.assertIn(required, text)

    def test_read_only_qualification_suspension_fixtures_remain_available(self):
        text = (ROOT / "ci" / "administrative_protected_receipt_live.py").read_text(
            encoding="utf-8"
        )
        for required in (
            "def suspended_eligible_candidates",
            "def suspended_pending_closures",
            "def suspended_stage_completion_receipt",
            "LIVE_QUALIFICATION_GREEN__REACTIVATION_NOT_AUTHORIZED",
        ):
            self.assertIn(required, text)

    def test_reactivated_runtime_retains_generic_non_occurrence_specific_boundary(self):
        text = (ROOT / "ci" / "administrative_autonomy_runtime.py").read_text(encoding="utf-8")
        for forbidden in ("#475", "#476", "#596", "2026-08-13"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
