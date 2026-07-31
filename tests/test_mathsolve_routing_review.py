from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "mathsolve_routing_review", ROOT / "ci" / "validate_mathsolve_routing.py"
)
routing = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(routing)


class ReviewedRoutingTests(unittest.TestCase):
    def registry(self):
        return json.loads(
            (ROOT / "governance" / "mathsolve_routing_audit.json").read_text(
                encoding="utf-8"
            )
        )

    def campaign(self, data, campaign_id):
        return next(
            entry for entry in data["campaigns"]
            if entry["campaign_id"] == campaign_id
        )

    def test_provider_pull_request_identity_is_fixed(self):
        data = self.registry()
        data["provider_pull_request"] = "https://github.com/grandchallenge/MATHSOLVE/pull/74"
        self.assertTrue(
            any(
                "provider_pull_request drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_cert_provider_identity_is_fixed(self):
        data = self.registry()
        data["certification_provider_commit"] = "0" * 40
        self.assertTrue(
            any(
                "certification_provider_commit drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_cert_route_registry_identity_is_fixed(self):
        data = self.registry()
        data["certification_route_registry_git_blob_sha1"] = "0" * 40
        self.assertTrue(
            any(
                "certification_route_registry_git_blob_sha1 drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_historical_predecessor_must_be_marked_superseded(self):
        data = self.registry()
        data["predecessor"]["status"] = "current"
        self.assertTrue(
            any(
                "historical predecessor" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_manifest_identity_is_fixed(self):
        data = self.registry()
        data["campaigns"][0]["manifest_git_blob_sha1"] = "0" * 40
        self.assertTrue(
            any(
                "manifest identity drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_handoff_identity_is_fixed(self):
        data = self.registry()
        data["campaigns"][0]["cert"]["handoff"]["git_blob_sha1"] = "0" * 40
        self.assertTrue(
            any(
                "handoff git_blob_sha1 drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_ready_packet_is_not_adjudicated(self):
        data = self.registry()
        self.assertTrue(routing.provider_gate_errors("HC-001", "JUDGMENT", data))
        self.assertTrue(routing.provider_gate_errors("UC-001", "INTEGRATION", data))

    def test_qualified_output_identity_is_fixed(self):
        data = self.registry()
        rh = self.campaign(data, "RH-001")
        rh["cert"]["cert_output"]["digest"] = "0" * 40
        self.assertTrue(
            any(
                "RH-001 Cert output digest drift" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_qualified_scope_cannot_expand_to_theorem(self):
        data = self.registry()
        ns = self.campaign(data, "NS-CI-001")
        ns["cert"]["qualification_scope"] = None
        self.assertTrue(
            any(
                "qualified route must be interface-only" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_intake_route_cannot_carry_cert_output(self):
        data = self.registry()
        hc = self.campaign(data, "HC-001")
        hc["cert"]["cert_output"] = copy.deepcopy(
            self.campaign(data, "RH-001")["cert"]["cert_output"]
        )
        self.assertTrue(
            any(
                "HC-001 intake route may not carry a Cert output" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_qualified_route_requires_unproved_blocker(self):
        data = self.registry()
        rh = self.campaign(data, "RH-001")
        rh["promotion"]["blockers"] = [
            "The statement interface was replayed."
        ]
        self.assertTrue(
            any(
                "qualification lacks an explicit unproved-target blocker" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_rejected_disposition_closes_integration_but_not_promotion(self):
        data = self.registry()
        hc = self.campaign(data, "HC-001")
        hc["cert"]["route_state"] = "rejected"
        self.assertEqual(
            routing.provider_gate_errors("HC-001", "INTEGRATION", data), []
        )
        self.assertTrue(
            routing.provider_gate_errors("HC-001", "CLAIM_PROMOTION", data)
        )

    def test_waiver_is_stage_scoped_and_has_all_authorities(self):
        data = self.registry()
        data["campaigns"] = [{
            "campaign_id": "HC-001",
            "title": "Hodge administrative exception",
            "disposition": "waiver",
            "waiver": {
                "waiver_id": "HC-WAIVER-001",
                "approved_by": ["Referee", "Steward", "Human Steward"],
                "human_steward_authorization": "HS-2026-001",
                "reason": "Administrative-only metadata repair with no mathematical content.",
                "scope": "One metadata-only correction.",
                "stages": ["CLAIM_PROMOTION"],
                "review_on": "2026-12-31",
            },
        }]
        self.assertEqual(
            routing.provider_gate_errors("HC-001", "CLAIM_PROMOTION", data), []
        )
        self.assertTrue(routing.provider_gate_errors("HC-001", "WP00", data))

    def test_expired_waiver_is_invalid(self):
        data = self.registry()
        data["campaigns"] = [{
            "campaign_id": "HC-001",
            "title": "Expired Hodge exception",
            "disposition": "waiver",
            "waiver": {
                "waiver_id": "HC-WAIVER-OLD",
                "approved_by": ["Referee", "Steward", "Human Steward"],
                "human_steward_authorization": "HS-2026-OLD",
                "reason": "Historical administrative exception retained only for testing.",
                "scope": "One historical metadata correction.",
                "stages": ["CLAIM_PROMOTION"],
                "review_on": "2026-07-27",
            },
        }]
        self.assertTrue(
            routing.provider_gate_errors("HC-001", "CLAIM_PROMOTION", data)
        )


if __name__ == "__main__":
    unittest.main()
