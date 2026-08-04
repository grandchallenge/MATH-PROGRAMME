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
        cls.activation = json.loads(module.ACTIVATION_PATH.read_text(encoding="utf-8"))
        cls.decision = json.loads(module.DECISION_PATH.read_text(encoding="utf-8"))

    def errors(self, **changes):
        values = {
            "admission": self.admission,
            "runtime": self.runtime,
            "active": self.active,
            "routing": self.routing,
            "activation": self.activation,
            "decision": self.decision,
        }
        values.update(changes)
        return module.validation_errors(**{k: copy.deepcopy(v) for k, v in values.items()})

    @staticmethod
    def record(admission, campaign_id):
        return next(item for item in admission["candidates"] if item["campaign_id"] == campaign_id)

    def test_current_activation_control_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_nsof_cannot_enter_active_registry(self):
        active = copy.deepcopy(self.active)
        active["campaigns"].append({"campaign_id": "NSOF-001"})
        self.assertTrue(any("active campaign portfolio drift" in e for e in self.errors(active=active)))

    def test_nsof_cannot_close_any_gate(self):
        admission = copy.deepcopy(self.admission)
        self.record(admission, "NSOF-001")["admission_gates"]["cert_route_registered"] = True
        self.assertTrue(any("NSOF-001: admission gate inflated" in e for e in self.errors(admission=admission)))

    def test_nsof_screenshot_digest_is_pinned(self):
        admission = copy.deepcopy(self.admission)
        self.record(admission, "NSOF-001")["source_provenance"]["intake_evidence"]["sha256"] = "0" * 64
        self.assertTrue(any("screenshot evidence identity drift" in e for e in self.errors(admission=admission)))

    def test_issue_mutation_cannot_admit(self):
        admission = copy.deepcopy(self.admission)
        admission["authority"]["candidate_issue_mutation_can_admit_campaign"] = True
        self.assertTrue(any("campaign admission registry" in e for e in self.errors(admission=admission)))

    def test_runtime_requires_consumer_repin(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["consumer_sync"]["intellect_repin_required"] = False
        self.assertTrue(any("INTELLECT consumer gate drift" in e or "runtime contract v5" in e for e in self.errors(runtime=runtime)))

    def test_runtime_cannot_claim_mathematical_proof(self):
        runtime = copy.deepcopy(self.runtime)
        runtime["claim_boundaries"]["mathematical_target_proved"] = True
        self.assertTrue(any("runtime claim inflation" in e for e in self.errors(runtime=runtime)))


if __name__ == "__main__":
    unittest.main()
