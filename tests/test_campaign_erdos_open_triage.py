from __future__ import annotations
import copy
import importlib.util
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("erdos_triage",ROOT/"ci"/"validate_erdos_open_triage.py")
MOD=importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)
BASE=MOD.load()

class ErdosOpenTriageTests(unittest.TestCase):
    def test_baseline(self): self.assertEqual(MOD.validate(BASE),[])
    def test_rejects_missing_row(self):
        x=copy.deepcopy(BASE); x["entries"]=x["entries"][:-1]; self.assertTrue(MOD.validate(x))
    def test_rejects_solve_authority_inflation(self):
        x=copy.deepcopy(BASE); x["entries"][0]["solve_authorized"]=True; self.assertTrue(MOD.validate(x))
    def test_rejects_problem3_duplicate_route(self):
        x=copy.deepcopy(BASE); next(r for r in x["entries"] if r["problem_id"]=="3")["triage_class"]="FIRST_RECONNAISSANCE_TRANCHE"; self.assertTrue(MOD.validate(x))
    def test_rejects_status_hold_loss(self):
        x=copy.deepcopy(BASE); next(r for r in x["entries"] if r["problem_id"]=="390")["triage_class"]="PROTECTED_READY_BACKLOG"; self.assertTrue(MOD.validate(x))
    def test_rejects_first_tranche_identity_drift(self):
        x=copy.deepcopy(BASE); next(r for r in x["entries"] if r["problem_id"]=="593")["triage_class"]="PROTECTED_READY_BACKLOG"; self.assertTrue(MOD.validate(x))
if __name__=="__main__": unittest.main()
