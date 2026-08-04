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


class VgseFinalActivationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admission = json.loads(module.ADMISSION_PATH.read_text(encoding="utf-8"))
        cls.decision = json.loads(module.DECISION_PATH.read_text(encoding="utf-8"))
        cls.runtime = json.loads(module.RUNTIME_PATH.read_text(encoding="utf-8"))
        cls.active = json.loads(module.ACTIVE_PATH.read_text(encoding="utf-8"))
        cls.routing = json.loads(module.ROUTING_PATH.read_text(encoding="utf-8"))
        cls.activation = json.loads(module.ACTIVATION_PATH.read_text(encoding="utf-8"))

    def errors(self, **changes):
        values = {
            "admission": self.admission,
            "decision": self.decision,
            "runtime": self.runtime,
            "active": self.active,
            "routing": self.routing,
            "activation": self.activation,
        }
        values.update(changes)
        return module.validation_errors(**{k: copy.deepcopy(v) for k, v in values.items()})

    @staticmethod
    def vgse(admission):
        return next(item for item in admission["candidates"] if item["campaign_id"] == "VGSE-001")

    def test_current_final_activation_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_vgse_must_be_active_in_governed_registry(self):
        active = copy.deepcopy(self.active)
        active["campaigns"] = [x for x in active["campaigns"] if x["campaign_id"] != "VGSE-001"]
        self.assertTrue(any("active campaign portfolio drift" in e for e in self.errors(active=active)))

    def test_solve_manifest_identity_is_pinned(self):
        routing = copy.deepcopy(self.routing)
        routing["successor_campaign"]["manifest"]["digest"] = "0" * 40
        self.assertTrue(any("Solve manifest identity drift" in e for e in self.errors(routing=routing)))

    def test_cert_route_identity_is_pinned(self):
        routing = copy.deepcopy(self.routing)
        routing["successor_campaign"]["cert"]["route_registration"]["digest"] = "0" * 40
        self.assertTrue(any("MATHCERT route identity drift" in e for e in self.errors(routing=routing)))

    def test_route_cannot_adjudicate(self):
        routing = copy.deepcopy(self.routing)
        routing["successor_campaign"]["cert"]["may_adjudicate"] = True
        self.assertTrue(any("Cert pending-route boundary drift" in e for e in self.errors(routing=routing)))

    def test_route_cannot_issue_output(self):
        routing = copy.deepcopy(self.routing)
        routing["successor_campaign"]["cert"]["cert_output"] = {"path": "certificate.json"}
        self.assertTrue(any("Cert pending-route boundary drift" in e for e in self.errors(routing=routing)))

    def test_active_lifecycle_cannot_roll_back(self):
        admission = copy.deepcopy(self.admission)
        self.vgse(admission)["lifecycle_state"] = "candidate"
        self.assertTrue(any("active lifecycle projection drift" in e for e in self.errors(admission=admission)))

    def test_completed_programme_gate_cannot_roll_back(self):
        admission = copy.deepcopy(self.admission)
        self.vgse(admission)["admission_gates"]["programme_routing_registry_updated"] = False
        self.assertTrue(any("admission gate inflated or rolled back" in e for e in self.errors(admission=admission)))

    def test_intellect_gate_cannot_close_early(self):
        admission = copy.deepcopy(self.admission)
        self.vgse(admission)["admission_gates"]["intellect_repin_complete_if_required"] = True
        self.assertTrue(any("INTELLECT repin may not close" in e for e in self.errors(admission=admission)))

    def test_issue_cannot_close_before_consumer_repin(self):
        activation = copy.deepcopy(self.activation)
        activation["consumer_obligation"]["programme_issue_may_close"] = True
        self.assertTrue(any("consumer obligation drift" in e for e in self.errors(activation=activation)))

    def test_activation_claim_inflation_is_rejected(self):
        activation = copy.deepcopy(self.activation)
        activation["claim_boundary"]["mathematical_target_proved"] = True
        self.assertTrue(any("activation claim boundary inflation" in e for e in self.errors(activation=activation)))


if __name__ == "__main__":
    unittest.main()
