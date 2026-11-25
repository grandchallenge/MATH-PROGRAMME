"""Validate the actual stored Lean replay, without pretending to execute Lean in CPU-only CI."""
import hashlib
import json
import unittest
from pathlib import Path
from ci.erdos_pv_0027_formal_replay import validate_axioms, printed_types

ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'governance/erdos_proof_verification/evidence/0027'
P=ROOT/'experiments/erdos_proof_verification/0027'

class TestErdos27CRT(unittest.TestCase):
    def setUp(self):
        self.r=json.loads((E/'C_LEAN_CRT_REPLAY_001.json').read_text())
        self.log=(E/'C_LEAN_CRT_STDOUT_001.txt').read_text()
    def test_receipt_hashes(self):
        for path,field in [(P/'Erdos27CRT.lean','source_sha256'),(P/'lean-toolchain','toolchain_sha256'),(P/'lake-manifest.json','manifest_sha256'),(E/'C_LEAN_CRT_STDOUT_001.txt','stdout_sha256')]:
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),self.r[field])
        self.assertEqual(self.r['dependency_revisions'],{x['name']:x['rev'] for x in json.loads((P/'lake-manifest.json').read_text())['packages']})
    def test_axiom_inventory(self):
        self.assertEqual({n:sorted(x) for n,x in validate_axioms(self.log).items()},self.r['axioms'])
    def test_types(self):
        for t,key in zip(printed_types(self.log),['covering_count_printed_type_sha256','covering_density_printed_type_sha256']):
            self.assertEqual(hashlib.sha256(t.encode()).hexdigest(),self.r[key])
    def test_missing_and_duplicated_reports(self):
        line=next(x for x in self.log.splitlines() if "depends on axioms" in x)
        for bad in [self.log.replace(line,''),self.log+'\n'+line,self.log.replace('Quot.sound','sorryAx')]:
            with self.assertRaises(ValueError): validate_axioms(bad)
    def test_negative_receipts(self):
        self.assertEqual(set(self.r['negative_controls']),{'noncoprime_split','drop_smooth_condition','drop_rough_condition'})
        for x in self.r['negative_controls'].values():
            self.assertEqual(x['negation_exit'],0)
            self.assertNotEqual(x['false_target_exit'],0)
            self.assertIn('is false',x['diagnostic'])
        self.assertFalse(self.r['full_problem_proof_or_mathcert'])
