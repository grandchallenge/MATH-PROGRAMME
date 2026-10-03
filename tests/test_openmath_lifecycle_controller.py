import copy
import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path

from ci.openmath_lifecycle_controller import apply_projection_to_state, dispatch_parts, ensure_solve_merge, candidate_sources, ControllerError, live_solve_projection, verify_locked_source_comment, synchronize_successor_issue

ROOT = Path(__file__).resolve().parents[1]


class OpenMathLifecycleControllerTest(unittest.TestCase):
    def test_terminal_submission_route_is_closed(self):
        from ci.validate_openmath_2026_core_clarity import validate_submission_route
        state=json.loads((ROOT/"governance/openmath_2026_campaign_state.json").read_text())
        validate_submission_route(state)
        self.assertEqual(state["event_window"]["official_submissions"],0)
        self.assertEqual(state["event_window"]["official_acceptances"],0)
        self.assertEqual(
            state["summary"]["competition"]["native_registration"]["blocking_boundary"],
            "EVENT_WINDOW_TERMINAL__DEADLINE_PASSED",
        )


    def test_terminal_state_rejects_automatic_programme_projection(self):
        state=json.loads((ROOT/"governance/openmath_2026_campaign_state.json").read_text())
        projection={
            "source_dispatch":"OM26-H3-WP01-IA-001",
            "hill":"OM26-H3",
            "predecessor":{"assignment_id":"OM26-H3-WP01","agent_ref":"INDEPENDENT-AGENT-003","adjudication":"ACCEPTED_EVIDENCE_WITHOUT_CLAIM_PROMOTION","accepted_claims":[]},
            "successor":{"assignment_id":"OM26-H3-WP02","dispatch_id":"OM26-H3-WP02-IA-001","agent_ref":"INDEPENDENT-AGENT-302","issue_number":999,"lifecycle":"LEASED_NOT_LAUNCHED"},
            "external_agent_summary":{"accepted_agents":4,"leased_not_launched_agents":6,"launched_agents":0,"returned_unadjudicated_agents":0},
        }
        with self.assertRaisesRegex(ControllerError,"event window terminal"):
            apply_projection_to_state(
                copy.deepcopy(state),projection,"a"*40,
                {".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json":"b"*40,
                 "work_packages/OPENMATH_2026/HILL_LANES.json":"c"*40},
            )


    def test_protected_advance_survives_deleted_candidate_branch(self):
        registry={"assignments":[{"lifecycle":{"pipeline_state":"ADVANCED"},"lease":{"dispatch_id":"OM26-H1-WP01-IA-001"}}]}
        with patch("ci.openmath_lifecycle_controller.fetch_content",return_value=(json.dumps(registry),"a"*40)), patch("ci.openmath_lifecycle_controller.optional_content",return_value=("{}","b"*40)), patch("ci.openmath_lifecycle_controller.branch_names",return_value=[]):
            self.assertEqual(candidate_sources(unittest.mock.Mock()),[("intake/openmath-om26-h1-wp01-ia-001","main")])

    def test_local_candidate_scan_skips_fully_reconciled_history(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            solve=root/"solve"
            programme=root/"programme"
            registry={
                "assignments":[
                    {"lifecycle":{"pipeline_state":"ADVANCED"},"lease":{"dispatch_id":"OM26-H1-WP01-IA-001"}},
                    {"lifecycle":{"pipeline_state":"ADVANCED"},"lease":{"dispatch_id":"OM26-H2-WP01-IA-001"}},
                ]
            }
            reg=solve/".gcl/campaigns/OPENMATH-2026/CEX_ASSIGNMENTS.json"
            reg.parent.mkdir(parents=True)
            reg.write_text(json.dumps(registry),encoding="utf-8")
            for dispatch,hill,wp in [
                ("OM26-H1-WP01-IA-001","OM26-H1","WP01"),
                ("OM26-H2-WP01-IA-001","OM26-H2","WP01"),
            ]:
                manifest=solve/f"contributions/OPENMATH-2026/{hill}/{wp}/lifecycle/{dispatch}/MANIFEST.json"
                manifest.parent.mkdir(parents=True,exist_ok=True)
                manifest.write_text("{}",encoding="utf-8")
            receipt=programme/"governance/openmath_2026_lifecycle_reconciliations/OM26-H2-WP01-IA-001.json"
            receipt.parent.mkdir(parents=True)
            receipt.write_text(json.dumps({
                "dispatch_id":"OM26-H2-WP01-IA-001",
                "result":"ADVANCED",
                "pipeline":["RETURNED","CAPTURED","REPLAYED","ADJUDICATED","ADVANCED"],
            }),encoding="utf-8")
            live=[
                "intake/openmath-om26-h1-wp01-ia-001",
                "intake/openmath-om26-h2-wp01-ia-001",
                "intake/openmath-om26-h3-wp01-ia-001",
            ]
            with patch("ci.openmath_lifecycle_controller.branch_names",return_value=live):
                sources=candidate_sources(unittest.mock.Mock(),solve,programme)
            self.assertEqual(sources,[
                ("intake/openmath-om26-h1-wp01-ia-001","main"),
                ("intake/openmath-om26-h3-wp01-ia-001",None),
            ])

    def test_protected_advance_with_invalid_dispatch_fails_closed(self):
        registry={"assignments":[{"lifecycle":{"pipeline_state":"ADVANCED"},"lease":{"dispatch_id":"untrusted"}}]}
        with patch("ci.openmath_lifecycle_controller.fetch_content",return_value=(json.dumps(registry),"a"*40)), self.assertRaises(ControllerError):
            candidate_sources(unittest.mock.Mock())

    def test_relay_framed_legacy_source_verifies_inner_and_envelope(self):
        import hashlib
        inner="GCL-CONTRIBUTION-RESULT/1\ndispatch_id: OM26-H2-WP06-IA-001\n"
        envelope=(
            "GCL-RETURN-RELAY/1\n"
            "DISPATCH_ID: OM26-H2-WP06-IA-001\n"
            "AGENT_REF: INDEPENDENT-AGENT-206\n"
            "INTENDED_RETURN: https://github.com/grandchallenge/MATHSOLVE/issues/614\n\n"
            "BEGIN_RESULT\n"+inner+"\nEND_RESULT"
        )
        receipt={
            "return_transport":"GCL-RETURN-RELAY/1",
            "relay_provenance":{
                "envelope_utf8":envelope,
                "envelope_sha256":hashlib.sha256(envelope.encode("utf-8")).hexdigest(),
                "inner_result_sha256":hashlib.sha256(inner.encode("utf-8")).hexdigest(),
            },
        }
        verify_locked_source_comment(receipt,inner,envelope,"OM26-H2-WP06-IA-001")
        with self.assertRaises(ControllerError):
            verify_locked_source_comment(receipt,inner+"changed",envelope,"OM26-H2-WP06-IA-001")
        with self.assertRaises(ControllerError):
            verify_locked_source_comment(receipt,inner,envelope+"changed","OM26-H2-WP06-IA-001")

    def test_direct_legacy_source_still_requires_raw_comment_equality(self):
        verify_locked_source_comment({},"RESULT\n","RESULT","OM26-H1-WP01-IA-001")
        with self.assertRaises(ControllerError):
            verify_locked_source_comment({},"RESULT","OTHER","OM26-H1-WP01-IA-001")

    def test_unused_successor_issue_contract_is_synchronized(self):
        gh=unittest.mock.Mock()
        gh.request.side_effect=[[],{"number":630,"body":"new body","state":"open"}]
        result=synchronize_successor_issue(
            gh,{"number":630,"body":"old body","state":"open"},"new body","OM26-H2-WP06-IA-001"
        )
        self.assertEqual(result["body"],"new body")
        self.assertEqual(
            gh.request.call_args_list[1],
            unittest.mock.call(
                "PATCH","/repos/grandchallenge/MATHSOLVE/issues/630",{"body":"new body"}
            ),
        )

    def test_successor_issue_with_participation_cannot_be_rewritten(self):
        gh=unittest.mock.Mock()
        gh.request.return_value=[{"id":1,"body":"participant evidence"}]
        with self.assertRaisesRegex(ControllerError,"refuse to rewrite return surface"):
            synchronize_successor_issue(
                gh,{"number":630,"body":"old body","state":"open"},"new body","OM26-H2-WP06-IA-001"
            )

    def test_exact_open_successor_issue_requires_no_mutation(self):
        gh=unittest.mock.Mock()
        issue={"number":630,"body":"same body","state":"open"}
        self.assertEqual(
            synchronize_successor_issue(gh,issue,"same body","OM26-H2-WP06-IA-001"),issue
        )
        gh.request.assert_not_called()

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

    def test_h1_successors_retain_source_conditional_claim_history(self):
        state=json.loads((ROOT/"governance/openmath_2026_campaign_state.json").read_text())
        h1=next(x for x in state["hills"] if x["hill_slot"]=="OM26-H1")
        current=h1["external_agent"]
        projection={"source_dispatch":"OM26-H1-WP02-IA-001","hill":"OM26-H1","predecessor":{"assignment_id":current["assignment_id"],"agent_ref":current["agent_ref"],"adjudication":"ACCEPTED_EVIDENCE_WITHOUT_CLAIM_PROMOTION","accepted_claims":[]},"successor":{"assignment_id":"OM26-H1-WP03","dispatch_id":"OM26-H1-WP03-IA-001","agent_ref":"INDEPENDENT-AGENT-103","issue_number":999,"lifecycle":"LEASED_NOT_LAUNCHED"},"external_agent_summary":{"accepted_agents":9,"leased_not_launched_agents":7}}
        result=apply_projection_to_state(state,projection,"a"*40,{})
        h1=next(x for x in result["hills"] if x["hill_slot"]=="OM26-H1")
        self.assertEqual(h1["solve"]["frontier"],"Q_GE_6__SOURCE_CONDITIONAL")
        history=h1["external_agent"]
        while history.get("assignment_id")!="OM26-H1-H1-12":
            history=history["predecessor"]
        self.assertEqual(history["accepted_claim"],"OM26-H1-RED-023")

    def test_resume_uses_current_totals_instead_of_historical_projection(self):
        historical={"external_agent_summary":{"accepted_agents":8}}
        registry={"mathematics_release_policy":{"summary":{"accepted_agents":12,"leased_not_launched_agents":7}}}
        def fetch(gh,repo,path,ref):
            value=historical if path=="projection.json" else registry if path.endswith("CEX_ASSIGNMENTS.json") else {}
            return json.dumps(value),"a"*40
        with patch("ci.openmath_lifecycle_controller.fetch_content",side_effect=fetch):
            projection,_=live_solve_projection(unittest.mock.Mock(),{"projection_path":"projection.json","manifest_path":"manifest.json"})
        self.assertEqual(projection["external_agent_summary"]["accepted_agents"],12)

    def test_event_chain_uses_protected_main_and_rate_budgeted_recovery_poll(self):
        workflow = (ROOT / ".github/workflows/openmath-unattended-lifecycle-controller.yml").read_text(encoding="utf-8")
        control = json.loads((ROOT / "governance/openmath_unattended_lifecycle_controller.json").read_text(encoding="utf-8"))
        self.assertNotIn("  workflow_run:", workflow)
        self.assertIn('      - "governance/openmath_2026_lifecycle_reconciliations/**"', workflow)
        self.assertIn('    - cron: "17,47 * * * *"', workflow)
        self.assertIn("          ref: main", workflow)
        self.assertIn("protected Programme lifecycle reconciliation merge push", control["wake"]["event_backstop"])
        self.assertIn("local protected state", control["wake"]["rate_budget"])
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
        self.assertEqual(control["wake"]["primary_operational_wake"], "repository_dispatch/openmath-return-ready plus protected lifecycle reconciliation pushes")
        self.assertEqual(control["wake"]["recovery_poll"], "scheduled recovery poll at minutes 17 and 47 of each hour")
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

class SupportingH1ProjectionTest(unittest.TestCase):
    def test_support_return_preserves_primary_and_claims(self):
        state=json.loads((ROOT/'governance/openmath_2026_campaign_state.json').read_text())
        h1=next(x for x in state['hills'] if x['hill_slot']=='OM26-H1')
        primary=copy.deepcopy(h1['external_agent']); solve=copy.deepcopy(h1['solve'])
        h1['supporting_agents']={'H1-Q6':{'assignment_id':'OM26-H1-WP30','agent_ref':'INDEPENDENT-AGENT-130','issue_number':598}}
        projection={'source_dispatch':'OM26-H1-WP30-IA-001','hill':'OM26-H1','lane_role':'SUPPORT','support_slot':'H1-Q6',
                    'predecessor':{'assignment_id':'OM26-H1-WP30','agent_ref':'INDEPENDENT-AGENT-130','adjudication':'ACCEPTED_EVIDENCE_WITHOUT_CLAIM_PROMOTION','accepted_claims':[]},
                    'successor':{'assignment_id':'OM26-H1-WP31','dispatch_id':'OM26-H1-WP31-IA-001','agent_ref':'INDEPENDENT-AGENT-131','issue_number':999,'lifecycle':'LEASED_NOT_LAUNCHED'},
                    'external_agent_summary':{'accepted_agents':13,'leased_not_launched_agents':9}}
        result=apply_projection_to_state(state,projection,'a'*40,{})
        row=next(x for x in result['hills'] if x['hill_slot']=='OM26-H1')
        self.assertEqual(row['external_agent'],primary)
        self.assertEqual(row['solve'],solve)
        self.assertEqual(row['supporting_agents']['H1-Q6']['assignment_id'],'OM26-H1-WP31')
        self.assertEqual(result['automation']['openmath_lifecycle']['last_transition_result'],'ADVANCED')

class EventWindowSupersessionHistoryTest(unittest.TestCase):
    def test_retired_unlaunched_task_remains_in_history_without_accepted_claim(self):
        state=json.loads((ROOT/'governance/openmath_2026_campaign_state.json').read_text())
        h2=next(x for x in state['hills'] if x['hill_slot']=='OM26-H2')
        history=h2['external_agent']
        while history.get('assignment_id')!='OM26-H2-WP04' and isinstance(history.get('predecessor'),dict):
            history=history['predecessor']
        self.assertEqual(history['assignment_id'],'OM26-H2-WP04')
        self.assertEqual(history['lifecycle'],'SUPERSEDED')
        self.assertEqual(history['accepted_claims'],[])
        self.assertIsNone(history['launch_evidence'])
