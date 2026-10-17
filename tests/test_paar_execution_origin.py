"""GitHub-hosted execution witness: bounded positive and adversarial controls."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"ci"))
from paar_execution_origin import (
    REPOSITORY,WORKFLOW_PATH,JOB_NAME,RECORD_TYPE,ALLOWED_COMMANDS,
    OriginError,fingerprint,source_binding,verify_witness,
)

RUN_ID = 80123456789
RUN_SHA = "a"*40
SUBJECT_SHA = "b"*40
FILE_SHA = "c"*40

class OriginWitnessTests(unittest.TestCase):
    def setUp(self):
        self.files=[{"filename":"ci/agent_role_receipt.py",
                     "status":"modified","sha":FILE_SHA}]
        self.material=fingerprint(self.files)
        self.current_blob=FILE_SHA
        self.subject={"repository":REPOSITORY,"pr_number":2710,
                      "head_sha":SUBJECT_SHA,"material_sha256":self.material}
        self.outputs=[]
        for role,cmd in ALLOWED_COMMANDS:
            if role=="REFEREE":
                stdout=json.dumps({"result":"PASS_BOUNDED_ONLY",
                                   "global_integrity_certified":False})
                stderr=""
            else:
                stdout=""
                stderr="Ran "+("14" if role=="VERIFIER" else "36")+" tests\nOK\n"
            selected="stderr" if stderr else "stdout"
            self.outputs.append({"role":role,"command":list(cmd),"exit_code":0,
                                 "stdout":stdout,"stderr":stderr,
                                 "selected_stream":selected,
                                 "selected_sha256":hashlib.sha256(
                                     (stderr if stderr else stdout).encode()).hexdigest()})
        self.witness={"record_type":RECORD_TYPE,"source":self.subject,
                      "protected_source_blobs":[{"path":self.files[0]["filename"],
                                                 "sha":FILE_SHA}],
                      "workflow_path":WORKFLOW_PATH,"workflow_sha":RUN_SHA,
                      "run_id":RUN_ID,"run_attempt":1,
                      "run_event":"workflow_dispatch",
                      "runner_environment":"github-hosted",
                      "producer_code":"protected-main-workflow",
                      "executions":self.outputs,
                      "limits":{"independent_platform_replay":True,
                                "original_chad_execution_attested":False,
                                "scientific_certification":False,
                                "gcl_wide_assurance_certified":False}}
        self.run={"repository":{"full_name":REPOSITORY},"event":"workflow_dispatch",
                  "status":"completed","conclusion":"success",
                  "path":WORKFLOW_PATH,"head_branch":"main","head_sha":RUN_SHA,
                  "run_attempt":1}
        self.main={"protected":True,"commit":{"sha":RUN_SHA}}
        self.compare={"status":"ahead","ahead_by":2,"behind_by":0,
                      "base_commit":{"sha":RUN_SHA},
                      "merge_base_commit":{"sha":RUN_SHA}}
        self.job={"name":JOB_NAME,"head_sha":RUN_SHA,"conclusion":"success",
                  "status":"completed","runner_group_name":"GitHub Actions",
                  "steps":[{"name":x,"status":"completed","conclusion":"success"}
                           for x in ("Run independent bounded assertions",
                                     "Upload execution origin artifact")]}
        self.artifact={"id":42,"name":f"paar-c-origin-{RUN_ID}-1",
                       "expired":False,"workflow_run":{"id":RUN_ID}}
        self.pr={"merged_at":"2026-10-16T22:00:00Z",
                 "head":{"sha":SUBJECT_SHA,"repo":{"full_name":REPOSITORY}},
                 "base":{"ref":"main"},"changed_files":1}

    def api(self,path):
        suffix=f"/repos/{REPOSITORY}"
        data={
          suffix+f"/actions/runs/{RUN_ID}":self.run,
          suffix+"/branches/main":self.main,
          suffix+f"/compare/{RUN_SHA}...{self.main['commit']['sha']}":self.compare,
          suffix+f"/actions/runs/{RUN_ID}/jobs?per_page=100":
              {"total_count":1,"jobs":[self.job]},
          suffix+f"/actions/runs/{RUN_ID}/artifacts?per_page=100":
              {"total_count":1,"artifacts":[self.artifact]},
          suffix+"/pulls/2710":self.pr,
          suffix+"/pulls/2710/files?per_page=100":self.files,
          suffix+"/contents/ci/agent_role_receipt.py?ref="+RUN_SHA:{"sha":self.current_blob},
        }
        if path not in data: raise AssertionError("untracked origin endpoint "+path)
        return data[path]

    def verify(self):
        return verify_witness(api_get=self.api,witness=self.witness,run_id=RUN_ID)

    def reject(self,phrase):
        with self.assertRaises(OriginError) as raised:self.verify()
        self.assertIn(phrase,str(raised.exception))

    def test_positive_external_platform_run(self):
        result=self.verify()
        self.assertEqual(result["result"],"PASS_BOUNDED_PLATFORM_ORIGIN_REPLAY")
        self.assertEqual(result["roles_verified"],["VERIFIER","ADVERSARY","REFEREE"])
        self.assertFalse(result["historical_chad_execution_attested"])
        self.assertFalse(result["gcl_wide_assurance_certified"])

    def test_wrong_run_id(self):
        self.witness["run_id"]+=1
        self.reject("another run")

    def test_wrong_event(self):
        self.run["event"]="pull_request"
        self.reject("run identity/status")

    def test_failed_actual_job(self):
        self.job["conclusion"]="failure"
        self.reject("no successful GitHub-hosted")

    def test_external_runner_rejected(self):
        self.job["runner_group_name"]="private"
        self.reject("no successful GitHub-hosted")

    def test_source_ref_not_protected(self):
        self.main["protected"]=False
        self.reject("no longer protected")

    def test_protected_main_fast_forward_accepts_historical_run(self):
        self.main["commit"]["sha"]="f"*40
        result=self.verify()
        self.assertEqual(result["protected_history_relation"], "VERIFIED_PROTECTED_ANCESTOR")
        self.assertEqual(result["trusted_workflow_head"], RUN_SHA)
        self.assertEqual(result["current_protected_main"], "f"*40)

    def test_protected_main_diverged_fails_closed(self):
        self.main["commit"]["sha"]="f"*40
        self.compare["status"]="diverged"
        self.reject("not ancestor")

    def test_rebased_history_fails_closed(self):
        self.main["commit"]["sha"]="f"*40
        self.compare["merge_base_commit"]["sha"]="e"*40
        self.reject("not ancestor")

    def test_reversed_history_fails_closed(self):
        self.main["commit"]["sha"]="f"*40
        self.compare.update({"status":"behind","ahead_by":0,"behind_by":3})
        self.reject("not ancestor")

    def test_compare_wrong_base_commit_fails_closed(self):
        self.main["commit"]["sha"]="f"*40
        self.compare["base_commit"]["sha"]="d"*40
        self.reject("not ancestor")

    def test_compare_malformed_counters_fail_closed(self):
        self.main["commit"]["sha"]="f"*40
        self.compare["ahead_by"]=True
        self.reject("not ancestor")

    def test_missing_upload_step(self):
        self.job["steps"].pop()
        self.reject("missing actual trusted runner step")

    def test_artifact_expired(self):
        self.artifact["expired"]=True
        self.reject("artifact missing or expired")

    def test_artifact_other_run(self):
        self.artifact["workflow_run"]["id"]+=1
        self.reject("artifact missing or expired")

    def test_protected_main_blob_differs_from_reviewed_source(self):
        self.current_blob="f"*40
        self.reject("protected workflow code differs")

    def test_fake_source_blob_list(self):
        self.witness["protected_source_blobs"][0]["sha"]="0"*40
        self.reject("runner source blob list not source-bound")

    def test_output_digest_forgery(self):
        self.outputs[0]["selected_sha256"]="0"*64
        self.reject("output SHA-256 drift")

    def test_role_substitution_rejected(self):
        self.outputs[1]["role"]="VERIFIER"
        self.reject("role command or bounded output invalid")

    def test_referee_fake_certification(self):
        self.outputs[2]["stdout"]=json.dumps({"result":"PASS_BOUNDED_ONLY",
                                             "global_integrity_certified":True})
        self.outputs[2]["selected_sha256"]=hashlib.sha256(
            self.outputs[2]["stdout"].encode()).hexdigest()
        self.reject("referee claimed unsupported certification")

    def test_source_material_drift(self):
        self.files[0]["sha"]="d"*40
        self.reject("candidate material SHA-256 drift")

    def test_candidate_not_merged(self):
        self.pr["merged_at"]=None
        self.reject("not exact-head merged")

    def test_witness_tries_to_certify_chad(self):
        self.witness["limits"]["original_chad_execution_attested"]=True
        self.reject("untrue or expanded origin")

    def test_bad_candidate_repo_rejected(self):
        self.pr["head"]["repo"]["full_name"]="untrusted/fork"
        self.reject("not exact-head merged")


if __name__=="__main__":
    unittest.main()
