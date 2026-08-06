from __future__ import annotations

import copy
import importlib.util
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "ci" / "administrative_autonomy.py"
sys.path.insert(0, str(ROOT / "ci"))
SPEC = importlib.util.spec_from_file_location(
    "administrative_autonomy",
    MODULE_PATH,
)
assert SPEC and SPEC.loader
autonomy = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = autonomy
SPEC.loader.exec_module(autonomy)


class AdministrativeAutonomyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.record = json.loads(
            (
                ROOT
                / "governance"
                / "administrative_autonomy_transition.json"
            ).read_text(encoding="utf-8")
        )

    def test_transition_is_valid(self) -> None:
        self.assertEqual(
            [],
            autonomy.validate_transition(self.record),
        )

    def test_candidate_and_referee_must_be_distinct(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["agents"]["referee"]["expected_login"] = mutated[
            "agents"
        ]["candidate"]["expected_login"]
        self.assertIn(
            "candidate and referee identities are not distinct",
            autonomy.validate_transition(mutated),
        )

    def test_human_steward_impersonation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["delegated_authority"][
            "automated_human_steward_disposition"
        ] = True
        self.assertIn(
            "automation may not impersonate the Human Steward",
            autonomy.validate_transition(mutated),
        )

    def test_direct_push_bypass_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["delegated_authority"][
            "branch_protection_bypass"
        ]["direct_push"] = True
        self.assertIn(
            "bypass must be pull-request-only",
            autonomy.validate_transition(mutated),
        )

    def test_silent_cadence_rewrite_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["delegated_authority"]["cadence_anchor_reset"][
            "silent_rewrite"
        ] = True
        self.assertIn(
            "cadence anchor reset must be append-only",
            autonomy.validate_transition(mutated),
        )

    def test_claim_inflation_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["claim_boundaries"]["campaign_admitted"] = True
        self.assertIn(
            "claim boundaries must remain false",
            autonomy.validate_transition(mutated),
        )

    def test_github_review_dependency_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["delegated_authority"]["approval_record"][
            "github_review_submission_required"
        ] = True
        self.assertIn(
            (
                "Referee approval must use a post-check exact-head "
                "issue comment"
            ),
            autonomy.validate_transition(mutated),
        )

    def test_precheck_disposition_is_rejected(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["delegated_authority"]["approval_record"][
            "required_checks_must_precede_disposition"
        ] = False
        self.assertIn(
            (
                "Referee approval must use a post-check exact-head "
                "issue comment"
            ),
            autonomy.validate_transition(mutated),
        )

    def test_failed_attempt_must_remain_fail_closed(self) -> None:
        mutated = copy.deepcopy(self.record)
        mutated["activation_attempts"][0][
            "authority_created"
        ] = True
        self.assertIn(
            "first activation failure receipt drift",
            autonomy.validate_transition(mutated),
        )


if __name__ == "__main__":
    unittest.main()
