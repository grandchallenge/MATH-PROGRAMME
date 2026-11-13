#!/usr/bin/env python3
"""Hostile fixtures for the Erdős proof-verification admission boundary."""
import copy
import importlib.util
import unittest
from pathlib import Path

p = Path(__file__).with_name('validate_erdos_proof_verification.py')
spec = importlib.util.spec_from_file_location('erdos_pv_validation', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class VerificationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = mod.load(mod.SCHEMA)
        cls.good = mod.load('governance/erdos_proof_verification/manifests/0248.json')

    def test_current_registry_and_five_children(self):
        result = mod.validate_registry()
        self.assertEqual(result['problem_ids'], [246,247,248,249,250])
        self.assertEqual(set(result['statuses'].values()), {'QUEUED_UNEXECUTED'})

    def test_unexecuted_cannot_claim_kernel_replay(self):
        bad = copy.deepcopy(self.good)
        bad['stage_results']['REPLAY_EXECUTION']='PASS'
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)

    def test_replay_receipt_cannot_skip_semantic_review(self):
        bad = copy.deepcopy(self.good)
        bad['work_status']='IN_PROGRESS'
        bad['stage_results']['REPLAY_EXECUTION']='PASS'
        bad['proof_receipts']=['evidence/foo/replay.json']
        bad['toolchain_pins']={'lean':'4.0'}
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)

    def test_no_self_adjudication_without_review(self):
        bad = copy.deepcopy(self.good)
        bad['work_status']='IN_PROGRESS'
        bad['stage_results']['INTERNAL_ADJUDICATION']='PASS'
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)

    def test_no_mathcert_status_from_source_return(self):
        bad = copy.deepcopy(self.good)
        bad['certification_status']='MATHCERT_CERTIFIED'
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)

    def test_source_sha_must_be_frozen(self):
        bad = copy.deepcopy(self.good)
        bad['source_locks']['formal_commit']='main'
        with self.assertRaises(Exception): mod.validate_manifest(bad,self.schema)

    def test_zero_pinned_provider_path_mismatch(self):
        bad = copy.deepcopy(self.good)
        bad['source_locks']['formal_path']='FormalConjectures/ErdosProblems/249.lean'
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)

    def test_no_open_conjecture_as_full_verified_claim(self):
        bad = mod.load('governance/erdos_proof_verification/manifests/0249.json')
        bad['verification_kind']='FULL_CONJECTURE_CERTIFICATION'
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)

    def test_external_formal_source_requires_pin(self):
        bad = copy.deepcopy(self.good)
        bad['source_locks']['external_formal_commit']=None
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)


if __name__ == '__main__':
    unittest.main()
