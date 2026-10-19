import copy
import hashlib
import json
import subprocess
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from ci import erdos_catalogue_programme_intake as intake
from ci import erdos_return_exceptions as ex
from ci import erdos_return_arbitration as arbitration
from ci import verify_erdos_return_exceptions as aggregate


class ReturnExceptions(unittest.TestCase):
    def setUp(self):
        self.issue=1273
        self.problem=4
        self.content="Precise mathematical statement, source reference and a bounded falsification obligation."
        self.body=("RESULT/1\nASSIGNMENT_ID: ERDOS-CATALOGUE-0004-S01\n"
                   "PROBLEM_ID: 4\nDISPOSITION: PARTIAL\nCONTEXT_CLASS: ZERO_CONTEXT\n"
                   "TIMEBOX_OBSERVED: NO\nPINNED_CATALOGUE: exact-test-source@a1\n\n"+
                   "\n\n".join(f"## {h}\n{self.content} {i}" for i,h in enumerate(intake.SECTIONS)))
        self.receipt={"issue_number":self.issue,"comment_id":9001,"problem_id":4,
                      "comment_body_sha256":ex.sha(self.body.encode()),
                      "validation":"REJECTED",
                      "errors":["invalid, duplicate, or unsupported return header"]}
        self.report={"tasks":[{"issue_number":self.issue,"problem_id":4}],
                     "receipts":[self.receipt]}

    def test_header_relocation_preserves_all_content(self):
        with self.assertRaises(intake.IntakeError):
            intake.parse_return(self.body,4)
        result=ex.normalize(self.body,4,9001,self.receipt["comment_body_sha256"],self.issue)
        self.assertEqual(intake.parse_return(result,4)["worker_reported_disposition"],"PARTIAL")
        self.assertIn("PINNED_CATALOGUE: exact-test-source@a1",result)
        self.assertIn("issuecomment-9001",result)
        self.assertIn("Original SHA-256:",result)
        for i in range(6):
            self.assertIn(f"{self.content} {i}",result)
        self.assertIn("Not a second independent worker return",result)

    def test_missing_sections_and_identity_mismatch_fail_closed(self):
        incomplete=self.body.replace("## Prerequisites and blocker","### Prerequisites and blocker")
        with self.assertRaisesRegex(ValueError,"six"):
            ex.normalize(incomplete,4,9001,ex.sha(incomplete.encode()),self.issue)
        mismatch=self.body.replace("PROBLEM_ID: 4","PROBLEM_ID: 5")
        with self.assertRaisesRegex(ValueError,"identity"):
            ex.normalize(mismatch,4,9001,ex.sha(mismatch.encode()),self.issue)
        unsafe=self.body.replace("PINNED_CATALOGUE:","AUTHORIZE_SOLVE:")
        with self.assertRaisesRegex(ValueError,"unsafe"):
            ex.normalize(unsafe,4,9001,ex.sha(unsafe.encode()),self.issue)

    def test_manifest_bounds_and_no_duplicate_source_tasks(self):
        m=ex.manifest(self.report,16,"f"*64)
        self.assertEqual(m["include"][0]["issues"],[self.issue])
        with self.assertRaises(ValueError):
            ex.manifest(self.report,17,"f"*64)
        self.report["tasks"].append(self.report["tasks"][0])
        with self.assertRaises(ValueError):
            ex.exceptions(self.report)

    def test_protected_arbitration_needs_full_comparison_and_exact_hashes(self):
        rows=[{"comment_id":11,"comment_body_sha256":"a"*64},
              {"comment_id":12,"comment_body_sha256":"b"*64}]
        with self.assertRaisesRegex(ValueError,"missing"):
            arbitration.choose(self.issue,rows,decisions={})
        decision={"disposition":"SELECT_FOR_QUEUE_ONLY","selected_comment_id":12,
                  "candidate_comment_sha256":{"11":"a"*64,"12":"b"*64},
                  "source_specialist":"specialist-role-source-audit",
                  "protected_review_pr":"https://github.com/grandchallenge/MATH-PROGRAMME/pull/100",
                  "comparative_review":"Conflicting source interpretations require independent comparative replay. "*4,
                  "selection_rationale":"Selected item 12 reproduces the exact source interpretation and rejects the alternative. "*2,
                  "source_claim_accepted":False,"mathematical_certification":False}
        self.assertEqual(12,arbitration.choose(self.issue,rows,decisions={self.issue:decision})["comment_id"])
        decision["candidate_comment_sha256"]["11"]="c"*64
        with self.assertRaisesRegex(ValueError,"stale"):
            arbitration.choose(self.issue,rows,decisions={self.issue:decision})

    def test_live_repair_publishes_once_with_readback(self):
        fake_issue={"number":self.issue,"body":"frozen issue",
                    "title":"[GCL-ERDOS] ERDOS-CATALOGUE-0004-S01 — Problem 4: source audit",
                    "labels":[{"name":x} for x in intake.LABELS]}
        registry={"issues":[{"issue_number":self.issue,"issue_body_sha256":intake.sha("frozen issue")}]}
        returned={"id":9001,"body":self.body,
                  "issue_url":f"https://api.github.com/repos/{intake.REPOSITORY}/issues/{self.issue}"}
        derived=[]
        def fake_gh(endpoint,*,post=None):
            if endpoint.endswith("/comments/9001"):return returned
            if endpoint.endswith(f"/issues/{self.issue}") and post is None:return fake_issue
            if endpoint.endswith(f"/issues/{self.issue}/comments?per_page=100"):
                return derived.copy()
            if post is not None:
                value=json.loads(post)["body"]
                entry={"id":9002,"body":value,"issue_url":returned["issue_url"]}
                derived.append(entry)
                return entry
            if endpoint.endswith("/comments/9002"):return derived[0]
            raise AssertionError(endpoint)
        with patch.object(ex,"gh",side_effect=fake_gh),patch.object(intake,"load_registry",return_value=registry):
            first=ex.process_issue(self.report,self.issue,apply=True)
            second=ex.process_issue(self.report,self.issue,apply=True)
        self.assertEqual("POSTED",first["effect"])
        self.assertEqual("ALREADY_EXISTS",second["effect"])
        self.assertTrue(first["readback"])
        self.assertEqual(1,len(derived))
        intake.parse_return(derived[0]["body"],4)

    def test_aggregate_requires_exact_successful_batch_and_reports_pending(self):
        digest="e"*64
        entry=ex.manifest(self.report,16,digest)["include"][0]
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            folder=root/"gcl-return-exception-batch-0-123-1"
            folder.mkdir()
            valid={"schema":ex.SCHEMA,"status":"VERIFIED_BATCH","verified":True,
                   "applied":True,"report_sha256":digest,"protected_head":"a"*40,
                   "run_id":"123","batch":entry,"blocker":None,
                   "in_flight_issue":None,"results":[{
                       "issue":self.issue,"kind":"SOURCE_INTEGRITY",
                       "effect":"POSTED","readback":True,
                       "posted_comment_id":9023,
                       "derived_sha256":"f"*64}]}
            receipt=folder/"receipt.json"
            receipt.write_text(json.dumps(valid))
            summary=aggregate.verify(self.report,ex.manifest(self.report,16,digest),
                                     digest,root,"123","1","a"*40)
            self.assertTrue(summary["verified"])
            self.assertFalse(summary["fully_remediated"])
            self.assertEqual(summary["unresolved_source_reviews"],1)
            valid["results"][0]["readback"]=False
            receipt.write_text(json.dumps(valid))
            with self.assertRaisesRegex(ValueError,"unverified"):
                aggregate.verify(self.report,ex.manifest(self.report,16,digest),
                                 digest,root,"123","1","a"*40)
            receipt.unlink()
            with self.assertRaises(OSError):
                aggregate.verify(self.report,ex.manifest(self.report,16,digest),
                                 digest,root,"123","1","a"*40)

    def test_transient_lost_post_response_does_not_duplicate(self):
        path=f"repos/{intake.REPOSITORY}/issues/{self.issue}/comments"
        body=json.dumps({"body":"exact payload"})
        existing={"id":9003,"body":"exact payload",
                  "issue_url":f"https://api.github.com/repos/{intake.REPOSITORY}/issues/{self.issue}"}
        calls=[]
        def fake_run(command,**kwargs):
            calls.append(command)
            if len(calls)==1:
                return subprocess.CompletedProcess(command,1,"","HTTP 503 service unavailable")
            return subprocess.CompletedProcess(command,0,json.dumps([existing]),"")
        with patch.object(ex.subprocess,"run",side_effect=fake_run):
            result=ex.gh(path,post=body)
        self.assertEqual(result["id"],9003)
        self.assertEqual(len(calls),2)
        self.assertIn("--method",calls[0])
        self.assertNotIn("--method",calls[1])

    def test_transient_post_retry_after_exact_negative_probe(self):
        path=f"repos/{intake.REPOSITORY}/issues/{self.issue}/comments"
        body=json.dumps({"body":"exact payload"})
        posted={"id":9005,"body":"exact payload"}
        calls=[]
        def fake_run(command,**kwargs):
            calls.append(command)
            if len(calls)==1:
                return subprocess.CompletedProcess(command,1,"","HTTP 429 secondary rate limit")
            if len(calls)==2:
                return subprocess.CompletedProcess(command,0,"[]","")
            return subprocess.CompletedProcess(command,0,json.dumps(posted),"")
        with patch.object(ex.subprocess,"run",side_effect=fake_run),patch.object(ex.time,"sleep") as pause:
            actual=ex.gh(path,post=body)
        self.assertEqual(actual["id"],9005)
        self.assertEqual(len(calls),3)
        pause.assert_called_once_with(4)

    def test_permanent_error_fails_with_actual_api_reason(self):
        path=f"repos/{intake.REPOSITORY}/issues/{self.issue}/comments"
        calls=[]
        def fake_run(command,**kwargs):
            calls.append(command)
            if len(calls)==1:
                return subprocess.CompletedProcess(command,1,"","HTTP 422 Validation Failed: body invalid")
            return subprocess.CompletedProcess(command,0,"[]","")
        with patch.object(ex.subprocess,"run",side_effect=fake_run):
            with self.assertRaisesRegex(ValueError,"HTTP 422 Validation Failed"):
                ex.gh(path,post=json.dumps({"body":"bad body"}))
        self.assertEqual(len(calls),2)

    def test_unreadable_probe_blocks_an_uncertain_write(self):
        path=f"repos/{intake.REPOSITORY}/issues/{self.issue}/comments"
        post=json.dumps({"body":"source report"})
        calls=[]
        def fake_run(command,**kwargs):
            calls.append(command)
            return subprocess.CompletedProcess(command,1,"","HTTP 503 unavailable")
        with patch.object(ex.subprocess,"run",side_effect=fake_run),patch.object(ex.time,"sleep"):
            with self.assertRaisesRegex(ValueError,"duplicate-safe probe failed"):
                ex.gh(path,post=post)
        self.assertEqual(sum("--method" in x for x in calls),4)


if __name__=="__main__":
    unittest.main()
