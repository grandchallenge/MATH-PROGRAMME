from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
RECORD_PATH = ROOT / "governance" / "five_repository_conformance_fifth_pass_closure.json"
SCHEMA_PATH = ROOT / "schemas" / "five_repository_conformance_fifth_pass_closure.schema.json"


class FifthPassClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.record = json.loads(RECORD_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.validator = Draft202012Validator(cls.schema, format_checker=FormatChecker())

    def schema_errors(self, record: dict) -> list[str]:
        return [error.message for error in self.validator.iter_errors(record)]

    def test_current_closure_passes_schema(self) -> None:
        self.assertEqual(self.schema_errors(self.record), [])

    def test_exact_protected_heads_and_workflow_evidence(self) -> None:
        programme = self.record["programme_stage"]
        self.assertEqual(programme["reviewed_head"], "b32a7f65f4ca308e0776363fa9e1f19d701f5a2a")
        self.assertEqual(programme["merge_commit"], "d56edc23152f3ccde4c7db272b7af37f6cf698b9")
        self.assertEqual(programme["policy_run_id"], 30669500337)
        self.assertEqual(programme["gcl_run_id"], 30669500714)

        solve = self.record["solve_stage"]
        self.assertEqual(solve["reviewed_head"], "5c5fb2195b3137667cfa299633780d2fecaf21f4")
        self.assertEqual(solve["merge_commit"], "5507354524302cc7f4fc7e6c178b40dfe9bf08fb")
        self.assertEqual(solve["solve_run_id"], 30669991624)
        self.assertEqual(solve["gcl_run_id"], 30669991959)
        self.assertEqual(solve["candidate_replay_run_id"], 30669991597)

        intellect = self.record["intellect_stage"]
        self.assertEqual(intellect["reviewed_head"], "24080fb37c89d7f7a7464ac1f3b2665a4b2ddb42")
        self.assertEqual(intellect["merge_commit"], "0c70ea9c3ec4f17b2ef6efc33646d102108f228f")
        self.assertEqual(intellect["ci_run_id"], 30670207210)
        self.assertEqual(intellect["gcl_run_id"], 30670207592)

    def test_exact_cross_repository_artifact_blobs(self) -> None:
        programme = self.record["programme_stage"]
        self.assertEqual(programme["candidate_admission_registry"]["digest"], "a6bffaa197aa3921e3eb9d4f8a02b5dc2bbded24")
        self.assertEqual(programme["runtime_contract"]["digest"], "02cdfabb04f5d273fcb7531c515a73baab2bc52d")
        self.assertEqual(programme["active_campaign_registry"]["digest"], "b1f1e4682d0f3ff0108d020e466fa2ecb0809b57")
        self.assertEqual(programme["active_routing_registry"]["digest"], "4a27ec8aaaa60f919ba51028807b83dc522bfcff")

        solve = self.record["solve_stage"]
        self.assertEqual(solve["candidate_admission_record"]["digest"], "4df13f366d39eae0cef04e7d00f69d0791a57b6d")
        self.assertEqual(solve["candidate_validator"]["digest"], "1c0df16f618a9aa286cfed95e8d137bb8412a7f5")
        self.assertEqual(solve["candidate_tests"]["digest"], "2211fb5611834c1821d984c8bb2b4b03559f0daf")
        self.assertEqual(solve["source_semantics_record"]["digest"], "ed10c62bd900f6d7ab0e1b9dea70aa66774f761e")

        intellect = self.record["intellect_stage"]
        self.assertEqual(intellect["provider_module"]["digest"], "9162342819b0199f034edee290122c0f8ab0c709")
        self.assertEqual(intellect["qualification_fixture"]["digest"], "e6954cb60b571d7d22a1ace9c8a4240ca271495d")
        self.assertEqual(intellect["alignment_tests"]["digest"], "9eebd937403dfb67f816ca6ba45eecb016ccb7b0")

    def test_reviewed_candidate_execution_is_not_admission(self) -> None:
        candidate = self.record["candidate_portfolio"]
        self.assertEqual(candidate["lifecycle_state"], "candidate")
        self.assertEqual(candidate["execution_state"], "merged_candidate_work_package")
        self.assertTrue(candidate["reviewed_candidate_work_package"])
        self.assertTrue(candidate["solve_candidate_package_reviewed"])
        self.assertFalse(candidate["active_portfolio_member"])
        self.assertEqual(candidate["active_portfolio_effect"], "none")
        self.assertEqual(candidate["source_provenance_state"], "unverified_candidate")
        self.assertIsNone(candidate["source_provider_manifest"])
        self.assertEqual(candidate["certification_state"], "pre_route_candidate")
        for field in (
            "cert_route_present",
            "cert_handoff_present",
            "cert_adjudication_present",
            "active_campaign_manifest_present",
            "promotion_record_present",
        ):
            self.assertFalse(candidate[field], field)
        self.assertTrue(candidate["all_other_admission_gates_closed"])

    def test_active_portfolio_is_unchanged(self) -> None:
        active = self.record["active_portfolio"]
        self.assertEqual(active["active_routing_member_count"], 8)
        self.assertTrue(active["unchanged_by_fifth_pass"])
        all_ids = set().union(
            active["qualified_interface_only"],
            active["ready_intake"],
            active["pending"],
            active["archived_outside_current_routing"],
        )
        self.assertNotIn("VGSE-001", all_ids)

    def test_issue_mirrors_match_reconciled_roles(self) -> None:
        mirrors = self.record["issue_mirrors"]
        self.assertEqual(mirrors["programme_candidate_tracker"]["state"], "open")
        self.assertFalse(mirrors["programme_candidate_tracker"]["active_campaign_label_present"])
        self.assertEqual(mirrors["programme_fourth_pass"]["state"], "closed_completed")
        self.assertEqual(mirrors["solve_candidate_work"]["state"], "closed_completed_candidate_work")
        self.assertEqual(mirrors["forge_source_audit"]["state"], "open")
        self.assertEqual(mirrors["cert_pre_route"]["state"], "open_pre_route_candidate")

    def test_all_mismatch_counts_are_zero(self) -> None:
        self.assertTrue(self.record["mismatch_counts"])
        self.assertTrue(all(value == 0 for value in self.record["mismatch_counts"].values()))
        self.assertEqual(self.record["remaining_cross_repository_governance_obligations"], [])

    def test_all_promotion_claims_remain_closed(self) -> None:
        boundaries = self.record["claim_boundaries"]
        self.assertTrue(boundaries["operational_release_complete_preserved"])
        self.assertFalse(boundaries["release_trust_issues_reopened"])
        for field, value in boundaries.items():
            if field == "operational_release_complete_preserved":
                continue
            self.assertFalse(value, field)

    def test_candidate_admission_inflation_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["candidate_portfolio"]["active_portfolio_member"] = True
        self.assertTrue(self.schema_errors(mutated))

    def test_source_verification_inflation_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["candidate_portfolio"]["source_provenance_state"] = "provider_verified"
        self.assertTrue(self.schema_errors(mutated))

    def test_cert_route_inflation_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["candidate_portfolio"]["cert_route_present"] = True
        self.assertTrue(self.schema_errors(mutated))

    def test_certification_inflation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["bounded_candidate_results"]["algebraic_fixture_certified"] = True
        self.assertTrue(self.schema_errors(mutated))

    def test_self_inclusive_publication_claim_fails_schema(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["publication_semantics"]["self_inclusive_head_claim"] = True
        self.assertTrue(self.schema_errors(mutated))


if __name__ == "__main__":
    unittest.main()
