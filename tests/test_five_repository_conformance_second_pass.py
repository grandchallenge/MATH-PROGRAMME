from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from ci.five_repository_conformance_second_pass import AUDIT_PATH, validation_errors


class FiveRepositorySecondPassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = json.loads(Path(AUDIT_PATH).read_text(encoding="utf-8"))

    def assert_rejected(self, mutate) -> None:
        candidate = copy.deepcopy(self.audit)
        mutate(candidate)
        self.assertTrue(validation_errors(candidate))

    def test_canonical_record_passes(self) -> None:
        self.assertEqual(validation_errors(), [])

    def test_rejects_self_inclusive_head_claim(self) -> None:
        self.assert_rejected(lambda item: item["publication_semantics"].__setitem__("self_inclusive_head_claim", True))

    def test_rejects_impossible_self_hash_claim(self) -> None:
        self.assert_rejected(lambda item: item["publication_semantics"].__setitem__("artifact_can_pin_own_future_merge_commit", True))

    def test_rejects_missing_external_attestation(self) -> None:
        self.assert_rejected(lambda item: item["publication_semantics"].__setitem__("external_post_merge_attestation_required", False))

    def test_rejects_pr_as_campaign_tracker(self) -> None:
        self.assert_rejected(lambda item: item["canonical_trackers"]["programme_campaigns"].__setitem__("RH-001", 89))

    def test_rejects_missing_campaign_tracker(self) -> None:
        self.assert_rejected(lambda item: item["canonical_trackers"]["programme_campaigns"].pop("YM-001"))

    def test_rejects_qualified_scope_inflation(self) -> None:
        self.assert_rejected(lambda item: item["portfolio"]["qualified_interface_only"].append("BSD-001"))

    def test_rejects_missing_blocker(self) -> None:
        self.assert_rejected(lambda item: item["preserved_blockers"].pop("OZ-001"))

    def test_rejects_theorem_promotion(self) -> None:
        self.assert_rejected(lambda item: item["claim_boundaries"].__setitem__("mathematical_target_proved", True))

    def test_rejects_post_merge_replay_overclaim(self) -> None:
        self.assert_rejected(lambda item: item["ci_semantics"].__setitem__("post_merge_push_replay_claimed", True))


if __name__ == "__main__":
    unittest.main()
