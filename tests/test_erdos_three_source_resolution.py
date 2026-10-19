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
    def test_installation_token_repository_scope(self):
        obj={'total_count':1,'repositories':[{'full_name':c.REPO}]}
        with patch.object(c,'api',return_value=obj):
            self.assertIsNone(c.verify_installation_scope())
        for bad in ({'total_count':2,'repositories':[{'full_name':c.REPO},{'full_name':'evil/other'}]},
                    {'total_count':1,'repositories':[{'full_name':'evil/other'}]},
                    {'login':'fyremael'}, {'total_count':1,'repositories':[]}):
            with self.subTest(bad=bad),patch.object(c,'api',return_value=bad):
                with self.assertRaises(c.CouncilError):c.verify_installation_scope()
    def test_reject_noninstallation_token(self):
        env={'GITHUB_ACTIONS':'true','GITHUB_REF':'refs/heads/main',
             'GCL_CONTROLLER_ID':'erdos-three-source-resolution','GH_TOKEN':'fake'}
        with patch.dict(os.environ,env,clear=True),patch.object(c,'api',return_value={'login':'fyremael'}):
            with self.assertRaises(c.CouncilError):c.apply_transitions([])
    def test_postwrite_bot_identity_must_match_source_blob(self):
        blob='a1b2-source-blob'
        row={'body':c.RESOLUTION+'\nNEW_GIT_BLOB_SHA1: '+blob+'\n',
             'user':{'login':'gcl-council-clerk[bot]'}}
        with patch.object(c,'comments',return_value=[row]):
            self.assertIsNone(c.verify_bot_resolution(2520,blob))
        for bad in ({'body':row['body'],'user':{'login':'fyremael'}},
                    {'body':c.RESOLUTION+'\nWRONG SOURCE','user':{'login':'gcl-council-clerk[bot]'}}):
            with self.subTest(bad=bad),patch.object(c,'comments',return_value=[bad]):
                with self.assertRaises(c.CouncilError):c.verify_bot_resolution(2520,blob)

    def test_protected_workflow_bootstrap_without_unpinned_dependencies(self):
        # Runner-level smoke guard is deliberately Python stdlib only.
        # The separate full workflow-coverage policy validator parses YAML
        # and tests hostile mutations under its governed CI dependency lane.
        workflow=c.ROOT/'.github/workflows/erdos-three-source-resolution.yml'
        source=workflow.read_text()
        self.assertEqual(source.count('environment: release-trust'),1)
        self.assertEqual(source.count('permission-issues: write'),1)
        self.assertEqual(source.count('permission-organization-projects: read'),1)
        self.assertEqual(source.count('refs/heads/main'),1)
        self.assertEqual(source.count('ci/erdos_three_source_resolution.py'),2)
        self.assertEqual(source.count('ci/erdos_final_two_source_resolution.py'),2)
        self.assertEqual(source.count("inputs.source_scope == 'final_two'"),3)
        self.assertEqual(source.count('--apply --receipt'),2)
        self.assertEqual(source.count('tests/test_erdos_three_source_resolution.py'),1)
        self.assertEqual(source.count('actions/create-github-app-token@'),1)
        self.assertNotIn('pip install',source)
        self.assertNotIn('permission-administration',source)
        self.assertNotIn('pull_request_target:',source)

if __name__=='__main__':unittest.main(verbosity=2)
