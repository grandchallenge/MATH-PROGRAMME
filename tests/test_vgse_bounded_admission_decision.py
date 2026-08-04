from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "campaign_admission_control_vgse",
    ROOT / "ci" / "campaign_admission_control.py",
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class VgseBoundedAdmissionDecisionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admission = json.loads(module.ADMISSION_PATH.read_text(encoding="utf-8"))
        cls.decision = json.loads(module.DECISION_PATH.read_text(encoding="utf-8"))
        cls.runtime = json.loads(module.RUNTIME_PATH.read_text(encoding="utf-8"))
        cls.active = json.loads(module.ACTIVE_PATH.read_text(encoding="utf-8"))
        cls.routing = json.loads(module.ROUTING_PATH.read_text(encoding="utf-8"))

    @staticmethod
    def candidate(admission, campaign_id):
        return next(item for item in admission["candidates"] if item["campaign_id"] == campaign_id)

    def errors(self, *, admission=None, decision=None, runtime=None, active=None, routing=None):
        return module.validation_errors(
            admission=copy.deepcopy(self.admission if admission is None else admission),
            decision=copy.deepcopy(self.decision if decision is None else decision),
            runtime=copy.deepcopy(self.runtime if runtime is None else runtime),
            active=copy.deepcopy(self.active if active is None else active),
            routing=copy.deepcopy(self.routing if routing is None else routing),
        )

    def test_current_bounded_decision_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_provider_manifest_identity_is_pinned(self):
        admission = copy.deepcopy(self.admission)
        vgse = self.candidate(admission, "VGSE-001")
        vgse["source_provenance"]["provider_manifest"]["digest"] = "0" * 40
        self.assertTrue(any("provider manifest identity drift" in e for e in self.errors(admission=admission)))

    def test_completed_provider_gate_cannot_roll_back(self):
        admission = copy.deepcopy(self.admission)
        vgse = self.candidate(admission, "VGSE-001")
        vgse["admission_gates"]["source_revision_concordance_complete"] = False
        self.assertTrue(any("admission gate inflated or rolled back" in e for e in self.errors(admission=admission)))

    def test_activation_gate_cannot_close_before_downstream_records(self):
        admission = copy.deepcopy(self.admission)
        vgse = self.candidate(admission, "VGSE-001")
        vgse["admission_gates"]["cert_route_registered"] = True
        self.assertTrue(any("admission gate inflated or rolled back" in e for e in self.errors(admission=admission)))

    def test_decision_cannot_adjudicate(self):
        decision = copy.deepcopy(self.decision)
        decision["downstream_authority"]["may_adjudicate"] = True
        self.assertTrue(any("prohibited downstream authority" in e for e in self.errors(decision=decision)))

    def test_decision_cannot_issue_certificate(self):
        decision = copy.deepcopy(self.decision)
        decision["downstream_authority"]["may_issue_certificate_output"] = True
        self.assertTrue(any("prohibited downstream authority" in e for e in self.errors(decision=decision)))

    def test_decision_cannot_project_active_effect(self):
        decision = copy.deepcopy(self.decision)
        decision["active_portfolio_effect"] = "active"
        self.assertTrue(any("premature active-portfolio effect" in e for e in self.errors(decision=decision)))

    def test_claim_inflation_is_rejected(self):
        decision = copy.deepcopy(self.decision)
        decision["claim_boundaries"]["five_root_theorem_certified"] = True
        self.assertTrue(any("claim boundary inflation" in e for e in self.errors(decision=decision)))

    def test_vgse_cannot_leak_into_active_registry(self):
        active = copy.deepcopy(self.active)
        active["campaigns"].append({"campaign_id": "VGSE-001"})
        self.assertTrue(any("active campaign portfolio drift" in e or "leaked" in e for e in self.errors(active=active)))

    def test_vgse_cannot_leak_into_routing_registry(self):
        routing = copy.deepcopy(self.routing)
        routing["campaigns"].append({"campaign_id": "VGSE-001"})
        self.assertTrue(any("active routing portfolio drift" in e or "leaked" in e for e in self.errors(routing=routing)))


if __name__ == "__main__":
    unittest.main()
