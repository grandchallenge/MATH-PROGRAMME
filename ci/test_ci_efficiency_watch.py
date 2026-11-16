#!/usr/bin/env python3
"""Adversarial checks: bounded sampling, exact PR identity, failure modes."""
import datetime as dt
import unittest
from unittest.mock import patch
import urllib.error
import ci_efficiency_watch as watch

SHA='a'*40
NOW=dt.datetime(2026,11,16,12,tzinfo=dt.timezone.utc)
RUN={'id':123,'event':'pull_request','head_sha':SHA,'status':'completed',
     'created_at':'2026-11-16T09:30:00Z'}
PR={'number':3391,'head':{'sha':SHA},'base':{'ref':'main'},'changed_files':1}

class FakeReader:
    def __init__(self, pilot='success', paths=('docs/test.md',), limit=32):
        self.calls=0;self.maximum=limit;self.pilot=pilot;self.paths=paths
    def get(self,path):
        self.calls+=1
        if self.calls>self.maximum:raise watch.BudgetExceeded()
        if 'gcl-conformance.yml' in path:return {'workflow_runs':[RUN]}
        if '/actions/runs/123/jobs' in path:
            return {'total_count':2,'jobs':[
                {'name':'GCL ASSURE PR synthetic dossier','conclusion':self.pilot},
                {'name':'GCL DISCLOSE PR synthetic release gate','conclusion':'skipped'}]}
        if path.endswith('/pulls?per_page=10'):return [PR]
        if path.endswith('/pulls/3391'):return PR
        if path.endswith('/pulls/3391/files?per_page=100'):
            return [{'filename':p} for p in self.paths]
        if 'pages.yml' in path:return {'workflow_runs':[{'conclusion':'skipped'}]}
        if 'deployments?' in path:return [{'sha':'b'*40}]
        if 'rate_limit' in path:return {'resources':{'graphql':{
            'remaining':4000,'limit':5000,'reset':int(NOW.timestamp())+3000}}}
        raise AssertionError(path)

class WatchTests(unittest.TestCase):
    def test_actual_unneeded_success_is_alert(self):
        r=FakeReader()
        report=watch.audit(r,NOW)
        self.assertEqual(report['status'],'ALERT')
        self.assertEqual(report['alerts'][0]['kind'],'IRRELEVANT_PILOT_START')
        self.assertLessEqual(r.calls,r.maximum)
    def test_skipped_unneeded_pilots_is_clean(self):
        report=watch.audit(FakeReader(pilot='skipped'),NOW)
        self.assertEqual(report['status'],'OBSERVED_NO_ALERT')
    def test_relevant_assurance_is_allowed(self):
        # One modified file, so PR file count is internally consistent.
        report=watch.audit(FakeReader(paths=('ci/assure_pr.py',)),NOW)
        self.assertEqual(report['status'],'OBSERVED_NO_ALERT')
    def test_identity_drift_is_inconclusive(self):
        class Drift(FakeReader):
            def get(self,path):
                if path.endswith('/pulls/3391'):
                    self.calls+=1;return dict(PR,head={'sha':'c'*40})
                return super().get(path)
        report=watch.audit(Drift(),NOW)
        self.assertEqual(report['status'],'INCONCLUSIVE')
        self.assertFalse(report['alerts'])
    def test_budget_exhaustion_is_bounded(self):
        report=watch.audit(FakeReader(limit=2),NOW)
        self.assertEqual(report['status'],'INCONCLUSIVE')
        self.assertTrue(any(x['reason']=='EVIDENCE_READ_INCOMPLETE' for x in report['inconclusive']))
    def test_api_denial_fails_to_inconclusive_without_claim(self):
        class Denied(FakeReader):
            def get(self,path):
                raise urllib.error.HTTPError('https://api.github.com',403,'Denied',None,None)
        report=watch.audit(Denied(),NOW)
        self.assertEqual(report['status'],'INCONCLUSIVE')
        self.assertFalse(report['alerts'])
    def test_duplicate_deployment_not_proved_redundant(self):
        class Duplicate(FakeReader):
            def get(self,path):
                if 'deployments?' in path:
                    self.calls+=1;return [{'sha':'d'*40},{'sha':'d'*40}]
                return super().get(path)
        report=watch.audit(Duplicate(pilot='skipped'),NOW)
        self.assertEqual(report['status'],'INCONCLUSIVE')
        self.assertFalse(report['alerts'])
    def test_graphql_pressure_reset_aware(self):
        class Pressure(FakeReader):
            def get(self,path):
                if 'rate_limit' in path:
                    self.calls+=1;return {'resources':{'graphql':{'remaining':150,'limit':5000,
                              'reset':int(NOW.timestamp())+3600}}}
                return super().get(path)
        report=watch.audit(Pressure(pilot='skipped'),NOW)
        self.assertEqual(report['alerts'][0]['kind'],'GRAPHQL_BUDGET_PRESSURE')

if __name__=='__main__':
    unittest.main()
