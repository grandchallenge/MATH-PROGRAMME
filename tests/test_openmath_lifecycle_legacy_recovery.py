import base64
import json
import unittest

from ci.openmath_lifecycle_controller import (
    BRANCH_PREFIX,
    RECOVERY_PREFIX,
    ControllerError,
    branch_names,
    dispatch_parts,
    legacy_source,
)


class FakeGithub:
    def __init__(self, modified=False):
        self.dispatch="OM26-H3-WP01-IA-001"
        self.branch=f"{BRANCH_PREFIX}{self.dispatch.lower()}"
        self.base="contributions/OPENMATH-2026/OM26-H3/WP01"
        self.cid=5883811624
        self.raw_path=f"{self.base}/raw/{self.dispatch}/github-comment-{self.cid}.md"
        self.receipt_path=f"{self.base}/receipts/{self.dispatch}/github-comment-{self.cid}.json"
        self.raw="GCL-CONTRIBUTION-RESULT/1\ndispatch_id: OM26-H3-WP01-IA-001\n"
        self.receipt={
            "dispatch_id":self.dispatch,
            "assignment_id":"OM26-H3-WP01",
            "agent_ref":"INDEPENDENT-AGENT-003",
            "github_comment_id":self.cid,
            "github_issue_number":506,
            "raw_artifact_path":self.raw_path,
            "schema_result":"valid",
            "canonical_claim_effect":False,
            "handling_state":"received_unadjudicated",
            "result_protocol":"GCL-CONTRIBUTION-RESULT/1",
        }
        self.modified=modified

    def get_optional(self,path):
        if "/git/matching-refs/heads/intake/openmath-" in path:
            return [{"ref":f"refs/heads/{self.branch}"}]
        if "/git/matching-refs/heads/candidate/openmath-" in path:
            return [{"ref":"refs/heads/candidate/openmath-om26-h6-wp01-ia-001"}]
        if f"/raw/{self.dispatch}?" in path:
            return [{"name":f"github-comment-{self.cid}.md"}]
        if f"/receipts/{self.dispatch}?" in path:
            return [{"name":f"github-comment-{self.cid}.json"}]
        return None

    def request(self,method,path,payload=None):
        if method!="GET":
            raise AssertionError("unexpected mutation in read-only test")
        if self.raw_path in path:
            data=self.raw
        elif self.receipt_path in path:
            data=json.dumps(self.receipt)
        elif path.endswith(f"/issues/comments/{self.cid}"):
            return {
                "id":self.cid,
                "issue_url":"https://api.github.com/repos/grandchallenge/MATHSOLVE/issues/506",
                "body":self.raw + ("tampered" if self.modified else ""),
            }
        elif f"/git/ref/heads/{self.branch}" in path:
            return {"object":{"sha":"a"*40}}
        else:
            raise AssertionError(f"unexpected mocked API read: {path}")
        return {
            "content":base64.b64encode(data.encode()).decode(),
            "encoding":"base64",
            "sha":"b"*40,
        }


class OpenMathLegacyRecoveryTest(unittest.TestCase):
    def test_branch_discovery_preserves_both_formats(self):
        names=branch_names(FakeGithub())
        self.assertEqual(names,[
            "candidate/openmath-om26-h6-wp01-ia-001",
            "intake/openmath-om26-h3-wp01-ia-001",
        ])
        self.assertEqual(dispatch_parts(names[0]),("OM26-H6-WP01-IA-001","OM26-H6","WP01"))
        self.assertEqual(dispatch_parts(names[1]),("OM26-H3-WP01-IA-001","OM26-H3","WP01"))

    def test_locked_legacy_receipt_recovered_without_mutation(self):
        gh=FakeGithub()
        result=legacy_source(gh,gh.branch)
        self.assertEqual(result["dispatch_id"],gh.dispatch)
        self.assertEqual(result["raw_text"],gh.raw)
        self.assertEqual(result["receipt"]["schema_result"],"valid")
        self.assertEqual(result["source_commit"],"a"*40)
        self.assertEqual(result["comment_id"],gh.cid)

    def test_modified_source_comment_fails_closed(self):
        gh=FakeGithub(modified=True)
        with self.assertRaises(ControllerError):
            legacy_source(gh,gh.branch)


if __name__=="__main__":
    unittest.main()
