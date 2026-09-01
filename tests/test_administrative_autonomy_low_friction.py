from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import administrative_autonomy_low_friction as low


class FakeClient:
    def __init__(self):
        self.get_map = {}
        self.posts = []
        self.puts = []
        self.get_sequences = {}

    def get(self, path):
        seq = self.get_sequences.get(path)
        if seq:
            value = seq.pop(0)
            self.get_map[path] = value
            return copy.deepcopy(value)
        if path not in self.get_map:
            raise AssertionError(f"unexpected GET {path}")
        return copy.deepcopy(self.get_map[path])

    def post(self, path, payload):
        self.posts.append((path, copy.deepcopy(payload)))
        if path == "/graphql":
            return {
                "data": {
                    "markPullRequestReadyForReview": {
                        "pullRequest": {
                            "number": 7,
                            "isDraft": False,
                            "headRefOid": "a" * 40,
                        }
                    }
                }
            }
        return {"id": 99, "user": {"login": low.EXPECTED_REFEREE_LOGIN}}

    def put(self, path, payload):
        self.puts.append((path, copy.deepcopy(payload)))
        return {"merged": True, "message": "ok"}


class LowFrictionTests(unittest.TestCase):
    def setUp(self):
        self.control = low.load_json(low.CONTROL_PATH)
        errors = low.validate_control(self.control)
        self.assertEqual(errors, [])

    def pull(self, *, draft=False, head="a" * 40, branch="routine/low-friction/render-001", body=None, login="fyremael"):
        return {
            "number": 7,
            "state": "open",
            "draft": draft,
            "node_id": "PR_node",
            "body": body or "<!-- MP-ADMIN-LOW-FRICTION-001 -->\nRoutine rendering repair.",
            "user": {"login": login},
            "base": {"ref": "main"},
            "head": {
                "ref": branch,
                "sha": head,
                "repo": {"full_name": low.EXPECTED_REPOSITORY},
            },
        }

    def readme_file(self, old="docs/assets/a.png", new="https://raw.githubusercontent.com/x/a.png"):
        return {
            "filename": "README.md",
            "status": "modified",
            "additions": 1,
            "deletions": 1,
            "patch": (
                "@@ -1 +1 @@\n"
                f"-[![proof]({old})](governance/evidence/README.md)\n"
                f"+[![proof]({new})](governance/evidence/README.md)\n"
            ),
        }

    def asset_file(self, path="docs/assets/proof.png", status="added"):
        return {
            "filename": path,
            "status": status,
            "additions": 0,
            "deletions": 0,
            "patch": None,
        }

    def test_authorized_control_disables_redundant_steward_checkpoints(self):
        auth = self.control["authorization"]
        self.assertFalse(auth["intermediate_human_steward_checkpoint_required"])
        self.assertFalse(auth["terminal_exact_head_human_steward_checkpoint_required"])
        self.assertTrue(auth["bounded_terminal_admission_delegated"])

    def test_state_machine_exhausts_normal_path(self):
        trace = low.Trace(7)
        for state in (
            "CLASSIFIED",
            "CHECKS_PENDING",
            "REVIEW_READY",
            "REFEREE_DISPOSED",
            "STABILIZING",
            "MERGED",
            "READBACK_VERIFIED",
            "TERMINAL",
        ):
            trace.transition(state)
        self.assertEqual(trace.state, "TERMINAL")

    def test_state_machine_allows_repeated_behind_reentry(self):
        trace = low.Trace(7)
        trace.transition("CLASSIFIED")
        for _ in range(3):
            trace.transition("SYNC_REQUIRED")
            trace.transition("CLASSIFIED")
        trace.transition("CHECKS_PENDING")
        trace.transition("REVIEW_READY")
        trace.transition("REFEREE_DISPOSED")
        trace.transition("STABILIZING")
        trace.transition("CLASSIFIED")
        trace.transition("CHECKS_PENDING")
        self.assertEqual(trace.state, "CHECKS_PENDING")

    def test_state_machine_rejects_skip_to_merge(self):
        trace = low.Trace(7)
        with self.assertRaisesRegex(low.AutonomyError, "forbidden lifecycle transition"):
            trace.transition("MERGED")

    def test_classifier_accepts_exact_readme_render_repair(self):
        result = low.classify_pull(self.pull(), [self.readme_file()], self.control)
        self.assertEqual(result.changed_paths, ("README.md",))
        self.assertEqual(result.markdown_paths, ("README.md",))

    def test_classifier_accepts_png_asset_plus_link(self):
        result = low.classify_pull(
            self.pull(), [self.asset_file(), self.readme_file()], self.control
        )
        self.assertEqual(result.asset_paths, ("docs/assets/proof.png",))

    def test_classifier_rejects_prose_change(self):
        item = self.readme_file()
        item["patch"] = "@@ -1 +1 @@\n-old prose\n+new prose\n"
        with self.assertRaisesRegex(low.AutonomyError, "link/image-only"):
            low.classify_pull(self.pull(), [item], self.control)

    def test_classifier_rejects_control_plane_path(self):
        item = {
            "filename": ".github/workflows/x.yml",
            "status": "modified",
            "additions": 1,
            "deletions": 1,
            "patch": "@@ -1 +1 @@\n-a\n+b\n",
        }
        with self.assertRaisesRegex(low.AutonomyError, "forbidden path"):
            low.classify_pull(self.pull(), [item], self.control)

    def test_classifier_rejects_governance_path(self):
        item = {
            "filename": "governance/control.json",
            "status": "modified",
            "additions": 1,
            "deletions": 1,
            "patch": "@@ -1 +1 @@\n-a\n+b\n",
        }
        with self.assertRaisesRegex(low.AutonomyError, "forbidden path"):
            low.classify_pull(self.pull(), [item], self.control)

    def test_classifier_rejects_svg_asset(self):
        with self.assertRaisesRegex(low.AutonomyError, "unsupported"):
            low.classify_pull(self.pull(), [self.asset_file("docs/assets/proof.svg")], self.control)

    def test_classifier_rejects_asset_deletion(self):
        with self.assertRaisesRegex(low.AutonomyError, "deletion"):
            low.classify_pull(self.pull(), [self.asset_file(status="removed")], self.control)

    def test_classifier_rejects_missing_marker(self):
        with self.assertRaisesRegex(low.AutonomyError, "opt-in marker"):
            low.classify_pull(self.pull(body="ordinary PR"), [self.readme_file()], self.control)

    def test_classifier_rejects_foreign_branch(self):
        pull = self.pull()
        pull["head"]["repo"]["full_name"] = "someone/fork"
        with self.assertRaisesRegex(low.AutonomyError, "same-repository"):
            low.classify_pull(pull, [self.readme_file()], self.control)

    def test_classifier_rejects_wrong_namespace(self):
        with self.assertRaisesRegex(low.AutonomyError, "namespace"):
            low.classify_pull(
                self.pull(branch="docs/manual"), [self.readme_file()], self.control
            )

    def test_classifier_rejects_unknown_author(self):
        with self.assertRaisesRegex(low.AutonomyError, "allowlist"):
            low.classify_pull(
                self.pull(login="outside-contributor"), [self.readme_file()], self.control
            )

    def test_check_snapshot_green(self):
        runs = [
            {"name": "A", "status": "completed", "conclusion": "success", "started_at": "2"},
            {"name": "B", "status": "completed", "conclusion": "neutral", "started_at": "2"},
        ]
        state, observed = low.check_snapshot(runs, ["A", "B"], {"success", "neutral", "skipped"})
        self.assertEqual(state, "green")
        self.assertEqual(observed["A"], "success")

    def test_check_snapshot_pending_missing_context(self):
        state, observed = low.check_snapshot([], ["A"], {"success"})
        self.assertEqual(state, "pending")
        self.assertEqual(observed["A"], "missing")

    def test_check_snapshot_failure(self):
        runs = [{"name": "A", "status": "completed", "conclusion": "failure", "started_at": "2"}]
        state, _ = low.check_snapshot(runs, ["A"], {"success"})
        self.assertEqual(state, "failed")

    def test_mark_ready_is_exact_head_bound(self):
        client = FakeClient()
        low.mark_ready(client, self.pull(draft=True), "a" * 40)
        self.assertEqual(client.posts[0][0], "/graphql")

    def test_referee_disposition_is_idempotent_for_same_head(self):
        client = FakeClient()
        path = f"/repos/{low.EXPECTED_REPOSITORY}/issues/7/comments?per_page=100"
        existing = {
            "id": 42,
            "user": {"login": low.EXPECTED_REFEREE_LOGIN},
            "body": (
                f"{low.REFEREE_PREFIX}\n\n- exact head: `{'a'*40}`;\n"
                "Disposition: `LOW_FRICTION_ROUTINE_EXPECTED_HEAD_PROTECTED_MERGE`."
            ),
        }
        client.get_map[path] = [existing]
        classification = low.classify_pull(self.pull(), [self.readme_file()], self.control)
        found = low.record_referee_disposition(
            client, classification, {"A": "success"}, low.EXPECTED_REFEREE_LOGIN
        )
        self.assertEqual(found["id"], 42)
        self.assertEqual(client.posts, [])

    def test_old_head_disposition_does_not_authorize_new_head(self):
        client = FakeClient()
        path = f"/repos/{low.EXPECTED_REPOSITORY}/issues/7/comments?per_page=100"
        client.get_map[path] = [{
            "id": 42,
            "user": {"login": low.EXPECTED_REFEREE_LOGIN},
            "body": (
                f"{low.REFEREE_PREFIX}\n\n- exact head: `{'b'*40}`;\n"
                "Disposition: `LOW_FRICTION_ROUTINE_EXPECTED_HEAD_PROTECTED_MERGE`."
            ),
        }]
        self.assertIsNone(
            low.referee_disposition_present(client, 7, "a" * 40, low.EXPECTED_REFEREE_LOGIN)
        )

    def test_readback_requires_signed_merge_and_exact_head_parent(self):
        pull = {
            "merged": True,
            "head": {"sha": "a" * 40},
            "merged_by": {"login": low.EXPECTED_CANDIDATE_LOGIN},
            "merge_commit_sha": "c" * 40,
        }
        commit = {
            "sha": "c" * 40,
            "commit": {"verification": {"verified": True, "reason": "valid"}},
            "parents": [{"sha": "d" * 40}, {"sha": "a" * 40}],
        }
        result = low.validate_protected_readback_payload(
            pull, commit, {"status": "ahead"}, "a" * 40, low.EXPECTED_CANDIDATE_LOGIN
        )
        self.assertTrue(result["signature_verified"])

    def test_readback_rejects_unsigned_merge(self):
        pull = {
            "merged": True,
            "head": {"sha": "a" * 40},
            "merged_by": {"login": low.EXPECTED_CANDIDATE_LOGIN},
            "merge_commit_sha": "c" * 40,
        }
        commit = {
            "sha": "c" * 40,
            "commit": {"verification": {"verified": False, "reason": "unsigned"}},
            "parents": [{"sha": "a" * 40}],
        }
        with self.assertRaisesRegex(low.AutonomyError, "signed/verified"):
            low.validate_protected_readback_payload(
                pull, commit, {"status": "ahead"}, "a" * 40, low.EXPECTED_CANDIDATE_LOGIN
            )

    def test_readback_rejects_nonancestor_merge(self):
        pull = {
            "merged": True,
            "head": {"sha": "a" * 40},
            "merged_by": {"login": low.EXPECTED_CANDIDATE_LOGIN},
            "merge_commit_sha": "c" * 40,
        }
        commit = {
            "sha": "c" * 40,
            "commit": {"verification": {"verified": True, "reason": "valid"}},
            "parents": [{"sha": "a" * 40}],
        }
        with self.assertRaisesRegex(low.AutonomyError, "ancestor"):
            low.validate_protected_readback_payload(
                pull, commit, {"status": "diverged"}, "a" * 40, low.EXPECTED_CANDIDATE_LOGIN
            )

    def test_existing_heartbeat_is_the_only_scheduler(self):
        workflow = (ROOT / ".github/workflows/administrative-maintenance-candidate.yml").read_text(encoding="utf-8")
        self.assertIn("- cron: '7 * * * *'", workflow)
        self.assertIn("- cron: '17 * * * *'", workflow)
        self.assertIn("- cron: '27 * * * *'", workflow)
        self.assertIn("- cron: '47 * * * *'", workflow)
        self.assertFalse((ROOT / ".github/workflows/administrative-maintenance-low-friction.yml").exists())

    def test_runtime_integration_reuses_existing_credentials_and_reports(self):
        runtime = (ROOT / "ci/administrative_autonomy_runtime.py").read_text(encoding="utf-8")
        self.assertIn("import administrative_autonomy_low_friction as low_friction", runtime)
        self.assertIn("executor.submit(low_friction.sweep, low_report)", runtime)
        self.assertIn("ADMIN_READ_TOKEN", runtime)
        self.assertIn("ADMIN_TOKEN", runtime)
        self.assertIn("human_steward_checkpoint_requested", runtime)

    def test_runtime_starts_both_lanes_before_waiting_on_either(self):
        runtime = (ROOT / "ci/administrative_autonomy_runtime.py").read_text(encoding="utf-8")
        low_submit = "low_future = executor.submit(low_friction.sweep, low_report)"
        base_submit = "base_future = executor.submit(_base_execute, report_path)"
        first_wait = "outcome = low_future.result()"
        self.assertIn("ThreadPoolExecutor", runtime)
        self.assertIn(low_submit, runtime)
        self.assertIn(base_submit, runtime)
        self.assertIn(first_wait, runtime)
        self.assertLess(runtime.index(low_submit), runtime.index(first_wait))
        self.assertLess(runtime.index(base_submit), runtime.index(first_wait))

    def test_runtime_has_no_base_success_precondition_for_low_friction(self):
        runtime = (ROOT / "ci/administrative_autonomy_runtime.py").read_text(encoding="utf-8")
        old_serial_gate = (
            "result = _base_execute(report_path)\n"
            "    if result != 0:\n"
            "        return result\n"
        )
        self.assertNotIn(old_serial_gate, runtime)
        self.assertIn("if base_result != 0:", runtime)
        self.assertIn("if low_error is not None:", runtime)

    def test_full_state_space_has_no_unlisted_state(self):
        self.assertEqual(set(low.ALLOWED_TRANSITIONS), set(low.STATES))
        self.assertEqual(low.ALLOWED_TRANSITIONS["TERMINAL"], set())
        for state, successors in low.ALLOWED_TRANSITIONS.items():
            for successor in successors:
                self.assertIn(successor, low.STATES, (state, successor))


if __name__ == "__main__":
    unittest.main()