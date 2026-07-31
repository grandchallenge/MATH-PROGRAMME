from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "five_repository_conformance_third_pass",
    ROOT / "ci" / "five_repository_conformance_third_pass.py",
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class FiveRepositoryConformanceThirdPassTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit = json.loads(module.AUDIT_PATH.read_text(encoding="utf-8"))
        cls.campaigns = json.loads(module.CAMPAIGN_PATH.read_text(encoding="utf-8"))
        cls.predecessor = json.loads(module.PREDECESSOR_PATH.read_text(encoding="utf-8"))
        cls.runtime = json.loads(module.RUNTIME_PATH.read_text(encoding="utf-8"))
        cls.historical_runtime = json.loads(module.HISTORICAL_RUNTIME_PATH.read_text(encoding="utf-8"))

    def errors(
        self,
        *,
        audit=None,
        campaigns=None,
        predecessor=None,
        runtime=None,
        historical_runtime=None,
    ):
        return module.validation_errors(
            audit=copy.deepcopy(self.audit if audit is None else audit),
            campaigns=copy.deepcopy(self.campaigns if campaigns is None else campaigns),
            predecessor=copy.deepcopy(self.predecessor if predecessor is None else predecessor),
            runtime=copy.deepcopy(self.runtime if runtime is None else runtime),
            historical_runtime=copy.deepcopy(
                self.historical_runtime if historical_runtime is None else historical_runtime
            ),
        )

    def test_third_pass_staged_record_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_predecessor_omission_is_exactly_bsd_pnp_ym(self):
        predecessor = copy.deepcopy(self.predecessor)
        predecessor["canonical_trackers"]["cert"]["BSD-001"] = 26
        self.assertTrue(any("predecessor Cert tracker snapshot drift" in error for error in self.errors(predecessor=predecessor)))

    def test_cert_tracker_coverage_cannot_omit_pending_route(self):
        audit = copy.deepcopy(self.audit)
        del audit["cert_tracker_mirrors"]["YM-001"]
        self.assertTrue(any("Cert tracker mirror drift" in error for error in self.errors(audit=audit)))

    def test_pull_request_cannot_replace_programme_tracker(self):
        audit = copy.deepcopy(self.audit)
        audit["programme_tracker_mirrors"]["RH-001"] = 89
        errors = self.errors(audit=audit)
        self.assertTrue(any("Programme tracker mirror drift" in error for error in errors))
        self.assertTrue(any("pull request substituted" in error for error in errors))

    def test_governed_registry_tracker_drift_is_rejected(self):
        campaigns = copy.deepcopy(self.campaigns)
        rh = next(item for item in campaigns["campaigns"] if item["campaign_id"] == "RH-001")
        rh["programme_tracker_issue"] = 89
        self.assertTrue(any("governed registry RH-001 tracker drift" in error for error in self.errors(campaigns=campaigns)))

    def test_issue_mirror_cannot_become_state_authority(self):
        audit = copy.deepcopy(self.audit)
        audit["authority_model"]["github_issue_role"] = "canonical_state_authority"
        self.assertTrue(any("navigational mirror" in error for error in self.errors(audit=audit)))

    def test_issue_edit_cannot_change_cert_state(self):
        audit = copy.deepcopy(self.audit)
        audit["authority_model"]["issue_mutation_can_change_cert_state"] = True
        self.assertTrue(any("issue mutation may not change Cert state" in error for error in self.errors(audit=audit)))

    def test_cert_route_registry_identity_is_exact(self):
        audit = copy.deepcopy(self.audit)
        audit["external_cert_route_registry"]["digest"] = "0" * 40
        self.assertTrue(any("external Cert route registry identity drift" in error for error in self.errors(audit=audit)))

    def test_runtime_contract_identity_is_exact(self):
        audit = copy.deepcopy(self.audit)
        audit["programme_runtime_contract"]["digest"] = "0" * 40
        self.assertTrue(any("Programme runtime contract identity drift" in error for error in self.errors(audit=audit)))

    def test_runtime_contract_cannot_pin_consumer(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["consumer_independence"]["pins_intellect_commit"] = True
        self.assertTrue(any("consumer-independence drift" in error for error in self.errors(runtime=runtime)))

    def test_runtime_contract_cannot_carry_downstream_obligation(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["consumer_independence"]["contains_downstream_completion_obligation"] = True
        self.assertTrue(any("consumer-independence drift" in error for error in self.errors(runtime=runtime)))

    def test_historical_runtime_evidence_must_show_stale_obligation(self):
        historical = copy.deepcopy(self.historical_runtime)
        historical["remaining_cross_repository_obligation"] = "none"
        self.assertTrue(any("completed-obligation evidence drift" in error for error in self.errors(historical_runtime=historical)))

    def test_mirror_coverage_must_be_eight_plus_eight(self):
        audit = copy.deepcopy(self.audit)
        audit["mirror_coverage"]["cert_route_count"] = 5
        self.assertTrue(any("8+8 mirror coverage drift" in error for error in self.errors(audit=audit)))

    def test_blocker_loss_is_rejected(self):
        audit = copy.deepcopy(self.audit)
        del audit["preserved_blockers"]["PNP-001"]
        self.assertTrue(any("blocker coverage" in error for error in self.errors(audit=audit)))

    def test_mathematical_promotion_is_rejected(self):
        audit = copy.deepcopy(self.audit)
        audit["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(any("mathematical_target_proved" in error for error in self.errors(audit=audit)))

    def test_staged_intellect_repin_cannot_be_silently_cleared(self):
        audit = copy.deepcopy(self.audit)
        audit["reviewed_correction_unresolved_mismatch_count"] = 0
        self.assertTrue(any("staged unresolved mismatch count" in error for error in self.errors(audit=audit)))

    def test_tp06_must_remain_staged_until_consumer_repin(self):
        audit = copy.deepcopy(self.audit)
        tp06 = next(item for item in audit["third_pass_findings"] if item["id"] == "TP-06")
        tp06["disposition"] = "corrected"
        self.assertTrue(any("TP-06 staged disposition drift" in error for error in self.errors(audit=audit)))

    def test_self_inclusive_publication_claim_is_rejected(self):
        audit = copy.deepcopy(self.audit)
        audit["publication_semantics"]["self_inclusive_head_claim"] = True
        self.assertTrue(any("self-inclusive head claim" in error for error in self.errors(audit=audit)))


if __name__ == "__main__":
    unittest.main()
