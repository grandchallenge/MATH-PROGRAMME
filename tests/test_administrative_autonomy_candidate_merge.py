from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ci"))
MODULE_PATH = ROOT / "ci" / "administrative_autonomy_candidate_merge.py"
SPEC = importlib.util.spec_from_file_location(
    "administrative_autonomy_candidate_merge",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
candidate_merge = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = candidate_merge
SPEC.loader.exec_module(candidate_merge)


class AdministrativeAutonomyCandidateMergeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_merge_executor_correction.json"
            ).read_text(encoding="utf-8")
        )

    def test_correction_is_valid(self) -> None:
        self.assertEqual([], candidate_merge.validate_correction(self.record))

    def test_third_failure_receipt_may_not_create_authority(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["activation_attempt_003"]["authority_created"] = True
        self.assertIn(
            "third activation failure receipt drift",
            candidate_merge.validate_correction(mutated),
        )

    def test_referee_remains_approval_actor(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["corrected_control"]["approval_decision_actor"] = (
            "gcl-release-trust[bot]"
        )
        self.assertIn(
            "Referee approval actor drift",
            candidate_merge.validate_correction(mutated),
        )

    def test_candidate_is_merge_executor(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["corrected_control"]["merge_executor_actor"] = (
            "github-actions[bot]"
        )
        self.assertIn(
            "Candidate merge executor actor drift",
            candidate_merge.validate_correction(mutated),
        )

    def test_referee_disposition_must_precede_auto_merge(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["corrected_control"][
            "referee_disposition_must_precede_auto_merge"
        ] = False
        self.assertIn(
            "Referee disposition must precede auto-merge",
            candidate_merge.validate_correction(mutated),
        )

    def test_canary_bypass_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["corrected_control"]["canary_bypass_must_not_be_used"] = False
        self.assertIn(
            "activation canary may not use bypass",
            candidate_merge.validate_correction(mutated),
        )

    def test_human_steward_impersonation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["corrected_control"]["human_steward_impersonation"] = True
        self.assertIn(
            "Human Steward impersonation must remain prohibited",
            candidate_merge.validate_correction(mutated),
        )

    def test_manual_review_requires_assignment_and_mention(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["manual_review_notification"][
            "explicit_mention_comment_required"
        ] = False
        self.assertIn(
            "manual reviewer notification contract drift",
            candidate_merge.validate_correction(mutated),
        )

    def test_candidate_token_executes_auto_merge(self) -> None:
        captured: dict[str, object] = {}

        class FakeClient:
            def __init__(self, token: str):
                self.token = token

        def fake_auto_merge(client, node_id, sha, executor) -> None:
            captured["token"] = client.token
            captured["node_id"] = node_id
            captured["sha"] = sha
            captured["login"] = executor.login
            captured["role"] = executor.token_role

        env = {
            "CANDIDATE_TOKEN": "candidate-token",
            "CANDIDATE_LOGIN": "gcl-release-trust[bot]",
            "CANDIDATE_APP_ID": "4423678",
        }
        with (
            patch.dict(os.environ, env, clear=False),
            patch.object(candidate_merge, "Client", FakeClient),
            patch.object(candidate_merge, "github_auto_merge", fake_auto_merge),
        ):
            candidate_merge.candidate_auto_merge(
                None,
                "PR_node",
                "a" * 40,
                None,
            )

        self.assertEqual("candidate-token", captured["token"])
        self.assertEqual("PR_node", captured["node_id"])
        self.assertEqual("a" * 40, captured["sha"])
        self.assertEqual("gcl-release-trust[bot]", captured["login"])
        self.assertEqual("candidate-merge-executor", captured["role"])

    def test_missing_candidate_token_fails_closed(self) -> None:
        env = {
            "CANDIDATE_TOKEN": "",
            "CANDIDATE_LOGIN": "gcl-release-trust[bot]",
            "CANDIDATE_APP_ID": "4423678",
        }
        with patch.dict(os.environ, env, clear=False):
            with self.assertRaisesRegex(
                candidate_merge.AutonomyError,
                "Candidate merge executor token is missing",
            ):
                candidate_merge.candidate_auto_merge(
                    None,
                    "PR_node",
                    "b" * 40,
                    None,
                )


if __name__ == "__main__":
    unittest.main()
