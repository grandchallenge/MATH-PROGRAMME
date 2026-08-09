from __future__ import annotations

import base64
import json
import sys
import unittest
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from aether_controls_admin import (  # noqa: E402
    AetherControlsError,
    BRANCH_RULESET_NAME,
    REQUIRED_JOBS,
    TAG_RULESET_NAME,
    branch_ruleset_payload,
    retire,
    stage,
    tag_ruleset_payload,
    validate_policy,
)


HEAD = "a" * 40


def policy() -> dict[str, Any]:
    return {
        "schema_version": "aether.repository-controls.v1",
        "repository": "grandchallenge/AETHER",
        "protected_branch": {
            "name": "main",
            "required_status_checks": sorted(REQUIRED_JOBS),
            "strict": True,
            "minimum_approvals": 0,
            "dismiss_stale_reviews": True,
            "require_code_owner_reviews": False,
            "require_last_push_approval": False,
            "required_conversation_resolution": True,
            "enforce_admins": True,
            "lock_branch": True,
            "allow_force_pushes": False,
            "allow_deletions": False,
        },
        "protection_model": {
            "default_branch_ruleset": {"name": BRANCH_RULESET_NAME},
            "release_tag_ruleset": {"name": TAG_RULESET_NAME},
        },
    }


class FakeClient:
    def __init__(self, *, jobs: set[str] | None = None):
        self.policy = policy()
        self.jobs = REQUIRED_JOBS if jobs is None else jobs
        self.rulesets: dict[int, dict[str, Any]] = {}
        self.next_id = 10
        self.classic: dict[str, Any] | None = {
            "lock_branch": {"enabled": True},
            "required_status_checks": {"strict": True},
        }

    def request(
        self,
        method: str,
        path: str,
        data: Any | None = None,
        *,
        allow_404: bool = False,
    ) -> Any:
        if path == "/repos/grandchallenge/AETHER/pulls/59":
            return {"state": "open", "head": {"sha": HEAD}}
        if "/contents/.github/repository-controls.json" in path:
            raw = json.dumps(self.policy).encode()
            return {
                "encoding": "base64",
                "content": base64.b64encode(raw).decode(),
                "sha": "b" * 40,
            }
        if path.startswith("/repos/grandchallenge/AETHER/actions/runs?"):
            return {"workflow_runs": [{"id": 1, "head_sha": HEAD, "conclusion": "success"}]}
        if path == "/repos/grandchallenge/AETHER/actions/runs/1/jobs?per_page=100":
            return {"jobs": [{"name": name, "conclusion": "success"} for name in self.jobs]}
        if path == "/repos/grandchallenge/AETHER/rulesets":
            if method == "GET":
                return [{"id": key, "name": value["name"]} for key, value in self.rulesets.items()]
            if method == "POST":
                current = self.next_id
                self.next_id += 1
                self.rulesets[current] = {"id": current, **data}
                return self.rulesets[current]
        if path.startswith("/repos/grandchallenge/AETHER/rulesets/"):
            current = int(path.rsplit("/", 1)[1])
            if method == "GET":
                return self.rulesets[current]
            if method == "PUT":
                self.rulesets[current] = {"id": current, **data}
                return self.rulesets[current]
        if path == "/repos/grandchallenge/AETHER/branches/main":
            return {"commit": {"sha": HEAD}}
        if path == "/repos/grandchallenge/AETHER/branches/main/protection":
            if method == "GET":
                if self.classic is None:
                    return {"_status": 404} if allow_404 else None
                return self.classic
            if method == "PUT":
                self.classic = {
                    "lock_branch": {"enabled": data["lock_branch"]},
                    "required_status_checks": data["required_status_checks"],
                }
                return self.classic
            if method == "DELETE":
                self.classic = None
                return None
        raise AssertionError(f"unhandled request: {method} {path}")


class AetherControlsAdminTests(unittest.TestCase):
    def test_policy_contract_passes(self) -> None:
        validate_policy(policy())

    def test_required_context_drift_fails_closed(self) -> None:
        value = policy()
        value["protected_branch"]["required_status_checks"].pop()
        with self.assertRaisesRegex(AetherControlsError, "required job set drift"):
            validate_policy(value)

    def test_stage_creates_rulesets_before_unlock(self) -> None:
        client = FakeClient()
        result = stage(client, 59, HEAD)
        self.assertEqual(result["state"], "staged")
        self.assertFalse(client.classic["lock_branch"]["enabled"])
        self.assertEqual(
            {item["name"] for item in client.rulesets.values()},
            {BRANCH_RULESET_NAME, TAG_RULESET_NAME},
        )
        self.assertEqual(
            client.rulesets[10], {"id": 10, **branch_ruleset_payload(policy())}
        )
        self.assertEqual(
            client.rulesets[11], {"id": 11, **tag_ruleset_payload()}
        )

    def test_stage_rejects_incomplete_exact_head_jobs(self) -> None:
        client = FakeClient(jobs={"Required CI gate"})
        with self.assertRaisesRegex(AetherControlsError, "jobs are incomplete"):
            stage(client, 59, HEAD)
        self.assertEqual(client.rulesets, {})
        self.assertTrue(client.classic["lock_branch"]["enabled"])

    def test_retire_requires_exact_protected_main_and_keeps_rulesets(self) -> None:
        client = FakeClient()
        client.rulesets = {
            10: {"id": 10, **branch_ruleset_payload(policy())},
            11: {"id": 11, **tag_ruleset_payload()},
        }
        result = retire(client, HEAD)
        self.assertEqual(result["state"], "retired_classic")
        self.assertIsNone(client.classic)
        self.assertEqual(len(client.rulesets), 2)

    def test_workflow_uses_only_bounded_app_permissions(self) -> None:
        workflow = yaml.load(
            (ROOT / ".github/workflows/aether-controls-admin.yml").read_text(
                encoding="utf-8"
            ),
            Loader=yaml.BaseLoader,
        )
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        job = workflow["jobs"]["administer"]
        self.assertEqual(job["environment"], "release-trust")
        token = next(step for step in job["steps"] if step.get("id") == "app-token")
        self.assertEqual(token["with"]["repositories"], "AETHER")
        self.assertEqual(token["with"]["permission-administration"], "write")
        self.assertEqual(token["with"]["permission-actions"], "read")
        self.assertEqual(token["with"]["permission-contents"], "read")
        self.assertEqual(token["with"]["permission-pull-requests"], "read")
        uses = [step.get("uses", "") for step in job["steps"]]
        self.assertTrue(all("@" in value for value in uses if value))


if __name__ == "__main__":
    unittest.main()
