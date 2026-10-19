#!/usr/bin/env python3
"""Hostile tests for source-only, exact-receipt Council Clerk transition."""
import copy,json,os,unittest
from pathlib import Path
from unittest.mock import patch
from ci import erdos_final_two_source_resolution as m
P=Path("governance/source_erdos_critical_005")
class FinalTwoTests(unittest.TestCase):
 def record(self,n):
  s=m.T[n];return json.loads((P/s["receipt"]).read_text()),(P/s["file"]).read_bytes()
 def test_both_exact_source_receipts(self):
  self.assertEqual(set(m.T),{2522,2536})
  for n in m.T:
   with self.subTest(n=n):
    self.assertEqual(m.material(n)["source_only"],True)
 def test_14_reject_wrong_source_claim_authority_and_proof(self):
  r,src=self.record(2522)
  for mutate in (
   lambda x:x.update(gcl_discovered_proof=True),
   lambda x:x["replayed_submissions"][0].update(kernel_exit_code=1),
   lambda x:x["replayed_submissions"][0].update(depends_on_sorryAx=True),
   lambda x:x["replayed_submissions"][1].update(defeq_intended_challenge_target=False),
   lambda x:x["replayed_submissions"][1].update(defeq_hostile_altered_target=True),
   lambda x:x["replayed_submissions"][1].update(transitive_axioms=["sorryAx"]),
   lambda x:x["replayed_submissions"][1].update(submission_sha256="0"*64),
   lambda x:x["authority_effects"].update(revision_clearance_authorized=True),
  ):
   test=copy.deepcopy(r);mutate(test)
   with self.assertRaises(m.GateError):m.check_material(2522,test,src)
  with self.assertRaises(m.GateError):m.check_material(2522,r,src+b"x")
 def test_41_reject_false_semantics_and_axioms(self):
  r,src=self.record(2536)
  for mutate in (
   lambda x:x.update(sorry_count=1),
   lambda x:x.update(imported_mathlib_finset_multiset_comparison_complete=False),
   lambda x:x.update(mathematical_conjecture_solved=True),
   lambda x:x.update(refreshed_provider_blob_sha1="0"*40),
   lambda x:x["historical_theorem_specification"].update(historical_variant_name="erdos_41"),
   lambda x:x["kernel_proved_theorems"]["modern_implies_fixed"].update(axioms=["sorryAx"]),
  ):
   test=copy.deepcopy(r);mutate(test)
   with self.assertRaises(m.GateError):m.check_material(2536,test,src)
  with self.assertRaises(m.GateError):m.check_material(2536,r,src+b"bad")
 def test_pre_council_label_change_fails_closed(self):
  n=2522;s=m.T[n]
  old={"issue":n,"state":"OPEN","revise":False,"corrected":True}
  cm=[{"id":s["review"],"body":"GCL-CRITICAL-REVIEW/1\nDISPOSITION: REVISE\n"}]
  child=[{"id":s["result"],"body":"RESULT/1\n"},{"id":s["readback"],"body":"EVIDENCE_REVIEW/1\n"}]
  with patch.object(m.c,"issue_snapshot",return_value=old),patch.object(m.c,"comments",side_effect=lambda x:cm if x==n else child):
   with self.assertRaises(m.GateError):m.snapshot(n)
 def test_untrusted_bot_resolution_fails_closed(self):
  n=2536;s=m.T[n]
  old={"issue":n,"state":"OPEN","revise":False,"corrected":True}
  cm=[{"id":s["review"],"body":"GCL-CRITICAL-REVIEW/1\nDISPOSITION: REVISE\n"},
      {"body":m.PREFIX+"\n"+s["sha"]+"\n"+s["merge"],"user":{"login":"fyremael"}}]
  child=[{"id":s["result"],"body":"RESULT/1\n"},{"id":s["readback"],"body":"EVIDENCE_REVIEW/1\n"}]
  with patch.object(m.c,"issue_snapshot",return_value=old),patch.object(m.c,"comments",side_effect=lambda x:cm if x==n else child):
   with self.assertRaises(m.GateError):m.snapshot(n)
 def test_protected_app_runtime_guard(self):
  with patch.dict(os.environ,{"GITHUB_ACTIONS":"false","GITHUB_REF":"refs/heads/main",
                              "GCL_CONTROLLER_ID":"erdos-final-two-source-resolution","GH_TOKEN":"fake"}):
   with self.assertRaises(m.GateError):m.apply([])
  with patch.dict(os.environ,{"GITHUB_ACTIONS":"true","GITHUB_REF":"refs/heads/feature",
                              "GCL_CONTROLLER_ID":"erdos-final-two-source-resolution","GH_TOKEN":"fake"}):
   with self.assertRaises(m.GateError):m.apply([])
 def test_route_stays_on_existing_persistent_controller(self):
  workflow=Path(".github/workflows/erdos-three-source-resolution.yml").read_text()
  self.assertEqual(workflow.count("environment: release-trust"),1)
  self.assertEqual(workflow.count("actions/create-github-app-token@"),1)
  self.assertEqual(workflow.count("ci/erdos_final_two_source_resolution.py"),2)
  self.assertIn("inputs.source_scope == 'final_two'",workflow)
  self.assertIn("permission-issues: write",workflow)
  self.assertNotIn("pull_request_target:",workflow)
  registry=json.loads(Path(".ghos-routing/workflows.json").read_text())
  matched=[x for x in registry["workflows"] if x["path"]==".github/workflows/erdos-three-source-resolution.yml"]
  self.assertEqual(len(matched),1)
  self.assertEqual(matched[0]["controller_id"],"GITHUB_ACTIONS")
  self.assertIn("WRITE_CAPABLE",matched[0]["observed_features"])
if __name__=="__main__":unittest.main(verbosity=2)
