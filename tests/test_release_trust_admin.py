from __future__ import annotations

import copy
import json
import sys
import unittest
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from release_trust_admin import (  # noqa: E402
    RULESET_NAMES,
    ReleaseTrustError,
    normalize_ruleset,
    ruleset_errors,
    ruleset_payload,
    validate_contract,
)
from github_http import CrossOriginAuthStrippingRedirectHandler  # noqa: E402


class ReleaseTrustAdminTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(
            (ROOT / "governance/release_trust_admin_contract.json").read_text(encoding="utf-8")
        )
        cls.schema = json.loads(
            (ROOT / "schemas/release_trust_admin_contract.schema.json").read_text(encoding="utf-8")
        )

    def test_current_contract_passes(self) -> None:
        validate_contract(self.contract, self.schema)

    def test_intellect_uses_constitutional_ruleset_name(self) -> None:
        self.assertEqual(
            RULESET_NAMES["grandchallenge/INTELLECT"],
            "Constitutional profile - main",
        )

    def test_repository_omission_is_rejected(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["repositories"].pop()
        with self.assertRaises(ReleaseTrustError):
            validate_contract(contract, self.schema)

    def test_required_context_drift_is_rejected(self) -> None:
        contract = copy.deepcopy(self.contract)
        contract["repositories"][0]["required_checks"] = ["wrong-check"]
        with self.assertRaises(ReleaseTrustError):
            validate_contract(contract, self.schema)

    def test_ruleset_payload_is_fail_closed_without_approval_deadlock(self) -> None:
        policy = self.contract["branch_policy"]
        payload = ruleset_payload("Cert profile - main", policy, ["certify"])
        self.assertEqual(payload["target"], "branch")
        self.assertEqual(payload["enforcement"], "active")
        self.assertEqual(payload["bypass_actors"], [])
        self.assertEqual(
            payload["conditions"],
            {"ref_name": {"include": ["~DEFAULT_BRANCH"], "exclude": []}},
        )
        rules = {rule["type"]: rule for rule in payload["rules"]}
        status = rules["required_status_checks"]["parameters"]
        reviews = rules["pull_request"]["parameters"]
        self.assertTrue(status["strict_required_status_checks_policy"])
        self.assertEqual(status["required_status_checks"], [{"context": "certify"}])
        self.assertEqual(reviews["required_approving_review_count"], 0)
        self.assertFalse(reviews["require_last_push_approval"])
        self.assertTrue(reviews["required_review_thread_resolution"])
        self.assertIn("non_fast_forward", rules)
        self.assertIn("deletion", rules)

    def test_normalized_matching_ruleset_passes(self) -> None:
        raw = ruleset_payload(
            "Cert profile - main", self.contract["branch_policy"], ["certify"]
        )
        raw["source"] = "grandchallenge/MATHCERT"
        normalized = normalize_ruleset(raw)
        self.assertEqual(
            ruleset_errors(
                normalized,
                self.contract["branch_policy"],
                ["certify"],
                "Cert profile - main",
            ),
            [],
        )

    def test_bypass_actor_is_rejected(self) -> None:
        raw = ruleset_payload(
            "Cert profile - main", self.contract["branch_policy"], ["certify"]
        )
        raw["source"] = "grandchallenge/MATHCERT"
        raw["bypass_actors"] = [{"actor_id": 1, "actor_type": "Team"}]
        errors = ruleset_errors(
            normalize_ruleset(raw),
            self.contract["branch_policy"],
            ["certify"],
            "Cert profile - main",
        )
        self.assertTrue(any("bypass actors" in error for error in errors))

    def test_relaxed_status_checks_are_rejected(self) -> None:
        raw = ruleset_payload(
            "Cert profile - main", self.contract["branch_policy"], ["certify"]
        )
        raw["source"] = "grandchallenge/MATHCERT"
        status = next(
            rule for rule in raw["rules"] if rule["type"] == "required_status_checks"
        )
        status["parameters"]["strict_required_status_checks_policy"] = False
        errors = ruleset_errors(
            normalize_ruleset(raw),
            self.contract["branch_policy"],
            ["certify"],
            "Cert profile - main",
        )
        self.assertTrue(any("strict_status_checks drift" in error for error in errors))

    def test_cross_origin_artifact_redirect_drops_authorization(self) -> None:
        request = urllib.request.Request(
            "https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/actions/artifacts/1/zip",
            headers={"Authorization": "Bearer secret", "Accept": "application/zip"},
        )
        redirected = CrossOriginAuthStrippingRedirectHandler().redirect_request(
            request,
            None,
            302,
            "Found",
            {},
            "https://pipelines.actions.githubusercontent.com/signed-artifact",
        )
        self.assertIsNotNone(redirected)
        assert redirected is not None
        self.assertNotIn("Authorization", redirected.headers)
        self.assertEqual(redirected.get_header("Accept"), "application/zip")

    def test_same_origin_redirect_keeps_authorization(self) -> None:
        request = urllib.request.Request(
            "https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/actions/artifacts/1/zip",
            headers={"Authorization": "Bearer secret"},
        )
        redirected = CrossOriginAuthStrippingRedirectHandler().redirect_request(
            request,
            None,
            302,
            "Found",
            {},
            "https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/actions/artifacts/2/zip",
        )
        self.assertIsNotNone(redirected)
        assert redirected is not None
        self.assertEqual(redirected.get_header("Authorization"), "Bearer secret")

    def test_administration_workflow_is_governed(self) -> None:
        workflow = yaml.load(
            (ROOT / ".github/workflows/release-trust-admin.yml").read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        self.assertEqual(workflow["name"], "Release trust administration")
        self.assertIn("workflow_dispatch", workflow["on"])
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        self.assertEqual(workflow["concurrency"]["group"], "release-trust-administration")
        job = workflow["jobs"]["administer"]
        self.assertEqual(job["runs-on"], "ubuntu-24.04")
        self.assertEqual(job["timeout-minutes"], "30")
        self.assertEqual(job["environment"], "release-trust")
        uses = [step.get("uses", "") for step in job["steps"]]
        self.assertIn(
            "actions/create-github-app-token@"
            "bcd2ba49218906704ab6c1aa796996da409d3eb1",
            uses,
        )
        self.assertIn(
            "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1", uses
        )
        self.assertIn(
            "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97", uses
        )
        self.assertIn(
            "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
            uses,
        )
        app_step = next(step for step in job["steps"] if step.get("id") == "app-token")
        self.assertEqual(
            app_step["with"]["app-id"], "${{ secrets.GCL_RELEASE_TRUST_APP_ID }}"
        )
        self.assertEqual(
            app_step["with"]["private-key"],
            "${{ secrets.GCL_RELEASE_TRUST_PRIVATE_KEY }}",
        )
        admin_steps = [
            step
            for step in job["steps"]
            if "GCL_REPOSITORY_ADMIN_TOKEN" in step.get("env", {})
        ]
        self.assertEqual(len(admin_steps), 2)
        for step in admin_steps:
            self.assertEqual(
                step["env"]["GCL_REPOSITORY_ADMIN_TOKEN"],
                "${{ steps.app-token.outputs.token }}",
            )
        runs = "\n".join(str(step.get("run", "")) for step in job["steps"])
        self.assertIn("python -m pip install --requirement requirements/policy.txt", runs)
        self.assertIn("python ci/release_trust_admin.py --mode validate", runs)
        self.assertIn("--wait-seconds 1200", runs)
        self.assertIn("--close-child-issues", runs)
        upload = next(step for step in job["steps"] if step.get("name") == "Upload release-trust evidence")
        self.assertEqual(upload["with"]["retention-days"], "90")
        self.assertEqual(upload["with"]["if-no-files-found"], "error")


if __name__ == "__main__":
    unittest.main()
