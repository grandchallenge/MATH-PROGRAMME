from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "governance" / "five_repository_conformance_seventh_pass_closure.json"
SCHEMA_PATH = ROOT / "schemas" / "five_repository_conformance_seventh_pass_closure.schema.json"


class SeventhPassClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def schema_errors(self, record: dict) -> list[str]:
        return [error.message for error in self.validator.iter_errors(record)]

    def test_current_closure_passes_schema(self) -> None:
        self.assertEqual(self.schema_errors(self.record), [])

    def test_sixth_pass_external_attestation_is_exact(self) -> None:
        attestation = self.record["sixth_pass_attestation"]
        self.assertEqual(attestation["issue"], 178)
        self.assertEqual(attestation["attestation_comment_id"], 5148279008)
        self.assertEqual(attestation["closure_pull_request"], 179)
        self.assertEqual(attestation["reviewed_head"], "66e10ec4a2071f314680b21132f80a2c8f45a16b")
        self.assertEqual(attestation["closure_merge_commit"], "72025995924275778611f1e436e871604fb3e4c9")
        self.assertEqual(attestation["policy_run_id"], 30672521555)
        self.assertEqual(attestation["gcl_run_id"], 30672521901)
        self.assertTrue(attestation["reviewed_head_and_merge_have_no_file_differences"])
        artifacts = attestation["closure_artifacts"]
        self.assertEqual(artifacts["record"]["digest"], "b690d013dc2cb9172523bcf36e05fc0c8996b466")
        self.assertEqual(artifacts["schema"]["digest"], "9faa2976720a394c668a8630915e63fb14096d18")
        self.assertEqual(artifacts["tests"]["digest"], "0aab4926de92ab90962da63df34966b6fa390775")

    def test_exact_five_repository_heads_are_unchanged(self) -> None:
        heads = self.record["reviewed_repository_heads"]
        expected = {
            "math_programme": "72025995924275778611f1e436e871604fb3e4c9",
            "mathforge": "0faee396ffa56c568ee0ae6a348bdb43ca80ac4d",
            "mathsolve": "26c1060c2e40b170570fcf2fccc88539fa5b26e6",
            "mathcert": "0258e4f0bca0d90fac05b62aeef108f16dccffdd",
            "intellect": "949f84fef76c1d4cd64e90d7b3e97d13be15332f",
        }
        self.assertEqual({key: value["commit_sha"] for key, value in heads.items()}, expected)

    def test_no_material_drift_or_downstream_repin(self) -> None:
        drift = self.record["drift_assessment"]
        numeric_fields = (
            "protected_head_changes_since_sixth_pass",
            "open_pull_requests_in_reviewed_repositories",
            "open_issues_modified_after_sixth_pass_closure_before_seventh_pass_intake",
            "material_contract_changes_since_sixth_pass",
            "active_manifest_changes_since_sixth_pass",
            "cert_route_changes_since_sixth_pass",
            "certificate_output_changes_since_sixth_pass",
        )
        for field in numeric_fields:
            self.assertEqual(drift[field], 0, field)
        for field, value in drift.items():
            if field in numeric_fields:
                continue
            self.assertFalse(value, field)

    def test_authority_model_distinguishes_heads_from_material_artifacts(self) -> None:
        authority = self.record["authority_model"]
        self.assertTrue(authority["protected_repository_records_are_state_authority"])
        self.assertTrue(authority["repository_head_identity_is_distinct_from_material_artifact_identity"])
        self.assertTrue(authority["unchanged_material_artifacts_do_not_require_repin"])
        self.assertTrue(authority["mutable_issue_mirrors_are_navigation_only"])
        self.assertTrue(authority["closure_record_may_pin_completed_prior_merge_and_attestation"])
        self.assertTrue(authority["closure_record_cannot_pin_its_own_future_merge"])

    def test_portfolio_state_is_unchanged(self) -> None:
        active = self.record["active_portfolio"]
        self.assertEqual(active["active_routing_member_count"], 8)
        self.assertTrue(active["unchanged_since_sixth_pass"])
        self.assertEqual(active["qualified_interface_only"], ["NS-CI-001", "RH-001"])
        self.assertEqual(active["ready_intake"], ["UC-001", "HC-001"])
        self.assertEqual(active["pending"], ["BSD-001", "PNP-001", "YM-001", "OZ-001"])
        self.assertEqual(active["archived_outside_current_routing"], ["PC-001"])

        candidate = self.record["candidate_portfolio"]
        self.assertEqual(candidate["campaign_id"], "VGSE-001")
        self.assertEqual(candidate["lifecycle_state"], "candidate")
        self.assertEqual(candidate["source_provenance_state"], "unverified_candidate")
        self.assertTrue(candidate["unchanged_since_sixth_pass"])
        for field in (
            "active_portfolio_member",
            "active_campaign_manifest_present",
            "cert_handoff_present",
            "cert_route_present",
            "cert_adjudication_present",
            "promotion_record_present",
        ):
            self.assertFalse(candidate[field], field)

    def test_candidate_mirrors_are_repinned_to_seventh_pass(self) -> None:
        mirrors = self.record["issue_mirror_reconciliation"]
        self.assertEqual(set(mirrors), {"programme_candidate", "forge_source_audit", "cert_pre_route"})
        for mirror in mirrors.values():
            self.assertEqual(mirror["current_umbrella_issue"], 180)
            self.assertEqual(mirror["pinned_closure_merge"], "72025995924275778611f1e436e871604fb3e4c9")

    def test_all_mismatch_counts_are_zero(self) -> None:
        self.assertTrue(self.record["mismatch_counts"])
        self.assertTrue(all(value == 0 for value in self.record["mismatch_counts"].values()))
        self.assertEqual(self.record["remaining_cross_repository_governance_obligations"], [])

    def test_claim_boundaries_remain_closed(self) -> None:
        boundaries = self.record["claim_boundaries"]
        self.assertTrue(boundaries["operational_release_complete_preserved"])
        for field, value in boundaries.items():
            if field == "operational_release_complete_preserved":
                continue
            self.assertFalse(value, field)

    def test_head_drift_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["reviewed_repository_heads"]["mathsolve"]["commit_sha"] = "0" * 40
        self.assertTrue(self.schema_errors(mutated))

    def test_open_pr_interference_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["drift_assessment"]["open_pull_requests_in_reviewed_repositories"] = 1
        self.assertTrue(self.schema_errors(mutated))

    def test_unnecessary_downstream_repin_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["drift_assessment"]["downstream_consumer_repin_required"] = True
        self.assertTrue(self.schema_errors(mutated))

    def test_candidate_admission_inflation_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["candidate_portfolio"]["active_portfolio_member"] = True
        self.assertTrue(self.schema_errors(mutated))

    def test_stale_mirror_authority_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["issue_mirror_reconciliation"]["programme_candidate"]["current_umbrella_issue"] = 178
        self.assertTrue(self.schema_errors(mutated))

    def test_self_inclusive_publication_claim_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["publication_semantics"]["self_inclusive_head_claim"] = True
        self.assertTrue(self.schema_errors(mutated))


if __name__ == "__main__":
    unittest.main()
