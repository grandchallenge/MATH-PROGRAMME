import copy
import json
import unittest
from pathlib import Path

from ci.openmath_lifecycle_controller import apply_projection_to_state

ROOT = Path(__file__).resolve().parents[1]


class OpenMathLifecycleControllerTest(unittest.TestCase):
    def test_projection_advances_without_manual_bridge(self):
        state = json.loads(
            (ROOT / "governance/openmath_2026_campaign_state.json").read_text(encoding="utf-8")
        )
        projection = {
            "source_dispatch": "OM26-H3-WP01-IA-001",
            "hill": "OM26-H3",
            "predecessor": {
                "assignment_id": "OM26-H3-WP01",
                "agent_ref": "INDEPENDENT-AGENT-003",
                "adjudication": "ACCEPTED_EVIDENCE_WITHOUT_CLAIM_PROMOTION",
                "accepted_claims": [],
            },
            "successor": {
                "assignment_id": "OM26-H3-WP02",
                "dispatch_id": "OM26-H3-WP02-IA-001",
                "agent_ref": "INDEPENDENT-AGENT-302",
                "issue_number": 999,
                "lifecycle": "LEASED_NOT_LAUNCHED",
            },
            "external_agent_summary": {
                "accepted_agents": 4,
                "leased_not_launched_agents": 6,
                "launched_agents": 0,
                "returned_unadjudicated_agents": 0,
            },
        }
        candidate = apply_projection_to_state(
            copy.deepcopy(state),
            projection,
            "a" * 40,
            {
                ".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json": "b" * 40,
                "work_packages/OPENMATH_2026/HILL_LANES.json": "c" * 40,
            },
        )
        h3 = next(x for x in candidate["hills"] if x["hill_slot"] == "OM26-H3")
        self.assertEqual(h3["external_agent"]["assignment_id"], "OM26-H3-WP02")
        self.assertEqual(h3["external_agent"]["lifecycle"], "LEASED_NOT_LAUNCHED")
        self.assertEqual(
            h3["external_agent"]["predecessor"]["adjudication"],
            "ACCEPTED_EVIDENCE_WITHOUT_CLAIM_PROMOTION",
        )
        automation = candidate["automation"]["openmath_lifecycle"]
        self.assertEqual(automation["last_transition_result"], "ADVANCED")
        self.assertFalse(automation["manual_transport_required"])
        self.assertFalse(automation["manual_controller_wake_required"])
        self.assertIn("OM26-H3", candidate["next_action"]["currently_selected"])

    def test_frozen_pipeline_is_exact(self):
        control = json.loads(
            (ROOT / "governance/openmath_unattended_lifecycle_controller.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            control["lifecycle"],
            ["READY", "LAUNCHED", "RETURNED", "CAPTURED", "REPLAYED", "ADJUDICATED", "ADVANCED"],
        )
        self.assertFalse(control["acceptance_test"]["manual_transport_allowed"])
        self.assertFalse(control["acceptance_test"]["manual_controller_wake_allowed"])
        binding = control["paired_solve_implementation"]
        self.assertEqual(binding["repository"], "grandchallenge/MATHSOLVE")
        self.assertEqual(binding["base_pull_request"], 542)
        self.assertEqual(binding["hardening_pull_request"], 543)
        self.assertEqual(
            binding["protected_merge"],
            "1b4c0496b0dfe6b304272910875de71274d95c32",
        )
        self.assertEqual(
            binding["lifecycle_contract_git_blob_sha1"],
            "c3f4fc75424210def1ad025e20da36b7fce6257f",
        )
        self.assertEqual(
            binding["candidate_generator_git_blob_sha1"],
            "30d0db5bfe09a5a173482b70352fbc9153fc6299",
        )


if __name__ == "__main__":
    unittest.main()
