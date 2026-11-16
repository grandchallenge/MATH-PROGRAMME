#!/usr/bin/env python3
"""One-shot, fail-closed Erdős PV worker pickup. NOT an unattended worker.

This adapter makes a fresh, stage-fair, issue/manifest/claim-checked handoff
to the existing per-problem lease. A persistent authorized controller must
invoke it and supply its last actually served phase; this module neither
schedules tasks nor executes mathematical work.
"""
from __future__ import annotations

import argparse
import json
import sys

from erdos_pv_queue import candidates
import erdos_pv_worker_lease as lease

PHASES = "ABCD"
MAX_SCAN = 25


def phase_order(last_phase: str) -> str:
    if last_phase not in tuple(PHASES):
        raise ValueError("last_phase must be a phase actually served: A/B/C/D")
    i = PHASES.index(last_phase)
    return PHASES[i + 1:] + PHASES[:i + 1]


def select(last_phase: str = "D", scan_limit: int = 5) -> dict:
    """Inspect only bounded live candidates, without mutating GitHub.

    A reservation is never reclaimed just because it looks old. A mismatch in
    issue projection, source blob, or prior RESULT/1 stops this pass for
    reconciliation rather than silently moving to another task.
    """
    if not 1 <= scan_limit <= MAX_SCAN:
        raise ValueError("scan_limit outside 1..25")
    skips = []
    for phase in phase_order(last_phase):
        for c in candidates(phase, limit=scan_limit):
            s = lease.scope(c["task_id"], require_eligible=True)
            if s["stage"] != phase or s["issue"] != c["queue_issue"]:
                raise ValueError("Selector and exact scoped lease disagree")
            held = lease.current_ref(s)
            if held:
                skips.append({"task_id": s["id"], "reason": "CLAIM_HELD",
                              "claim_sha": held["object"]["sha"]})
                continue
            try:
                pre = lease.preflight(s)
            except ValueError as exc:
                return {"result": "RECONCILIATION_REQUIRED",
                        "task_id": s["id"], "phase": phase,
                        "reason": str(exc), "skipped": skips,
                        "mutation": False}
            return {"result": "READY_FOR_ATOMIC_CLAIM", "candidate": c,
                    "protected_cohort_blob": pre["source_blob"],
                    "last_served_phase": last_phase,
                    "next_last_served_phase_if_claimed": phase,
                    "scoped_issue": s["issue"],
                    "skipped": skips, "mutation": False,
                    "project_v2_item_readback": "NOT_PERFORMED"}
    return {"result": "NO_UNCLAIMED_CANDIDATE_IN_SCAN",
            "last_served_phase": last_phase, "scan_limit": scan_limit,
            "skipped": skips, "mutation": False,
            "project_v2_item_readback": "NOT_PERFORMED"}


def dispatch(mode: str, last_phase: str = "D", scan_limit: int = 5) -> dict:
    if mode not in ("inspect", "claim"):
        raise ValueError("Unknown dispatch mode")
    chosen = select(last_phase, scan_limit)
    if mode == "inspect" or chosen["result"] != "READY_FOR_ATOMIC_CLAIM":
        return chosen
    s = lease.scope(chosen["candidate"]["task_id"], require_eligible=True)
    # The existing lease implementation rechecks the live source/issue/return
    # before the atomic GitHub ref create and then verifies its exact SHA.
    result = lease.claim(s)
    return {"result": ("CLAIMED_HANDOFF_ONLY" if
                       result["result"] == "ACQUIRED" else
                       "CLAIM_RACE_OR_UNCERTAIN"),
            "lease": result,
            "candidate": chosen["candidate"],
            "next_last_served_phase_if_claimed":
                chosen["next_last_served_phase_if_claimed"]
                if result["result"] == "ACQUIRED" else last_phase,
            "mutation": True if result["result"] == "ACQUIRED" else "UNKNOWN_RECONCILE",
            "worker_execution": "NOT_PERFORMED",
            "protected_admission": "NOT_PERFORMED",
            "project_v2_item_readback": "NOT_PERFORMED"}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("mode", choices=("inspect", "claim"),
                   help="inspect is read-only; claim is a GitHub mutation")
    p.add_argument("--last-served-phase", choices=list(PHASES), default="D")
    p.add_argument("--scan-limit", type=int, default=5)
    a = p.parse_args()
    try:
        out = dispatch(a.mode, a.last_served_phase, a.scan_limit)
        print(json.dumps(out, sort_keys=True))
        if out["result"] in ("RECONCILIATION_REQUIRED", "CLAIM_RACE_OR_UNCERTAIN"):
            return 4
        return 0
    except (RuntimeError, ValueError, KeyError) as exc:
        print(json.dumps({"result": "FAIL_CLOSED", "error": str(exc),
                          "mutation": ("UNKNOWN_IF_CLAIM_ATTEMPTED" if a.mode == "claim"
                                       else False)}, sort_keys=True))
        return 2


if __name__ == "__main__":
    sys.exit(main())
