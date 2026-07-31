from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "campaign_admission_control", ROOT / "ci" / "campaign_admission_control.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class CampaignAdmissionControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admission = json.loads(module.ADMISSION_PATH.read_text(encoding="utf-8"))
        cls.runtime = json.loads(module.RUNTIME_PATH.read_text(encoding="utf-8"))
        cls.active = json.loads(module.ACTIVE_PATH.read_text(encoding="utf-8"))
        cls.routing = json.loads(module.ROUTING_PATH.read_text(encoding="utf-8"))

    def errors(self, *, admission=None, runtime=None, active=None, routing=None):
        return module.validation_errors(
            admission=copy.deepcopy(self.admission if admission is None else admission),
            runtime=copy.deepcopy(self.runtime if runtime is None else runtime),
            active=copy.deepcopy(self.active if active is None else active),
            routing=copy.deepcopy(self.routing if routing is None else routing),
        )

    def test_current_candidate_control_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_candidate_cannot_enter_active_registry(self):
        active = copy.deepcopy(self.active)
        active["campaigns"].append({
            "campaign_id": "VGSE-001",
            "domain_id": None,
            "lifecycle": "active_additional_campaign",
            "programme_tracker_issue": 170,
            "canonical_record": "candidate",
            "routing_member": True,
        })
        self.assertTrue(any("active campaign portfolio drift" in error or "leaked" in error for error in self.errors(active=active)))

    def test_candidate_cannot_enter_routing_registry(self):
        routing = copy.deepcopy(self.routing)
        routing["campaigns"].append({"campaign_id": "VGSE-001"})
        self.assertTrue(any("active routing portfolio drift" in error or "leaked" in error for error in self.errors(routing=routing)))

    def test_issue_edit_cannot_admit_campaign(self):
        admission = copy.deepcopy(self.admission)
        admission["authority"]["candidate_issue_mutation_can_admit_campaign"] = True
        self.assertTrue(any("issue mutation" in error for error in self.errors(admission=admission)))

    def test_source_digest_cannot_be_marked_verified_without_manifest(self):
        admission = copy.deepcopy(self.admission)
        source = admission["candidates"][0]["source_provenance"]
        source["state"] = "provider_verified"
        self.assertTrue(any("source provenance inflated" in error for error in self.errors(admission=admission)))

    def test_candidate_cannot_create_campaign_manifest(self):
        admission = copy.deepcopy(self.admission)
        admission["candidates"][0]["solve_candidate"]["may_create_campaign_manifest"] = True
        self.assertTrue(any("may_create_campaign_manifest" in error for error in self.errors(admission=admission)))

    def test_candidate_cannot_create_cert_handoff(self):
        admission = copy.deepcopy(self.admission)
        admission["candidates"][0]["solve_candidate"]["may_create_cert_handoff"] = True
        self.assertTrue(any("may_create_cert_handoff" in error for error in self.errors(admission=admission)))

    def test_pre_route_candidate_cannot_adjudicate(self):
        admission = copy.deepcopy(self.admission)
        admission["candidates"][0]["certification_candidate"]["may_adjudicate"] = True
        self.assertTrue(any("Cert pre-route boundary drift" in error for error in self.errors(admission=admission)))

    def test_admission_gate_cannot_be_preemptively_closed(self):
        admission = copy.deepcopy(self.admission)
        admission["candidates"][0]["admission_gates"]["forge_provider_manifest_admitted"] = True
        self.assertTrue(any("admission gate inflated" in error for error in self.errors(admission=admission)))

    def test_runtime_must_pin_candidate_registry(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["candidate_admission_contract"]["digest"] = "0" * 40
        self.assertTrue(any("candidate admission digest drift" in error for error in self.errors(runtime=runtime)))

    def test_candidate_has_no_active_portfolio_effect(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["candidate_portfolio"]["active_portfolio_effect"] = "adds_route"
        self.assertTrue(any("candidate effect must remain none" in error for error in self.errors(runtime=runtime)))

    def test_candidate_work_cannot_self_admit(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["authority_model"]["candidate_work_can_self_admit"] = True
        self.assertTrue(any("may not self-admit" in error for error in self.errors(runtime=runtime)))

    def test_candidate_campaign_admission_claim_is_rejected(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["claim_boundaries"]["candidate_campaign_admitted"] = True
        self.assertTrue(any("admission inflation" in error for error in self.errors(runtime=runtime)))


if __name__ == "__main__":
    unittest.main()
