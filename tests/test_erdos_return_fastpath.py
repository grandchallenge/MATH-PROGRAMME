import copy
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ci import erdos_return_fastpath as fast


class FastPath(unittest.TestCase):
    def setUp(self):
        self.repo = fast.REPO
        self.cid = 812345
        self.n = 2096
        self.issue = {"number": self.n, "state": "open", "title": "GCL", "body": "bound"}
        self.body = "RESULT/1\nsome text\n"
        self.comment = {"id": self.cid, "body": self.body,
                        "issue_url": f"https://api.github.com/repos/{self.repo}/issues/{self.n}",
                        "user": {"id": 12, "login": "worker"}}
        self.event = {"action": "created", "repository": {"full_name": self.repo},
                      "issue": {"number": self.n}, "comment": copy.deepcopy(self.comment)}
        self.env = {"GITHUB_ACTIONS": "true", "GITHUB_REPOSITORY": self.repo,
                    "GITHUB_REF": "refs/heads/main", "GITHUB_EVENT_NAME": "issue_comment",
                    "GITHUB_SHA": "f" * 40, "GITHUB_RUN_ID": "123",
                    "GH_TOKEN": "TEST", "GCL_RETURN_FASTPATH_CONTROL": "protected-main"}
        self.row = {"issue_number": self.n, "comment_id": self.cid,
                    "problem_id": 825, "task_id": "ERDOS-CATALOGUE-0825-S01",
                    "validation": "STRUCTURALLY_VALID_UNADJUDICATED",
                    "comment_body_sha256": hashlib.sha256(self.body.encode()).hexdigest()}

    def test_source_read_timeout_recovered_once(self):
        import subprocess
        success = subprocess.CompletedProcess(["gh"], 0, '{"ok": true}', "")
        with patch.object(fast.subprocess, "run", side_effect=[
            subprocess.TimeoutExpired("gh", 60), success]) as run:
            self.assertEqual(fast.api("repos/example"), {"ok": True})
        self.assertEqual(run.call_count, 2)

    def test_source_read_second_timeout_propagates(self):
        import subprocess
        with patch.object(fast.subprocess, "run", side_effect=subprocess.TimeoutExpired("gh", 60)) as run:
            with self.assertRaises(subprocess.TimeoutExpired):
                fast.api("repos/example")
        self.assertEqual(run.call_count, 2)

    def test_explicit_denial_is_not_retried(self):
        import subprocess
        denial = subprocess.CompletedProcess(["gh"], 1, "", "HTTP 403: forbidden")
        with patch.object(fast.subprocess, "run", return_value=denial) as run:
            with self.assertRaisesRegex(RuntimeError, "403"):
                fast.api("repos/example")
        self.assertEqual(run.call_count, 1)

    def test_malformed_success_does_not_retry_or_fabricate_evidence(self):
        import subprocess
        bad = subprocess.CompletedProcess(["gh"], 0, "{bad", "")
        with patch.object(fast.subprocess, "run", return_value=bad) as run:
            with self.assertRaises(json.JSONDecodeError):
                fast.api("repos/example")
        self.assertEqual(run.call_count, 1)

    def setup_capture(self, directory, comments=None, row=None):
        path = Path(directory) / "event.json"
        path.write_text(json.dumps(self.event))
        comments = comments if comments is not None else [self.comment]
        row = row if row is not None else self.row
        def api(endpoint):
            if endpoint.endswith(f"/issues/{self.n}"):
                return self.issue
            if endpoint.endswith(f"/comments/{self.cid}"):
                return self.comment
            if endpoint.endswith(f"/issues/{self.n}/comments?per_page=100"):
                return comments
            raise AssertionError(endpoint)
        fake_registry = {"registry_id": "test-registry", "issues": [
            {"issue_number": self.n, "problem_id": 825}]}
        return path, api, fake_registry, row

    def capture_with(self, directory, **kwargs):
        event, api, registry, row = self.setup_capture(directory, **kwargs)
        with patch.dict(os.environ, self.env), patch.object(fast, "api", side_effect=api), \
             patch.object(fast.intake, "load_registry", return_value=registry), \
             patch.object(fast.intake, "capture", return_value=(row, self.body)):
            return fast.capture(event, Path(directory)), event

    def test_one_valid_captures_only_the_target_issue(self):
        with tempfile.TemporaryDirectory() as d:
            result, _ = self.capture_with(d)
            self.assertEqual(result["comment_id"], self.cid)
            self.assertEqual(result["issue"], self.n)
            self.assertEqual(json.loads((Path(d)/"REPORT.json").read_text())["tasks"][0]
                             ["structurally_valid_returns"], 1)
            self.assertFalse(result["mathematical_certification"])

    def test_lost_or_edited_event_refuses_reconciliation(self):
        with tempfile.TemporaryDirectory() as d:
            self.event["comment"]["body"] = "RESULT/1\nolder body\n"
            with self.assertRaisesRegex(ValueError, "superseded"):
                self.capture_with(d)

    def test_invalid_comment_stays_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            bad = dict(self.row, validation="REJECTED", errors=["missing section"])
            with self.assertRaisesRegex(ValueError, "invalid incoming"):
                self.capture_with(d, row=bad)

    def test_competing_valid_returns_remain_unadjudicated(self):
        with tempfile.TemporaryDirectory() as d:
            other = dict(self.comment, id=812346, body="RESULT/1\nindependent\n")
            otherrow = dict(self.row, comment_id=812346,
                comment_body_sha256=hashlib.sha256(other["body"].encode()).hexdigest())
            path, api, registry, row = self.setup_capture(d, comments=[self.comment, other])
            def capture(ev, unused):
                return (row if ev["comment"]["id"] == self.cid else otherrow), ""
            with patch.dict(os.environ, self.env), patch.object(fast, "api", side_effect=api), \
                 patch.object(fast.intake, "load_registry", return_value=registry), \
                 patch.object(fast.intake, "capture", side_effect=capture):
                with self.assertRaisesRegex(ValueError, "arbitration missing"):
                    fast.capture(path, Path(d))

    def test_apply_returns_only_readback_verified_result(self):
        with tempfile.TemporaryDirectory() as d:
            bound, event = self.capture_with(d)
            item = {"target": "RETURNED", "verified_status": "RETURNED",
                    "verified_gcl_state": "RETURNED", "available_removed": True}
            receipt = {"status": "VERIFIED", "verified": True, "complete": True,
                       "blocker": None, "results": [item]}
            with patch.dict(os.environ, self.env), patch.object(
                 fast.project, "project_source_returns", return_value=(receipt, 0)) as invoke:
                result = fast.apply(event, Path(d))
            self.assertEqual(result["status"], "VERIFIED")
            self.assertFalse(result["source_semantics_accepted"])
            self.assertEqual(invoke.call_args.kwargs["issues"] if "issues" in invoke.call_args.kwargs
                             else invoke.call_args.args[1], [self.n])

    def test_changed_snapshot_or_privileges_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            bound, event = self.capture_with(d)
            (Path(d)/"REPORT.json").write_text("{}")
            with patch.dict(os.environ, self.env):
                with self.assertRaisesRegex(ValueError, "binding failed"):
                    fast.apply(event, Path(d))
            (Path(d)/"REPORT.json").write_text("{}")
            with patch.dict(os.environ, {**self.env, "GCL_RETURN_FASTPATH_CONTROL": ""}):
                with self.assertRaisesRegex(ValueError, "binding failed"):
                    fast.apply(event, Path(d))

    def test_projector_failure_does_not_claim_success(self):
        with tempfile.TemporaryDirectory() as d:
            _, event = self.capture_with(d)
            receipt = {"verified": False, "complete": False, "blocker": "source changed"}
            with patch.dict(os.environ, self.env), patch.object(
                 fast.project, "project_source_returns", return_value=(receipt, 1)):
                with self.assertRaisesRegex(ValueError, "source changed"):
                    fast.apply(event, Path(d))


if __name__ == "__main__":
    unittest.main()
