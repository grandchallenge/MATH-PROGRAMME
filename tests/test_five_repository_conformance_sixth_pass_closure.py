from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "governance" / "five_repository_conformance_sixth_pass_closure.json"
SCHEMA_PATH = ROOT / "schemas" / "five_repository_conformance_sixth_pass_closure.schema.json"


class SixthPassClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def schema_errors(self, record: dict) -> list[str]:
        return [error.message for error in self.validator.iter_errors(record)]

    def test_current_closure_passes_schema(self) -> None:
        self.assertEqual(self.schema_errors(self.record), [])

    def test_exact_repository_heads(self) -> None:
        heads = self.record["reviewed_repository_heads"]
        self.assertEqual(heads["math_programme"]["commit_sha"], "7104b81e523f713b8dab080611fcde15c4ed67f6")
        self.assertEqual(heads["mathforge"]["commit_sha"], "0faee396ffa56c568ee0ae6a348bdb43ca80ac4d")
        self.assertEqual(heads["mathsolve"]["commit_sha"], "26c1060c2e40b170570fcf2fccc88539fa5b26e6")
        self.assertEqual(heads["mathcert"]["commit_sha"], "0258e4f0bca0d90fac05b62aeef108f16dccffdd")
        self.assertEqual(heads["intellect"]["commit_sha"], "949f84fef76c1d4cd64e90d7b3e97d13be15332f")

    def test_fifth_pass_external_attestation_is_pinned(self) -> None:
        attestation = self.record["fifth_pass_attestation"]
        self.assertEqual(attestation["issue"], 175)
        self.assertEqual(attestation["issue_state"], "closed_completed")
        self.assertEqual(attestation["closure_pull_request"], 177)
        self.assertEqual(attestation["closure_merge_commit"], "7104b81e523f713b8dab080611fcde15c4ed67f6")
        self.assertEqual(attestation["closure_record"]["digest"], "4b8e20627d65012a49a767db82b8489483496aac")
        self.assertTrue(attestation["external_post_merge_attestation_complete"])

    def test_solve_reconciliation_and_workflows_are_exact(self) -> None:
        solve = self.record["solve_reconciliation"]
        self.assertEqual(solve["reviewed_head"], "db4b16c2abc170dea6a1735284430147a956261f")
        self.assertEqual(solve["merge_commit"], "26c1060c2e40b170570fcf2fccc88539fa5b26e6")
        self.assertEqual(solve["solve_run_id"], 30671881534)
        self.assertEqual(solve["gcl_run_id"], 30671881847)
        self.assertEqual(solve["current_route_overlay"]["digest"], "2f6bb27a453a8615ba3af75ca77452ceb7b83ca8")
        self.assertEqual(solve["current_route_schema"]["digest"], "3c7c3c53cdff909fabb9c2ec5bc6efbb924f6a9d")
        self.assertEqual(solve["current_route_validator"]["digest"], "4300cafdfb66fc508e58551d21290782490b90d0")
        self.assertEqual(solve["mutation_tests"]["digest"], "a720df7da87359b96e23e901325affde85959007")

    def test_producer_handoff_and_current_route_are_distinct(self) -> None:
        states = self.record["solve_reconciliation"]["campaign_states"]
        self.assertEqual(states["NS-CI-001"]["handoff_state"], "ready")
        self.assertEqual(states["NS-CI-001"]["route_state"], "qualified")
        self.assertEqual(states["RH-001"]["handoff_state"], "pending")
        self.assertEqual(states["RH-001"]["route_state"], "qualified")
        for campaign in states.values():
            self.assertFalse(campaign["mathematical_target_proved"])

    def test_current_cert_authority_requires_no_repin(self) -> None:
        cert = self.record["cert_authority"]
        self.assertEqual(cert["commit_sha"], "0258e4f0bca0d90fac05b62aeef108f16dccffdd")
        self.assertEqual(cert["route_registry"]["digest"], "5b3e8d48b9f6c5b03ed3dc439bf9e43876e017b1")
        self.assertFalse(cert["protected_branch_change_required"])
        self.assertFalse(cert["source_manifest_repin_required"])

    def test_intellect_consumer_reconciliation_is_exact(self) -> None:
        intellect = self.record["intellect_reconciliation"]
        self.assertEqual(intellect["reviewed_head"], "7c8e9670b0a77281a0d31cf55b7ae1f06f2284a3")
        self.assertEqual(intellect["merge_commit"], "949f84fef76c1d4cd64e90d7b3e97d13be15332f")
        self.assertEqual(intellect["ci_run_id"], 30672274559)
        self.assertEqual(intellect["gcl_run_id"], 30672274832)
        self.assertEqual(intellect["provider_module"]["digest"], "203fc6d2923fc2669868a172ce67682c795d4d01")
        self.assertEqual(intellect["qualification_fixture"]["digest"], "ee7eb7a844d917df493f68b9752de8001881ec80")
        self.assertEqual(intellect["alignment_tests"]["digest"], "2f4c4d4a7e75c027b0a85bae8fdeed33962b0e80")
        self.assertEqual(intellect["provider_contract_count"], 5)
        self.assertEqual(intellect["package_version_preserved"], "0.2.2")

    def test_active_portfolio_is_exact_and_candidate_is_separate(self) -> None:
        active = self.record["active_portfolio"]
        self.assertEqual(active["active_routing_member_count"], 8)
        all_active = set().union(
            active["qualified_interface_only"],
            active["ready_intake"],
            active["pending"],
        )
        self.assertEqual(all_active, {"UC-001", "NS-CI-001", "HC-001", "BSD-001", "PNP-001", "RH-001", "YM-001", "OZ-001"})
        self.assertNotIn("VGSE-001", all_active)
        candidate = self.record["candidate_portfolio"]
        self.assertEqual(candidate["lifecycle_state"], "candidate")
        self.assertFalse(candidate["active_portfolio_member"])
        self.assertFalse(candidate["cert_route_present"])
        self.assertFalse(candidate["promotion_record_present"])

    def test_tracker_mirrors_are_reconciled(self) -> None:
        mirrors = self.record["issue_mirror_reconciliation"]
        self.assertEqual(mirrors["solve_route_state"]["state"], "closed_completed")
        self.assertEqual(mirrors["intellect_consumer"]["state"], "closed_completed")
        self.assertEqual(mirrors["forge_ns_ci_provider"]["state"], "closed_completed")
        self.assertEqual(mirrors["programme_vgse_candidate"]["state"], "open_candidate_repin_complete")
        self.assertEqual(mirrors["cert_vgse_pre_route"]["state"], "open_pre_route_candidate_repin_complete")

    def test_all_mismatches_are_zero(self) -> None:
        self.assertEqual(len(self.record["mismatch_counts"]), 10)
        self.assertTrue(all(value == 0 for value in self.record["mismatch_counts"].values()))
        self.assertEqual(self.record["remaining_cross_repository_governance_obligations"], [])

    def test_all_claim_boundaries_remain_closed(self) -> None:
        boundaries = self.record["claim_boundaries"]
        self.assertTrue(boundaries["operational_release_complete_preserved"])
        for field, value in boundaries.items():
            if field != "operational_release_complete_preserved":
                self.assertFalse(value, field)

    def test_handoff_route_conflation_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["solve_reconciliation"]["campaign_states"]["RH-001"]["route_state"] = "pending"
        mutated["solve_reconciliation"]["campaign_states"]["RH-001"]["qualification_scope"] = None
        self.assertTrue(self.schema_errors(mutated))

    def test_qualification_to_theorem_inflation_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["claim_boundaries"]["interface_qualification_promoted_to_theorem"] = True
        self.assertTrue(self.schema_errors(mutated))

    def test_candidate_admission_inflation_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["candidate_portfolio"]["active_portfolio_member"] = True
        self.assertTrue(self.schema_errors(mutated))

    def test_identity_drift_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["solve_reconciliation"]["current_route_overlay"]["digest"] = "0" * 40
        self.assertTrue(self.schema_errors(mutated))

    def test_self_inclusive_publication_claim_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["publication_semantics"]["self_inclusive_head_claim"] = True
        self.assertTrue(self.schema_errors(mutated))


if __name__ == "__main__":
    unittest.main()
