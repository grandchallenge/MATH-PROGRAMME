from __future__ import annotations

import copy
import importlib.util
import json
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
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
        self.stabilization = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_stabilization_correction.json"
            ).read_text(encoding="utf-8")
        )

    def test_correction_is_valid(self) -> None:
        self.assertEqual([], candidate_merge.validate_correction(self.record))

    def test_stabilization_is_valid(self) -> None:
        self.assertEqual(
            [],
            candidate_merge.validate_stabilization(self.stabilization),
        )

    def test_third_failure_receipt_may_not_create_authority(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["activation_attempt_003"]["authority_created"] = True
        self.assertIn(
            "third activation failure receipt drift",
            candidate_merge.validate_correction(mutated),
        )

    def test_fourth_failure_receipt_may_not_create_authority(self) -> None:
        mutated = copy.deepcopy(self.stabilization)
        mutated["activation_attempt_004"]["authority_created"] = True
        self.assertIn(
            "fourth activation failure receipt drift",
            candidate_merge.validate_stabilization(mutated),
        )

    def test_referee_remains_approval_actor(self) -> None:
        mutated = copy.deepcopy(self.stabilization)
        mutated["corrected_control"]["approval_decision_actor"] = (
            "gcl-release-trust[bot]"
        )
        self.assertIn(
            "stabilization control approval_decision_actor drift",
            candidate_merge.validate_stabilization(mutated),
        )

    def test_candidate_is_merge_executor(self) -> None:
        mutated = copy.deepcopy(self.stabilization)
        mutated["corrected_control"]["merge_executor_actor"] = (
            "github-actions[bot]"
        )
        self.assertIn(
            "stabilization control merge_executor_actor drift",
            candidate_merge.validate_stabilization(mutated),
        )

    def test_clean_pre_merge_state_is_required(self) -> None:
        mutated = copy.deepcopy(self.stabilization)
        mutated["corrected_control"]["required_pre_merge_state"] = "UNSTABLE"
        self.assertIn(
            "stabilization control required_pre_merge_state drift",
            candidate_merge.validate_stabilization(mutated),
        )

    def test_canary_bypass_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.stabilization)
        mutated["corrected_control"]["canary_bypass_must_not_be_used"] = False
        self.assertIn(
            "stabilization control canary_bypass_must_not_be_used must be true",
            candidate_merge.validate_stabilization(mutated),
        )

    def test_human_steward_impersonation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.stabilization)
        mutated["corrected_control"]["human_steward_impersonation"] = True
        self.assertIn(
            "stabilization control human_steward_impersonation must be false",
            candidate_merge.validate_stabilization(mutated),
        )

    def test_manual_review_requires_assignment_and_mention(self) -> None:
        mutated = copy.deepcopy(self.stabilization)
        mutated["manual_review_notification"][
            "explicit_mention_comment_required"
        ] = False
        self.assertIn(
            "stabilization reviewer notification drift",
            candidate_merge.validate_stabilization(mutated),
        )

    def test_effective_routing_has_no_routine_reviewer(self) -> None:
        routing = json.loads(candidate_merge.ROUTING.read_text(encoding="utf-8"))
        self.assertEqual(candidate_merge.validate_effective_reviewer_routing(routing), [])
        mutated = copy.deepcopy(routing)
        mutated["effective_routing"]["mandatory_routine_reviewers"] = ["jimsteeg"]
        self.assertIn(
            "effective routine reviewer routing drift",
            candidate_merge.validate_effective_reviewer_routing(mutated),
        )

    def test_missing_referee_disposition_fails_closed(self) -> None:
        candidate = SimpleNamespace()
        referee = SimpleNamespace()
        control = self.stabilization["corrected_control"]
        with (
            patch.dict(
                os.environ,
                {"GITHUB_REPOSITORY": "grandchallenge/MATH-PROGRAMME"},
                clear=False,
            ),
            patch.object(
                candidate_merge,
                "_pull_request_snapshot",
                return_value={
                    "number": 258,
                    "state": "OPEN",
                    "isDraft": False,
                    "headRefOid": "a" * 40,
                    "mergeStateStatus": "CLEAN",
                },
            ),
            patch.object(
                candidate_merge,
                "_referee_disposition_present",
                return_value=False,
            ),
        ):
            with self.assertRaisesRegex(
                candidate_merge.AutonomyError,
                "exact-head Referee disposition is absent",
            ):
                candidate_merge._wait_for_clean_merge_state(
                    candidate,
                    referee,
                    "PR_node",
                    "a" * 40,
                    "github-actions[bot]",
                    control,
                )

    def test_failed_post_disposition_check_fails_closed(self) -> None:
        class FakeClient:
            def get(self, path: str):
                return {
                    "check_runs": [
                        {
                            "name": "dispatcher",
                            "status": "completed",
                            "conclusion": "failure",
                        }
                    ]
                }

        with self.assertRaisesRegex(
            candidate_merge.AutonomyError,
            "post-disposition check run failed",
        ):
            candidate_merge._check_runs_state(
                FakeClient(),
                "grandchallenge/MATH-PROGRAMME",
                "b" * 40,
                {"success", "neutral", "skipped"},
            )

    def test_candidate_performs_clean_exact_head_merge(self) -> None:
        captured: dict[str, object] = {}
        sha = "c" * 40

        class FakeCandidateClient:
            def __init__(self, token: str):
                captured["token"] = token

            def put(self, path: str, payload):
                captured["merge_path"] = path
                captured["merge_payload"] = payload
                return {"merged": True, "sha": "d" * 40}

            def get(self, path: str):
                return {
                    "merged": True,
                    "head": {"sha": sha},
                    "merged_by": {"login": "gcl-release-trust[bot]"},
                }

        env = {
            "GITHUB_REPOSITORY": "grandchallenge/MATH-PROGRAMME",
            "CANDIDATE_TOKEN": "candidate-token",
            "CANDIDATE_LOGIN": "gcl-release-trust[bot]",
            "CANDIDATE_APP_ID": "4423678",
        }
        referee_identity = SimpleNamespace(login="github-actions[bot]")
        with (
            patch.dict(os.environ, env, clear=False),
            patch.object(candidate_merge, "Client", FakeCandidateClient),
            patch.object(
                candidate_merge,
                "_wait_for_clean_merge_state",
                return_value=258,
            ),
        ):
            candidate_merge.candidate_exact_head_merge(
                SimpleNamespace(),
                "PR_node",
                sha,
                referee_identity,
            )

        self.assertEqual("candidate-token", captured["token"])
        self.assertEqual(
            "/repos/grandchallenge/MATH-PROGRAMME/pulls/258/merge",
            captured["merge_path"],
        )
        payload = captured["merge_payload"]
        self.assertEqual(sha, payload["sha"])
        self.assertEqual("merge", payload["merge_method"])

    def test_activation_record_describes_clean_exact_head_merge(self) -> None:
        original = {
            "referee_disposition": {"recorded_before_auto_merge": True},
            "auto_merge": {},
            "canary": {},
        }
        with patch.object(
            candidate_merge,
            "ORIGINAL_ACTIVATION_RECORD",
            return_value=original,
        ):
            record = candidate_merge.corrected_activation_record()
        self.assertNotIn(
            "recorded_before_auto_merge",
            record["referee_disposition"],
        )
        self.assertTrue(
            record["referee_disposition"][
                "recorded_before_merge_execution"
            ]
        )
        self.assertFalse(record["auto_merge"]["used_for_canary"])
        self.assertEqual(
            "CLEAN",
            record["canary"]["required_pre_merge_state"],
        )

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
                candidate_merge.candidate_exact_head_merge(
                    SimpleNamespace(),
                    "PR_node",
                    "e" * 40,
                    SimpleNamespace(login="github-actions[bot]"),
                )


if __name__ == "__main__":
    unittest.main()
