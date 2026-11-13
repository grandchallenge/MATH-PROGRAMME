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
        x=q.candidates('A');self.assertEqual((x[0]['problem_id'],x[0]['queue_issue']),(2,3212))
    def test_cohort_transition_exact(self):
        x=q.candidates('A',after=99,limit=2)
        self.assertEqual([r['problem_id'] for r in x],[100,101])
    def test_shard_filter(self):
        x=q.candidates('A',cohort='1201-1221',limit=30)
        self.assertEqual((len(x),x[0]['problem_id'],x[-1]['problem_id']),(21,1201,1221))
        self.assertTrue(all(r['queue_issue']==3224 for r in x))
    def test_only_source_ready_problem_enters_math_stage(self):
        x=q.candidates('B',limit=5)
        self.assertEqual([(item['problem_id'],item['queue_issue']) for item in x],[(1,3225)])
        self.assertEqual(q.candidates('B',after=1,limit=1),[])
    def test_downstream_formal_not_prematurely_dispatched(self):self.assertEqual(q.candidates('C',limit=5),[])
    def test_downstream_documentary_not_prematurely_dispatched(self):self.assertEqual(q.candidates('D',limit=5),[])
    def test_pilot_reuse_does_not_run_duplicate_work(self):
        x=q.read('governance/erdos_proof_verification/coverage/cohorts/0201-0300.json')['items'][45]
        self.assertEqual(x['problem_id'],246)
        self.assertFalse(q.permitted(x,'B'))
        self.assertEqual(x['stage_work_items']['B']['issue_number'],3202)
    def test_none_beyond_last(self):self.assertEqual(q.candidates('A',after=1221),[])
    def test_source_snapshots_are_not_claims(self):
        x=q.candidates('A')[0]
        self.assertTrue(x['requires_atomic_claim_and_live_readback'])
        self.assertNotIn('certified',x)

if __name__=='__main__':unittest.main()
