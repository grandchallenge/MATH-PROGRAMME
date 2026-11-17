"""Exact Clerk exception event regression: #1836 closure preceded rejection."""
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from ci import erdos_late_exception_recovery as m

class LateExceptionRecoveryTest(unittest.TestCase):
    def setUp(self):
        self.issue = 1836
        self.cid = 6288214238
        self.body = ("GCL-RETURN-EXCEPTION/1\nISSUE: 1836\n"
                     "PROBLEM: 565\nTYPE: SOURCE_INTEGRITY\n"
                     "REVIEW: REQUIRED, NO SOURCE ACCEPTANCE\n"
                     "DETAIL: duplicate or unsafe header EVIDENCE_AUTHORITY\n")
        self.e = {"action":"created",
                  "repository":{"full_name":m.REPO},
                  "issue":{"number":self.issue},
                  "comment":{"id":self.cid,"body":self.body,
                             "user":{"login":m.BOT}}}
        self.env={"GITHUB_ACTIONS":"true","GITHUB_REPOSITORY":m.REPO,
                  "GITHUB_REF":"refs/heads/main",
                  "GITHUB_EVENT_NAME":"issue_comment",
                  "GCL_RETURN_FASTPATH_CONTROL":"protected-main"}
        self.live={"issue_url":f"https://api.github.com/repos/{m.REPO}/issues/{self.issue}",
                   "body":self.body,"user":{"login":m.BOT}}
        self.registry={"issues":[{"issue_number":self.issue,"problem_id":565}]}

    def fixture(self, directory):
        p=Path(directory)/"event.json"
        p.write_text(json.dumps(self.e))
        return p

    def test_reject_wrong_clerk_issue_and_corpus(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ,self.env), \
            patch.object(m.intake,"load_registry",return_value=self.registry), \
            patch.object(m.project,"gh",return_value=self.live):
            path=self.fixture(d)
            self.assertEqual(m.bound_event(path)[:2],(self.issue,self.cid))
            for bad in ("other-user","not-clerk"):
                self.e["comment"]["user"]["login"]=bad
                path.write_text(json.dumps(self.e))
                with self.assertRaisesRegex(ValueError,"untrusted"):
                    m.bound_event(path)
            self.e["comment"]["user"]["login"]=m.BOT
            self.e["issue"]["number"]=9999
            path.write_text(json.dumps(self.e))
            with self.assertRaises(ValueError):
                m.bound_event(path)

    def test_closed_done_is_reopened_and_project_returns(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ,self.env), \
            patch.object(m.intake,"load_registry",return_value=self.registry):
            path=self.fixture(d)
            state={"issue":"closed","status":"Done"}
            def gh(*args):
                if args[1].endswith(f"/issues/comments/{self.cid}"):
                    return self.live
                if args[1].endswith(f"/issues/{self.issue}"):
                    return {"state":state["issue"],"labels":[{"name":x} for x in
                        ("gcl-job","gcl-pickup:direct-editorial","gcl-role:source-audit")]}
                raise AssertionError(args)
            def metadata(): return ("PROJECT","FIELD","OPTION")
            def item(*args): return {"id":"ITEM","status":state["status"]}
            def update_project(*args): state["status"]="RETURNED"
            def patch_issue(*args,**kwargs):
                state["issue"]="open"
                return None
            with patch.object(m.project,"gh",side_effect=gh), \
                patch.object(m.project,"project_metadata",side_effect=metadata), \
                patch.object(m.project,"issue_project_item",side_effect=item), \
                patch.object(m.project,"apply_returned_project_status",side_effect=update_project), \
                patch.object(m.project,"source_issue_gcl_state",return_value="RETURNED"), \
                patch.object(m.project,"apply_returned_issue_field"), \
                patch.object(m.project,"remove_available_label"), \
                patch.object(m.subprocess,"run",side_effect=patch_issue) as mutation:
                receipt=m.run("capture",path,Path(d))
                self.assertFalse(receipt["source_semantics_accepted"])
                first=m.run("restore",path,Path(d))
                self.assertEqual(first["status"],"VERIFIED_SOURCE_REVIEW_PENDING")
                self.assertEqual(first["issue_state"],"open")
                self.assertEqual(first["project_status"],"RETURNED")
                self.assertFalse(first["source_review_complete"])
                self.assertEqual(mutation.call_count,1)
                # Idempotent reentry must not repeat the issue PATCH.
                again=m.run("restore",path,Path(d))
                self.assertEqual(again["status"],"VERIFIED_SOURCE_REVIEW_PENDING")
                self.assertEqual(mutation.call_count,1)

    def test_missing_protected_control_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as d, patch.dict(os.environ,self.env), \
            patch.object(m.intake,"load_registry",return_value=self.registry), \
            patch.object(m.project,"gh",return_value=self.live):
            p=self.fixture(d)
            m.run("capture",p,Path(d))
            with patch.dict(os.environ,{"GCL_RETURN_FASTPATH_CONTROL":""}):
                with self.assertRaisesRegex(ValueError,"protected Council Clerk control"):
                    m.run("restore",p,Path(d))

if __name__ == "__main__":
    unittest.main()
