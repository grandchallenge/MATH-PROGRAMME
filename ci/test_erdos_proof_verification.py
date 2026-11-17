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
        self.assertEqual(set(result['statuses']), {str(n) for n in result['problem_ids']})
        self.assertTrue(
            set(result['statuses'].values()).issubset(
                set(self.schema['properties']['work_status']['enum'])
            )
        )

    def test_unexecuted_cannot_claim_kernel_replay(self):
        bad = copy.deepcopy(self.good)
        bad['stage_results']['REPLAY_EXECUTION']='PASS'
        bad['proof_receipts']=[]  # explicit unexecuted hostile input
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)

    def test_red_receipt_cannot_promote_kernel_pass(self):
        # The protected first Colab attempt is a genuine RED receipt.
        # Its presence must not pass an otherwise source-locked manifest.
        bad = copy.deepcopy(self.good)
        bad['stage_results']['REPLAY_EXECUTION']='PASS'
        self.assertTrue(bad['proof_receipts'])
        with self.assertRaisesRegex(ValueError,'pinned GREEN kernel/axiom receipt'):
            mod.validate_manifest(bad,self.schema)

    def test_replay_receipt_cannot_skip_semantic_review(self):
        bad = copy.deepcopy(self.good)
        bad['work_status']='IN_PROGRESS'
        bad['stage_results']['REPLAY_EXECUTION']='PASS'
        bad['stage_results']['STATEMENT_EQUIVALENCE']='PENDING'  # explicit hostile input
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

    def test_stale_source_566_567_cannot_be_promoted(self):
        for problem, old_blob in (
            (566, '0db66813b8f17be6819c53afca9cd3f853426a53'),
            (567, 'f2e29d94a0391f71f78d4b32168ce5e627e28b27'),
        ):
            with self.subTest(problem=problem):
                row = copy.deepcopy(self.good)
                row['problem_id'] = problem
                row['manifest_id'] = f'ERDOS-PV-{problem:04}-S01'
                row['source_audit_issue'] = problem + 1271
                row['source_locks']['catalogue_entry'] = str(problem)
                row['source_locks']['formal_path'] = f'FormalConjectures/ErdosProblems/{problem}.lean'
                row['source_locks']['formal_repository'] = 'google-deepmind/formal-conjectures'
                row['source_locks']['formal_commit'] = '85f863718beeec7b58a3a1926ee92e3472bc2020'
                row['source_locks']['formal_blob'] = old_blob
                row['source_locks']['external_formal_commit'] = None
                row['source_locks']['external_formal_path'] = None
                row['source_locks']['source_return_comment'] = (
                    f'https://github.com/grandchallenge/MATH-PROGRAMME/issues/{row["source_audit_issue"]}'
                    '#issuecomment-1')
                with self.assertRaisesRegex(ValueError, 'stale sizeRamsey'):
                    mod.validate_manifest(row, self.schema)
                row['source_locks']['external_formal_commit'] = (
                    '6751c0f043985ac6647db28a45a63afdf21acffe')
                row['source_locks']['external_formal_path'] = (
                    f'FormalConjectures/ErdosProblems/{problem}.lean')
                mod.validate_manifest(row, self.schema)

    def test_external_formal_source_requires_pin(self):
        bad = copy.deepcopy(self.good)
        bad['source_locks']['external_formal_commit']=None
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)


if __name__ == '__main__':
    unittest.main()
