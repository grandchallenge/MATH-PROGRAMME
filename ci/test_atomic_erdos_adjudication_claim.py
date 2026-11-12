"""Mocked state-machine regression tests; no live issue mutations."""
import contextlib
import importlib.util
import io
import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "claim", Path(__file__).with_name("atomic_erdos_adjudication_claim.py"))
claim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(claim)

class ClaimTests(unittest.TestCase):
    def run_cli(self, args, api, comments=lambda n: ([], 1)):
        out = io.StringIO()
        with patch.object(sys, "argv", ["claim"] + args), \
             patch.object(claim, "api", side_effect=api), \
             patch.object(claim, "comments", side_effect=comments), \
             contextlib.redirect_stdout(out):
            status = claim.main()
        return status, json.loads(out.getvalue())

    def test_preexisting_adjudication_never_creates_ref(self):
        calls = []
        def api(method, path, fields=None):
            calls.append((method, path))
            return {"state": "open"}
        comments = lambda n: ([{"id": 11, "body": "Source-critical adjudication"}], 1)
        status, output = self.run_cli(["acquire", "1495"], api, comments)
        self.assertEqual(status, 3)
        self.assertEqual(output["result"], "ALREADY_ADJUDICATED")
        self.assertFalse(any(m == "POST" for m, _ in calls))

    def test_release_wrong_sha_preserves_ref(self):
        calls = []
        def api(method, path, fields=None):
            calls.append(method)
            return {"object": {"sha": "actual"}}
        with self.assertRaisesRegex(RuntimeError, "mismatch"):
            self.run_cli(["release", "1495", "--claim-sha", "wrong"], api)
        self.assertNotIn("DELETE", calls)

    def test_inspect_closed_issue_still_reads_ref(self):
        status, output = self.run_cli(["inspect", "1495"],
            lambda method, path, fields=None: {"object": {"sha": "abc"}})
        self.assertEqual((status, output["result"]), (0, "HELD"))

    def test_ref_conflict_is_non_authorizing(self):
        def api(method, path, fields=None):
            if path.startswith("issues/"):
                return {"state": "open"}
            if path == "git/ref/heads/main":
                return {"object": {"sha": "mainsha"}}
            if path == "git/commits/mainsha":
                return {"tree": {"sha": "treesha"}}
            if path == "git/commits":
                return {"sha": "claimsha"}
            if path == "git/refs":
                raise RuntimeError("HTTP 422 reference already exists")
            raise AssertionError((method, path))
        import subprocess
        with patch.object(claim.subprocess, "run",
                          return_value=subprocess.CompletedProcess([], 0, "tester", "")):
            status, output = self.run_cli(["acquire", "1496"], api)
        self.assertEqual((status, output["result"]), (4, "NOT_ACQUIRED"))

if __name__ == "__main__":
    unittest.main()
