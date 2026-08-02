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

    def uc(self, data):
        return next(
            entry for entry in data["campaigns"]
            if entry["campaign_id"] == "UC-001"
        )

    def test_registry_passes(self):
        active = {
            "UC-001", "NS-CI-001", "HC-001", "BSD-001",
            "PNP-001", "RH-001", "YM-001", "OZ-001",
        }
        self.assertEqual(routing.routing_errors(active=active), [])

    def test_missing_active_campaign_fails(self):
        data = self.registry()
        data["campaigns"] = [
            entry for entry in data["campaigns"]
            if entry["campaign_id"] != "RH-001"
        ]
        self.assertTrue(
            any(
                "RH-001" in error
                for error in routing.routing_errors(data, active={"RH-001"})
            )
        )

    def test_provider_commit_drift_fails(self):
        data = self.registry()
        data["provider_commit"] = "0" * 40
        self.assertTrue(
            any(
                "provider_commit drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_cert_provider_commit_drift_fails(self):
        data = self.registry()
        data["certification_provider_commit"] = "0" * 40
        self.assertTrue(
            any(
                "certification_provider_commit drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_programme_embedded_future_stage_fails(self):
        self.assertTrue(
            routing.provider_gate_errors("PNP-001", "WP02", self.registry())
        )

    def test_native_early_stage_route_is_admissible(self):
        self.assertEqual(
            routing.provider_gate_errors("HC-001", "WP02", self.registry()), []
        )

    def test_qualified_interface_allows_integration_review_only(self):
        data = self.registry()
        self.assertEqual(
            routing.provider_gate_errors("RH-001", "INTEGRATION", data), []
        )
        self.assertTrue(
            routing.provider_gate_errors("RH-001", "CLAIM_PROMOTION", data)
        )

    def test_uc_restricted_qualification_allows_integration_review_only(self):
        data = self.registry()
        self.assertEqual(
            routing.provider_gate_errors("UC-001", "INTEGRATION", data), []
        )
        self.assertTrue(
            routing.provider_gate_errors("UC-001", "CLAIM_PROMOTION", data)
        )

    def test_claim_promotion_remains_blocked(self):
        self.assertTrue(
            routing.provider_gate_errors("NS-CI-001", "CLAIM_PROMOTION", self.registry())
        )

    def test_silence_is_not_waiver(self):
        data = self.registry()
        data["campaigns"] = []
        self.assertIn(
            "no MATHSOLVE route or approved waiver",
            routing.provider_gate_errors("HC-001", "WP00", data)[0],
        )

    def test_uc_manifest_identity_drift_fails(self):
        data = self.registry()
        self.uc(data)["manifest_git_blob_sha1"] = "0" * 40
        self.assertTrue(
            any(
                "UC-001 manifest identity drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_uc_route_state_cannot_regress_to_ready(self):
        data = self.registry()
        self.uc(data)["cert"]["route_state"] = "ready"
        self.assertTrue(
            any(
                "UC-001 Cert provider state drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_uc_handoff_state_cannot_be_rewritten_as_qualified(self):
        data = self.registry()
        self.uc(data)["cert"]["handoff"]["state"] = "qualified"
        self.assertTrue(
            any(
                "UC-001 handoff state drift" in error or "is not one of" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_uc_cert_output_identity_drift_fails(self):
        data = self.registry()
        self.uc(data)["cert"]["cert_output"]["digest"] = "0" * 40
        self.assertTrue(
            any(
                "UC-001 Cert output digest drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_uc_qualification_scope_drift_fails(self):
        data = self.registry()
        self.uc(data)["cert"]["qualification_scope"] = "qualified_interface_only"
        self.assertTrue(
            any(
                "UC-001 qualification scope drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_uc_qualification_requires_unproved_target_blocker(self):
        data = self.registry()
        self.uc(data)["promotion"]["blockers"] = [
            "Finite replay remains bounded at n <= 4."
        ]
        self.assertTrue(
            any(
                "UC-001 qualification lacks an explicit unproved-target blocker" in error
                for error in routing.routing_errors(data, active=set())
            )
        )


if __name__ == "__main__":
    unittest.main()
