from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
RECORD = ROOT / "governance" / "oz_rt_bz_t3_010_a_authority_reconciliation_post_merge_closure.json"
SCHEMA = ROOT / "schemas" / "oz_rt_bz_t3_010_a_authority_reconciliation_post_merge_closure.schema.json"


class OzT3010AAuthorityReconciliationPostMergeClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema)

    def fresh_record(self) -> dict:
        return json.loads(RECORD.read_text(encoding="utf-8"))

    def errors_for(self, record: dict) -> list[str]:
        return [error.message for error in self.validator.iter_errors(record)]

    def test_record_is_schema_valid(self) -> None:
        self.assertEqual(self.errors_for(self.fresh_record()), [])

    def test_original_exact_head_authority_is_not_rewritten(self) -> None:
        record = self.fresh_record()
        self.assertEqual(
            record["source_pull_request"]["original_authorized_head"],
            "26c5736e90954c751fb84eedc6310388d5e09c8d",
        )
        self.assertTrue(
            record["source_pull_request"]["original_human_steward_disposition"][
                "invalidated_by_head_movement"
            ]
        )

    def test_actual_merged_head_is_bound_non_cyclically(self) -> None:
        record = self.fresh_record()
        self.assertEqual(
            record["synchronization"]["merged_head"],
            "b7dcc667622cc4d9b7996dc03430a10dfdcb59fd",
        )
        self.assertEqual(
            record["protected_merge"]["merge_commit"],
            "8bbc24421c1b5b37110f608b90c95d57f19af0b2",
        )
        self.assertFalse(record["successor_reconciliation"]["history_rewritten"])

    def test_actual_head_had_fresh_machine_replay_but_not_fresh_authority(self) -> None:
        record = self.fresh_record()
        self.assertTrue(
            record["actual_head_machine_replay"][
                "all_named_exact_head_checks_successful"
            ]
        )
        self.assertFalse(
            record["authority_defect"][
                "fresh_independent_review_on_actual_head_present"
            ]
        )
        self.assertFalse(
            record["authority_defect"][
                "fresh_human_steward_disposition_on_actual_head_present"
            ]
        )

    def test_protected_payload_is_exactly_five_file_package(self) -> None:
        record = self.fresh_record()
        self.assertEqual(record["protected_merge"]["post_merge_diff_file_count"], 5)
        self.assertEqual(
            record["protected_merge"]["post_merge_diff_files"],
            [
                "campaigns/odd_zeta/OZ_RT_BZ_T3_010/T3_010_A_CONTRACT.json",
                "campaigns/odd_zeta/OZ_RT_BZ_T3_010/t3_010_a.py",
                "campaigns/odd_zeta/OZ_RT_BZ_T3_010/verify_t3_010_a.py",
                "ci/campaign_replay_registry.json",
                "tests/test_oz_rt_bz_t3_010_a.py",
            ],
        )
        self.assertTrue(
            record["protected_merge"][
                "payload_delta_matches_intended_five_file_package"
            ]
        )

    def test_successor_closure_requires_full_fresh_authority_chain(self) -> None:
        record = self.fresh_record()["successor_reconciliation"]
        self.assertTrue(record["separate_protected_successor_closure_required"])
        self.assertTrue(record["fresh_exact_head_machine_gates_required"])
        self.assertTrue(record["fresh_independent_non_author_review_required"])
        self.assertTrue(record["fresh_human_steward_disposition_required"])
        self.assertTrue(record["protected_merge_required"])
        self.assertTrue(record["protected_main_readback_required"])
        self.assertFalse(record["waiver_used"])
        self.assertFalse(record["substantive_reexecution_required"])

    def test_claim_firewall_is_preserved(self) -> None:
        claim = self.fresh_record()["claim_boundaries"]
        self.assertFalse(claim["residual_sum_zero_proved"])
        self.assertEqual(claim["proof_effect"], "NONE")
        self.assertEqual(claim["promotion_effect"], "NONE")
        self.assertEqual(claim["t3_status"], "OPEN_WITH_CHARACTERIZED_BLOCKER")

    def test_mutation_rejects_wrong_merged_head(self) -> None:
        record = self.fresh_record()
        record["synchronization"]["merged_head"] = "0" * 40
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_false_authority_cleanliness(self) -> None:
        record = self.fresh_record()
        record["authority_defect"]["authority_integrity_clean"] = True
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_waiver(self) -> None:
        record = self.fresh_record()
        record["successor_reconciliation"]["waiver_used"] = True
        self.assertTrue(self.errors_for(record))

    def test_mutation_rejects_claim_inflation(self) -> None:
        record = copy.deepcopy(self.fresh_record())
        record["claim_boundaries"]["mathematical_certification_created"] = True
        self.assertTrue(self.errors_for(record))


if __name__ == "__main__":
    unittest.main()
