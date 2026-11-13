#!/usr/bin/env python3
"""Fail-closed per-problem lease simulation; not live agent dispatch evidence."""
import copy,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import erdos_pv_worker_lease as w
import erdos_pv_binary_blocks as math

class LeaseTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.s=w.scope("ERDOS-PV-0001-B",require_eligible=False)
 def test_only_one_b_ready(self):
  self.assertEqual(self.s["issue"],3225)
  with self.assertRaises(ValueError):w.scope("ERDOS-PV-0002-B")
  with self.assertRaises(ValueError):w.scope("ERDOS-PV-0001-B")
  self.assertEqual(w.scope("ERDOS-PV-0001-C")["issue"],3238)
 def test_bad_ids(self):
  for x in ["ERDOS-PV-0000-B","ERDOS-PV-1222-A","ERDOS-PV-0001-Z","ERDOS-PV-1-B"]:
   with self.subTest(x=x), self.assertRaises(ValueError):w.scope(x)
 def test_ref_is_per_problem_not_whole_cohort(self):
  self.assertEqual(w.ref(self.s),"refs/heads/gcl-pv-claims/ERDOS-PV-0001-B")
 def test_live_labels_not_available(self):
  with patch.object(w,"api",return_value={"state":"open","labels":[{"name":"gcl-state:blocked"}]}):
   with self.assertRaisesRegex(ValueError,"AVAILABLE"):w.preflight(self.s)
 def test_manifest_blob_drift(self):
  def fake(method,path,data=None):
   if path.startswith("issues/"):return {"state":"open","labels":[{"name":"gcl-state:available"}]}
   return {"sha":"0"*40}
  with patch.object(w,"api",side_effect=fake),patch.object(w,"run",return_value="a"*40):
   with self.assertRaisesRegex(ValueError,"differs"):w.preflight(self.s)
 def test_duplicate_prior_result_blocks_claim(self):
  def fake(method,path,data=None):
   if path.startswith("issues/"):return {"state":"open","labels":[{"name":"gcl-state:available"}]}
   return {"sha":"a"*40}
  with patch.object(w,"api",side_effect=fake),patch.object(w,"run",return_value="a"*40),patch.object(w,"comments",return_value=[{"body":"RESULT/1\nASSIGNMENT_ID: ERDOS-PV-0001-B\n"}]):
   with self.assertRaisesRegex(ValueError,"already returned"):w.preflight(self.s)
 def test_existing_reservation_no_second_commit(self):
  with patch.object(w,"preflight",return_value={"source_blob":"a"*40}),patch.object(w,"current_ref",return_value={"object":{"sha":"b"*40}}),patch.object(w,"api") as api:
   result=w.claim(self.s)
   self.assertEqual(result["result"],"HELD")
   api.assert_not_called()
 def test_contending_ref_creation_fails_closed(self):
  def fake_api(method,path,data=None):
   if path=="git/ref/heads/main":return {"object":{"sha":"1"*40}}
   if path.startswith("git/commits/"):return {"tree":{"sha":"2"*40}}
   if path=="git/commits":return {"sha":"3"*40}
   if path=="git/refs":raise RuntimeError("HTTP 422 Reference already exists")
   raise AssertionError(path)
  with patch.object(w,"preflight",return_value={"source_blob":"4"*40}),patch.object(w,"current_ref",side_effect=[None,{"object":{"sha":"5"*40}}]),patch.object(w,"api",side_effect=fake_api),patch.object(w,"run",return_value="testactor"):
   result=w.claim(self.s)
  self.assertEqual((result["result"],result["winner_sha"]),("LOST_RACE_OR_UNCERTAIN","5"*40))
 def test_uncertain_write_reconciles_missing_ref(self):
  def fake_api(method,path,data=None):
   if path=="git/ref/heads/main":return {"object":{"sha":"1"*40}}
   if path.startswith("git/commits/"):return {"tree":{"sha":"2"*40}}
   if path=="git/commits":return {"sha":"3"*40}
   if path=="git/refs":raise RuntimeError("transport timeout")
   raise AssertionError(path)
  with patch.object(w,"preflight",return_value={"source_blob":"4"*40}),patch.object(w,"current_ref",side_effect=[None,None]),patch.object(w,"api",side_effect=fake_api),patch.object(w,"run",return_value="testactor"):
   x=w.claim(self.s)
  self.assertEqual((x["result"],x["winner_sha"]),("LOST_RACE_OR_UNCERTAIN",None))
 def test_absent_lease_forbids_return(self):
  with patch.object(w,"current_ref",return_value=None):
   with self.assertRaisesRegex(ValueError,"not held"):w.submit(self.s,"a"*40,"/dev/null")
 def test_wrong_lease_owner_forbids_return(self):
  with patch.object(w,"current_ref",return_value={"object":{"sha":"a"*40}}):
   with self.assertRaisesRegex(ValueError,"not held"):w.submit(self.s,"b"*40,"/dev/null")
 def test_release_requires_admitted_status_before_any_delete(self):
  with patch.object(w,"api") as api:
   with self.assertRaisesRegex(ValueError,"protected completion"):
    w.release(self.s,"a"*40,"b"*40)
   api.assert_not_called()
 def test_release_rejects_unverified_claim_sha(self):
  s=copy.deepcopy(self.s);q=s["row"]["stage_work_items"]["B"]
  q["work_status"]="PROTECTED_ADMITTED"
  q["protected_admission_ref"]="grandchallenge/MATH-PROGRAMME@"+"b"*40
  with patch.object(w,"current_ref",return_value=None),patch.object(w,"api") as api:
   with self.assertRaisesRegex(ValueError,"not held"):
    w.release(s,"a"*40,"b"*40)
   api.assert_not_called()
 def test_release_rejects_fake_parent_commit_before_delete(self):
  s=copy.deepcopy(self.s);q=s["row"]["stage_work_items"]["B"]
  q["work_status"]="PROTECTED_ADMITTED"
  q["protected_admission_ref"]="grandchallenge/MATH-PROGRAMME@"+"b"*40
  with patch.object(w,"current_ref",return_value={"object":{"sha":"a"*40}}),\
       patch.object(w,"api",return_value={"message":"not a claim"}) as api,\
       patch.object(w,"run",return_value="testactor"):
   with self.assertRaisesRegex(ValueError,"Actor or source"):
    w.release(s,"a"*40,"b"*40)
   self.assertFalse(any(call.args[0]=="DELETE" for call in api.call_args_list))
 def test_release_does_not_accept_wrong_receipt_sha(self):
  s=copy.deepcopy(self.s);q=s["row"]["stage_work_items"]["B"]
  q["work_status"]="PROTECTED_ADMITTED"
  q["protected_admission_ref"]="grandchallenge/MATH-PROGRAMME@"+"b"*40
  with self.assertRaisesRegex(ValueError,"protected completion"):
   w.release(s,"a"*40,"c"*40)
 def test_negative_finite_fixture_detected(self):
  x=math.evidence()
  self.assertEqual(x["result"],"PASS_EXACT_FINITE_FIXTURES_NOT_UNIVERSAL_THEOREM")
  self.assertEqual([v["distinct_subset_sum_count"] for v in x["fixtures"]],[16,64,13])
  self.assertEqual(x["fixtures"][2]["collision"]["sum"],3)
  self.assertFalse(x["limitations"]["full_erdos1_counterexample_verified"])
 def test_preflight_requires_genuine_source_hash(self):
  self.assertEqual(len(self.s["row"]["source_issue_body_sha256"]),64)
  self.assertEqual(self.s["row"]["source_audit_issue"],1270)

if __name__=="__main__":unittest.main()
