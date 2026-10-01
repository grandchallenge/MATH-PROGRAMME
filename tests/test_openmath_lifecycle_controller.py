import copy
import json
import unittest
from unittest.mock import patch
from pathlib import Path

from ci.openmath_lifecycle_controller import apply_projection_to_state, dispatch_parts, ensure_solve_merge, candidate_sources, ControllerError

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

    def test_protected_advance_survives_deleted_candidate_branch(self):
        registry={"assignments":[{"lifecycle":{"pipeline_state":"ADVANCED"},"lease":{"dispatch_id":"OM26-H1-WP01-IA-001"}}]}
        with patch("ci.openmath_lifecycle_controller.fetch_content",return_value=(json.dumps(registry),"a"*40)), patch("ci.openmath_lifecycle_controller.optional_content",return_value=("{}","b"*40)), patch("ci.openmath_lifecycle_controller.branch_names",return_value=[]):
            self.assertEqual(candidate_sources(unittest.mock.Mock()),[("intake/openmath-om26-h1-wp01-ia-001","main")])

    def test_protected_advance_with_invalid_dispatch_fails_closed(self):
        registry={"assignments":[{"lifecycle":{"pipeline_state":"ADVANCED"},"lease":{"dispatch_id":"untrusted"}}]}
        with patch("ci.openmath_lifecycle_controller.fetch_content",return_value=(json.dumps(registry),"a"*40)), self.assertRaises(ControllerError):
            candidate_sources(unittest.mock.Mock())

    def test_pending_merge_is_bounded_and_does_not_wait(self):
        gh=unittest.mock.Mock()
        gh.request.return_value={"number":564,"mergeable":True,"merged_at":None}
        item={"branch":"intake/openmath-om26-h7-wp02-ia-001","dispatch_id":"OM26-H7-WP02-IA-001"}
        with patch("ci.openmath_lifecycle_controller.main_has_manifest",return_value=False), patch("ci.openmath_lifecycle_controller.find_pr",return_value={"number":564}), patch("ci.openmath_lifecycle_controller.enable_auto_merge"), patch("ci.openmath_lifecycle_controller.wait_merged",side_effect=AssertionError("blocking wait")):
            result=ensure_solve_merge(gh,item)
        self.assertTrue(result["pending"])
        self.assertEqual(result["number"],564)

    def test_conflict_refresh_uses_protected_generator_and_rebinds_projection(self):
        gh=unittest.mock.Mock()
        gh.request.side_effect=[{"number":564,"mergeable":False},{"number":565,"merged_at":None}]
        item={"branch":"intake/openmath-om26-h7-wp02-ia-001","dispatch_id":"OM26-H7-WP02-IA-001","projection_blob":"old"}
        refreshed={**item,"branch":"candidate/openmath-om26-h7-wp02-ia-001","projection_blob":"fresh"}
        with patch("ci.openmath_lifecycle_controller.main_has_manifest",return_value=False), patch("ci.openmath_lifecycle_controller.find_pr",side_effect=[{"number":564},{"number":565}]), patch("ci.openmath_lifecycle_controller.enable_auto_merge"), patch("ci.openmath_lifecycle_controller.recover_legacy",return_value=refreshed) as rebuild:
            result=ensure_solve_merge(gh,item,ROOT)
        rebuild.assert_called_once_with(gh,"intake/openmath-om26-h7-wp02-ia-001",ROOT,refresh=True)
        self.assertEqual(item["projection_blob"],"fresh")
        self.assertEqual(result["branch"],refreshed["branch"])

    def test_event_backstop_uses_protected_main(self):
        workflow = (ROOT / ".github/workflows/openmath-unattended-lifecycle-controller.yml").read_text(encoding="utf-8")
        control = json.loads((ROOT / "governance/openmath_unattended_lifecycle_controller.json").read_text(encoding="utf-8"))
        self.assertIn("  workflow_run:\n    workflows:\n      - Administrative maintenance dispatcher\n    types:\n      - completed\n", workflow)
        self.assertIn("github.event.workflow_run.conclusion == 'success'", workflow)
        self.assertIn("          ref: main", workflow)
        self.assertNotIn("github.event.workflow_run.head_sha", workflow)
        self.assertIn("successful completion of Administrative maintenance dispatcher", control["wake"]["event_backstop"])
        self.assertFalse(control["wake"]["scheduled_delivery_guaranteed"])

    def test_h1_wp_dispatch_uses_the_same_pipeline(self):
        self.assertEqual(dispatch_parts('intake/openmath-om26-h1-wp01-ia-001'), ('OM26-H1-WP01-IA-001', 'OM26-H1', 'WP01'))

    def test_return_wake_is_narrow_and_uses_no_payload_code(self):
        workflow = (ROOT / '.github/workflows/openmath-unattended-lifecycle-controller.yml').read_text(encoding='utf-8')
        self.assertIn('  repository_dispatch:\n    types:\n      - openmath-return-ready\n', workflow)
        self.assertNotIn('github.event.client_payload', workflow)

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
        self.assertTrue(control["acceptance_test"]["live_controller_smoke_required"])
        self.assertFalse(control["wake"]["manual_controller_wake_required"])
        self.assertEqual(control["wake"]["primary_operational_wake"], "scheduled poll every five minutes")
        binding = control["paired_solve_implementation"]
        self.assertEqual(binding["repository"], "grandchallenge/MATHSOLVE")
        self.assertEqual(binding["base_pull_request"], 542)
        self.assertEqual(binding["hardening_pull_request"], 543)
        self.assertEqual(binding["acceptance_closure_pull_request"], 544)
        self.assertEqual(
            binding["protected_merge"],
            "631ddb201ac2ead06373e8cc3e6d08eadbf51c16",
        )
        self.assertEqual(
            binding["lifecycle_contract_git_blob_sha1"],
            "c3f4fc75424210def1ad025e20da36b7fce6257f",
        )
        self.assertEqual(
            binding["candidate_generator_git_blob_sha1"],
            "30d0db5bfe09a5a173482b70352fbc9153fc6299",
        )
        self.assertEqual(
            binding["acceptance_runner_git_blob_sha1"],
            "0ae6986d8f164199712f014c8501ae89a5c0ec8d",
        )


if __name__ == "__main__":
    unittest.main()
