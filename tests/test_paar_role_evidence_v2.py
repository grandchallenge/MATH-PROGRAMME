import hashlib
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ci"))
from agent_role_receipt import AgentRoleError, CHECKS, NEW_RECEIPT, NEW_DOSSIER, EXECUTION_RECORD, verify_agent_role_receipt

H="a"*40
S="b"*40
P="c"*40
B="d"*40
M="e"*64
ACTOR="fyremael"
SUB={"repository":"grandchallenge/MATH-PROGRAMME","head_sha":H,"material_sha256":M}
DOS=f"governance/agent_execution/reviews/MATH-PROGRAMME-{H}.json"
ORIGIN="/repos/grandchallenge/INTELLECT"

class RoleEvidenceV2Tests(unittest.TestCase):
    def setUp(self):
        self.passes=[]
        self.outputs={}
        self.files=[{"filename":DOS,"sha":B,"status":"added"}]
        for i,role in enumerate(("VERIFIER","ADVERSARY","REFEREE")):
            ident=f"test-{role}-{i}"
            path=f"governance/agent_execution/executions/MATH-PROGRAMME-{H}/{role.lower()}-0.json"
            blob=str(i+1)*40
            command="python test_"+role.lower()+".py"
            raw="Ran "+str(i+1)+" tests\nOK\n"
            self.outputs[path]=[{"record_type":EXECUTION_RECORD,"subject":SUB,"role":role,
                "logical_pass_id":ident,"reviewer_system_id":"GPT-6","transport_login":ACTOR,
                "mode":"non_authoring_read_only","command":command,"exit_code":0,
                "finding":"PASS","environment":{"python":"3.12","os":"linux","toolchain":"python unittest"},
                "observed_utc":"2026-10-16T12:00:00Z",
                "output":{"stdout":"","stderr":raw,"selected_stream":"stderr"}},blob]
            self.files.append({"filename":path,"sha":blob,"status":"added"})
            pp={"role":role,"logical_pass_id":ident,"reviewer_system_id":"GPT-6",
                "transport_login":ACTOR,"subject_head_sha":H,"mode":"non_authoring_read_only",
                "read_set":["test"],"write_set":[],"finding":"ACCEPT_BOUNDED","unresolved":[],
                "checks":[{"command":command,"exit_code":0,
                  "receipt_sha256":hashlib.sha256(raw.encode()).hexdigest(),
                  "execution_evidence":{"path":path,"blob_sha":blob}}]}
            if role=="ADVERSARY":pp["negative_controls"]=["hostile"]
            self.passes.append(pp)
        self.dossier={"record_type":NEW_DOSSIER,"subject":SUB,"work_class":"MATERIAL_CONTROL",
            "transport_login":ACTOR,"claimed_effects":{"mathematical_certification":False,
            "reserved_authorization":False,"credential_escalation":False},"passes":self.passes}
        self.receipt={"schema_version":"3.0.0","record_type":NEW_RECEIPT,
            "source_repository":"grandchallenge/INTELLECT","authority_domain":"PROTECTION",
            "subject":SUB,"verdict":"ADMISSIBLE_FOR_PROTECTED_ADMISSION",
            "protected_evidence":{"path":DOS,"blob_sha":B},
            "source_review_anchor":{"source_pr_number":301,"source_pr_head_sha":S,
                                    "review_dossier_blob_sha":B}}
        self.reviews=[{"id":77,"state":"APPROVED","commit_id":S,
            "submitted_at":"2026-10-16T12:20:00Z","user":{"login":"jimsteeg"}}]
        self.author=ACTOR;self.ci="success";self.branch=P

    def read(self,repo,path,head):
        assert repo=="grandchallenge/INTELLECT" and head==P
        if path==DOS:return self.dossier,B
        return self.outputs[path]

    def api(self,path):
        pr=ORIGIN+"/pulls/301"
        if path==pr:return {"merged_at":"2026-10-16T12:30:00Z","head":{"sha":S},
                            "base":{"ref":"main"},"user":{"login":self.author},
                            "changed_files":len(self.files)}
        if path==pr+"/reviews?per_page=100":return self.reviews
        if path==pr+"/files?per_page=100":return self.files
        if path==ORIGIN+f"/commits/{S}/check-runs?per_page=100":
            return {"total_count":len(CHECKS),"check_runs":[
                {"name":x,"conclusion":self.ci,"head_sha":S} for x in CHECKS]}
        if path==ORIGIN+"/git/ref/heads/main":return {"object":{"sha":self.branch}}
        raise AssertionError(path)

    def verify(self):
        return verify_agent_role_receipt(receipt=self.receipt,
            receipt_path="governance/material_admission_receipts/example.json",
            receipt_blob="f"*40,read_protected_json=self.read,api_get=self.api,
            protected_sha=P,subject_head=H,material_digest=M,actual_actor=ACTOR)

    def reject(self,msg):
        with self.assertRaises(AgentRoleError) as e:self.verify()
        self.assertIn(msg,str(e.exception))

    def test_positive_v2(self):
        x=self.verify()
        self.assertEqual(len(x["execution_evidence"]["protected_outputs"]),3)
        self.assertEqual(x["execution_evidence"]["native_source_reviewers"],["jimsteeg"])
        self.assertFalse(x["authority"]["new_certification_created"])
        self.assertFalse(x["execution_evidence"]["independent_execution_certified"])

    def test_missing_evidence_ref(self):
        del self.passes[0]["checks"][0]["execution_evidence"]
        self.reject("path or blob missing")

    def test_fake_digest(self):
        self.passes[0]["checks"][0]["receipt_sha256"]="0"*64
        self.reject("does not match protected raw output")

    def test_tampered_output(self):
        self.outputs[next(iter(self.outputs))][0]["output"]["stderr"]+="tampered\n"
        self.reject("does not match protected raw output")

    def test_blob_drift(self):
        x=next(iter(self.outputs))
        self.outputs[x][1]="9"*40
        self.reject("protected blob drift")

    def test_fake_role(self):
        self.outputs[next(iter(self.outputs))][0]["role"]="REFEREE"
        self.reject("identity, scope or result mismatch")

    def test_source_pr_must_protect_output(self):
        self.files[-1]["sha"]="9"*40
        self.reject("did not introduce exact execution outputs")

    def test_no_native_review(self):
        self.reviews=[]
        self.reject("no current nonauthor native approval")

    def test_self_review(self):
        self.reviews[0]["user"]["login"]=ACTOR
        self.reject("no current nonauthor native approval")

    def test_stale_review(self):
        self.reviews[0]["commit_id"]="0"*40
        self.reject("no current nonauthor native approval")

    def test_dismissal_supersedes_approval(self):
        self.reviews.append({"id":78,"state":"DISMISSED","commit_id":S,
            "submitted_at":"2026-10-16T12:22:00Z","user":{"login":"jimsteeg"}})
        self.reject("no current nonauthor native approval")

    def test_bad_source_ci(self):
        self.ci="failure"
        self.reject("missing actual protected source check")

    def test_legacy_unpinned_rejected(self):
        self.receipt["record_type"]="GCL_PROTECTED_AGENT_ROLE_ADMISSION_EVIDENCE_V1"
        self.receipt["schema_version"]="2.0.0"
        self.reject("new unverified legacy V1")

    def test_protected_source_branch_moves(self):
        self.branch="0"*40
        self.reject("source branch moved")

if __name__=="__main__": unittest.main()
