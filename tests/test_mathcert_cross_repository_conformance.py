from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
AUDIT_PATH = ROOT / "governance" / "mathcert_cross_repository_conformance.json"
SCHEMA_PATH = ROOT / "schemas" / "mathcert_cross_repository_conformance.schema.json"
ROUTING_PATH = ROOT / "governance" / "mathsolve_routing_audit.json"
HEX40 = re.compile(r"^[0-9a-f]{40}$")


class MathCertCrossRepositoryConformanceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.audit = json.loads(AUDIT_PATH.read_text(encoding="utf-8"))
        self.routing = json.loads(ROUTING_PATH.read_text(encoding="utf-8"))

    def test_audit_is_schema_valid(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        errors = list(
            Draft202012Validator(
                schema, format_checker=FormatChecker()
            ).iter_errors(self.audit)
        )
        self.assertEqual([], [error.message for error in errors])

    def test_campaign_identity_matches_programme_registry(self) -> None:
        audited = {item["campaign_id"]: item for item in self.audit["campaigns"]}
        routed = {item["campaign_id"]: item for item in self.routing["campaigns"]}
        self.assertEqual(set(audited), set(routed))
        self.assertEqual(
            set(audited),
            {"UC-001", "NS-CI-001", "HC-001", "BSD-001", "PNP-001", "RH-001", "YM-001", "OZ-001"},
        )
        for campaign_id, record in audited.items():
            route = routed[campaign_id]
            self.assertEqual(record["manifest_git_blob_sha1"], route["manifest_git_blob_sha1"])
            self.assertEqual(record["handoff_id"], route["cert"]["handoff"]["handoff_id"])
            self.assertEqual(
                record["handoff_git_blob_sha1"],
                route["cert"]["handoff"]["git_blob_sha1"],
            )
            self.assertEqual(record["handoff_state"], route["cert"]["handoff"]["state"])
            self.assertEqual(record["mathcert_route_state"], route["cert"]["route_state"])
            self.assertEqual(
                record["mathcert_route_issue"],
                int(route["cert"]["route_issue"].rstrip("/").rsplit("/", 1)[1]),
            )
            self.assertEqual(record["promotion_state"], route["promotion"]["state"])

    def test_no_pending_route_claims_a_cert_output(self) -> None:
        for record in self.audit["campaigns"]:
            self.assertEqual(record["mathcert_route_state"], "pending")
            self.assertIsNone(record["mathcert_output"])
            self.assertEqual(record["promotion_state"], "blocked")
        self.assertEqual(
            {item["campaign_id"] for item in self.audit["campaigns"] if item["handoff_state"] == "ready"},
            {"UC-001", "NS-CI-001", "HC-001"},
        )

    def test_status_semantics_are_disjoint_and_fail_closed(self) -> None:
        semantics = self.audit["status_semantics"]
        intake = set(semantics["intake_states"])
        adjudicated = set(semantics["adjudicated_states"])
        promoting = set(semantics["positive_promotion_states"])
        self.assertEqual(intake, {"pending", "ready", "submitted"})
        self.assertEqual(adjudicated, {"certified", "qualified", "rejected", "proof_debt"})
        self.assertFalse(intake & adjudicated)
        self.assertEqual(promoting, {"certified", "qualified"})
        self.assertTrue(promoting < adjudicated)

    def test_exact_head_workflow_evidence_is_complete(self) -> None:
        repositories = self.audit["repositories"]
        expected_runs = {
            "mathcert": 30417641550,
            "mathsolve": 30422681058,
            "math_programme": 30421341832,
            "intellect": 30422791727,
        }
        for name, run_id in expected_runs.items():
            workflow = repositories[name]["workflow"]
            self.assertEqual(workflow["run_id"], run_id)
            self.assertEqual(workflow["conclusion"], "success")
            self.assertRegex(workflow["exact_head"], HEX40)

    def test_provider_and_semantic_artifact_pins_are_exact(self) -> None:
        repositories = self.audit["repositories"]
        self.assertEqual(
            repositories["mathcert"]["route_registry"]["git_blob_sha1"],
            self.routing["certification_route_registry_git_blob_sha1"],
        )
        self.assertEqual(
            repositories["mathsolve"]["handoff_merge_commit"],
            self.routing["provider_commit"],
        )
        self.assertEqual(
            repositories["math_programme"]["routing_registry"]["git_blob_sha1"],
            "39e907cce79137168e5b2a240674d7f4e6f56cdd",
        )
        for key, value in repositories["intellect"]["semantic_artifacts"].items():
            if key.endswith("git_blob_sha1"):
                self.assertRegex(value, HEX40)

    def test_closure_preserves_operational_blockers(self) -> None:
        closure = self.audit["closure"]
        self.assertTrue(closure["repository_conformance_complete"])
        self.assertTrue(closure["parent_issue_123_close_after_audit_merge"])
        self.assertTrue(closure["programme_umbrella_issue_6_remains_open"])
        self.assertEqual(set(closure["remaining_operational_issues"]), {7, 125})
        self.assertEqual(self.audit["administrative_enforcement_status"], "unverified")


if __name__ == "__main__":
    unittest.main()
