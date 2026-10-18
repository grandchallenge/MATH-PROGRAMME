#!/usr/bin/env python3
"""Hostile/positive tests of run outcome vs schedule-control separation."""
import json
import unittest
from pathlib import Path
from recurring_task_continuity import assess

POLICY = json.loads((Path(__file__).resolve().parents[1] / "governance/recurring_queue_continuity.json").read_text())
KEY = POLICY["task_key"]

class GuardTests(unittest.TestCase):
    def event(self, **changes):
        return {"task_key": KEY, **changes}

    def test_failure_never_retires_task(self):
        for outcome in ("PARTIAL", "TRANSIENT_ERROR", "SAFETY_DENIAL", "PERMISSION_ERROR", "NO_ELIGIBLE_WORK", "BLOCKED"):
            with self.subTest(outcome=outcome):
                e = self.event(type="RUN_RESULT", outcome=outcome, next_action="Resume independent authorized task")
                self.assertEqual(assess(POLICY, e)["desired_state"], "ENABLED")
                self.assertEqual(assess(POLICY, {**e, "schedule_mutation":"DISABLED"})["decision"], "DENY")
                self.assertEqual(assess(POLICY, {**e, "next_action":""})["decision"], "DENY")

    def test_success_does_not_infer_programme_termination(self):
        self.assertEqual(assess(POLICY, self.event(type="RUN_RESULT", outcome="SUCCEEDED"))["desired_state"], "ENABLED")

    def test_scheduler_drift_is_alarm(self):
        self.assertEqual(assess(POLICY, self.event(type="OBSERVATION", observed_state="DISABLED"))["decision"], "DRIFT_ALERT")
        self.assertEqual(assess(POLICY, self.event(type="OBSERVATION", observed_state="ENABLED"))["decision"], "OBSERVED_OK")

    def test_claimed_authority_without_actor_or_evidence_denied(self):
        e = self.event(type="SCHEDULE_MUTATION", target_state="DISABLED", authority="EXPLICIT_USER_DIRECTIVE")
        self.assertEqual(assess(POLICY,e)["decision"],"DENY")
        e["actor"]="assistant";self.assertEqual(assess(POLICY,e)["decision"],"DENY")
        e["authority_evidence"]="tool failed";e["authority"]="PLATFORM_SAFETY_DENIAL"
        self.assertEqual(assess(POLICY,e)["decision"],"DENY")

    def test_user_directive_and_protected_retirement(self):
        e = self.event(type="SCHEDULE_MUTATION", target_state="DISABLED", actor="authenticated actor", authority_evidence="source receipt", authority="EXPLICIT_USER_DIRECTIVE")
        self.assertEqual(assess(POLICY,e)["decision"],"PROPOSE_RETIREMENT")
        e["authority"]="PROTECTED_GOVERNED_RETIREMENT"
        self.assertEqual(assess(POLICY,e)["decision"],"DENY")
        e["protected_readback_verified"]=True
        self.assertEqual(assess(POLICY,e)["decision"],"PROPOSE_RETIREMENT")

    def test_enablement_and_policy_identity(self):
        e=self.event(type="SCHEDULE_MUTATION", target_state="ENABLED", actor="reconciler", authority_evidence="protected desired-state readback", authority="AUTHORIZED_CONTROLLER_RECONCILIATION")
        self.assertEqual(assess(POLICY,e)["decision"],"PROPOSE_ENABLEMENT")
        self.assertEqual(assess({**POLICY,"desired_state":"DISABLED"},e)["decision"],"DENY")
        self.assertEqual(assess(POLICY,{**e,"task_key":"another"})["decision"],"DENY")

if __name__ == '__main__':
    unittest.main()
