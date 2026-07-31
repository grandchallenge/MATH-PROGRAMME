from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "umbrella_current_state", ROOT / "ci" / "umbrella_current_state.py"
)
module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(module)


class UmbrellaCurrentStateTests(unittest.TestCase):
    def load(self, name):
        return json.loads((ROOT / "governance" / name).read_text(encoding="utf-8"))

    def test_current_state_passes(self):
        self.assertEqual(module.validation_errors(), [])

    def test_historical_audit_cannot_be_presented_as_current(self):
        audit = self.load("umbrella_current_state_conformance.json")
        audit["predecessor"]["status"] = "current"
        self.assertTrue(
            any("historical and superseded" in error for error in module.validation_errors(audit=audit))
        )

    def test_rh_qualification_cannot_expand_to_theorem(self):
        routing = self.load("mathsolve_routing_audit.json")
        rh = next(item for item in routing["campaigns"] if item["campaign_id"] == "RH-001")
        rh["cert"]["qualification_scope"] = None
        self.assertTrue(
            any("RH-001 qualification is not interface-only" in error for error in module.validation_errors(routing=routing))
        )

    def test_ns_qualification_cannot_enable_promotion(self):
        routing = self.load("mathsolve_routing_audit.json")
        ns = next(item for item in routing["campaigns"] if item["campaign_id"] == "NS-CI-001")
        ns["promotion"]["state"] = "allowed"
        self.assertTrue(
            any("NS-CI-001 qualification may not enable promotion" in error for error in module.validation_errors(routing=routing))
        )

    def test_ready_route_cannot_be_silently_qualified(self):
        routing = self.load("mathsolve_routing_audit.json")
        hc = next(item for item in routing["campaigns"] if item["campaign_id"] == "HC-001")
        hc["cert"]["route_state"] = "qualified"
        self.assertTrue(
            any("qualified portfolio drift" in error for error in module.validation_errors(routing=routing))
        )

    def test_odd_zeta_must_remain_additional_campaign(self):
        campaigns = self.load("governed_campaign_registry.json")
        oz = next(item for item in campaigns["campaigns"] if item["campaign_id"] == "OZ-001")
        oz["domain_id"] = "OZ"
        self.assertTrue(
            any("additional campaign" in error for error in module.validation_errors(campaigns=campaigns))
        )

    def test_archived_poincare_cannot_enter_active_routing(self):
        campaigns = self.load("governed_campaign_registry.json")
        pc = next(item for item in campaigns["campaigns"] if item["campaign_id"] == "PC-001")
        pc["routing_member"] = True
        self.assertTrue(
            any("archived PC-001" in error for error in module.validation_errors(campaigns=campaigns))
        )

    def test_release_trust_cannot_be_reopened(self):
        audit = self.load("umbrella_current_state_conformance.json")
        audit["claim_boundaries"]["release_trust_issues_reopened"] = True
        self.assertTrue(
            any("may not be reopened" in error for error in module.validation_errors(audit=audit))
        )


if __name__ == "__main__":
    unittest.main()
