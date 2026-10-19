"""Fail-closed tests for the direct-editorial queue projector."""
import unittest
import copy
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch
from ci import erdos_catalogue_queue_projection as mod


class QueueProjectionTests(unittest.TestCase):
    def setUp(self):
        self.issue = 2491
        self.body = "RESULT/1\nASSIGNMENT_ID: ERDOS-CATALOGUE-1220-S01\n"
        import hashlib
        self.receipt = {"issue_number": self.issue, "problem_id": 1220,
                        "validation": "STRUCTURALLY_VALID_UNADJUDICATED",
                        "event_action": "created", "task_id": "ERDOS-CATALOGUE-1220-S01",
                        "comment_id": 77, "comment_body_sha256": hashlib.sha256(self.body.encode()).hexdigest()}
        self.report = {"tasks": [{"issue_number": self.issue, "task_id": self.receipt["task_id"]}],
                       "receipts": [self.receipt]}

    def test_registry_bound_valid_receipt(self):
        self.assertEqual(mod.validate_receipt(self.report, self.issue)["comment_id"], 77)

    def test_duplicate_delivery_is_idempotent(self):
        receipt = mod.validate_receipt({**self.report, "receipts": [self.receipt, self.receipt]}, self.issue)
        self.assertEqual(self.receipt["comment_id"], receipt["comment_id"])

    def test_no_registry_binding_fail_closed(self):
        with self.assertRaises(ValueError):
            mod.validate_receipt({**self.report, "tasks": []}, self.issue)

    def test_invalid_result_fail_closed(self):
        bad = {**self.receipt, "validation": "REJECTED"}
        with self.assertRaises(ValueError):
            mod.validate_receipt({**self.report, "receipts": [bad]}, self.issue)

    def test_already_closed_done_return_is_terminal_and_never_demoted(self):
        def gh(*args):
            if args[1].endswith("/issues/2491"):
                return {"state":"closed","labels":[{"name":x} for x in
                        ("gcl-job","gcl-pickup:direct-editorial","gcl-role:source-audit")]}
            if args[1].endswith("/issues/comments/77"):
                return {"issue_url":"https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/issues/2491",
                        "body":self.body}
            raise AssertionError(f"unexpected API: {args}")
        with patch.object(mod,"gh",side_effect=gh), \
             patch.object(mod,"project_metadata",return_value=("PROJECT","FIELD","RETURNED")), \
             patch.object(mod,"issue_project_item",return_value={"id":"ITEM","status":"Done"}), \
             patch.object(mod.subprocess,"run") as mutation:
            for dry in (False,True):
                receipt=mod.reconcile(self.report,self.issue,dry)
                self.assertEqual(receipt["target"],"PRESERVE_DONE")
                self.assertEqual(receipt["verified_status"],"Done")
                self.assertTrue(receipt["historical_terminal"])
                self.assertFalse(receipt["available_removed"])
            mutation.assert_not_called()

    def test_closed_nonterminal_project_is_rejected_without_write(self):
        def gh(*args):
            if args[1].endswith("/issues/2491"):
                return {"state":"closed","labels":[{"name":x} for x in
                        ("gcl-job","gcl-pickup:direct-editorial","gcl-role:source-audit")]}
            if args[1].endswith("/issues/comments/77"):
                return {"issue_url":"https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/issues/2491",
                        "body":self.body}
            raise AssertionError("unrecognized API")
        with patch.object(mod,"gh",side_effect=gh), \
             patch.object(mod,"project_metadata",return_value=("PROJECT","FIELD","RETURNED")), \
             patch.object(mod,"issue_project_item",return_value={"id":"ITEM","status":"Todo"}), \
             patch.object(mod.subprocess,"run") as mutation:
            with self.assertRaisesRegex(ValueError,"closed source return lacks terminal Done custody"):
                mod.reconcile(self.report,self.issue,False)
            mutation.assert_not_called()

    def test_issue_field_requires_exact_bound_identity(self):
        valid=[{"issue_field_name":"GCL State","issue_field_id":mod.GCL_STATE_FIELD,
                "single_select_option":{"name":"AVAILABLE"}}]
        with patch.object(mod,"gh",return_value=valid):
            self.assertEqual(mod.source_issue_gcl_state(self.issue),"AVAILABLE")
        for bad in ([],valid+valid,[{**valid[0],"issue_field_id":99}],
                    [{**valid[0],"single_select_option":{"name":"CANCELLED"}}]):
            with self.subTest(bad=bad), patch.object(mod,"gh",return_value=bad):
                with self.assertRaises(ValueError):
                    mod.source_issue_gcl_state(self.issue)

    def test_open_return_converges_project_issuefield_and_label(self):
        state={"project":"Todo","field":"AVAILABLE","labels":{
               "gcl-job","gcl-pickup:direct-editorial","gcl-role:source-audit",
               "gcl-state:available"}}
        writes=[]
        def gh(*args):
            path=args[1]
            if path.endswith("/issues/2491"):
                return {"state":"open","labels":[{"name":x} for x in state["labels"]]}
            if path.endswith("/issues/comments/77"):
                return {"issue_url":"https://api.github.com/repos/grandchallenge/MATH-PROGRAMME/issues/2491",
                        "body":self.body}
            if path.endswith("/issue-field-values"):
                return [{"issue_field_name":"GCL State",
                         "issue_field_id":mod.GCL_STATE_FIELD,
                         "single_select_option":{"name":state["field"]}}]
            raise AssertionError(path)
        def write(argv,**kw):
            writes.append((argv,kw))
            if argv[1]=="project":
                state["project"]="RETURNED"
            elif argv[3]=="POST":
                self.assertIn(str(mod.GCL_STATE_FIELD),kw["input"])
                state["field"]="RETURNED"
            elif argv[3]=="DELETE":
                state["labels"].remove("gcl-state:available")
            else:
                raise AssertionError(argv)
        with patch.object(mod,"gh",side_effect=gh), \
             patch.object(mod,"project_metadata",return_value=("PROJECT","FIELD","OPTION")), \
             patch.object(mod,"issue_project_item",
                side_effect=lambda n,p:{"id":"ITEM","status":state["project"]}), \
             patch.object(mod.subprocess,"run",side_effect=write):
            receipt=mod.reconcile(self.report,self.issue,False)
            self.assertEqual(receipt["verified_status"],"RETURNED")
            self.assertEqual(receipt["verified_gcl_state"],"RETURNED")
            self.assertTrue(receipt["available_removed"])
            self.assertEqual(len(writes),3)
            writes.clear()
            replay=mod.reconcile(self.report,self.issue,False)
            self.assertEqual(replay["verified_gcl_state"],"RETURNED")
            self.assertEqual(writes,[])

    @patch.object(mod, "graph")
    def test_missing_project_state_no_mutation(self, graphql):
        graphql.return_value = {"organization": {"projectV2": {
            "id": "PROJECT", "fields": {"pageInfo": {"hasNextPage": False},
            "nodes": [{"name": "Status", "id": "F", "options": [{"name": "Todo", "id": "T"}]}]}
        }}}
        with self.assertRaisesRegex(ValueError, "one RETURNED option"):
            mod.project_metadata()
        graphql.assert_called_once()

    @patch.object(mod, "graph")
    def test_targeted_project_membership_and_status(self, graphql):
        graphql.return_value = {"repository": {"issue": {
            "projectItems": {"pageInfo": {"hasNextPage": False}, "nodes": [
                {"id": "ITEM", "project": {"id": "PROJECT", "number": 2},
                 "fieldValueByName": {"name": "RETURNED"}}
            ]}
        }}}
        self.assertEqual(mod.issue_project_item(self.issue, "PROJECT"),
                         {"id": "ITEM", "status": "RETURNED"})
        self.assertEqual(graphql.call_count, 1)

    @patch.object(mod, "graph")
    def test_targeted_project_membership_ambiguity_fails_closed(self, graphql):
        graphql.return_value = {"repository": {"issue": {
            "projectItems": {"pageInfo": {"hasNextPage": True}, "nodes": []}
        }}}
        with self.assertRaisesRegex(ValueError, "paginated"):
            mod.issue_project_item(self.issue, "PROJECT")




# The protected catalogue projector also reconciles completed critic returns.
c = mod
ROSTER = json.loads(c.ROSTER.read_text())

class ReviewCompletionTests(unittest.TestCase):
    def test_protected_roster_bindings(self):
        x=c.roster_rows(ROSTER)
        self.assertEqual(len(x),14)
        self.assertEqual(x[11]["issue"],2520)
        self.assertEqual(x[41]["issue"],2536)

    def test_wrong_issue_binding_fails(self):
        r=copy.deepcopy(ROSTER)
        next(x for x in r["items"] if x["problem_id"]==11)["source_critical_review_issue"]=9999
        with self.assertRaisesRegex(ValueError,"bound changed"):c.roster_rows(r)

    def test_original_result_required(self):
        r=copy.deepcopy(ROSTER)
        next(x for x in r["items"] if x["problem_id"]==11)["worker_result_comment_id"]=None
        with self.assertRaises(ValueError):c.roster_rows(r)

    def comment(self,text="REVISE",author="fyremael",i=13):
        return {"body":"GCL-CRITICAL-REVIEW/1\nDISPOSITION: "+text+"\n",
                "id":i,"html_url":"https://github.com/org/repo/issues/2520#issuecomment-"+str(i),
                "user":{"login":author}}

    def test_review_exact_disposition(self):
        v=c.parse_review if hasattr(c,"parse_review") else c.review_comment
        with patch.object(c.old,"gh",return_value=[self.comment()]):
            self.assertEqual(v(2520,"REVISE")["comment_id"],13)

    def test_review_wrong_actor_rejected(self):
        with patch.object(c.old,"gh",return_value=[self.comment(author="untrusted")]):
            with self.assertRaises(ValueError):c.review_comment(2520,"REVISE")

    def test_review_wrong_disposition_rejected(self):
        with patch.object(c.old,"gh",return_value=[self.comment()]):
            with self.assertRaises(ValueError):c.review_comment(2520,"SOURCE_ACCEPTED")

    def test_review_duplicates_rejected(self):
        with patch.object(c.old,"gh",return_value=[self.comment(),self.comment(i=14)]):
            with self.assertRaises(ValueError):c.review_comment(2520,"REVISE")

    def test_review_missing_and_pagination_rejected(self):
        with patch.object(c.old,"gh",return_value=[]):
            with self.assertRaises(ValueError):c.review_comment(2520,"REVISE")
        with patch.object(c.old,"gh",return_value=[self.comment()]*100):
            with self.assertRaises(ValueError):c.review_comment(2520,"REVISE")

    def mock_preflight(self,states=None,review_labels=False):
        states=states or {}
        def details(task):
            nr=task["issue"]
            return {"labels":[{"name":v} for v in
                 ["gcl-state:available","gcl-job","gcl-pickup:direct-editorial",
                  "gcl-role:source-audit"]+
                 ([c.CORRECTED_LABEL] if nr in c.COUNCIL_CORRECTIONS else [])+
                 ([c.REVISE_LABEL] if review_labels else [])]}
        def status(item):
            return {"name":states.get("project","Todo"),
                    "optionId":"option1" if states.get("project")=="RETURNED" else "option0"}
        patches=[
            patch.object(c.old,"verified_source_issue",side_effect=details),
            patch.object(c,"roster_rows",return_value=c.roster_rows(ROSTER)),
            patch.object(c,"status_options",return_value={"Todo":"option0","RETURNED":"option1"}),
            patch.object(c,"review_comment",return_value={"comment_id":1,"comment_sha256":"sha"}),
            patch.object(c,"council_correction",side_effect=lambda issue,problem:
                         {"comment_id":c.COUNCIL_CORRECTIONS[issue][1],"comment_sha256":"council-locked"}
                         if issue in c.COUNCIL_CORRECTIONS else None),
            patch.object(c.old,"issue_fields",return_value={"GCL State":states.get("issue","AVAILABLE")}),
            patch.object(c.old,"project_item_for_issue",return_value="item1"),
            patch.object(c.old,"project_status",side_effect=status),
        ]
        return patches

    def test_preflight_all_fourteen(self):
        from contextlib import ExitStack
        with ExitStack() as st:
            for p in self.mock_preflight():st.enter_context(p)
            d=c.preflight()
        self.assertEqual(len(d["rows"]),14)
        self.assertEqual(sum(x["disposition"]=="REVISE" for x in d["rows"]),5)

    def test_preflight_rejects_revision_label_on_accepted(self):
        from contextlib import ExitStack
        with ExitStack() as st:
            for p in self.mock_preflight(review_labels=True):st.enter_context(p)
            with self.assertRaisesRegex(ValueError,"(Council correction|source-accepted)"):c.preflight()

    def test_preflight_rejects_invalid_project_status(self):
        from contextlib import ExitStack
        with ExitStack() as st:
            for p in self.mock_preflight(states={"project":"In Progress"}):st.enter_context(p)
            with self.assertRaises(ValueError):c.preflight()

    def test_preflight_accepts_half_returned_state(self):
        from contextlib import ExitStack
        with ExitStack() as st:
            for p in self.mock_preflight(states={"project":"RETURNED","issue":"RETURNED"}):
                st.enter_context(p)
            self.assertEqual(c.preflight()["rows"][0]["gcl_state"],"RETURNED")

    def test_apply_all_fourteen_and_replay(self):
        state={}
        rows=[]
        for n,(issue,disposition) in c.TARGET.items():
            state[issue]={"project":"Todo","field":"AVAILABLE",
                          "labels":{"gcl-state:available"} |
                              ({c.CORRECTED_LABEL} if issue in c.COUNCIL_CORRECTIONS else set())}
            rows.append({"problem":n,"issue":issue,"disposition":disposition,
                         "comment":{"comment_id":issue,"comment_sha256":"stable"},
                         "project_item":"item"+str(issue),"project_status":"Todo",
                         "gcl_state":"AVAILABLE","available_label":True,
                         "revise_label":False,
                         "council_correction":({"comment_id":c.COUNCIL_CORRECTIONS[issue][1],
                                                "comment_sha256":"council-locked"}
                                               if issue in c.COUNCIL_CORRECTIONS else None)})
        snap={"rows":rows,"returned_option":"optionRETURNED"}
        writes=[]
        def fake_mutation(*args,data=None):
            writes.append(args)
            if args[0]=="project":
                issue=int(args[args.index("--id")+1].removeprefix("item"))
                state[issue]["project"]="RETURNED"
            else:
                issue=int(args[1].split("/issues/")[1].split("/")[0])
                if "issue-field-values" in args[1]:
                    self.assertEqual(data["issue_field_values"][0]["value"],"RETURNED")
                    state[issue]["field"]="RETURNED"
                elif args[1].endswith("gcl-state%3Aavailable"):
                    state[issue]["labels"].discard("gcl-state:available")
                else:
                    self.assertEqual(data,{"labels":[c.REVISE_LABEL]})
                    state[issue]["labels"].add(c.REVISE_LABEL)
        def label_issue(issue):
            return {"state":"open","labels":[{"name":n} for n in state[issue]["labels"]]}
        def status(item):
            issue=int(item.removeprefix("item"))
            return {"name":state[issue]["project"],"optionId":"optionRETURNED"}
        with patch.object(c,"ensure_revision_label"), \
             patch.object(c,"mutation",side_effect=fake_mutation), \
             patch.object(c.old,"project_item_for_issue",side_effect=lambda issue:"item"+str(issue)), \
             patch.object(c.old,"project_status",side_effect=status), \
             patch.object(c.old,"issue_fields",side_effect=lambda issue:{"GCL State":state[issue]["field"]}), \
             patch.object(c.old,"issue",side_effect=label_issue), \
             patch.object(c,"review_comment",side_effect=lambda issue,d:{"comment_id":issue,"comment_sha256":"stable"}), \
             patch.object(c,"council_correction",side_effect=lambda issue,problem:
                          {"comment_id":c.COUNCIL_CORRECTIONS[issue][1],"comment_sha256":"council-locked"}
                          if issue in c.COUNCIL_CORRECTIONS else None):
            result=c.apply(snap)
            self.assertEqual(len(result),14)
            self.assertEqual(sum(x["source_correction_accepted"] for x in result),5)
            self.assertEqual(sum(x["source_correction_open"] for x in result),0)
            self.assertEqual(len(writes),14*3)
            for r in rows:
                r["project_status"]="RETURNED"
                r["gcl_state"]="RETURNED"
                r["available_label"]=False
                r["revise_label"]=False
            writes.clear()
            result2=c.apply(snap)
            self.assertEqual(len(result2),14)
            self.assertEqual(writes,[])

    def test_protected_council_corrections_accept_only_bot_exact_sources(self):
        for issue,(problem,comment_id,prefix,material,pr) in c.COUNCIL_CORRECTIONS.items():
            lines=[prefix,f"ERDOS_PROBLEM: {problem}",f"REVIEW_ISSUE: #{issue}",
                   "DISPOSITION: SOURCE_CORRECTION_ACCEPTED",
                   f"PROTECTED_SOURCE_LOCK_PR: https://github.com/grandchallenge/MATH-PROGRAMME/pull/{pr}",
                   material,"MATHEMATICAL_CERTIFICATION: FALSE",
                   "OPEN_PROBLEM_STATUS: UNCHANGED"]
            good={"id":comment_id,"body":"\n".join(lines)+"\n",
                  "html_url":f"https://github.com/grandchallenge/MATH-PROGRAMME/issues/{issue}#issuecomment-{comment_id}",
                  "user":{"login":"gcl-council-clerk[bot]"}}
            with self.subTest(issue=issue),patch.object(c.old,"gh",return_value=[good]):
                self.assertEqual(c.council_correction(issue,problem)["comment_id"],comment_id)
            for bad in (
                {**good,"user":{"login":"fyremael"}},
                {**good,"body":good["body"].replace(material,"SHA_CHANGED")},
                {**good,"id":comment_id+1},
            ):
                with self.subTest(issue=issue,mutation=str(bad.get("id"))), patch.object(c.old,"gh",return_value=[bad]):
                    with self.assertRaises(ValueError):
                        c.council_correction(issue,problem)
        with self.assertRaises(ValueError):
            c.council_correction(2522,41)

    def test_apply_guards_untrusted_environment_without_preflight(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict("os.environ",{},clear=True), patch.object(c,"preflight") as pre,                  patch.object(sys,"argv",["controller","--apply","--receipt",tmp+"/receipt.json"]):
                self.assertEqual(c.review_completion_main(),1)
                pre.assert_not_called()
                d=json.loads(Path(tmp,"receipt.json").read_text())
                self.assertIn("untrusted apply context",d["error"])
                self.assertFalse(d["applied"])

    def test_dry_run_no_mutations(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(c,"preflight",return_value={"rows":[]}),                  patch.object(c,"apply") as apply,                  patch.object(sys,"argv",["controller","--dry-run","--receipt",tmp+"/r.json"]):
                self.assertEqual(c.review_completion_main(),0)
                apply.assert_not_called()
                d=json.loads(Path(tmp,"r.json").read_text())
                self.assertTrue(d["complete"])
                self.assertFalse(d["applied"])


if __name__ == "__main__":
    unittest.main()
