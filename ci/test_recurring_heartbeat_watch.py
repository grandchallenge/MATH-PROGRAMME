#!/usr/bin/env python3
"""Hostile acceptance tests for an independent GitHub missed-heartbeat monitor."""
import unittest
from recurring_heartbeat_watch import evaluate, fields, ALERT_HEADER

POLICY={'task_key':'GCL-QUEUE-REDUCTION-HOURLY','desired_state':'ENABLED','cadence':'HOURLY',
        'heartbeat_issue':2763,'heartbeat_authorized_actors':['fyremael'],
        'heartbeat_activation_utc':'2026-10-18T23:45:00Z','heartbeat_grace_minutes':180}

def receipt(when='2026-10-19T00:00:00Z',actor='fyremael',reported=None,comment_id=100,kind='SUCCEEDED'):
    body=f'GCL-SCHEDULER-RUN/1\nTASK_KEY: {POLICY["task_key"]}\nRUN_AT_UTC: {reported or when}\nOUTCOME: {kind}\nNEXT_ACTION: Continue bounded authenticated queue reduction\n'
    return {'createdAt':when,'author':{'login':actor},'body':body,'databaseId':comment_id,
            'url':f'https://github.com/grandchallenge/MATH-PROGRAMME/issues/2763#issuecomment-{comment_id}'}

class WatchTests(unittest.TestCase):
    def test_fresh_valid_run_and_failure_outcomes_count_as_liveness(self):
        for kind in ('SUCCEEDED','PARTIAL','SAFETY_DENIAL','BLOCKED','TRANSIENT_ERROR','NO_ELIGIBLE_WORK'):
            with self.subTest(kind=kind):
                r=evaluate(POLICY,[receipt(kind=kind)],'2026-10-19T01:00:00Z')
                self.assertEqual(r['state'],'HEALTHY_HEARTBEAT')
                self.assertEqual(r['valid_count_in_window'],1)
    def test_retrospective_recovery_cannot_certify_worker_origin(self):
        manual=receipt('2026-10-19T03:50:00Z',comment_id=300,kind='BLOCKED')
        manual['body']+='RECOVERY_MODE: STEWARD_AUTHORIZED_RETROSPECTIVE_HEARTBEAT\n'
        result=evaluate(POLICY,[manual],'2026-10-19T04:00:00Z')
        self.assertEqual(result['state'],'ALERT_MISSED_HEARTBEAT')
        self.assertEqual(result['valid_count_in_window'],0)
        self.assertEqual(result['retrospective_recovery_count'],1)
        self.assertEqual(result['rejected_marker_count'],0)
        actual=receipt('2026-10-19T03:55:00Z',comment_id=301,kind='PARTIAL')
        actual['body']+='REPORT_STAGE: EARLY_RUN_LIVENESS_ONLY\n'
        accepted=evaluate(POLICY,[manual,actual],'2026-10-19T04:00:00Z')
        self.assertEqual(accepted['state'],'HEALTHY_HEARTBEAT')
        self.assertEqual(accepted['valid_count_in_window'],1)
        self.assertEqual(accepted['retrospective_recovery_count'],1)
        self.assertEqual(accepted['last_valid_comment'],actual['url'])
    def test_absence_triggers_alert_only_after_grace(self):
        self.assertEqual(evaluate(POLICY,[],'2026-10-19T02:44:00Z')['state'],'AWAITING_FIRST_HEARTBEAT')
        self.assertEqual(evaluate(POLICY,[],'2026-10-19T02:46:00Z')['state'],'ALERT_MISSED_HEARTBEAT')
    def test_stale_episode_and_fresh_recovery(self):
        t='2026-10-19T04:00:00Z'
        r=evaluate(POLICY,[receipt() ],t)
        self.assertEqual(r['state'],'ALERT_MISSED_HEARTBEAT')
        newer=receipt('2026-10-19T03:50:00Z',comment_id=200)
        r2=evaluate(POLICY,[receipt(),newer],t)
        self.assertEqual(r2['state'],'HEALTHY_HEARTBEAT')
        self.assertNotEqual(r['episode_id'],r2['episode_id'])
    def test_spoofed_wrong_actor_or_stale_body_does_not_extend(self):
        bad=[receipt(actor='attacker'),receipt(reported='2026-10-19T04:00:00Z',comment_id=2),
             receipt(kind='UNKNOWN',comment_id=3)]
        r=evaluate(POLICY,bad,'2026-10-19T04:00:00Z')
        self.assertEqual(r['state'],'ALERT_MISSED_HEARTBEAT')
        self.assertEqual(r['valid_count_in_window'],0)
        self.assertEqual(r['rejected_marker_count'],3)
    def test_ordinary_comments_or_alerts_do_not_fake_heartbeats(self):
        xs=[{'body':'I ran something','createdAt':'2026-10-19T03:30:00Z'},
            {'body':'GCL-SCHEDULER-OUTAGE/1\nEPISODE_ID: X\n','createdAt':'2026-10-19T03:30:00Z'}]
        self.assertEqual(evaluate(POLICY,xs,'2026-10-19T04:00:00Z')['state'],'ALERT_MISSED_HEARTBEAT')
    def test_protected_retirement_not_reenabled_by_monitor(self):
        p={**POLICY,'desired_state':'DISABLED'}
        self.assertEqual(evaluate(p,[receipt()],'2026-10-19T04:00:00Z')['state'],'CONTRACT_NOT_ENABLED')
    def test_duplicate_and_malformed_fields_rejected(self):
        invalid=receipt();invalid['body']+='OUTCOME: SUCCEEDED\n'
        self.assertEqual(evaluate(POLICY,[invalid],'2026-10-19T04:00:00Z')['valid_count_in_window'],0)
        self.assertIsNone(fields('GCL-SCHEDULER-RUN/1\nNO_SEP','GCL-SCHEDULER-RUN/1'))
        self.assertEqual(fields(ALERT_HEADER+'\nEPISODE_ID: abc\n',ALERT_HEADER),{'EPISODE_ID':'abc'})
    def test_independent_wake_paths_configured(self):
        from pathlib import Path
        workflow = (Path(__file__).resolve().parents[1] /
                    '.github/workflows/recurring-queue-heartbeat-watch.yml').read_text()
        self.assertIn("cron: '17 * * * *'", workflow)
        self.assertIn("cron: '43 * * * *'", workflow)
        self.assertIn("issue_comment:\n    types: [created]", workflow)
        self.assertIn("workflow_dispatch:", workflow)

    def test_issue_comment_wakeup_cannot_expand_to_other_issues(self):
        from pathlib import Path
        workflow = (Path(__file__).resolve().parents[1] /
                    '.github/workflows/recurring-queue-heartbeat-watch.yml').read_text()
        self.assertIn("github.event_name != 'issue_comment' || github.event.issue.number == 2763", workflow)
        self.assertIn('contents: read', workflow)
        self.assertNotIn('issues: write', workflow)
        self.assertIn('cancel-in-progress: false', workflow)

if __name__=='__main__':unittest.main()
