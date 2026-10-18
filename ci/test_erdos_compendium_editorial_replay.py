#!/usr/bin/env python3
"""Static replay-contract guard for the exact protected Compendium admission path."""
from pathlib import Path
import json
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/erdos-catalogue-queue-projection.yml"


class CompendiumEditorialReplayTests(unittest.TestCase):
    def test_scheduled_replay_uses_original_clerk_and_is_never_issue_comment_pickup(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("schedule:", text)
        self.assertIn("workflow_dispatch:", text)
        self.assertIn("id: editorial-admit\n        if: github.event_name != 'issue_comment'", text)
        self.assertIn("GH_TOKEN: ${{ steps.queue-token.outputs.token }}", text)
        self.assertIn("--apply --receipt editorial-admission/receipt.json", text)

    def test_verified_receipt_seals_replay_and_no_duplicate_publication(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("ERDOS-COMPENDIUM-EDITORIAL-ADMISSION/1", text)
        self.assertIn("gcl-council-clerk[bot]", text)
        self.assertIn("already_admitted=true", text)
        self.assertGreaterEqual(text.count("steps.editorial-admit.outputs.already_admitted != 'true'"), 2)
        self.assertIn("no work-state replay", text)

    def test_live_jq_seal_expression_matches_actual_clerk_receipt(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        start = "          if jq -e '"
        anchor = 'any(.[]; .user.login == "gcl-council-clerk[bot]"'
        pos = text.index(start + anchor)
        finish = text.index("' " + chr(92) + "\n", pos)
        expr = text[pos + len(start):finish]
        success = (
            "ERDOS-COMPENDIUM-EDITORIAL-ADMISSION/1\\n\\n"
            "Three Editorial writing assignments #2556–#2558: **VERIFIED**.\\n"
            "Protected Programme SHA: `85127e1f4d64e4f5d771921807e650e967c75fd1`"
        )
        blocked = (
            "ERDOS-COMPENDIUM-EDITORIAL-ADMISSION/1\\n\\n"
            "Three Editorial writing assignments #2556–#2558: **BLOCKED / UNVERIFIED**."
        )
        def run(rows):
            proc = subprocess.run(
                ["jq", "-e", expr], input=json.dumps(rows),
                text=True, capture_output=True, check=False
            )
            self.assertNotIn("compile error", proc.stderr)
            return proc.returncode
        self.assertEqual(run([
            {"user": {"login": "gcl-council-clerk[bot]"}, "body": blocked},
            {"user": {"login": "gcl-council-clerk[bot]"}, "body": success}
        ]), 0)
        self.assertEqual(run([
            {"user": {"login": "gcl-council-clerk[bot]"}, "body": blocked}
        ]), 1)
        self.assertEqual(run([
            {"user": {"login": "untrusted-user"}, "body": success}
        ]), 1)

    def test_source_and_worker_authority_boundaries_unchanged(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("python ci/test_erdos_compendium_editorial_activate.py", text)
        self.assertIn("python ci/erdos_compendium_editorial_activate.py", text)
        self.assertNotIn("gh issue comment 2556", text)
        self.assertNotIn("gh issue comment 2557", text)
        self.assertNotIn("gh issue comment 2558", text)


if __name__ == "__main__":
    unittest.main()
