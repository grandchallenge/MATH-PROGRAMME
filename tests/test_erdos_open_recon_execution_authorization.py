from __future__ import annotations
import copy, importlib.util, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("v",ROOT/"ci"/"validate_erdos_open_recon_execution_authorization.py")
MOD=importlib.util.module_from_spec(SPEC); assert SPEC.loader is not None; SPEC.loader.exec_module(MOD)
BASE=MOD.load()
class Tests(unittest.TestCase):
    def test_baseline(self): self.assertEqual(MOD.validate(BASE),[])
    def test_rejects_extra_problem(self):
        x=copy.deepcopy(BASE); x["selected_problem_ids"].append("20"); self.assertTrue(MOD.validate(x))
    def test_rejects_unbound_execution(self):
        x=copy.deepcopy(BASE); x["execution_scope"]["lease_identity_required"]=False; self.assertTrue(MOD.validate(x))
    def test_rejects_synthesis_open(self):
        x=copy.deepcopy(BASE); x["synthesis_policy"]["initial_synthesis_allowed"]=True; self.assertTrue(MOD.validate(x))
    def test_rejects_claim_promotion(self):
        x=copy.deepcopy(BASE); x["authority_boundary"]["theorem_claim_promotion_authorized"]=True; self.assertTrue(MOD.validate(x))
if __name__=="__main__": unittest.main()
