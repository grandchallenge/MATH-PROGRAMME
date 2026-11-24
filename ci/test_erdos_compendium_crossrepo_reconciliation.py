"""Regression checks for cross-repository discovery versus mathematical authority."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from erdos_compendium_crossrepo_reconciliation import load_trees,problem_ids,reconcile,snapshot

P,S,C="MATH-PROGRAMME","MATHSOLVE","MATHCERT"
A="a"*40
B="b"*40
T="c"*40
CERT="certificates/formal_sources/MC-ERDOS-579-LEVEL5-001.json"
ROUTE="governance/certification_routes.json"
ARTICLE="governance/erdos_compendium/editorial/0579.md"
class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.trees={P:{ARTICLE:A},S:{"research/ERDOS-602/README.md":A},C:{CERT:A,ROUTE:A}}
        self.heads={r:T for r in self.trees}
        self.admissions={"admissions":[{"problem_id":579}],"batches":[]}
        self.baseline={"record_type":"ERDOS_CROSSREPO_RECONCILIATION_BASELINE/1",
            "inventory":snapshot(self.trees),"assessments":[
              {"problem_id":579,"editorial_disposition":"RECONCILED_EXACT_CERTIFIED_ARTICLE",
               "editorially_admitted":True,"manuscript_blob":A,
               "anchors":[{"repository":C,"path":CERT,"blob":A},{"repository":C,"path":ROUTE,"blob":A}]}]}
    def result(self):
        return reconcile(self.heads,self.trees,self.baseline,self.admissions)
    def row(self,n):
        return next(x for x in self.result()["review_candidates"] if x["problem_id"]==n)
    def test_known_boundary_retained(self):
        row=self.row(579)
        self.assertEqual(row["state"],"RECONCILED_EXACT_CERTIFIED_ARTICLE")
        self.assertFalse(row["publication_authorized"])
        self.assertFalse(row["theorem_status_inferred"])
        self.assertFalse(self.result()["history_exhaustive"])
    def test_changed_global_route_reopens_exact_certificate(self):
        self.trees[C][ROUTE]=B
        self.assertEqual(self.row(579)["state"],"REASSESS_SOURCE_OR_EDITORIAL_CHANGE")
        self.assertEqual(self.row(579)["anchor_drift"][0]["path"],ROUTE)
    def test_deleted_source_reopens(self):
        del self.trees[C][CERT]
        self.assertEqual(self.row(579)["state"],"REASSESS_SOURCE_OR_EDITORIAL_CHANGE")
    def test_article_or_admission_change_reopens(self):
        self.trees[P][ARTICLE]=B
        self.assertTrue(self.row(579)["editorial_identity_changed"])
        self.trees[P][ARTICLE]=A
        self.admissions["admissions"]=[]
        self.assertTrue(self.row(579)["editorial_identity_changed"])
    def test_new_result_is_not_certified(self):
        self.trees[S]["research/ERDOS-249/new.json"]=B
        row=self.row(249)
        self.assertEqual(row["state"],"UNASSESSED_EVIDENCE_DISCOVERY")
        self.assertTrue(row["evidence_inventory_changed"])
        self.assertFalse(row["theorem_status_inferred"])
    def test_ids_not_campaign_numbers_or_issue_comment_ids(self):
        self.assertEqual(problem_ids(S,"contributions/ERDOS-OPEN-001/receipts/ERDOS-99-A1-IA-001/github-comment-6027288017.json"),[99])
        self.assertEqual(problem_ids(S,"contributions/ERDOS-OPEN-001/README.md"),[])
        self.assertEqual(problem_ids(S,"MathSolve/Erdos/E602SetBridge.lean"),[602])
        self.assertEqual(problem_ids(P,"experiments/erdos249_full_series_phase/README.md"),[249])
        self.assertEqual(problem_ids(P,"governance/erdos_compendium/editorial/0249.md"),[])
    def test_unassigned_paths_tracked(self):
        self.trees[S]["contributions/ERDOS-OPEN-001/SHARED.json"]=A
        self.assertTrue(self.result()["shared_or_unassigned_inventory_changed"])
    def test_protected_tree_binding_and_truncation(self):
        with tempfile.TemporaryDirectory() as tmp:
            d=Path(tmp)
            h={"protected":True,"commit":{"sha":A,"commit":{"tree":{"sha":T}}}}
            tree={"sha":T,"truncated":False,"tree":[{"type":"blob","path":"x","sha":B}]}
            for repo in (P,S,C):
                (d/f"{repo}-head.json").write_text(json.dumps(h))
                (d/f"{repo}-tree.json").write_text(json.dumps(tree))
            self.assertEqual(load_trees(d)[0][P],A)
            for bad in (dict(tree,sha=A),dict(tree,truncated=True)):
                (d/f"{S}-tree.json").write_text(json.dumps(bad))
                with self.assertRaises(ValueError):load_trees(d)
if __name__=="__main__":unittest.main()
