from __future__ import annotations

import sys
import unittest
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

from release_trust_admin import ReleaseTrustError  # noqa: E402
from release_trust_admin_entry import branch_ruleset  # noqa: E402


class FakeClient:
    def __init__(self, listing: list[dict[str, Any]], details: dict[int, dict[str, Any]]):
        self.listing = listing
        self.details = details

    def request(self, method: str, path: str, data: Any | None = None) -> Any:
        self.assert_get(method, data)
        if path.endswith("/rulesets"):
            return self.listing
        ruleset_id = int(path.rsplit("/", 1)[1])
        return self.details[ruleset_id]

    @staticmethod
    def assert_get(method: str, data: Any | None) -> None:
        if method != "GET" or data is not None:
            raise AssertionError((method, data))


def ruleset_detail(ruleset_id: int, name: str, include: list[str] | None = None) -> dict[str, Any]:
    return {
        "id": ruleset_id,
        "name": name,
        "target": "branch",
        "enforcement": "active",
        "conditions": {
            "ref_name": {
                "include": include if include is not None else ["~DEFAULT_BRANCH"],
                "exclude": [],
            }
        },
        "rules": [],
        "bypass_actors": [],
        "_links": {
            "self": {
                "href": f"https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/rulesets/{ruleset_id}"
            }
        },
    }


class ReleaseTrustAdminEntryTests(unittest.TestCase):
    def test_selects_named_default_profile_among_other_active_branch_rulesets(self) -> None:
        listing = [
            {"id": 21121103, "name": "MP Construction Gate - candidate creator", "target": "branch", "enforcement": "active"},
            {"id": 21121105, "name": "MP Construction Gate - candidate immutable", "target": "branch", "enforcement": "active"},
            {"id": 21121101, "name": "MP Construction Gate - development anti-delete-force", "target": "branch", "enforcement": "active"},
            {"id": 21121096, "name": "MP Construction Gate - development writer", "target": "branch", "enforcement": "active"},
            {"id": 17137629, "name": "Programme profile - main", "target": "branch", "enforcement": "active"},
        ]
        expected = ruleset_detail(17137629, "Programme profile - main")
        client = FakeClient(listing, {17137629: expected})
        self.assertEqual(branch_ruleset(client, "grandchallenge/MATH-PROGRAMME"), expected)

    def test_duplicate_named_profiles_fail_closed(self) -> None:
        listing = [
            {"id": 1, "name": "Programme profile - main", "target": "branch", "enforcement": "active"},
            {"id": 2, "name": "Programme profile - main", "target": "branch", "enforcement": "active"},
        ]
        with self.assertRaisesRegex(ReleaseTrustError, "expected exactly one active governed branch ruleset"):
            branch_ruleset(FakeClient(listing, {}), "grandchallenge/MATH-PROGRAMME")

    def test_named_profile_must_target_default_branch(self) -> None:
        listing = [
            {"id": 17137629, "name": "Programme profile - main", "target": "branch", "enforcement": "active"},
        ]
        detail = ruleset_detail(17137629, "Programme profile - main", ["refs/heads/main"])
        with self.assertRaisesRegex(ReleaseTrustError, "selector rejected structural drift"):
            branch_ruleset(FakeClient(listing, {17137629: detail}), "grandchallenge/MATH-PROGRAMME")

    def test_governed_workflow_uses_selector_compatibility_entrypoint(self) -> None:
        workflow = yaml.load(
            (ROOT / ".github/workflows/release-trust-admin.yml").read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        job = workflow["jobs"]["administer"]
        runs = "\n".join(str(step.get("run", "")) for step in job["steps"])
        self.assertIn("python ci/release_trust_admin_entry.py", runs)


if __name__ == "__main__":
    unittest.main()
