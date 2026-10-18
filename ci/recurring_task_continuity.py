#!/usr/bin/env python3
"""Pure recurrence-state guard. The actual scheduler adapter must enforce it."""
import argparse
import json
from pathlib import Path

CONTRACT = "GCL-RECURRENT-EXECUTION-CONTINUITY-001"
FAILURES = {"PARTIAL", "TRANSIENT_ERROR", "SAFETY_DENIAL", "PERMISSION_ERROR", "NO_ELIGIBLE_WORK", "BLOCKED"}


def assess(policy, event):
    if policy.get("contract_id") != CONTRACT or policy.get("desired_state") != "ENABLED" or policy.get("cadence") != "HOURLY":
        return {"decision": "DENY", "reason": "invalid-protected-intent"}
    if event.get("task_key") != policy.get("task_key"):
        return {"decision": "DENY", "reason": "task-mismatch"}
    kind = event.get("type")
    if kind == "RUN_RESULT":
        outcome = event.get("outcome")
        if outcome not in FAILURES | {"SUCCEEDED"}:
            return {"decision": "DENY", "reason": "invalid-run-result"}
        if event.get("schedule_mutation") not in (None, "NONE"):
            return {"decision": "DENY", "reason": "run-cannot-retire-recurrence"}
        if outcome in FAILURES and not str(event.get("next_action", "")).strip():
            return {"decision": "DENY", "reason": "missing-durable-resume-action"}
        return {"decision": "RUN_RECORDED", "desired_state": "ENABLED"}
    if kind == "OBSERVATION":
        actual = event.get("observed_state")
        if actual not in ("ENABLED", "DISABLED"):
            return {"decision": "DENY", "reason": "unverified-observed-state"}
        return {"decision": "DRIFT_ALERT" if actual != "ENABLED" else "OBSERVED_OK", "desired_state": "ENABLED"}
    if kind != "SCHEDULE_MUTATION":
        return {"decision": "DENY", "reason": "invalid-event-type"}
    actor, evidence = event.get("actor"), event.get("authority_evidence")
    if not isinstance(actor, str) or not actor.strip() or not isinstance(evidence, str) or not evidence.strip():
        return {"decision": "DENY", "reason": "missing-actor-or-evidence"}
    target, authority = event.get("target_state"), event.get("authority")
    if target == "DISABLED":
        if authority == "EXPLICIT_USER_DIRECTIVE":
            return {"decision": "PROPOSE_RETIREMENT", "reason": "verify-directive-with-host"}
        if authority == "PROTECTED_GOVERNED_RETIREMENT" and event.get("protected_readback_verified") is True:
            return {"decision": "PROPOSE_RETIREMENT", "reason": "verify-protected-receipt-with-host"}
        return {"decision": "DENY", "reason": "unapproved-retirement"}
    if target == "ENABLED" and authority in ("EXPLICIT_USER_DIRECTIVE", "AUTHORIZED_CONTROLLER_RECONCILIATION"):
        return {"decision": "PROPOSE_ENABLEMENT", "reason": "verify-authority-with-host"}
    return {"decision": "DENY", "reason": "unapproved-scheduler-transition"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--policy", type=Path, required=True)
    p.add_argument("--event", type=Path, required=True)
    a = p.parse_args()
    result = assess(json.loads(a.policy.read_text()), json.loads(a.event.read_text()))
    print(json.dumps(result, sort_keys=True))
    return 1 if result["decision"] in ("DENY", "DRIFT_ALERT") else 0


if __name__ == "__main__":
    raise SystemExit(main())
