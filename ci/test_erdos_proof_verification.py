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
        bad['proof_receipts'] = [
            path for path in bad['proof_receipts']
            if '/LEAN_REPLAY_RED_' in path
        ]  # a genuine RED-only set despite the now-admitted GREEN fixture
        self.assertTrue(bad['proof_receipts'])
        self.assertFalse(any('GREEN' in path for path in bad['proof_receipts']))
        with self.assertRaisesRegex(ValueError,'pinned GREEN kernel/axiom receipt'):
            mod.validate_manifest(bad,self.schema)

    def test_green_receipt_is_valid_but_not_mathematical_certification(self):
        good = copy.deepcopy(self.good)
        self.assertEqual(good['stage_results']['REPLAY_EXECUTION'], 'PASS')
        self.assertEqual(good['stage_results']['ADVERSARIAL_REVIEW'], 'PASS')
        self.assertEqual(good['stage_results']['INTERNAL_ADJUDICATION'], 'PASS')
        self.assertEqual(good['stage_results']['PROTECTED_EVIDENCE_ADMISSION'], 'PASS')
        self.assertEqual(good['certification_status'], 'NOT_SUBMITTED')
        mod.validate_manifest(good, self.schema)

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
        bad['stage_results']['ADVERSARIAL_REVIEW']='PENDING'
        bad['review_receipts']=[]
        bad['stage_results']['INTERNAL_ADJUDICATION']='PASS'
        with self.assertRaises(ValueError): mod.validate_manifest(bad,self.schema)

    def test_scoped_adversarial_review_cannot_be_replaced_by_generic_receipt(self):
        bad = copy.deepcopy(self.good)
        bad['review_receipts']=['evidence/fake-critical-review.json']
        with self.assertRaisesRegex(ValueError, 'exact qualified review receipt'):
            mod.validate_manifest(bad, self.schema)

    def test_forged_full_paper_omega_claim_fails_review_gate(self):
        from unittest.mock import patch
        p = ('governance/erdos_proof_verification/reviews/'
             '0248_SOURCE_CRITICAL_REVIEW_001.json')
        real_load = mod.load
        r = copy.deepcopy(real_load(p))
        r['checks']['full_paper_Omega_proved_in_lean'] = True
        def inject(path, *args, **kwargs):
            return r if path == p else real_load(path, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=inject):
            with self.assertRaisesRegex(ValueError, 'exact qualified scope'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_real_scoped_adversarial_pass_preserves_certification_boundary(self):
        good = copy.deepcopy(self.good)
        self.assertEqual(good['stage_results']['ADVERSARIAL_REVIEW'], 'PASS')
        self.assertEqual(good['stage_results']['INTERNAL_ADJUDICATION'], 'PASS')
        self.assertEqual(good['stage_results']['PROTECTED_EVIDENCE_ADMISSION'], 'PASS')
        self.assertEqual(good['work_status'], 'VERIFIED_WITHOUT_CERTIFICATION')
        self.assertEqual(good['certification_status'], 'NOT_SUBMITTED')
        mod.validate_manifest(good, self.schema)

    def test_referee_adjudication_cannot_be_forged_with_placeholder_receipt(self):
        bad = copy.deepcopy(self.good)
        bad['review_receipts'] = [
            x for x in bad['review_receipts']
            if 'REFEREE_ADJUDICATION' not in x
        ]
        with self.assertRaisesRegex(ValueError, 'exact Referee receipt'):
            mod.validate_manifest(bad, self.schema)

    def test_referee_cannot_claim_stronger_Omega_theorem(self):
        from unittest.mock import patch
        p = ('governance/erdos_proof_verification/adjudications/'
             '0248_REFEREE_ADJUDICATION_001.json')
        original = mod.load
        forged = copy.deepcopy(original(p))
        forged['findings']['published_Omega_multiplicity_formalized'] = True
        def injected(path, *args, **kwargs):
            return forged if path == p else original(path, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=injected):
            with self.assertRaisesRegex(ValueError, 'real scoped noncertifying custody'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_referee_cannot_claim_independent_human_or_certification(self):
        from unittest.mock import patch
        p = ('governance/erdos_proof_verification/adjudications/'
             '0248_REFEREE_ADJUDICATION_001.json')
        original = mod.load
        forged = copy.deepcopy(original(p))
        forged['independent_human_attestation'] = True
        forged['authority_effects']['mathcert_certification'] = True
        def injected(path, *args, **kwargs):
            return forged if path == p else original(path, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=injected):
            with self.assertRaisesRegex(ValueError, 'real scoped noncertifying custody'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_no_protected_admission_without_internal_referee(self):
        bad = copy.deepcopy(self.good)
        bad['stage_results']['INTERNAL_ADJUDICATION'] = 'PENDING'
        bad['stage_results']['PROTECTED_EVIDENCE_ADMISSION'] = 'PASS'
        with self.assertRaisesRegex(ValueError, 'admitted without adjudication'):
            mod.validate_manifest(bad, self.schema)

    def test_final_custody_cannot_be_replaced_with_generic_marker(self):
        bad = copy.deepcopy(self.good)
        bad['review_receipts'] = [
            x for x in bad['review_receipts']
            if 'PROTECTED_EVIDENCE_ADMISSION_001' not in x
        ]
        with self.assertRaisesRegex(ValueError, 'exact final custody packet'):
            mod.validate_manifest(bad, self.schema)

    def test_final_custody_rejects_forged_protected_referee_merge(self):
        from unittest.mock import patch
        path = ('governance/erdos_proof_verification/admissions/'
                '0248_PROTECTED_EVIDENCE_ADMISSION_001.json')
        real = mod.load
        forged = copy.deepcopy(real(path))
        forged['protected_referee_adjudication_merge'] = '0' * 40
        def inject(p, *args, **kwargs):
            return forged if p == path else real(p, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=inject):
            with self.assertRaisesRegex(ValueError, 'exact noncertifying source custody'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_final_custody_rejects_false_full_paper_or_mathcert_claim(self):
        from unittest.mock import patch
        path = ('governance/erdos_proof_verification/admissions/'
                '0248_PROTECTED_EVIDENCE_ADMISSION_001.json')
        real = mod.load
        forged = copy.deepcopy(real(path))
        forged['claim_exclusions']['full_published_paper_verified'] = True
        forged['claim_exclusions']['mathcert_certified'] = True
        def inject(p, *args, **kwargs):
            return forged if p == path else real(p, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=inject):
            with self.assertRaisesRegex(ValueError, 'exact noncertifying source custody'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_terminal_status_cannot_claim_mathcert_or_missing_admission(self):
        bad = copy.deepcopy(self.good)
        bad['certification_status'] = 'MATHCERT_CERTIFIED'
        with self.assertRaises(ValueError):
            mod.validate_manifest(bad, self.schema)
        bad = copy.deepcopy(self.good)
        bad['stage_results']['PROTECTED_EVIDENCE_ADMISSION'] = 'PENDING'
        with self.assertRaisesRegex(ValueError, 'verified absent protected evidence'):
            mod.validate_manifest(bad, self.schema)

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



class Erdos249LacunaryReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schema = mod.load(mod.SCHEMA)
        cls.good = mod.load('governance/erdos_proof_verification/manifests/0249.json')
        cls.receipt = ('governance/erdos_proof_verification/evidence/0249/'
                       'LACUNARY_LEAN_GREEN_001.receipt.json')

    def test_actual_green_auxiliary_proof_keeps_original_open(self):
        m = copy.deepcopy(self.good)
        self.assertEqual(m['literature_status'], 'OPEN')
        self.assertEqual(m['work_status'], 'IN_PROGRESS')
        self.assertEqual(m['stage_results']['REPLAY_EXECUTION'], 'PASS')
        self.assertEqual(m['stage_results']['ADVERSARIAL_REVIEW'], 'PASS')
        self.assertEqual(m['stage_results']['INTERNAL_ADJUDICATION'], 'PASS')
        self.assertEqual(m['stage_results']['PROTECTED_EVIDENCE_ADMISSION'], 'PENDING')
        self.assertEqual(m['certification_status'], 'NOT_SUBMITTED')
        mod.validate_manifest(m, self.schema)

    def test_generic_or_missing_replay_cannot_pass(self):
        bad = copy.deepcopy(self.good)
        bad['proof_receipts'] = [x for x in bad['proof_receipts']
                                 if not x.endswith('LACUNARY_LEAN_GREEN_001.receipt.json')]
        with self.assertRaisesRegex(ValueError, 'exact bounded lacunary receipt'):
            mod.validate_manifest(bad, self.schema)

    def test_forged_original_full_series_result_fails(self):
        from unittest.mock import patch
        real = mod.load
        r = copy.deepcopy(real(self.receipt))
        r['original_erdos_249_full_series_irrational_claim'] = True
        def inject(path, *args, **kwargs):
            return r if path == self.receipt else real(path, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=inject):
            with self.assertRaisesRegex(ValueError, 'limited to exact pinned T'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_forged_sorry_ax_or_kernel_status_fails(self):
        from unittest.mock import patch
        real = mod.load
        r = copy.deepcopy(real(self.receipt))
        r['sorryAx_observed'] = True
        r['build_exit_code'] = 1
        def inject(path, *args, **kwargs):
            return r if path == self.receipt else real(path, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=inject):
            with self.assertRaisesRegex(ValueError, 'limited to exact pinned T'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_wrong_mathlib_or_compiler_pin_fails(self):
        bad = copy.deepcopy(self.good)
        bad['toolchain_pins']['mathlib'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'limited to exact pinned T'):
            mod.validate_manifest(bad, self.schema)

    def test_249_review_requires_exact_source_critical_receipt(self):
        m = copy.deepcopy(self.good)
        m['review_receipts'] = [p for p in m['review_receipts']
                                if '0249_SOURCE_CRITICAL_REVIEW_001' not in p]
        with self.assertRaisesRegex(ValueError, 'exact T review receipt'):
            mod.validate_manifest(m, self.schema)

    def test_249_referee_requires_exact_adjudication_receipt(self):
        m = copy.deepcopy(self.good)
        m['review_receipts'] = [p for p in m['review_receipts']
                                if '0249_REFEREE_ADJUDICATION_001' not in p]
        with self.assertRaisesRegex(ValueError, 'exact scoped Referee receipt'):
            mod.validate_manifest(m, self.schema)

    def test_249_adversary_cannot_claim_independent_human(self):
        from unittest.mock import patch
        file = ('governance/erdos_proof_verification/reviews/'
                '0249_SOURCE_CRITICAL_REVIEW_001.json')
        real = mod.load
        forged = copy.deepcopy(real(file))
        forged['independent_human_review'] = True
        def altered(path, *args, **kwargs):
            return forged if path == file else real(path, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=altered):
            with self.assertRaisesRegex(ValueError, 'exact qualified same-agent'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_249_referee_cannot_promote_original_S(self):
        from unittest.mock import patch
        file = ('governance/erdos_proof_verification/adjudications/'
                '0249_REFEREE_ADJUDICATION_001.json')
        real = mod.load
        forged = copy.deepcopy(real(file))
        forged['authority_effects']['original_conjecture_solved'] = True
        def altered(path, *args, **kwargs):
            return forged if path == file else real(path, *args, **kwargs)
        with patch.object(mod, 'load', side_effect=altered):
            with self.assertRaisesRegex(ValueError, 'exact noncertifying T scope'):
                mod.validate_manifest(copy.deepcopy(self.good), self.schema)

    def test_no_proof_of_open_series_from_bounded_green(self):
        bad = copy.deepcopy(self.good)
        bad['verification_kind'] = 'FULL_CONJECTURE_CERTIFICATION'
        with self.assertRaises(ValueError):
            mod.validate_manifest(bad, self.schema)
        bad = copy.deepcopy(self.good)
        bad['certification_status'] = 'MATHCERT_CERTIFIED'
        with self.assertRaises(ValueError):
            mod.validate_manifest(bad, self.schema)



if __name__ == '__main__':
    unittest.main()
