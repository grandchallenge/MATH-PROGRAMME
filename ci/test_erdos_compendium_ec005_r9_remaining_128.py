"""Fail-closed R9 census and source-bound batch acceptance: 128 accounted for."""
import hashlib,json,unittest
from pathlib import Path
try:
    from ci.erdos_compendium import manuscript,load_batch_admissions,ACCEPTANCE
    from ci.math_markdown_gate import issues
except ModuleNotFoundError:
    from erdos_compendium import manuscript,load_batch_admissions,ACCEPTANCE
    from math_markdown_gate import issues
R=Path(__file__).resolve().parents[1]
B=R/"governance/erdos_compendium/batches"
class R9Remaining128(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.q=json.loads((B/"EC-BULK-005_R9_128_CENSUS_AND_SOURCE_TRIAGE.json").read_text())
  cls.p=json.loads((B/"EC-BULK-005_R9_80_ADMISSION_PROPOSAL.json").read_text())
  cls.d=json.loads((B/"EC-BULK-005.json").read_text())
  cls.a=json.loads((B/"EC-BULK-005_COMPLETENESS_AUDIT.json").read_text())
  cls.ledger=json.loads((R/"governance/erdos_compendium/EDITORIAL_ADMISSIONS.json").read_text())
 def test_128_original_source_returns_complete_nonoverlapping(self):
  q=self.q
  self.assertEqual(len(q["per_article"]),128)
  self.assertEqual(len({x["problem_id"] for x in q["per_article"]}),128)
  self.assertEqual((q["unique_original_authenticated_returns"],
                    q["live_maintained_source_pages_http200"],
                    q["exact_original_manuscript_hashes"]),(128,128,128))
  self.assertEqual(len(q["candidate_ids"]),80)
  self.assertEqual(len(q["source_exception_hold_ids"]),48)
  self.assertFalse(set(q["candidate_ids"])&set(q["source_exception_hold_ids"]))
  self.assertEqual({x["original_disposition"] for x in q["per_article"]},
                   {"BOUNDED_TASK_DESIGNED","PARTIAL","STATUS_CONFLICT","SOURCE_LOCK_READY"})
  self.assertEqual(sum(x["original_disposition"]=="BOUNDED_TASK_DESIGNED" for x in q["per_article"]),80)
  self.assertEqual(sum(x["original_disposition"]=="PARTIAL" for x in q["per_article"]),19)
  self.assertEqual(sum(x["original_disposition"]=="STATUS_CONFLICT" for x in q["per_article"]),26)
  self.assertEqual(sum(x["original_disposition"]=="SOURCE_LOCK_READY" for x in q["per_article"]),3)
 def test_80_exact_hash_critical_reviewed_articles(self):
  A=load_batch_admissions(ACCEPTANCE)
  q=self.q;p=self.p
  self.assertEqual(len(A),650)
  self.assertEqual((p["proposed_programme_reviewed"],p["proposed_ec005_reviewed"],
                    p["proposed_ec005_unaccepted"]),(602,152,48))
  batch=next(x for x in self.ledger["batches"] if x["batch_id"]=="EC-BULK-005-R9-80")
  self.assertEqual(batch["entries"],p["80_exact_hash_entries"])
  self.assertEqual([x["problem_id"] for x in batch["entries"]],q["candidate_ids"])
  for x in batch["entries"]:
   n=x["problem_id"]
   with self.subTest(problem=n):
    census=next(z for z in q["per_article"] if z["problem_id"]==n)
    reg=self.d["items"][n-652];f=R/reg["article_path"];text=f.read_text()
    self.assertEqual(census["original_disposition"],"BOUNDED_TASK_DESIGNED")
    self.assertEqual(census["comment_author"],"fyremael")
    self.assertEqual(census["source_http"],200)
    self.assertEqual(x["source_check"],census["authenticated_return"])
    self.assertEqual(x["source_check"],reg["source_return"])
    self.assertIn(x["source_check"],text)
    self.assertEqual(hashlib.sha256(manuscript(n).encode()).hexdigest(),x["source_sha256"])
    self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),reg["draft_sha256"])
    self.assertEqual(reg["draft_sha256"],self.a["article_sha256"][str(n)])
    self.assertNotEqual(census["manuscript_raw_sha256"],reg["draft_sha256"])
    self.assertIn("editorially reviewed",text.lower())
    self.assertIn("BOUNDED_TASK_DESIGNED",text)
    self.assertNotIn("UNACCEPTED",text)
    self.assertFalse(issues(text))
 def test_48_conflicts_and_partial_not_silently_admitted(self):
  q=self.q;A=load_batch_admissions(ACCEPTANCE)
  r10=json.loads((B/"EC-BULK-005_R10_48_SOURCE_QUALIFICATIONS.json").read_text())
  self.assertEqual(set(q["source_exception_hold_ids"]),
                   {x["problem_id"] for x in r10["per_problem"]})
  for n in q["source_exception_hold_ids"]:
   with self.subTest(problem=n):
    row=self.d["items"][n-652]
    census=next(z for z in q["per_article"] if z["problem_id"]==n)
    qualifier=next(z for z in r10["per_problem"] if z["problem_id"]==n)
    self.assertIn(row["source_return_disposition"],("PARTIAL","STATUS_CONFLICT","SOURCE_LOCK_READY"))
    self.assertEqual(row["source_return_disposition"],census["original_disposition"])
    self.assertEqual(census["manuscript_raw_sha256"],qualifier["historical_manuscript_raw_sha256"])
    self.assertEqual(A[n]["batch_id"],"EC-BULK-005-R10-48")
    self.assertFalse(qualifier["disputed_source_status_cleared"])
    self.assertEqual(qualifier["mathematical_proof_status"],"ORIGINAL_HOLD_RETAINED_NOT_CERTIFIED")
    self.assertEqual(row["draft_sha256"],qualifier["editorially_reviewed_raw_sha256"])
    self.assertEqual(row["draft_sha256"],hashlib.sha256((R/row["article_path"]).read_bytes()).hexdigest())
    self.assertEqual(row["draft_sha256"],self.a["article_sha256"][str(n)])
    self.assertTrue(q["source_exception_hold_reasons"][str(n)])
 def test_22_previous_admitted_typography_overlays_preserved(self):
  A=load_batch_admissions(ACCEPTANCE)
  h=self.q["prior_protected_amendment_reconciliation"]
  self.assertEqual(h["count"],22)
  self.assertEqual(len(h["entries"]),22)
  for e in h["entries"]:
   n=e["problem_id"]
   self.assertEqual(e["authority"],"EC-LEGACY-25-TEX-20261015")
   self.assertEqual(e["authority"],A[n]["legacy25_typography_id"])
   self.assertEqual(hashlib.sha256(manuscript(n).encode()).hexdigest(),A[n]["source_sha256"])
   self.assertEqual(e["current_protected_typography_raw_sha256"],
                    self.d["items"][n-652]["draft_sha256"])
