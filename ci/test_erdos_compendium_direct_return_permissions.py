#!/usr/bin/env python3
"""Hostile policy guards for an exact three-issue write-capable return projector."""
from pathlib import Path
import unittest

FLOW = (Path(__file__).resolve().parents[1] /
        ".github/workflows/erdos-compendium-editorial-returns.yml")

class DirectReturnWorkflowTests(unittest.TestCase):
    def test_existing_protected_clerk_is_the_only_writer(self):
        text = FLOW.read_text(encoding="utf-8")
        self.assertIn("    permissions:\n      contents: read\n    environment: release-trust", text)
        self.assertIn("actions/create-github-app-token@64ab729a6294000f5aa4a4bc0b73d1f32bc45510", text)
        self.assertEqual(text.count("permission-issues: write"), 1)
        self.assertIn("GCL_COUNCIL_CLERK_APP_ID", text)
        self.assertIn("GCL_COUNCIL_CLERK_PRIVATE_KEY", text)
        self.assertIn("repositories: MATH-PROGRAMME", text)
        self.assertEqual(text.count("steps.returns-token.outputs.token"), 2)
        self.assertNotIn("GH_TOKEN: " + chr(36) + "{{ github.token }}", text)

    def test_no_broad_issue_comment_trigger_or_cross_lane_claim(self):
        text = FLOW.read_text(encoding="utf-8")
        self.assertIn("startsWith(github.event.comment.body, 'RESULT/1')", text)
        self.assertIn("issue_numbers=\"2556 2557 2558\"", text)
        self.assertIn("2556|2557|2558", text)
        self.assertIn("schedule:", text)
        self.assertIn("queue: max", text)
        self.assertNotIn("gh issue comment 2556", text)
        self.assertNotIn("gh issue comment 2557", text)
        self.assertNotIn("gh issue comment 2558", text)
        self.assertNotIn(" /claim", text)

    def test_verified_readback_before_only_transport_receipt(self):
        text = FLOW.read_text(encoding="utf-8")
        self.assertIn('"value":"RETURNED"', text)
        self.assertIn("field-readback-$n.json", text)
        self.assertIn("label-readback-$n.json", text)
        self.assertIn("GCL-COMPENDIUM-DIRECT-RESULT-READBACK/1", text)
        self.assertIn("gh issue comment 2552", text)
        self.assertIn("editorial_accepted:false", text)
        self.assertIn("publication_authorized:false", text)
        self.assertIn("mathematical_effect:false", text)

if __name__ == "__main__":
    unittest.main()
