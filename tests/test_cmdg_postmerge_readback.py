from __future__ import annotations

import unittest
from unittest.mock import patch

from ci import cmdg_postmerge_readback as readback


SHA = "1" * 40
BASE = "2" * 40
DIGEST = "3" * 64


def results(value: str) -> dict[str, str]:
    return {name: value for name in readback.ROSTER}


class CMDGPostmergeReadbackTests(unittest.TestCase):
    def build(self, *, shards: list[str], suites: dict[str, str], observed: str = SHA, impact: str = "success"):
        with patch.object(readback, "changed_paths", return_value=["README.md"]):
            return readback.build_receipt(
                repository="grandchallenge/MATH-PROGRAMME", protected_ref="refs/heads/main",
                merge_sha=SHA, observed_sha=observed, classifier_digest=DIGEST,
                event_name="push", event={"before": BASE}, policy_shards=shards,
                unknown_count=0, impact_result=impact, suite_results=suites,
                run_id="123", run_attempt=1,
            )

    def test_unrelated_merge_is_readback_only(self):
        receipt = self.build(shards=["core", "docs"], suites=results("skipped"))
        self.assertFalse(receipt["cmdg_required"])
        self.assertEqual(receipt["terminal_state"], "observed_pass_no_further_governance_action")

    def test_relevant_or_unknown_merge_requires_every_suite(self):
        receipt = self.build(shards=["core", "cmdg"], suites=results("success"))
        self.assertTrue(receipt["cmdg_required"])
        broken = results("success")
        broken[readback.ROSTER[0]] = "failure"
        self.assertEqual(self.build(shards=["core", "cmdg"], suites=broken)["terminal_state"], "downstream_hold_requires_compensation")

    def test_sha_or_classifier_failure_places_hold(self):
        self.assertEqual(self.build(shards=["core"], suites=results("skipped"), observed="4" * 40)["terminal_state"], "downstream_hold_requires_compensation")
        self.assertEqual(self.build(shards=["core"], suites=results("skipped"), impact="failure")["terminal_state"], "downstream_hold_requires_compensation")

    def test_duplicate_delivery_has_same_terminal_identity(self):
        first = self.build(shards=["core"], suites=results("skipped"))
        second = self.build(shards=["core"], suites=results("skipped"))
        self.assertEqual(first["receipt_id"], second["receipt_id"])

    def test_readback_cannot_create_reserved_effect(self):
        receipt = self.build(shards=["core"], suites=results("skipped"))
        self.assertTrue(receipt["authority_boundary"]["integration_facts_only"])
        self.assertFalse(any(value for key, value in receipt["authority_boundary"].items() if key != "integration_facts_only"))


if __name__ == "__main__":
    unittest.main()
