from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "mathsolve_routing", ROOT / "ci" / "validate_mathsolve_routing.py"
)
routing = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(routing)


class RoutingTests(unittest.TestCase):
    def registry(self):
        return json.loads(
            (ROOT / "governance" / "mathsolve_routing_audit.json").read_text(
                encoding="utf-8"
            )
        )

    def test_registry_passes(self):
        active = {"UC-001", "NS-CI-001", "HC-001", "BSD-001", "PNP-001", "RH-001", "YM-001", "OZ-001"}
        self.assertEqual(routing.routing_errors(active=active), [])

    def test_missing_active_campaign_fails(self):
        data = self.registry()
        data["campaigns"] = [entry for entry in data["campaigns"] if entry["campaign_id"] != "RH-001"]
        self.assertTrue(any("RH-001" in error for error in routing.routing_errors(data, active={"RH-001"})))

    def test_provider_commit_drift_fails(self):
        data = self.registry()
        data["provider_commit"] = "0" * 40
        self.assertTrue(any("provider_commit drift" in error for error in routing.routing_errors(data, active=set())))

    def test_programme_embedded_future_stage_fails(self):
        self.assertTrue(routing.provider_gate_errors("PNP-001", "WP02", self.registry()))

    def test_native_early_stage_route_is_admissible(self):
        self.assertEqual(routing.provider_gate_errors("HC-001", "WP02", self.registry()), [])

    def test_claim_promotion_requires_cert_handoff(self):
        self.assertTrue(routing.provider_gate_errors("HC-001", "CLAIM_PROMOTION", self.registry()))

    def test_silence_is_not_waiver(self):
        data = self.registry()
        data["campaigns"] = []
        self.assertIn(
            "no MATHSOLVE route or approved waiver",
            routing.provider_gate_errors("HC-001", "WP00", data)[0],
        )


if __name__ == "__main__":
    unittest.main()
