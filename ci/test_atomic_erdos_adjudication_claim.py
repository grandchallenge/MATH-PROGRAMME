"""Mocked state-machine regression tests; no live issue mutations."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location(
    "claim", Path(__file__).with_name("atomic_erdos_adjudication_claim.py")
)
claim = importlib.util.module_from_spec(spec)
spec.loader.exec_module(claim)


class FakeGitHub:
    """In-memory mock of GitHub issue, comment, and git-ref state."""

    def __init__(self, *, issue_state="open", initial_comments=None, existing_ref_sha=None):
        self.issue_state = issue_state
        self.comments_list = list(initial_comments or [])
        self.ref_sha = existing_ref_sha
        self.calls = []
        self.fail_create_ref = None
        self.fail_delete_ref = None
        self.fail_comments_on_call = None
        self.comments_calls = 0
        self.inject_comment_after_acquire = None
        self.swap_ref_before_release_to = None
        self.commit_counter = 0

    def api(self, method, path, fields=None):
        self.calls.append((method, path, fields))
        if method == "GET" and path.startswith("issues/"):
            return {"state": self.issue_state}
        if method == "GET" and path == "git/ref/heads/main":
            return {"object": {"sha": "mainsha000"}}
        if method == "GET" and path == "git/commits/mainsha000":
            return {"tree": {"sha": "treesha000"}}
        if method == "POST" and path == "git/commits":
            self.commit_counter += 1
            return {"sha": f"claimsha{self.commit_counter:03d}"}
        if method == "POST" and path == "git/refs":
            if self.fail_create_ref is not None:
                raise RuntimeError(self.fail_create_ref)
            if self.ref_sha is not None:
                raise RuntimeError("HTTP 422 Reference already exists")
            self.ref_sha = fields["sha"]
            if self.inject_comment_after_acquire is not None:
                self.comments_list.append(self.inject_comment_after_acquire)
            return {"ref": fields["ref"], "object": {"sha": self.ref_sha}}
        if method == "GET" and path.startswith("git/ref/heads/gcl-adjudication-claims/"):
            if self.swap_ref_before_release_to is not None and any(
                m == "POST" and p == "git/refs" for m, p, _ in self.calls
            ):
                # Swap only after the initial post-acquisition verification GET.
                get_ref_count = sum(
                    1
                    for m, p, _ in self.calls
                    if m == "GET" and p.startswith("git/ref/heads/gcl-adjudication-claims/")
                )
                if get_ref_count >= 2:
                    self.ref_sha = self.swap_ref_before_release_to
            if self.ref_sha is None:
                raise RuntimeError("HTTP 404 Not Found")
            return {"object": {"sha": self.ref_sha}}
        if method == "DELETE" and path.startswith("git/refs/heads/gcl-adjudication-claims/"):
            if self.fail_delete_ref is not None:
                raise RuntimeError(self.fail_delete_ref)
            self.ref_sha = None
            return {}
        raise AssertionError(f"unexpected api call: {(method, path, fields)}")

    def comments(self, issue):
        self.comments_calls += 1
        if self.fail_comments_on_call == self.comments_calls:
            raise RuntimeError("HTTP 502 Bad Gateway during comment readback")
        return list(self.comments_list), 1


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

    def test_cohort_other_assignment_does_not_block(self):
        comments = [
            {
                "id": 11,
                "body": "SOURCE-CRITICAL ADJUDICATION/1\nASSIGNMENT_ID: ERDOS-PV-0003-A",
            }
        ]
        self.assertEqual(claim.adjudications(comments, "ERDOS-PV-0004-A"), [])
        self.assertEqual(claim.adjudications(comments, "ERDOS-PV-0003-A")[0]["id"], 11)

    def test_cohort_ambiguous_adjudication_blocks(self):
        comments = [{"id": 12, "body": "SOURCE-CRITICAL ADJUDICATION/1"}]
        self.assertEqual(claim.adjudications(comments, "ERDOS-PV-0004-A")[0]["id"], 12)

    def test_invalid_assignment_id_rejected(self):
        with self.assertRaises(ValueError):
            claim.adjudications([], "../../evil")

    def test_release_wrong_sha_preserves_ref(self):
        calls = []

        def api(method, path, fields=None):
            calls.append(method)
            return {"object": {"sha": "actual"}}

        with self.assertRaisesRegex(RuntimeError, "mismatch"):
            self.run_cli(["release", "1495", "--claim-sha", "wrong"], api)
        self.assertNotIn("DELETE", calls)

    def test_inspect_closed_issue_still_reads_ref(self):
        status, output = self.run_cli(
            ["inspect", "1495"],
            lambda method, path, fields=None: {"object": {"sha": "abc"}},
        )
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

        with patch.object(
            claim.subprocess,
            "run",
            return_value=subprocess.CompletedProcess([], 0, "tester", ""),
        ):
            status, output = self.run_cli(["acquire", "1496"], api)
        self.assertEqual((status, output["result"]), (4, "NOT_ACQUIRED"))


class GuardedLifecycleTests(unittest.TestCase):
    def _run_guarded(self, gh, worker_fn, *, issue=1500, assignment_id=None, cp_path=None):
        if cp_path is None:
            tmp = tempfile.TemporaryDirectory()
            self.addCleanup(tmp.cleanup)
            cp_path = Path(tmp.name) / f"claim-{issue}.json"
        with patch.object(claim, "api", side_effect=gh.api), \
             patch.object(claim, "comments", side_effect=gh.comments), \
             patch.object(claim, "current_actor", return_value="fyremael"):
            status, summary = claim.guarded_claim_run(
                issue,
                cp_path,
                worker_fn,
                assignment_id=assignment_id,
                worker_id="worker-test-01",
            )
        return status, summary, claim.read_checkpoint(cp_path), cp_path

    def test_successful_adjudication_readback_releases_own_claim(self):
        gh = FakeGitHub()

        def worker(ctx):
            self.assertEqual(ctx["claim_sha"], "claimsha001")
            gh.comments_list.append(
                {
                    "id": 9001,
                    "html_url": "https://example.invalid/c/9001",
                    "body": "SOURCE-CRITICAL ADJUDICATION/1\nASSIGNMENT_ID: ERDOS-PV-0010-A",
                }
            )
            return 0

        status, summary, cp, _ = self._run_guarded(
            gh, worker, assignment_id="ERDOS-PV-0010-A"
        )
        self.assertEqual(status, claim.EXIT_OK)
        self.assertEqual(summary["result"], "ADJUDICATED_AND_RELEASED")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_SUBSTANTIVE)
        self.assertEqual(summary["new_adjudication_comments"][0]["id"], 9001)
        self.assertEqual(summary["release_status"], "RELEASED")
        self.assertFalse(summary["claim_still_held"])
        self.assertIsNone(gh.ref_sha)
        self.assertEqual(cp["phase"], "CLOSED")
        self.assertEqual(cp["claim_sha"], "claimsha001")
        self.assertIsNone(cp["abort_reason"])

    def test_read_only_completion_records_explicit_abort_and_releases(self):
        gh = FakeGitHub()
        status, summary, cp, _ = self._run_guarded(gh, lambda ctx: 0)
        self.assertEqual(status, claim.EXIT_OK)
        self.assertEqual(summary["result"], "READ_ONLY_AND_RELEASED")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_READ_ONLY)
        self.assertEqual(summary["abort_reason"], "no_adjudication_posted_read_only")
        self.assertEqual(summary["release_status"], "RELEASED")
        self.assertFalse(summary["claim_still_held"])
        self.assertIsNone(gh.ref_sha)
        self.assertEqual(cp["phase"], "CLOSED")

    def test_interrupted_operation_reconciles_and_releases_own_claim(self):
        gh = FakeGitHub()

        def interrupted_worker(ctx):
            raise KeyboardInterrupt("SIGTERM")

        status, summary, cp, _ = self._run_guarded(gh, interrupted_worker)
        self.assertEqual(status, claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(summary["result"], "INTERRUPTED_AND_RELEASED")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertIn("interrupted_before_adjudication", summary["abort_reason"])
        self.assertEqual(summary["release_status"], "RELEASED")
        self.assertFalse(summary["claim_still_held"])
        self.assertIsNone(gh.ref_sha)
        self.assertEqual(cp["phase"], "CLOSED")

    def test_interrupted_after_posting_preserves_readback_and_failed_closure(self):
        gh = FakeGitHub()

        def interrupted_after_post(ctx):
            gh.comments_list.append({"id": 9002, "body": "SOURCE-CRITICAL ADJUDICATION/1"})
            raise KeyboardInterrupt("SIGTERM")

        status, summary, cp, _ = self._run_guarded(gh, interrupted_after_post)
        self.assertEqual(status, claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertEqual(summary["new_adjudication_comments"][0]["id"], 9002)
        self.assertIn("interrupted_after_readback", summary["abort_reason"])
        self.assertEqual(summary["release_status"], "RELEASED")
        self.assertIsNone(gh.ref_sha)
        self.assertEqual(cp["phase"], "CLOSED")

    def test_release_error_holds_checkpoint_for_recovery(self):
        gh = FakeGitHub()
        gh.fail_delete_ref = "HTTP 500 Internal Server Error"
        status, summary, cp, _ = self._run_guarded(gh, lambda ctx: 0)
        self.assertEqual(status, claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(summary["result"], "RELEASE_ERROR")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertTrue(summary["claim_still_held"])
        self.assertIn("HTTP 500", summary["release_error"])
        self.assertEqual(cp["phase"], "HELD_PENDING_RECOVERY")
        self.assertTrue(cp["claim_still_held"])
        self.assertEqual(gh.ref_sha, "claimsha001")

    def test_readback_error_refuses_blind_release(self):
        gh = FakeGitHub()
        # Call 1 = pre-acquire comments; Call 2 = post-acquire duplicate check; Call 3 = finally readback
        gh.fail_comments_on_call = 3
        status, summary, cp, _ = self._run_guarded(gh, lambda ctx: 0)
        self.assertEqual(status, claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(summary["result"], "HELD_AMBIGUOUS")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertTrue(summary["claim_still_held"])
        self.assertEqual(gh.ref_sha, "claimsha001")
        self.assertFalse(any(m == "DELETE" for m, _, _ in gh.calls))
        self.assertEqual(cp["phase"], "HELD_PENDING_RECOVERY")

    def test_concurrent_422_is_exclusive_claim_block(self):
        gh = FakeGitHub(existing_ref_sha="otherownersha")
        worker_called = False

        def worker(ctx):
            nonlocal worker_called
            worker_called = True
            return 0

        status, summary, cp, _ = self._run_guarded(gh, worker)
        self.assertEqual(status, claim.EXIT_NOT_ACQUIRED)
        self.assertEqual(summary["result"], "NOT_ACQUIRED")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_EXCLUSIVE_BLOCK)
        self.assertFalse(worker_called)
        self.assertFalse(summary["claim_still_held"])
        self.assertEqual(gh.ref_sha, "otherownersha")
        self.assertFalse(any(m == "DELETE" for m, _, _ in gh.calls))
        self.assertEqual(cp["phase"], "CLOSED")

    def test_ambiguous_create_ref_error_holds_checkpoint_without_retry(self):
        gh = FakeGitHub()
        gh.fail_create_ref = "HTTP 502 Bad Gateway"
        status, summary, cp, _ = self._run_guarded(gh, lambda ctx: 0)
        self.assertEqual(status, claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(summary["result"], "AMBIGUOUS_CREATE_REF_HOLD")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertTrue(summary["claim_still_held"])
        self.assertEqual(cp["phase"], "HELD_PENDING_RECOVERY")
        self.assertEqual(cp["claim_sha"], "claimsha001")

    def test_existing_adjudication_pre_acquire_is_read_only_without_ref(self):
        gh = FakeGitHub(
            initial_comments=[{"id": 77, "body": "SOURCE-CRITICAL ADJUDICATION/1"}]
        )
        status, summary, cp, _ = self._run_guarded(gh, lambda ctx: 0)
        self.assertEqual(status, claim.EXIT_ALREADY_ADJUDICATED)
        self.assertEqual(summary["result"], "ALREADY_ADJUDICATED")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_READ_ONLY)
        self.assertFalse(any(m == "POST" for m, _, _ in gh.calls))
        self.assertEqual(cp["phase"], "CLOSED")

    def test_existing_adjudication_post_acquire_race_releases_own_ref(self):
        gh = FakeGitHub()
        gh.inject_comment_after_acquire = {
            "id": 88,
            "body": "SOURCE-CRITICAL ADJUDICATION/1",
        }
        worker_called = False

        def worker(ctx):
            nonlocal worker_called
            worker_called = True
            return 0

        status, summary, cp, _ = self._run_guarded(gh, worker)
        self.assertEqual(status, claim.EXIT_ABORT_EXISTING)
        self.assertEqual(summary["result"], "ABORT_EXISTING_RELEASED")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_READ_ONLY)
        self.assertFalse(worker_called)
        self.assertIsNone(gh.ref_sha)
        self.assertEqual(cp["phase"], "CLOSED")

    def test_stale_custody_checkpoint_blocks_new_run_without_api_calls(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        cp_path = Path(tmp.name) / "stale.json"
        claim.write_checkpoint(
            cp_path,
            {
                "schema_version": claim.CHECKPOINT_SCHEMA,
                "issue": 1500,
                "claim_sha": "strandedsha999",
                "worker_id": "prior-worker",
                "phase": "EXECUTING",
                "claim_still_held": True,
            },
        )
        gh = FakeGitHub(existing_ref_sha="strandedsha999")
        status, summary, cp, _ = self._run_guarded(gh, lambda ctx: 0, cp_path=cp_path)
        self.assertEqual(status, claim.EXIT_STALE_CUSTODY_HOLD)
        self.assertEqual(summary["result"], "STALE_CUSTODY_HOLD")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertEqual(summary["existing_claim_sha"], "strandedsha999")
        self.assertEqual(gh.calls, [])
        self.assertEqual(cp["claim_sha"], "strandedsha999")
        self.assertEqual(cp["phase"], "EXECUTING")

    def test_stale_custody_sha_mismatch_in_finally_refuses_delete(self):
        gh = FakeGitHub()
        gh.swap_ref_before_release_to = "foreignownersha"
        status, summary, cp, _ = self._run_guarded(gh, lambda ctx: 0)
        self.assertEqual(status, claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(summary["result"], "HELD_STALE_CUSTODY")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertTrue(summary["claim_still_held"])
        self.assertEqual(gh.ref_sha, "foreignownersha")
        self.assertFalse(any(m == "DELETE" for m, _, _ in gh.calls))
        self.assertEqual(cp["phase"], "HELD_PENDING_RECOVERY")

    def test_recover_inspects_and_releases_only_matching_sha(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        cp_path = Path(tmp.name) / "crashed.json"
        claim.write_checkpoint(
            cp_path,
            {
                "schema_version": claim.CHECKPOINT_SCHEMA,
                "issue": 1505,
                "assignment_id": None,
                "claim_sha": "ownedsha123",
                "worker_id": "crashed-worker",
                "phase": "EXECUTING",
                "adjudication_comments_before": [],
                "claim_still_held": True,
            },
        )
        # 1. Mismatched live SHA must refuse release (no claim stealing).
        gh_mismatch = FakeGitHub(existing_ref_sha="someoneelsesha")
        with patch.object(claim, "api", side_effect=gh_mismatch.api), \
             patch.object(claim, "comments", side_effect=gh_mismatch.comments):
            st, res = claim.recover_checkpoint(
                1505, cp_path, release_owned=True, abort_reason="killed"
            )
        self.assertEqual(st, claim.EXIT_STALE_CUSTODY_HOLD)
        self.assertEqual(res["result"], "STALE_CUSTODY_SHA_MISMATCH")
        self.assertEqual(gh_mismatch.ref_sha, "someoneelsesha")
        self.assertFalse(any(m == "DELETE" for m, _, _ in gh_mismatch.calls))

        # 2. Matching live SHA without --release-owned stays held (inspect-only).
        gh_owned = FakeGitHub(existing_ref_sha="ownedsha123")
        with patch.object(claim, "api", side_effect=gh_owned.api), \
             patch.object(claim, "comments", side_effect=gh_owned.comments):
            st, res = claim.recover_checkpoint(1505, cp_path, release_owned=False)
        self.assertEqual(st, claim.EXIT_STALE_CUSTODY_HOLD)
        self.assertEqual(res["result"], "HELD_BY_CHECKPOINT_OWNER")
        self.assertEqual(gh_owned.ref_sha, "ownedsha123")

        # 3. Matching live SHA with --release-owned + --abort-reason releases cleanly.
        with patch.object(claim, "api", side_effect=gh_owned.api), \
             patch.object(claim, "comments", side_effect=gh_owned.comments):
            st, res = claim.recover_checkpoint(
                1505, cp_path, release_owned=True, abort_reason="worker_killed_sigkill"
            )
        self.assertEqual(st, claim.EXIT_OK)
        self.assertEqual(res["result"], "RECOVERED_AND_RELEASED")
        self.assertEqual(res["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertFalse(res["claim_still_held"])
        self.assertIsNone(gh_owned.ref_sha)
        final_cp = claim.read_checkpoint(cp_path)
        self.assertEqual(final_cp["phase"], "CLOSED")
        self.assertFalse(final_cp["claim_still_held"])

    def test_worker_nonzero_exit_records_failed_closure_and_releases_own_claim(self):
        gh = FakeGitHub()
        status, summary, cp, _ = self._run_guarded(gh, lambda ctx: 2)
        self.assertEqual(status, claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(summary["result"], "FAILED_AND_RELEASED")
        self.assertEqual(summary["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertEqual(summary["abort_reason"], "worker_nonzero_exit: 2")
        self.assertEqual(summary["release_status"], "RELEASED")
        self.assertFalse(summary["claim_still_held"])
        self.assertIsNone(gh.ref_sha)
        self.assertEqual(cp["phase"], "CLOSED")

    def test_recover_requires_abort_reason_without_new_adjudication(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        cp_path = Path(tmp.name) / "no-reason.json"
        claim.write_checkpoint(
            cp_path,
            {
                "schema_version": claim.CHECKPOINT_SCHEMA,
                "issue": 1506,
                "claim_sha": "ownedsha456",
                "phase": "EXECUTING",
                "adjudication_comments_before": [],
                "claim_still_held": True,
            },
        )
        gh = FakeGitHub(existing_ref_sha="ownedsha456")
        with patch.object(claim, "api", side_effect=gh.api), \
             patch.object(claim, "comments", side_effect=gh.comments):
            with self.assertRaisesRegex(ValueError, "--abort-reason"):
                claim.recover_checkpoint(1506, cp_path, release_owned=True)
        self.assertEqual(gh.ref_sha, "ownedsha456")
        self.assertFalse(any(m == "DELETE" for m, _, _ in gh.calls))

    def test_recover_unclaimed_ambiguous_checkpoint_preserves_failed_closure(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        cp_path = Path(tmp.name) / "ambig.json"
        claim.write_checkpoint(
            cp_path,
            {
                "schema_version": claim.CHECKPOINT_SCHEMA,
                "issue": 1507,
                "claim_sha": "ambigsha789",
                "phase": "HELD_PENDING_RECOVERY",
                "outcome_class": claim.OUTCOME_FAILED_CLOSURE,
                "adjudication_comments_before": [],
                "claim_still_held": True,
            },
        )
        gh = FakeGitHub(existing_ref_sha=None)
        with patch.object(claim, "api", side_effect=gh.api), \
             patch.object(claim, "comments", side_effect=gh.comments):
            st, res = claim.recover_checkpoint(1507, cp_path)
        self.assertEqual(st, claim.EXIT_OK)
        self.assertEqual(res["result"], "RECOVERED_ALREADY_UNCLAIMED")
        self.assertEqual(res["outcome_class"], claim.OUTCOME_FAILED_CLOSURE)
        self.assertFalse(res["claim_still_held"])

    def test_cli_run_subcommand_invokes_worker_with_claim_env(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        cp_path = Path(tmp.name) / "cli-run.json"
        gh = FakeGitHub()
        seen_env = {}

        def fake_worker_cmd(command, env_extra):
            seen_env.update(env_extra)
            self.assertEqual(command, ["echo", "ok"])
            gh.comments_list.append({"id": 9999, "body": "SOURCE-CRITICAL ADJUDICATION/1"})
            return 0

        out = io.StringIO()
        with patch.object(
            sys,
            "argv",
            ["claim", "run", "1510", "--checkpoint", str(cp_path), "--", "echo", "ok"],
        ), patch.object(claim, "api", side_effect=gh.api), \
             patch.object(claim, "comments", side_effect=gh.comments), \
             patch.object(claim, "current_actor", return_value="fyremael"), \
             patch.object(claim, "run_worker_command", side_effect=fake_worker_cmd), \
             contextlib.redirect_stdout(out):
            status = claim.main()
        payload = json.loads(out.getvalue())
        self.assertEqual(status, claim.EXIT_OK)
        self.assertEqual(payload["outcome_class"], claim.OUTCOME_SUBSTANTIVE)
        self.assertEqual(seen_env["GCL_CLAIM_ISSUE"], 1510)
        self.assertEqual(seen_env["GCL_CLAIM_SHA"], "claimsha001")
        self.assertIsNone(gh.ref_sha)



class ContinuationTests(unittest.TestCase):
    def setUp(self):
        import erdos_catalogue_programme_intake as intake
        self.b = dict(claim.CONTINUATIONS[2274])
        b = self.b
        self.issue = {"number": 2274, "state": "open", "body": "pinned source",
                      "title": "[GCL-ERDOS] ERDOS-CATALOGUE-1003-S01 — Problem 1003: fixture",
                      "labels": [{"name": n} for n in intake.LABELS]}
        old = "RESULT/1\nASSIGNMENT_ID: ERDOS-CATALOGUE-1003-S01\nDISPOSITION: PARTIAL\n\nHistorical"
        pred = ("SOURCE-CRITICAL ADJUDICATION/1\nASSIGNMENT_ID: ERDOS-CATALOGUE-1003-S01\n"
                f"ISSUE: 2274\nREVIEWED_RESULT_COMMENT: {b['old_result']}\n"
                f"DISPOSITION: {b['predecessor_disposition']}\n\nPartial review")
        new = ("RESULT/1\nASSIGNMENT_ID: ERDOS-CATALOGUE-1003-S01\nPROBLEM_ID: 1003\n"
               "DISPOSITION: BOUNDED_TASK_DESIGNED\nCONTEXT_CLASS: ZERO_CONTEXT\nTIMEBOX_OBSERVED: YES\n")
        new += "".join(f"\n## {section}\nSubstantive fixture\n" for section in intake.SECTIONS)
        self.items = [self.comment(b[k], body) for k, body in
                      (("old_result", old), ("predecessor", pred), ("new_result", new))]
        for k, body in (("old_result", old), ("predecessor", pred), ("new_result", new)):
            b[k + "_sha256"] = claim.digest(body)
        b["source_sha256"] = claim.digest(self.issue["body"])
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.dict(claim.CONTINUATIONS, {2274: b}))
        self.stack.enter_context(patch.object(intake, "load_registry", return_value={
            "issues": [{"issue_number": 2274, "problem_id": 1003,
                        "issue_body_sha256": b["source_sha256"]}]}))
        self.stack.enter_context(patch.object(claim, "current_actor", return_value=b["actor"]))
        self.stack.enter_context(patch.object(claim, "verify_protected_continuation_code"))
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cp = Path(self.tmp.name) / "continuation.json"
        self.gh = FakeGitHub(initial_comments=self.items)
        self.message = None
        self.post_mode = "success"
        self.stack.enter_context(patch.object(claim, "api", side_effect=self.api))
        self.stack.enter_context(patch.object(claim, "comments", side_effect=self.gh.comments))

    def comment(self, cid, body):
        return {"id": cid, "body": body, "user": {"login": self.b["actor"], "id": self.b["actor_id"]},
                "issue_url": f"https://api.github.com/repos/{claim.REPO}/issues/2274",
                "html_url": f"https://example.invalid/{cid}"}

    def api(self, method, path, fields=None):
        if method == "GET" and path == "issues/2274":
            return self.issue
        if method == "POST" and path == "git/commits":
            self.message = fields["message"]
        if method == "GET" and path == "git/commits/claimsha001":
            return {"message": self.message}
        if method == "POST" and path == "issues/2274/comments":
            self.gh.calls.append((method, path, fields))
            if self.post_mode != "no_ack_no_effect":
                self.gh.comments_list.append(self.comment(self.b["new_result"] + 1, fields["body"]))
            if self.post_mode != "success":
                raise KeyboardInterrupt("lost acknowledgement")
            return self.gh.comments_list[-1]
        return self.gh.api(method, path, fields)

    def run_cont(self):
        return claim.guarded_claim_run(2274, self.cp, None,
            assignment_id=self.b["assignment"], worker_id="fixture",
            continuation=self.b, continuation_prose="Bounded source design only; conjecture open.")

    def test_success_preserves_partial_and_blocks_duplicate(self):
        status, out = self.run_cont()
        self.assertEqual(status, claim.EXIT_OK)
        self.assertEqual(out["result"], "ADJUDICATED_AND_RELEASED")
        self.assertEqual(len(self.gh.comments_list), 4)
        self.assertEqual(self.gh.comments_list[:3], self.items)
        self.assertIn("SUPERSEDES_PARTIAL_ADJUDICATION", self.gh.comments_list[-1]["body"])
        self.assertIsNone(self.gh.ref_sha)
        self.cp = Path(self.tmp.name) / "second.json"
        status, out = self.run_cont()
        self.assertEqual((status, out["result"]), (claim.EXIT_INELIGIBLE, "CONTINUATION_REJECTED"))
        self.assertEqual(len(self.gh.comments_list), 4)

    def test_unadmitted_and_wrong_predecessor(self):
        for args in ((2275, self.b["assignment"], self.b["predecessor"], self.b["new_result"]),
                     (2274, self.b["assignment"], 1, self.b["new_result"]),
                     (2274, "WRONG", self.b["predecessor"], self.b["new_result"])):
            with self.assertRaises(ValueError):
                claim.continuation_binding(*args)

    def test_stale_edited_new_return_rejects_without_ref(self):
        self.gh.comments_list[-1] = dict(self.items[-1], body=self.items[-1]["body"] + "edited")
        status, out = self.run_cont()
        self.assertEqual((status, out["result"]), (claim.EXIT_INELIGIBLE, "CONTINUATION_REJECTED"))
        self.assertFalse(any(m == "POST" for m, _, _ in self.gh.calls))

    def test_unauthorized_actor_rejects_without_ref(self):
        with patch.object(claim, "current_actor", return_value="foreign"):
            self.assertEqual(self.run_cont()[0], claim.EXIT_INELIGIBLE)
        self.assertFalse(any(m == "POST" for m, _, _ in self.gh.calls))

    def test_concurrent_claim_cannot_post(self):
        self.gh.ref_sha = "foreign-claim"
        self.assertEqual(self.run_cont()[0], claim.EXIT_NOT_ACQUIRED)
        self.assertEqual(self.gh.ref_sha, "foreign-claim")
        self.assertFalse(any(m == "POST" and p.endswith("/comments") for m,p,_ in self.gh.calls))


    def test_competing_adjudication_after_acquire_holds_and_does_not_post(self):
        self.gh.inject_comment_after_acquire = self.comment(
            self.b["new_result"] + 1, "SOURCE-CRITICAL ADJUDICATION/1\nDISPOSITION: TERMINAL")
        self.assertEqual(self.run_cont()[0], claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(self.gh.ref_sha, "claimsha001")
        self.assertFalse(any(m == "POST" and p.endswith("/comments") for m,p,_ in self.gh.calls))

    def test_interrupted_post_with_exact_readback(self):
        self.post_mode = "lost_ack_after_effect"
        status, out = self.run_cont()
        self.assertEqual(status, claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(len(out["new_adjudication_comments"]), 1)
        self.assertIsNone(self.gh.ref_sha)
        status, recovered = claim.recover_checkpoint(2274, self.cp)
        self.assertEqual(status, claim.EXIT_OK)
        self.assertEqual(recovered["outcome_class"], claim.OUTCOME_SUBSTANTIVE)

    def test_interrupted_post_without_readback_holds_then_owned_recovery(self):
        self.post_mode = "no_ack_no_effect"
        self.assertEqual(self.run_cont()[0], claim.EXIT_FAILED_CLOSURE)
        self.assertEqual(self.gh.ref_sha, "claimsha001")
        with self.assertRaises(ValueError):
            claim.recover_checkpoint(2274, self.cp, release_owned=True)
        status, _ = claim.recover_checkpoint(2274, self.cp, release_owned=True,
                                              abort_reason="exact census confirms no terminal write")
        self.assertEqual(status, claim.EXIT_OK)
        self.assertIsNone(self.gh.ref_sha)

    def test_recovery_rejects_forged_terminal_and_edited_predecessor(self):
        self.post_mode = "no_ack_no_effect"
        self.run_cont()
        self.gh.comments_list.append(self.comment(self.b["new_result"]+1,
                                     "SOURCE-CRITICAL ADJUDICATION/1\nDISPOSITION: TERMINAL"))
        with self.assertRaises(ValueError):
            claim.recover_checkpoint(2274, self.cp, release_owned=True, abort_reason="abort")
        self.gh.comments_list.pop()
        self.gh.comments_list[1] = dict(self.items[1], body="edited")
        with self.assertRaises(ValueError):
            claim.recover_checkpoint(2274, self.cp, release_owned=True, abort_reason="abort")
        self.assertEqual(self.gh.ref_sha, "claimsha001")

    def test_stale_source_and_competing_return(self):
        self.issue["body"] += "changed"
        with self.assertRaises(ValueError):
            claim.continuation_census(2274, self.b, self.items, self.issue)
        self.issue["body"] = "pinned source"
        with self.assertRaises(ValueError):
            claim.continuation_census(2274, self.b,
                self.items + [self.comment(self.b["new_result"]+1, self.items[-1]["body"])], self.issue)

    def test_legacy_release_refuses_continuation(self):
        self.post_mode = "no_ack_no_effect"
        self.run_cont()
        with self.assertRaisesRegex(ValueError, "guarded recovery"):
            claim.main(["release", "2274", "--claim-sha", "claimsha001"])
        self.assertEqual(self.gh.ref_sha, "claimsha001")


if __name__ == "__main__":
    unittest.main()
