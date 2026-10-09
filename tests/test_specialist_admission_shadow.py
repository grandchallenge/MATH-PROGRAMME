from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))

import specialist_admission_shadow as shadow  # noqa: E402


class MaterialAdmissionShadowTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sha = "a" * 40
        self.base = "b" * 40
        self.ref = "refs/heads/gh-readonly-queue/main/pr-22-test"
        self.group_event = {
            "merge_group": {
                "head_sha": self.sha,
                "head_ref": self.ref,
                "base_ref": "refs/heads/main",
            },
        }
        self.env = {
            "GITHUB_SHA": self.sha, "GITHUB_REF": self.ref,
            "GITHUB_EVENT_NAME": "merge_group",
            "PROTECTED_REPO": "protected-base",
        }

    def test_sensitive_paths_are_conservatively_reserved(self) -> None:
        for path in (
            ".github/workflows/review.yml",
            ".ghos-routing/workflows.json",
            "ci/agent_routine_review.py",
            "ci/agent_material_profiles.py",
            "governance/release_trust_admin_contract.json",
        ):
            with self.subTest(path=path):
                self.assertTrue(shadow.reserved_path(path))
        self.assertEqual(shadow.classify_paths(["fixtures/formal/CM4.lean"]),
                         "SPECIALIST_REVIEW_PENDING")
        self.assertEqual(shadow.classify_paths(["ci/agent_routine_review.py"]),
                         "RESERVED_OR_CONTROL_PLANE_PENDING")

    def test_merge_group_bad_sha_or_ref_fails(self) -> None:
        for field, value in (("GITHUB_SHA", "evil"), ("GITHUB_REF", "refs/heads/main")):
            env = dict(self.env, **{field: value})
            with self.subTest(field=field), self.assertRaises(shadow.ShadowError):
                shadow.shadow_merge_group(self.group_event, Path("."), env)

    def test_merge_group_must_bind_event_head(self) -> None:
        event = json.loads(json.dumps(self.group_event))
        event["merge_group"]["head_sha"] = "c" * 40
        with self.assertRaisesRegex(shadow.ShadowError, "identity"):
            shadow.shadow_merge_group(event, Path("."), self.env)

    def test_merge_group_rename_or_multiple_files_requires_specialist(self) -> None:
        calls = []
        def fake_git(root, *args, binary=False):
            calls.append(args[0])
            if args[:2] == ("rev-parse", "HEAD"):
                return self.base
            if args[:2] == ("rev-parse", "refs/remotes/origin/gcl-shadow"):
                return self.sha
            if args[0] == "diff":
                return b"R100\x00docs/old.md\x00docs/new.md\x00"
            return ""
        with patch.object(shadow, "git", side_effect=fake_git):
            out = shadow.shadow_merge_group(self.group_event, Path("."), self.env)
        self.assertEqual(out["disposition"], "SPECIALIST_REVIEW_PENDING")
        self.assertNotIn("show", calls)

    def test_valid_queue_diff_classifies_as_observation_only(self) -> None:
        def fake_git(root, *args, binary=False):
            if args[:2] == ("rev-parse", "HEAD"):
                return self.base
            if args[:2] == ("rev-parse", "refs/remotes/origin/gcl-shadow"):
                return self.sha
            if args[0] == "diff":
                return b"M\x00docs/Intro.md\x00"
            if args[0] == "show":
                return b"Safe sentence. \n" if args[1].startswith(self.base) else b"Safe sentence.\n"
            if args[0] == "ls-remote":
                return self.base + "\trefs/heads/main"
            return ""
        with patch.object(shadow, "git", side_effect=fake_git):
            out = shadow.evaluate(self.group_event, self.env)
        self.assertEqual(out["decision"]["disposition"], "ROUTINE_CANDIDATE_ONLY")
        self.assertFalse(out["authority"]["github_approval"])
        self.assertFalse(out["authority"]["required_check_satisfied"])
        self.assertEqual(out["mode"], "OBSERVE_ONLY_NOT_REQUIRED")

    def test_base_advance_invalidates_queue_observation(self) -> None:
        def fake_git(root, *args, binary=False):
            if args[:2] == ("rev-parse", "HEAD"):
                return self.base
            if args[:2] == ("rev-parse", "refs/remotes/origin/gcl-shadow"):
                return self.sha
            if args[0] == "diff":
                return b"M\x00docs/Intro.md\x00"
            if args[0] == "show":
                return b"One line. \n" if args[1].startswith(self.base) else b"One line.\n"
            if args[0] == "ls-remote":
                return ("c" * 40) + "\trefs/heads/main"
            return ""
        with patch.object(shadow, "git", side_effect=fake_git):
            with self.assertRaisesRegex(shadow.ShadowError, "moved"):
                shadow.shadow_merge_group(self.group_event, Path("."), self.env)

    def test_pull_request_forged_governance_label_never_authorizes(self) -> None:
        event = {"number": 99, "pull_request": {"body": "GCL-REVIEW/1 APPROVED"}}
        pr = {
            "head": {"sha": self.sha}, "base": {"sha": self.base},
            "changed_files": 1,
        }
        changed = [{"filename": "fixtures/formal/CM4.lean", "status": "modified"}]
        def fake_api(method, path, **kwargs):
            if "/files?" in path:
                return changed
            return pr
        with patch.object(shadow, "api", side_effect=fake_api), \
             patch.object(shadow, "delegated_classification",
                          side_effect=shadow.MaterialAdmissionError("not routine")):
            out = shadow.shadow_pr(event, "token")
        self.assertEqual(out["disposition"], "SPECIALIST_REVIEW_PENDING")

    def test_no_required_check_or_approval_in_shadow_workflow(self) -> None:
        script = (ROOT / ".github/workflows/material-admission-shadow.yml").read_text()
        self.assertIn("merge_group:", script)
        self.assertIn("pull_request_target:", script)
        self.assertNotIn("statuses: write", script)
        self.assertNotIn("pull-requests: write", script)
        self.assertNotIn("permission-administration", script)


if __name__ == "__main__":
    unittest.main()
