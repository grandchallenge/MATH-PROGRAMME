from __future__ import annotations

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

    def test_provider_pull_request_identity_is_fixed(self):
        data = self.registry()
        data["provider_pull_request"] = "https://github.com/grandchallenge/MATHSOLVE/pull/71"
        self.assertTrue(
            any(
                "provider pull-request drift" in error
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

    def test_rejected_disposition_is_not_positive_promotion(self):
        data = self.registry()
        hc = next(
            entry for entry in data["campaigns"] if entry["campaign_id"] == "HC-001"
        )
        hc["cert"]["state"] = "rejected"
        hc["promotion"] = {"state": "allowed", "blockers": []}
        self.assertEqual(
            routing.provider_gate_errors("HC-001", "INTEGRATION", data), []
        )
        self.assertTrue(
            routing.provider_gate_errors("HC-001", "CLAIM_PROMOTION", data)
        )
        self.assertTrue(
            any(
                "allowed promotion lacks certified or qualified" in error
                for error in routing.routing_errors(data, active=set())
            )
        )

    def test_waiver_is_stage_scoped_and_has_all_authorities(self):
        data = self.registry()
        data["campaigns"] = [
            {
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
                    "review_on": "2026-12-31"
                }
            }
        ]
        self.assertEqual(
            routing.provider_gate_errors("HC-001", "CLAIM_PROMOTION", data), []
        )
        self.assertTrue(routing.provider_gate_errors("HC-001", "WP00", data))

        data["campaigns"][0]["waiver"]["approved_by"] = ["Referee", "Steward"]
        self.assertTrue(
            routing.provider_gate_errors("HC-001", "CLAIM_PROMOTION", data)
        )

    def test_expired_waiver_is_invalid(self):
        data = self.registry()
        data["campaigns"] = [
            {
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
                    "review_on": "2026-07-27"
                }
            }
        ]
        self.assertTrue(
            routing.provider_gate_errors("HC-001", "CLAIM_PROMOTION", data)
        )

    def test_cert_route_issue_is_required(self):
        data = self.registry()
        data["campaigns"][0]["cert"]["issue"] = None
        self.assertTrue(routing.routing_errors(data, active=set()))


if __name__ == "__main__":
    unittest.main()
