"""Final EC005 editorial cohort coverage with original source status retained."""
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
class EC005Final48(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.q=json.loads((B/"EC-BULK-005_R10_48_SOURCE_QUALIFICATIONS.json").read_text())
  cls.p=json.loads((B/"EC-BULK-005_R10_48_ADMISSION_PROPOSAL.json").read_text())
  cls.d=json.loads((B/"EC-BULK-005.json").read_text())
  cls.a=json.loads((B/"EC-BULK-005_COMPLETENESS_AUDIT.json").read_text())
  cls.ledger=json.loads((R/"governance/erdos_compendium/EDITORIAL_ADMISSIONS.json").read_text())
 def test_all_200_historically_source_bound_and_current_accepted(self):
  accepted=load_batch_admissions(ACCEPTANCE)
  self.assertEqual(len(accepted),650)
  self.assertEqual(len(self.d["items"]),200)
  expected=set(range(652,852))
  self.assertEqual(expected,set(x["problem_id"] for x in self.d["items"]))
  self.assertTrue(expected<=set(accepted))
  self.assertEqual(len(self.ledger["batches"]),14)
  for row in self.d["items"]:
   n=row["problem_id"]
   with self.subTest(problem=n):
    f=R/row["article_path"]
    text=f.read_text()
    self.assertEqual(hashlib.sha256(f.read_bytes()).hexdigest(),row["draft_sha256"])
    self.assertEqual(row["draft_sha256"],self.a["article_sha256"][str(n)])
    self.assertIn(row["source_return"],text)
    self.assertEqual(accepted[n]["source_sha256"],hashlib.sha256(manuscript(n).encode()).hexdigest())
    self.assertEqual(sum(line.startswith("## ") for line in text.splitlines()),6)
    self.assertFalse(issues(text))
 def test_final_48_explanatory_source_conflicts_and_proof_holds_retained(self):
  A=load_batch_admissions(ACCEPTANCE)
  self.assertEqual(len(self.q["per_problem"]),48)
  self.assertEqual(self.q["count"],48)
  self.assertEqual(self.p["program_after_protected_reviewed"],650)
  self.assertEqual(self.p["ec005_after_protected_reviewed"],200)
  self.assertEqual(self.p["ec005_drafts_after_protected_merge"],0)
  entries=self.p["exact_source_bound_admissions"]
  batch=next(z for z in self.ledger["batches"] if z["batch_id"]=="EC-BULK-005-R10-48")
  self.assertEqual(batch["entries"],entries)
  self.assertEqual([r["problem_id"] for r in entries],
                   [r["problem_id"] for r in self.q["per_problem"]])
  for r in self.q["per_problem"]:
   n=r["problem_id"]
   with self.subTest(problem=n):
    row=self.d["items"][n-652]
    self.assertEqual(row["source_return_disposition"],r["historical_disposition"])
    self.assertFalse(r["disputed_source_status_cleared"])
    self.assertEqual(r["mathematical_proof_status"],"ORIGINAL_HOLD_RETAINED_NOT_CERTIFIED")
    self.assertEqual(A[n]["batch_id"],"EC-BULK-005-R10-48")
    self.assertEqual(row["effective_editorial_v2"]["batch_id"],"EC-BULK-005-R10-48")
    self.assertTrue(row["effective_editorial_v2"]["original_proof_review_hold_retained"])
    body=(R/row["article_path"]).read_text()
    self.assertIn(r["source_claim_boundary"],body)
    self.assertIn("source-exception-annotated explanation",body)
    self.assertNotIn("UNACCEPTED",body)
    self.assertNotEqual(r["historical_manuscript_raw_sha256"],r["editorially_reviewed_raw_sha256"])
    self.assertEqual(r["editorially_reviewed_raw_sha256"],row["draft_sha256"])
    self.assertEqual(r["editorially_reviewed_trimmed_sha256"],A[n]["source_sha256"])
 def test_original_128_problem_partition_preserved_in_successor(self):
  older=json.loads((B/"EC-BULK-005_R9_128_CENSUS_AND_SOURCE_TRIAGE.json").read_text())
  self.assertEqual(len(older["candidate_ids"]),80)
  self.assertEqual(len(older["source_exception_hold_ids"]),48)
  self.assertEqual(set(older["source_exception_hold_ids"]),
                   {r["problem_id"] for r in self.q["per_problem"]})
  self.assertFalse(set(older["candidate_ids"]) & set(older["source_exception_hold_ids"]))
  self.assertEqual(len(set(older["candidate_ids"])|set(older["source_exception_hold_ids"])),128)
