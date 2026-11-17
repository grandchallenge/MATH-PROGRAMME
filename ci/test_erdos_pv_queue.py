#!/usr/bin/env python3
import importlib.util
import unittest
from pathlib import Path
p=Path(__file__).with_name('erdos_pv_queue.py')
spec=importlib.util.spec_from_file_location('pv_queue',p)
# command-line module import uses its same-directory validator
import sys
sys.path.insert(0,str(p.parent))
q=importlib.util.module_from_spec(spec);spec.loader.exec_module(q)

class QueueTests(unittest.TestCase):
    def test_first_runnable_reflects_protected_source_completion(self):
        x=q.candidates('A')
        self.assertTrue(x)
        first=x[0]
        self.assertEqual(first['queue_issue'],3212)
        self.assertGreater(first['problem_id'],1)
        row=q.read('governance/erdos_proof_verification/coverage/cohorts/0001-0100.json')['items'][first['problem_id']-1]
        self.assertTrue(q.permitted(row,'A'))
        self.assertEqual(row['stage_work_items']['A']['work_status'],'UNEXECUTED')
    def test_cohort_transition_exact(self):
        x=q.candidates('A',after=99,limit=2)
        self.assertEqual([r['problem_id'] for r in x],[100,101])
    def test_shard_filter(self):
        x=q.candidates('A',cohort='1201-1221',limit=30)
        self.assertEqual((len(x),x[0]['problem_id'],x[-1]['problem_id']),(21,1201,1221))
        self.assertTrue(all(r['queue_issue']==3224 for r in x))
    def test_protected_math_return_not_selected_again(self):
        x=q.candidates('B',limit=5)
        self.assertTrue(all(r['task_id']!='ERDOS-PV-0001-B' for r in x))
        self.assertTrue(all(r['problem_id']>1 for r in x))
        cohort=q.read('governance/erdos_proof_verification/coverage/cohorts/0001-0100.json')
        for candidate in x:
            if candidate['cohort']!='0001-0100':
                continue
            row=cohort['items'][candidate['problem_id']-1]
            self.assertTrue(q.permitted(row,'B'))
            self.assertIn(row['stage_work_items']['A']['work_status'],q.READY)
        self.assertTrue(all(r['problem_id']>1 for r in q.candidates('B',after=1,limit=5)))
    def test_formal_selection_is_scoped_to_reviewed_math(self):
        candidates=q.candidates('C',limit=5)
        self.assertTrue(all(x['problem_id']!=1 for x in candidates))
        for x in candidates:
            reg=q.read(q.REG)
            meta=reg['cohorts'][(x['problem_id']-1)//100]
            row=q.read(meta['packet'])['items'][(x['problem_id']-1)%100]
            self.assertTrue(q.permitted(row,'C'))
            self.assertIn(row['stage_work_items']['B']['work_status'],q.READY)
            self.assertEqual(row['stage_work_items']['C']['work_status'],'UNEXECUTED')
    def test_only_formal_reviewed_problem_enters_documentary(self):
        self.assertEqual(q.candidates('D',limit=5),[]) # returned D evidence is not re-dispatchable
    def test_pilot_reuse_does_not_run_duplicate_work(self):
        x=q.read('governance/erdos_proof_verification/coverage/cohorts/0201-0300.json')['items'][45]
        self.assertEqual(x['problem_id'],246)
        self.assertFalse(q.permitted(x,'B'))
        self.assertEqual(x['stage_work_items']['B']['issue_number'],3202)
    def test_566_567_formal_source_override_fails_closed(self):
        for problem, expected in q.RAMSEY_SOURCE_BLOBS.items():
            with self.subTest(problem=problem):
                row = q.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')['items'][problem-501]
                self.assertEqual(row['problem_id'], problem)
                x = q.checked_formal_source_override(problem)
                self.assertEqual(x['commit'], q.RAMSEY_SOURCE_COMMIT)
                self.assertEqual(x['git_blob_sha1'], expected)
                self.assertEqual(x['original_invariant'], 'SimpleGraph.graphRamsey')
                self.assertEqual(x['legacy_invariant_disallowed'], 'SimpleGraph.sizeRamsey')
        self.assertIsNone(q.checked_formal_source_override(564))

    def test_selected_560_562_enter_existing_phase_b_only(self):
        x=q.candidates('B',after=559,cohort='0501-0600',limit=10)
        self.assertEqual([r['problem_id'] for r in x],[560,561,562])
        self.assertTrue(all(r['queue_issue']==3230 for r in x))
        self.assertTrue(all(r['triage_decision']=='SELECTED_WITH_MANIFEST' for r in x))
        self.assertFalse(any(xi['problem_id'] in (563,564) for xi in x))

    def test_pending_triage_never_enters_phase_b(self):
        x=q.read('governance/erdos_proof_verification/coverage/cohorts/0501-0600.json')['items'][62]
        self.assertEqual(x['problem_id'],563)
        # Even if a future Phase A receipt becomes green, PENDING must not
        # convert source work automatically into mathematical-verification work.
        from copy import deepcopy
        lifted=deepcopy(x)
        lifted['stage_work_items']['A']['work_status']='VERIFIED_BOUNDED'
        self.assertFalse(q.permitted(lifted,'B'))

    def test_none_beyond_last(self):self.assertEqual(q.candidates('A',after=1221),[])
    def test_source_snapshots_are_not_claims(self):
        x=q.candidates('A')[0]
        self.assertTrue(x['requires_atomic_claim_and_live_readback'])
        self.assertNotIn('certified',x)

if __name__=='__main__':unittest.main()
