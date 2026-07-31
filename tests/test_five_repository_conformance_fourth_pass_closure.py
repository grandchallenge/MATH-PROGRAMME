from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
CLOSURE_PATH = ROOT / "governance" / "five_repository_conformance_fourth_pass_closure.json"
SCHEMA_PATH = ROOT / "schemas" / "five_repository_conformance_fourth_pass_closure.schema.json"

EXPECTED_ARTIFACTS = {
    ("programme_stage", "runtime_contract"): ("governance/umbrella_runtime_contract_v4.json", "d1503fba284aee29fb517a554ee3440da691fd16"),
    ("programme_stage", "candidate_admission_registry"): ("governance/campaign_admission_registry.json", "9b1a307fde8bfe814210088d544ec8b03f2b413e"),
    ("programme_stage", "active_campaign_registry"): ("governance/governed_campaign_registry.json", "b1f1e4682d0f3ff0108d020e466fa2ecb0809b57"),
    ("programme_stage", "active_routing_registry"): ("governance/mathsolve_routing_audit.json", "4a27ec8aaaa60f919ba51028807b83dc522bfcff"),
    ("intellect_stage", "provider_module"): ("src/grand_intellect/mathsolve_cert_current.py", "d9800608890e5938fdb32fab85e8d9f7fc36c942"),
    ("intellect_stage", "qualification_fixture"): ("tests/fixtures/rh_ns_interface_qualifications.json", "817c9902bc9cc0c7ecbf94a4d03576e8bd30aeb6"),
    ("solve_candidate_stage", "candidate_admission_record"): ("work_packages/VGSE_WP00/candidate_admission.json", "ffc06599747b80eed3034f5e08b959799a57551b"),
    ("solve_candidate_stage", "candidate_validator"): ("work_packages/VGSE_WP00/artifacts/code/validate_candidate_admission.py", "79523117fd4ed1c3dfbf16c5f5fc0d8dce57028a"),
    ("solve_candidate_stage", "source_semantics_record"): ("work_packages/VGSE_WP00_VARCHENKO_GALASHIN_SOURCE_SEMANTICS_LOCK.md", "27009573bb9e0bd79fc7d2cbca681074dad6663d"),
}


class FiveRepositoryFourthPassClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.closure = json.loads(CLOSURE_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))

    def schema_errors(self, closure=None):
        candidate = copy.deepcopy(self.closure if closure is None else closure)
        validator = Draft202012Validator(self.schema, format_checker=FormatChecker())
        return list(validator.iter_errors(candidate))

    def test_current_closure_passes_schema(self) -> None:
        self.assertEqual(self.schema_errors(), [])

    def test_exact_artifact_identities_are_pinned(self) -> None:
        for (stage, field), (path, digest) in EXPECTED_ARTIFACTS.items():
            artifact = self.closure[stage][field]
            self.assertEqual(artifact["path"], path)
            self.assertEqual(artifact["digest_algorithm"], "git_blob_sha1")
            self.assertEqual(artifact["digest"], digest)

    def test_active_portfolio_remains_unchanged(self) -> None:
        active = self.closure["active_portfolio"]
        self.assertEqual(active["qualified_interface_only"], ["NS-CI-001", "RH-001"])
        self.assertEqual(active["ready_intake"], ["UC-001", "HC-001"])
        self.assertEqual(active["pending"], ["BSD-001", "PNP-001", "YM-001", "OZ-001"])
        self.assertEqual(active["archived_outside_current_routing"], ["PC-001"])
        self.assertEqual(active["active_routing_member_count"], 8)
        self.assertTrue(active["unchanged_by_fourth_pass"])

    def test_vgse_remains_candidate_only(self) -> None:
        candidate = self.closure["candidate_portfolio"]
        self.assertEqual(candidate["campaign_id"], "VGSE-001")
        self.assertEqual(candidate["lifecycle_state"], "candidate")
        self.assertFalse(candidate["active_portfolio_member"])
        self.assertEqual(candidate["active_portfolio_effect"], "none")
        self.assertTrue(candidate["candidate_work_package_merged"])
        self.assertFalse(candidate["candidate_work_package_merge_admits_campaign"])

    def test_source_and_cert_states_remain_pre_admission(self) -> None:
        candidate = self.closure["candidate_portfolio"]
        self.assertEqual(candidate["source_provenance_state"], "unverified_candidate")
        self.assertIsNone(candidate["source_provider_manifest"])
        self.assertEqual(candidate["certification_state"], "pre_route_candidate")
        for field in (
            "cert_route_present", "cert_handoff_present", "cert_adjudication_present",
            "active_campaign_manifest_present", "promotion_record_present",
        ):
            self.assertFalse(candidate[field], field)

    def test_all_governance_mismatch_counts_are_zero(self) -> None:
        self.assertTrue(all(value == 0 for value in self.closure["mismatch_counts"].values()))
        self.assertEqual(self.closure["remaining_cross_repository_governance_obligations"], [])

    def test_candidate_admission_inflation_is_rejected(self) -> None:
        closure = copy.deepcopy(self.closure)
        closure["candidate_portfolio"]["lifecycle_state"] = "admitted_active"
        closure["candidate_portfolio"]["active_portfolio_member"] = True
        closure["claim_boundaries"]["candidate_campaign_admitted"] = True
        self.assertTrue(self.schema_errors(closure))

    def test_source_verification_inflation_is_rejected(self) -> None:
        closure = copy.deepcopy(self.closure)
        closure["candidate_portfolio"]["source_provenance_state"] = "provider_verified"
        closure["candidate_portfolio"]["source_provider_manifest"] = {"fake": True}
        closure["claim_boundaries"]["source_provider_verified"] = True
        self.assertTrue(self.schema_errors(closure))

    def test_cert_route_inflation_is_rejected(self) -> None:
        closure = copy.deepcopy(self.closure)
        closure["candidate_portfolio"]["certification_state"] = "ready"
        closure["candidate_portfolio"]["cert_route_present"] = True
        closure["claim_boundaries"]["cert_route_created"] = True
        self.assertTrue(self.schema_errors(closure))

    def test_candidate_active_effect_is_rejected(self) -> None:
        closure = copy.deepcopy(self.closure)
        closure["candidate_portfolio"]["active_portfolio_effect"] = "adds_route"
        closure["authority_model"]["candidate_work_can_self_admit"] = True
        self.assertTrue(self.schema_errors(closure))

    def test_mathematical_and_commercial_inflation_is_rejected(self) -> None:
        closure = copy.deepcopy(self.closure)
        closure["claim_boundaries"]["mathematical_target_proved"] = True
        closure["claim_boundaries"]["commercial_claim_authorized"] = True
        self.assertTrue(self.schema_errors(closure))

    def test_bounded_numerical_results_are_not_certificates(self) -> None:
        results = self.closure["bounded_candidate_results"]
        self.assertTrue(results["exact_arrangement_beta_five"])
        self.assertEqual(results["numerical_critical_witness_count"], 5)
        self.assertEqual(results["numerical_t_embedding_reconstruction_count"], 5)
        self.assertFalse(results["algebraic_fixture_certified"])
        self.assertFalse(results["t_embedding_certified"])
        self.assertFalse(results["generated_to_source_equivalence_complete"])


if __name__ == "__main__":
    unittest.main()
