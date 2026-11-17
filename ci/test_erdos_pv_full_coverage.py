#!/usr/bin/env python3
"""Adversarial regression checks for false proof/workstream closure."""
import copy
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).with_name('validate_erdos_pv_full_coverage.py')
spec=importlib.util.spec_from_file_location('pv_full_coverage',p)
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)

class CoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source=v.read(v.SRC)['issues']
        cls.pack=v.read('governance/erdos_proof_verification/coverage/cohorts/0201-0300.json')
        cls.base=cls.pack['items'][51]  # problem 252: ordinary nonpilot
        cls.src=cls.source[251]
        cls.phase=cls.pack['phase_issues']
    def reject(self,mutation):
        bad=copy.deepcopy(self.base)
        mutation(bad)
        with self.assertRaises(ValueError):v.validate_row(bad,self.src,self.phase)
    def test_full_population_and_one_bounded_terminal(self):
        result=v.validate()
        self.assertEqual((result['individual_problems'],result['project_issues'],result['substantive_terminal_count']),(1221,58,1))
        first=v.read('governance/erdos_proof_verification/coverage/cohorts/0001-0100.json')['items'][0]
        self.assertEqual(first['closure_status'], 'ADMITTED_BOUNDED_COMPLETE')
        self.assertEqual(first['mathcert_status'], 'NOT_SUBMITTED')
        self.assertFalse(v.read('governance/erdos_proof_verification/coverage/cohorts/0001-0100.json')['fully_verified'])
    def test_wrong_source_issue(self):self.reject(lambda x:x.__setitem__('source_audit_issue',3201))
    def test_wrong_source_body_sha(self):self.reject(lambda x:x.__setitem__('source_issue_body_sha256','0'*64))
    def test_status_at_lock_is_not_rewritable(self):self.reject(lambda x:x.__setitem__('catalogue_status_at_lock','proved'))
    def test_missing_phase(self):self.reject(lambda x:x['stage_work_items'].pop('C'))
    def test_duplicate_task_issue_without_manifest(self):self.reject(lambda x:x['stage_work_items']['B'].__setitem__('issue_number',3269))
    def test_false_math_result(self):self.reject(lambda x:x['stage_work_items']['B'].__setitem__('work_status','VERIFIED_BOUNDED'))
    def test_false_replay_without_axioms(self):self.reject(lambda x:x['stage_work_items']['C'].__setitem__('formal_replay_receipt','evidence/replay.json'))
    def test_false_protected_admission(self):
        def change(x):
            t=x['stage_work_items']['D'];t['work_status']='PROTECTED_ADMITTED';t['review_status']='PASS';t['evidence_refs']=['evidence/review.json']
        self.reject(change)
    def test_false_terminal_without_upstream(self):
        def change(x):
            x['closure_status']='ADMITTED_BOUNDED_COMPLETE';x['closure_evidence_refs']=['evidence/proposal.json']
            t=x['stage_work_items']['D'];t.update(work_status='PROTECTED_ADMITTED',review_status='PASS',evidence_refs=['evidence/review.json'],protected_admission_ref='main@abc')
        self.reject(change)
    def test_claimed_certificate_without_mathcert(self):self.reject(lambda x:x.__setitem__('mathcert_status','CERTIFIED'))
    def test_silent_decline(self):self.reject(lambda x:x.__setitem__('triage_decision','DECLINED_WITH_REASON'))
    def test_silent_reuse(self):self.reject(lambda x:x.__setitem__('triage_decision','REUSED_EXISTING_VERIFICATION'))
    def test_evidence_free_blocker(self):self.reject(lambda x:x['stage_work_items']['B'].__setitem__('work_status','EVIDENCE_BLOCKED'))
    def test_missing_pilot_reuse_is_rejected(self):
        row=copy.deepcopy(v.read('governance/erdos_proof_verification/coverage/cohorts/0201-0300.json')['items'][45]) #246
        self.assertEqual(row['problem_id'],246)
        row['existing_proof_issue']=None
        with self.assertRaises(ValueError):v.validate_row(row,self.source[245],self.phase)
    def test_five_source_scope_triage_is_complete_and_bounded(self):
        cohort=v.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')
        for n in range(560,565):
            with self.subTest(problem=n):
                row=cohort['items'][n-501]
                v.validate_row(row,self.source[n-1],cohort['phase_issues'])
                self.assertEqual(row['source_issue_live_state'],'OPEN_RETURNED')
                self.assertEqual(row['mathcert_status'],'NOT_SUBMITTED')
                self.assertEqual(row['stage_work_items']['B']['work_status'],
                                 'PROTECTED_ADMITTED' if n==560 else 'UNEXECUTED')
                if n<=562:
                    self.assertEqual(row['triage_decision'],'SELECTED_WITH_MANIFEST')
                    self.assertEqual(row['stage_work_items']['A']['work_status'],'VERIFIED_BOUNDED')
                else:
                    self.assertEqual(row['triage_decision'],'PENDING')
                    self.assertEqual(row['stage_work_items']['A']['work_status'],'EVIDENCE_BLOCKED')

    def test_five_source_triage_undocumented_promotion_rejected(self):
        cohort=v.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')
        for n in range(560,565):
            row=cohort['items'][n-501]
            for mutation in (
                lambda r:r.__setitem__('triage_decision','SELECTED_WITH_MANIFEST' if n>562 else 'PENDING'),
                lambda r:r['stage_work_items']['A'].__setitem__('evidence_refs',[]),
                lambda r:r['stage_work_items']['B'].__setitem__('work_status','VERIFIED_BOUNDED' if n==560 else 'PROTECTED_ADMITTED'),
                lambda r:r.__setitem__('scope','FULL_ORIGINAL_CONJECTURE_SOLVED'),
            ):
                with self.subTest(problem=n,mutation=str(mutation)):
                    bad=copy.deepcopy(row);mutation(bad)
                    with self.assertRaises(ValueError):
                        v.validate_row(bad,self.source[n-1],cohort['phase_issues'])

    def test_bounded_560_requires_exact_review_and_no_early_protected_claim(self):
        cohort=v.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')
        row=cohort['items'][560-501]
        for mutation in (
            lambda x:x['stage_work_items']['B'].__setitem__('evidence_refs',[]),
            lambda x:x['stage_work_items']['B'].__setitem__('source_lock_receipt','wrong'),
            lambda x:x['stage_work_items']['B'].__setitem__('review_status','NOT_REVIEWED'),
            lambda x:x['stage_work_items']['B'].__setitem__('semantic_equivalence_receipt',None),
            lambda x:x['stage_work_items']['B'].__setitem__('adversarial_review_receipt',None),
            lambda x:x['stage_work_items']['B'].__setitem__('protected_admission_ref','main@forged'),
            lambda x:x['stage_work_items']['C'].__setitem__('work_status','VERIFIED_BOUNDED'),
        ):
            bad=copy.deepcopy(row)
            mutation(bad)
            with self.assertRaises(ValueError):
                v.validate_row(bad,self.source[559],cohort['phase_issues'])

    def test_560_protected_b_exact_material_binding_and_noncertification(self):
        cohort=v.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')
        row=cohort['items'][59]
        b=row['stage_work_items']['B']
        self.assertEqual(b['work_status'],'PROTECTED_ADMITTED')
        self.assertEqual(b['protected_admission_ref'],
            'grandchallenge/MATH-PROGRAMME@997a3d8068c3b2a036d5811bfabfce2b92a4be15')
        self.assertIsNone(b['formal_replay_receipt'])
        self.assertEqual(row['mathcert_status'],'NOT_SUBMITTED')
        self.assertEqual(row['stage_work_items']['C']['work_status'],'PROTECTED_ADMITTED')

    def test_560_c_protected_custody_exact_sha_and_no_false_promotion(self):
        cohort=v.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')
        row=cohort['items'][59]
        c=row['stage_work_items']['C']
        custody_path='governance/erdos_proof_verification/evidence/0560/C_PROTECTED_CUSTODY_BINDING_001.json'
        self.assertEqual(c['work_status'],'PROTECTED_ADMITTED')
        self.assertEqual(c['protected_admission_ref'],
                         'grandchallenge/MATH-PROGRAMME@2371fb3feda35d98f6da19855a0a1348ca284afa')
        self.assertIn(custody_path,c['evidence_refs'])
        custody=v.read(custody_path)
        self.assertEqual(len(custody['protected_source_and_artifact_blob_ids']),15)
        self.assertTrue(custody['formalization_work_required'])
        self.assertTrue(all(flag is False for flag in custody['nonclaims'].values()))
        self.assertEqual(row['stage_work_items']['D']['work_status'],'VERIFIED_BOUNDED')
        self.assertEqual(row['mathcert_status'],'NOT_SUBMITTED')
        for mutation in (
            lambda b:b.__setitem__('protected_admission_ref','grandchallenge/MATH-PROGRAMME@'+'f'*40),
            lambda b:b.__setitem__('work_status','VERIFIED_BOUNDED'),
            lambda b:b.__setitem__('evidence_refs',b['evidence_refs'][:-1]),
        ):
            bad=copy.deepcopy(row)
            mutation(bad['stage_work_items']['C'])
            with self.assertRaises(ValueError):
                v.validate_row(bad,self.source[559],cohort['phase_issues'])

    def test_560_partial_formal_review_cannot_promote_full_proof(self):
        cohort=v.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')
        row=cohort['items'][59]
        for mutation in (
          lambda b:b.__setitem__('blocker',None),
          lambda b:b.__setitem__('formal_replay_receipt',None),
          lambda b:b.__setitem__('axiom_report_receipt',None),
          lambda b:b.__setitem__('evidence_refs',[]),
          lambda b:b.__setitem__('source_lock_receipt','forged'),
          lambda b:b.__setitem__('semantic_equivalence_receipt',None),
          lambda b:b.__setitem__('adversarial_review_receipt',None),
          lambda b:b.__setitem__('review_status','NOT_REVIEWED'),
          lambda b:b.__setitem__('protected_admission_ref','main@not_merged'),
        ):
            bad=copy.deepcopy(row)
            mutation(bad['stage_work_items']['C'])
            with self.assertRaises(ValueError):
                v.validate_row(bad,self.source[559],cohort['phase_issues'])

    def test_560_documentary_candidate_is_exact_reviewed_nonterminal(self):
        cohort=v.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')
        row=cohort['items'][59]
        d=row['stage_work_items']['D']
        self.assertEqual(d['work_status'],'VERIFIED_BOUNDED')
        self.assertEqual(d['review_status'],'ROLE_SCOPED_CRITICAL_PASS')
        self.assertEqual(d['protected_admission_ref'],None)
        self.assertEqual(row['closure_status'],'IN_PROGRESS')
        self.assertEqual(row['mathcert_status'],'NOT_SUBMITTED')
        self.assertEqual(len(d['evidence_refs']),4)
        proof=v.read('governance/erdos_proof_verification/evidence/0560/D_DOCUMENTARY_REVIEW_001.json')
        self.assertEqual(proof['original_problem_status'],'OPEN')
        self.assertFalse(proof['full_primary_proposition_in_lean'])
        self.assertEqual(proof['kernel_checked_auxiliary_declarations'],12)
        for mutation in (
            lambda r:r.__setitem__('closure_status','ADMITTED_BOUNDED_COMPLETE'),
            lambda r:r.__setitem__('scope','FULL_ORIGINAL_CONJECTURE_SOLVED'),
            lambda r:r.__setitem__('mathcert_status','CERTIFIED'),
            lambda r:r['stage_work_items']['D'].__setitem__('blocker',None),
            lambda r:r['stage_work_items']['D'].__setitem__('review_status','NOT_REVIEWED'),
            lambda r:r['stage_work_items']['D'].__setitem__('adversarial_review_receipt',None),
            lambda r:r['stage_work_items']['D'].__setitem__('evidence_refs',[]),
            lambda r:r['stage_work_items']['D'].__setitem__('protected_admission_ref','main@forged'),
            lambda r:r['stage_work_items']['C'].__setitem__('work_status','VERIFIED_BOUNDED'),
        ):
            bad=copy.deepcopy(row)
            mutation(bad)
            with self.assertRaises(ValueError):
                v.validate_row(bad,self.source[559],cohort['phase_issues'])

    def test_open_conjecture_promotion_is_rejected(self):
        row=next(x for x in self.pack['items'] if x['catalogue_status_at_lock']=='open' and x['problem_id'] not in v.PILOT)
        bad=copy.deepcopy(row);bad['scope']='FULL_ORIGINAL_CONJECTURE_SOLVED'
        with self.assertRaises(ValueError):v.validate_row(bad,self.source[row['problem_id']-1],self.phase)

if __name__=='__main__':unittest.main()
