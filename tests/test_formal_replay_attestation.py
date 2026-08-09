import datetime as dt
import importlib.util
from pathlib import Path
import subprocess
import tempfile
import unittest

MODULE_PATH = Path(__file__).resolve().parents[1] / "ci" / "formal_replay_attestation.py"
spec = importlib.util.spec_from_file_location("formal_replay_attestation", MODULE_PATH)
fra = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fra)


class FormalReplayAttestationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.repo, check=True)
        subprocess.run(["git", "config", "user.name", "test"], cwd=self.repo, check=True)
        (self.repo / "fixture").mkdir()
        (self.repo / "ci").mkdir()
        (self.repo / "schemas").mkdir()
        (self.repo / ".github/workflows").mkdir(parents=True)
        (self.repo / "fixture/Main.lean").write_text("theorem ok : True := by trivial\n", encoding="utf-8")
        (self.repo / "fixture/lean-toolchain").write_text("leanprover/lean4:v4.0.0\n", encoding="utf-8")
        (self.repo / "fixture/lake-manifest.json").write_text('{"version":"1"}\n', encoding="utf-8")
        (self.repo / "ci/formal_replay_attestation.py").write_text(MODULE_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        (self.repo / "schemas/formal_replay_receipt.schema.json").write_text("{}\n", encoding="utf-8")
        self.cache_sha = "1" * 40
        self.lean_sha = "2" * 40
        (self.repo / ".github/workflows/ci.yml").write_text(f"cache {self.cache_sha}\nlean {self.lean_sha}\n", encoding="utf-8")
        self.policy = {
            "schema_version": 1,
            "operation": "TEST",
            "global": {
                "repository": "grandchallenge/MATH-PROGRAMME",
                "cache_namespace": "test-cache",
                "cache_action_sha": self.cache_sha,
                "lean_action_sha": self.lean_sha,
                "runner": "ubuntu-24.04",
                "inputs": [".github/workflows/ci.yml", "ci/formal_replay_attestation.py", "schemas/formal_replay_receipt.schema.json"]
            },
            "sentinel": {"required_full_replay_within_hours": 24, "reuse_max_age_hours": 18},
            "lanes": {
                "fixture": {
                    "roots": ["fixture"],
                    "files": [],
                    "command": ["lake", "build"],
                    "proof_semantic_tcb": {"runner": "ubuntu-24.04", "lean_action_sha": self.lean_sha},
                    "forbidden_source_patterns": ["(^|[^A-Za-z])(sorry|axiom)([^A-Za-z]|$)"]
                }
            }
        }
        self._commit("baseline")

    def tearDown(self):
        self.tmp.cleanup()

    def _commit(self, message):
        subprocess.run(["git", "add", "-A"], cwd=self.repo, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.repo, check=True)
        return fra.git_head(self.repo)

    def _receipt(self, created_at, origin_commit=None):
        digest, _ = fra.compute_digest(self.repo, self.policy, "fixture")
        return {
            "schema_version": 1, "lane": "fixture", "status": fra.RECEIPT_STATUS,
            "input_digest": digest, "repository": "grandchallenge/MATH-PROGRAMME",
            "origin_commit": origin_commit or fra.git_head(self.repo), "origin_run_id": "123",
            "origin_run_attempt": "1", "origin_event": "push", "origin_ref": "refs/heads/main",
            "policy_operation": "TEST", "command": ["lake", "build"],
            "proof_semantic_tcb": {"runner": "ubuntu-24.04", "lean_action_sha": self.lean_sha},
            "result_digest": "3" * 64, "result_files": [], "created_at": created_at
        }

    def test_unrelated_file_does_not_change_digest(self):
        before, _ = fra.compute_digest(self.repo, self.policy, "fixture")
        (self.repo / "README.md").write_text("unrelated\n", encoding="utf-8")
        self._commit("unrelated")
        after, _ = fra.compute_digest(self.repo, self.policy, "fixture")
        self.assertEqual(before, after)

    def test_fixture_mutation_invalidates_digest(self):
        before, _ = fra.compute_digest(self.repo, self.policy, "fixture")
        (self.repo / "fixture/Main.lean").write_text("theorem ok : True := by exact True.intro\n", encoding="utf-8")
        self._commit("fixture mutation")
        after, _ = fra.compute_digest(self.repo, self.policy, "fixture")
        self.assertNotEqual(before, after)

    def test_workflow_mutation_invalidates_digest(self):
        before, _ = fra.compute_digest(self.repo, self.policy, "fixture")
        (self.repo / ".github/workflows/ci.yml").write_text(f"cache {self.cache_sha}\nlean {self.lean_sha}\nchanged\n", encoding="utf-8")
        self._commit("workflow mutation")
        after, _ = fra.compute_digest(self.repo, self.policy, "fixture")
        self.assertNotEqual(before, after)

    def test_forged_digest_is_not_reused(self):
        receipt = self._receipt("2026-08-09T07:00:00Z")
        receipt["input_digest"] = "0" * 64
        reuse, reason = fra.validate_receipt(self.repo, self.policy, "fixture", receipt, now=dt.datetime(2026, 8, 9, 8, 0, tzinfo=dt.timezone.utc))
        self.assertFalse(reuse)
        self.assertEqual(reason, "receipt_input_digest_mismatch")

    def test_stale_receipt_forces_replay(self):
        receipt = self._receipt("2026-08-08T13:00:00Z")
        reuse, reason = fra.validate_receipt(self.repo, self.policy, "fixture", receipt, now=dt.datetime(2026, 8, 9, 8, 0, tzinfo=dt.timezone.utc))
        self.assertFalse(reuse)
        self.assertEqual(reason, "sentinel_replay_due")

    def test_fresh_ancestor_receipt_reusable_after_unrelated_commit(self):
        origin = fra.git_head(self.repo)
        receipt = self._receipt("2026-08-09T07:00:00Z", origin_commit=origin)
        (self.repo / "README.md").write_text("unrelated\n", encoding="utf-8")
        self._commit("unrelated")
        reuse, reason = fra.validate_receipt(self.repo, self.policy, "fixture", receipt, now=dt.datetime(2026, 8, 9, 8, 0, tzinfo=dt.timezone.utc))
        self.assertTrue(reuse)
        self.assertEqual(reason, "receipt_valid_and_fresh")

    def test_nonancestor_receipt_rejected(self):
        receipt = self._receipt("2026-08-09T07:00:00Z")
        receipt["origin_commit"] = "f" * 40
        reuse, reason = fra.validate_receipt(self.repo, self.policy, "fixture", receipt, now=dt.datetime(2026, 8, 9, 8, 0, tzinfo=dt.timezone.utc))
        self.assertFalse(reuse)
        self.assertEqual(reason, "receipt_origin_not_ancestor")

    def test_forbidden_source_change_detected(self):
        (self.repo / "fixture/Main.lean").write_text("axiom hidden : True\n", encoding="utf-8")
        self._commit("forbidden")
        self.assertTrue(fra.scan_forbidden(self.repo, self.policy, "fixture"))

    def test_declared_missing_input_fails_closed(self):
        self.policy["lanes"]["fixture"]["files"] = ["missing.lean"]
        with self.assertRaises(fra.PolicyError):
            fra.compute_digest(self.repo, self.policy, "fixture")


if __name__ == "__main__":
    unittest.main()
