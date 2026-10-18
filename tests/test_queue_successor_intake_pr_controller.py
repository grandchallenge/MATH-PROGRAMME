from __future__ import annotations

import base64, hashlib, json, unittest
from unittest.mock import patch

from ci import ns_ci_intake_pr_controller as controller

DISPATCH="ERDOS-593-R2-IA-001"
BASE="contributions/ERDOS-OPEN-001/SUCCESSOR_002"
TASK="handoffs/GCL-WORKER-QUEUE/launch/2026-10-08/ERDOS-593-R2-IA-001.md"
BRANCH="intake/erdos-593-r2-ia-001"
BODY="GCL-CONTRIBUTION-RESULT/1\nbounded result"
COMMENT_ID=8001
TASK_TEXT="immutable exact task"
ISSUE_BODY_SHA="0"*64
BIND={
    "dispatch_id":DISPATCH,
    "campaign":"ERDOS-OPEN",
    "dispatch_path":BASE+"/dispatches/"+DISPATCH+".json",
    "github_issue_number":1008,
    "issue_body_sha256":ISSUE_BODY_SHA,
    "task_path":TASK,
    "task_commit":"3"*40,
    "task_sha256":hashlib.sha256(TASK_TEXT.encode()).hexdigest(),
    "allowed_dispositions":["PROVED_REDUCTION"],
    "allowed_external_sources":["PRIMARY_SOURCES_REQUIRED"],
}
DISPATCH_DATA={
    "dispatch_id":DISPATCH,
    "campaign":"ERDOS-OPEN",
    "dispatch_status":"READY_FOR_GITHUB_COMMENT",
    "return_protocol":"GCL-CONTRIBUTION-RESULT/1",
    "canonical_mutation_authorized":False,
    "assignment_id":"ERDOS-593-R2",
    "agent_ref":"INDEPENDENT-AGENT-ERDOS-593-R2",
    "source_handoff_commit_sha":"3"*40,
    "github_issue_number":1008,
    "task_path":TASK,
    "task_commit":"3"*40,
}
RAW=f"{BASE}/raw/{DISPATCH}/github-comment-{COMMENT_ID}.md"
RECEIPT_PATH=f"{BASE}/receipts/{DISPATCH}/github-comment-{COMMENT_ID}.json"
RECEIPT={
    "schema_version":"1.0.0",
    "dispatch_id":DISPATCH,
    "assignment_id":"ERDOS-593-R2",
    "agent_ref":"INDEPENDENT-AGENT-ERDOS-593-R2",
    "result_protocol":"GCL-CONTRIBUTION-RESULT/1",
    "github_issue_number":1008,
    "github_comment_id":COMMENT_ID,
    "raw_artifact_path":RAW,
    "raw_sha256":hashlib.sha256(BODY.encode()).hexdigest(),
    "source_handoff_commit_sha":"3"*40,
    "schema_result":"valid",
    "freshness":"current_for_dispatch",
    "handling_state":"received_unadjudicated",
    "mathematical_correctness_adjudicated":False,
    "independence_strength_adjudicated":False,
    "canonical_claim_effect":False,
    "intake_binding_kind":"PROTECTED_QUEUE_TASK_AND_ISSUE_DIGEST",
    "task_path":TASK,
    "task_commit":"3"*40,
    "task_sha256":BIND["task_sha256"],
    "issue_body_sha256":ISSUE_BODY_SHA,
    "certification_effect":False,
    "queue_managed":True,
    "worker_reservation_enforced":True,
    "worker_reservation_owner":"reviewer",
    "authenticated_github_actor":"reviewer",
}
def content(data):
    return {
        "encoding":"base64",
        "content":base64.b64encode(json.dumps(data).encode()).decode(),
        "sha":"1"*40,
    }
class GH:
    def __init__(self,manifest=None,has_branch=True):
        self.manifest=manifest if manifest is not None else {
            "record_type":"GCL_QUEUE_INTAKE_BINDINGS","schema_version":"1.0.0",
            "authority_effect":{"queue_operation_only":True,"mathematical":False,"certification":False},
            "bindings":[BIND]
        }
        self.has_branch=has_branch
    def get_optional(self,path):
        if "INTAKE_BINDINGS.json" in path:return content(self.manifest)
        if path.endswith("ref="+__import__("urllib.parse",fromlist=["quote"]).quote(BRANCH,safe="")):return [{"name":f"github-comment-{COMMENT_ID}.json"}] if self.has_branch else None
        return None
    def request(self,method,path):
        if method=="GET" and "/pulls?state=open" in path:return []
        raise AssertionError((method,path))

class QueueControllerTests(unittest.TestCase):
    def test_new_queue_dispatch_recognized_from_protected_manifest(self):
        gh=GH()
        p,id=controller.profile_for_branch(BRANCH,gh)
        self.assertEqual(id,DISPATCH)
        self.assertEqual(p.campaign,"ERDOS-OPEN")
        self.assertEqual(p.base,BASE)
        self.assertEqual(controller.expected_paths(DISPATCH,COMMENT_ID,gh),(RAW,RECEIPT_PATH))

    def test_missing_manifest_fails_closed(self):
        gh=GH({"record_type":"GCL_QUEUE_INTAKE_BINDINGS","schema_version":"1.0.0",
               "authority_effect":{"queue_operation_only":True,"mathematical":False,"certification":False},
               "bindings":[]})
        with self.assertRaises(controller.ControllerError):
            controller.profile_for_branch(BRANCH,gh)

    def test_unopened_branch_discovered_by_exact_manifest_receipt_directory(self):
        self.assertIn(BRANCH,controller.list_intake_branches(GH()))
        self.assertNotIn(BRANCH,controller.list_intake_branches(GH(has_branch=False)))

    def test_no_unlisted_branch_discovery(self):
        gh=GH()
        with self.assertRaises(controller.ControllerError):
            controller.profile_for_dispatch("ERDOS-593-R9-IA-001",gh)

    def test_protected_branch_candidate_validates_queue_receipt(self):
        gh=GH()
        def fetch(_gh,path,ref):
            if path == BIND["dispatch_path"] and ref=="main":return json.dumps(DISPATCH_DATA),"d"*40
            if path == RAW and ref==BRANCH:return BODY,"e"*40
            if path == RECEIPT_PATH and ref==BRANCH:return json.dumps(RECEIPT),"f"*40
            if path == TASK and ref=="main":return TASK_TEXT,"a"*40
            raise AssertionError((path,ref))
        with (
            patch.object(controller,"fetch_text",side_effect=fetch),
            patch.object(controller,"compare_files",return_value=[RAW,RECEIPT_PATH]),
            patch.object(controller,"main_has_any_raw",return_value=False),
            patch.object(controller,"find_open_pr",return_value=None),
        ):
            out=controller.validate_candidate(gh,BRANCH)
        self.assertEqual(out["state"],"PR_REQUIRED")
        self.assertEqual(out["github_comment_id"],COMMENT_ID)

    def test_tampered_authenticated_owner_rejected(self):
        gh=GH()
        receipt=dict(RECEIPT,worker_reservation_owner="different")
        def fetch(_gh,path,ref):
            if path == BIND["dispatch_path"]:return json.dumps(DISPATCH_DATA),"d"*40
            if path == RAW:return BODY,"e"*40
            if path == RECEIPT_PATH:return json.dumps(receipt),"f"*40
            if path == TASK:return TASK_TEXT,"a"*40
            raise AssertionError(path)
        with (
            patch.object(controller,"fetch_text",side_effect=fetch),
            patch.object(controller,"compare_files",return_value=[RAW,RECEIPT_PATH]),
        ):
            with self.assertRaisesRegex(controller.ControllerError,"queue_reservation_owner"):
                controller.validate_candidate(gh,BRANCH)

if __name__=="__main__":
    unittest.main()
