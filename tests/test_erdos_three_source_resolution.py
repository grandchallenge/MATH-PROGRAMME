#!/usr/bin/env python3
"""Hostile, no-network Council Clerk label-transition authorization tests."""
import json
import os
import unittest
from unittest.mock import patch
from ci import erdos_three_source_resolution as c

class CouncilThreeReviewTests(unittest.TestCase):
    def base(self,*,state='OPEN',queue='RETURNED',field='RETURNED',labels=None):
        if labels is None:labels=['gcl-review:revise']
        obj={'state':state,'labels':[{'name':name} for name in labels],
             'projectItems':[{'title':'GCL Worker Queue','status':{'name':queue}}]}
        fields=[{'issue_field_name':'GCL State','single_select_option':{'name':field}}]
        return obj,fields
    def inspect(self,**kwargs):
        obj,fields=self.base(**kwargs)
        def get(*args):return json.dumps(obj)
        with patch.object(c,'execute',side_effect=get),patch.object(c,'api',return_value=fields):
            return c.issue_snapshot(2520)
    def test_exact_source_only_authority_roster(self):
        self.assertEqual(c.TARGET,{2520:11,2521:12,2523:15})
        self.assertEqual(c.EXCLUDED,(2522,2536))
        self.assertEqual(len(c.MERGES),3)
    def test_positive_returned_and_revise(self):
        s=self.inspect()
        self.assertTrue(s['revise'])
        self.assertFalse(s['corrected'])
        self.assertEqual(s['state'],'OPEN')
    def test_completed_source_label_is_not_custody_mutation(self):
        s=self.inspect(labels=['gcl-review:source-corrected'])
        self.assertTrue(s['corrected'])
        self.assertFalse(s['revise'])
    def test_reject_closure(self):
        with self.assertRaises(c.CouncilError):self.inspect(state='CLOSED')
    def test_reject_project_change(self):
        with self.assertRaises(c.CouncilError):self.inspect(queue='AVAILABLE')
    def test_reject_issue_field_change(self):
        with self.assertRaises(c.CouncilError):self.inspect(field='AVAILABLE')
    def test_reject_project_unknown(self):
        with self.assertRaises(c.CouncilError):self.inspect(queue='Todo')
    def test_reject_app_action_outside_protected_env(self):
        env={'GITHUB_ACTIONS':'false','GITHUB_REF':'refs/heads/main',
             'GCL_CONTROLLER_ID':'erdos-three-source-resolution','GH_TOKEN':'fake'}
        with patch.dict(os.environ,env,clear=True):
            with self.assertRaises(c.CouncilError):c.apply_transitions([])
    def test_reject_app_action_outside_main(self):
        env={'GITHUB_ACTIONS':'true','GITHUB_REF':'refs/heads/something',
             'GCL_CONTROLLER_ID':'erdos-three-source-resolution','GH_TOKEN':'fake'}
        with patch.dict(os.environ,env,clear=True):
            with self.assertRaises(c.CouncilError):c.apply_transitions([])
    def test_reject_forged_bot(self):
        env={'GITHUB_ACTIONS':'true','GITHUB_REF':'refs/heads/main',
             'GCL_CONTROLLER_ID':'erdos-three-source-resolution','GH_TOKEN':'fake'}
        with patch.dict(os.environ,env,clear=True),patch.object(c,'api',return_value={'login':'fyremael'}):
            with self.assertRaises(c.CouncilError):c.apply_transitions([])

    def test_protected_workflow_contract_and_permission_falsifiers(self):
        import sys
        sys.path.insert(0,str(c.ROOT/'ci'))
        from validate_workflow_coverage_v2 import three_source_council_errors,THREE_SOURCE_COUNCIL_WORKFLOW
        source=(c.ROOT/'.github/workflows/erdos-three-source-resolution.yml').read_text()
        docs={THREE_SOURCE_COUNCIL_WORKFLOW:source}
        self.assertEqual(three_source_council_errors(docs),[])
        self.assertTrue(three_source_council_errors({THREE_SOURCE_COUNCIL_WORKFLOW:source.replace('permission-issues: write','permission-issues: read')}))
        self.assertTrue(three_source_council_errors({THREE_SOURCE_COUNCIL_WORKFLOW:source.replace('permission-organization-projects: read','permission-organization-projects: write')}))
        self.assertTrue(three_source_council_errors({THREE_SOURCE_COUNCIL_WORKFLOW:source.replace(' --apply --receipt ',' --dry-run --receipt ')}))
        self.assertTrue(three_source_council_errors({THREE_SOURCE_COUNCIL_WORKFLOW:source.replace('environment: release-trust','environment: other')}))

if __name__=='__main__':unittest.main(verbosity=2)
