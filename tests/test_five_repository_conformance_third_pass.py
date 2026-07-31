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

    def errors(self, *, audit=None, campaigns=None, predecessor=None):
        return module.validation_errors(
            audit=copy.deepcopy(self.audit if audit is None else audit),
            campaigns=copy.deepcopy(self.campaigns if campaigns is None else campaigns),
            predecessor=copy.deepcopy(self.predecessor if predecessor is None else predecessor),
        )

    def test_third_pass_current_record_passes(self):
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

    def test_self_inclusive_publication_claim_is_rejected(self):
        audit = copy.deepcopy(self.audit)
        audit["publication_semantics"]["self_inclusive_head_claim"] = True
        self.assertTrue(any("self-inclusive head claim" in error for error in self.errors(audit=audit)))


if __name__ == "__main__":
    unittest.main()
