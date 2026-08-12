from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import pr_visual_status_operational_split as split  # noqa: E402


class RecordingClient:
    def __init__(self, name: str):
        self.name = name
        self.calls: list[tuple[str, str]] = []

    def get(self, path: str):
        self.calls.append(("GET", path))
        return {"client": self.name}

    def post(self, path: str, payload):
        self.calls.append(("POST", path))
        return {"client": self.name, "id": 1}

    def patch(self, path: str, payload):
        self.calls.append(("PATCH", path))
        return {"client": self.name, "id": 1}


class PRVisualStatusCredentialSplitTests(unittest.TestCase):
    def test_rulesets_route_only_to_administration_client(self) -> None:
        source = RecordingClient("source")
        admin = RecordingClient("admin")
        publisher = RecordingClient("publisher")
        client = split.SplitCredentialClient(source, admin, publisher)

        self.assertEqual("admin", client.get("/repos/grandchallenge/MATH-PROGRAMME/rulesets")["client"])
        self.assertEqual("admin", client.get("/repos/grandchallenge/MATH-PROGRAMME/rulesets/123")["client"])
        self.assertEqual("source", client.get("/repos/grandchallenge/MATH-PROGRAMME/commits/abc/check-runs")["client"])
        self.assertEqual("source", client.get("/repos/grandchallenge/MATH-PROGRAMME/pulls/465")["client"])
        self.assertEqual(2, len(admin.calls))
        self.assertEqual(2, len(source.calls))

    def test_mutations_route_only_to_publisher_client(self) -> None:
        source = RecordingClient("source")
        admin = RecordingClient("admin")
        publisher = RecordingClient("publisher")
        client = split.SplitCredentialClient(source, admin, publisher)

        self.assertEqual("publisher", client.post("/repos/grandchallenge/MATH-PROGRAMME/git/blobs", {})["client"])
        self.assertEqual("publisher", client.patch("/repos/grandchallenge/MATH-PROGRAMME/issues/comments/1", {})["client"])
        self.assertEqual([], source.calls)
        self.assertEqual([], admin.calls)
        self.assertEqual(2, len(publisher.calls))

    def test_missing_publisher_fails_closed_on_mutation(self) -> None:
        client = split.SplitCredentialClient(
            RecordingClient("source"), RecordingClient("admin"), None
        )
        with self.assertRaisesRegex(Exception, "publisher credential is unavailable"):
            client.post("/repos/grandchallenge/MATH-PROGRAMME/git/blobs", {})

    def test_workflow_uses_split_least_authority_credentials(self) -> None:
        text = (ROOT / ".github" / "workflows" / "pr-visual-status-advisory.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("permission-contents: write", text)
        self.assertIn("permission-issues: write", text)
        self.assertIn("permission-administration: read", text)
        self.assertIn("GITHUB_ADMIN_TOKEN:", text)
        self.assertIn("GITHUB_PUBLISH_TOKEN:", text)
        self.assertIn("GITHUB_TOKEN: ${{ github.token }}", text)
        self.assertIn("python3 ci/pr_visual_status_operational_split.py", text)
        self.assertIn("checks: read", text)
        self.assertIn("issues: read", text)
        self.assertIn("pull-requests: read", text)
        self.assertNotIn("permission-actions:", text)
        self.assertNotIn("permission-checks:", text)
        self.assertNotIn("permission-administration: write", text)

    def test_protected_workflow_keeps_app_tokens_distinct(self) -> None:
        text = (ROOT / ".github" / "workflows" / "pr-visual-status-advisory.yml").read_text(
            encoding="utf-8"
        )
        publisher = text.split("- name: Mint bounded PRVSR publisher token", 1)[1].split(
            "- name: Mint bounded PRVSR administration token", 1
        )[0]
        admin = text.split("- name: Mint bounded PRVSR administration token", 1)[1].split(
            "- name: Checkout trusted protected implementation", 1
        )[0]
        self.assertIn("permission-contents: write", publisher)
        self.assertIn("permission-issues: write", publisher)
        self.assertNotIn("permission-administration", publisher)
        self.assertEqual(1, admin.count("permission-administration: read"))
        self.assertNotIn("permission-contents: write", admin)
        self.assertNotIn("permission-issues: write", admin)


if __name__ == "__main__":
    unittest.main()
