from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from ci.vgse_post_repin_closure import RECORD_PATH, validation_errors


class VGSEPostRepinClosureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(Path(RECORD_PATH).read_text(encoding="utf-8"))

    def assertRejected(self, mutated: dict, marker: str) -> None:
        errors = validation_errors(mutated)
        self.assertTrue(any(marker in error for error in errors), errors)

    def test_exact_record_passes(self) -> None:
        self.assertEqual(validation_errors(self.record), [])

    def test_stale_intellect_merge_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["intellect_consumer_repin"]["merge_commit"] = "0" * 40
        self.assertRejected(mutated, "INTELLECT protected merge identity drift")

    def test_unapproved_repin_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["intellect_consumer_repin"]["review"]["state"] = "COMMENTED"
        self.assertRejected(mutated, "INTELLECT independent approval missing")

    def test_runtime_mutation_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["closure_semantics"]["runtime_v5_mutated"] = True
        self.assertRejected(mutated, "closure may not mutate runtime v5")

    def test_missing_repin_completion_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["closure_semantics"]["intellect_repin_obligation_satisfied"] = False
        self.assertRejected(mutated, "closure semantic must remain true")

    def test_premature_issue_closure_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["closure_semantics"]["issue_may_close_only_after_this_record_protected"] = False
        self.assertRejected(mutated, "closure semantic must remain true")

    def test_adjudication_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["retained_route_state"]["may_adjudicate"] = True
        self.assertRejected(mutated, "retained route state inflated")

    def test_certificate_output_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["retained_route_state"]["cert_output"] = {"status": "certified"}
        self.assertRejected(mutated, "retained route state inflated")

    def test_route_state_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["retained_route_state"]["route_state"] = "certified"
        self.assertRejected(mutated, "retained route state drift")

    def test_claim_inflation_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["claim_boundaries"]["five_root_theorem_proved"] = True
        self.assertRejected(mutated, "claim boundary inflated")

    def test_false_direct_repin_obligation_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["intellect_consumer_repin"]["unchanged_direct_consumers"]["repin_required"] = True
        self.assertRejected(mutated, "unchanged direct consumers incorrectly require repin")

    def test_programme_identity_drift_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["programme_activation"]["runtime"]["digest"] = "0" * 40
        self.assertRejected(mutated, "closure Programme runtime identity drift")


if __name__ == "__main__":
    unittest.main()
