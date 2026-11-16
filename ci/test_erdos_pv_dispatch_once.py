#!/usr/bin/env python3
"""Adversarial one-shot dispatcher contract; no external mutations."""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import erdos_pv_dispatch_once as d


def candidate(n, phase="A", issue=3212):
    return {"task_id": f"ERDOS-PV-{n:04d}-{phase}",
            "queue_issue": issue, "phase": phase, "problem_id": n}


def scope(c, require_eligible=True):
    if isinstance(c, str):
        return {"id": c, "stage": c[-1], "issue": {"A": 3212, "B": 3225, "C": 3238, "D": 3251}[c[-1]]}
    return {"id": c["task_id"], "stage": c["phase"],
            "issue": c["queue_issue"]}


def offered(rows):
    return lambda phase, limit: [c for c in rows if c["phase"] == phase][:limit]


class DispatchTests(unittest.TestCase):
    def test_round_robin_rotation(self):
        self.assertEqual([d.phase_order(p) for p in "ABCD"],
                         ["BCDA", "CDAB", "DABC", "ABCD"])

    def test_invalid_phase_and_scan(self):
        for p in ("X", "", "a"):
            with self.assertRaises(ValueError):
                d.phase_order(p)
        for n in (-1, 0, 26):
            with self.assertRaises(ValueError):
                d.select(scan_limit=n)

    def test_fair_phase_selection_over_earlier_a(self):
        rows = [candidate(2), candidate(9, "C", 3238)]
        with patch.object(d, "candidates", side_effect=offered(rows)),\
             patch.object(d.lease, "scope", side_effect=scope),\
             patch.object(d.lease, "current_ref", return_value=None),\
             patch.object(d.lease, "preflight", return_value={"source_blob": "s"}):
            x = d.select(last_phase="B")
        self.assertEqual(x["candidate"]["task_id"], "ERDOS-PV-0009-C")
        self.assertEqual(x["next_last_served_phase_if_claimed"], "C")

    def test_held_claim_skip_without_reclaim(self):
        rows = [candidate(2), candidate(3)]
        def held(s):
            return {"object": {"sha": "a" * 40}} if s["id"].endswith("0002-A") else None
        with patch.object(d, "candidates", side_effect=offered(rows)),\
             patch.object(d.lease, "scope", side_effect=scope),\
             patch.object(d.lease, "current_ref", side_effect=held),\
             patch.object(d.lease, "preflight", return_value={"source_blob": "s"}) as pre:
            x = d.select(scan_limit=2)
        self.assertEqual(x["candidate"]["task_id"], "ERDOS-PV-0003-A")
        self.assertEqual(x["skipped"][0]["reason"], "CLAIM_HELD")
        pre.assert_called_once()

    def test_projection_drift_is_not_skipped(self):
        rows = [candidate(2), candidate(3)]
        with patch.object(d, "candidates", side_effect=offered(rows)),\
             patch.object(d.lease, "scope", side_effect=scope),\
             patch.object(d.lease, "current_ref", return_value=None),\
             patch.object(d.lease, "preflight",
                          side_effect=ValueError("Issue not OPEN and AVAILABLE")) as pre:
            x = d.select()
        self.assertEqual(x["result"], "RECONCILIATION_REQUIRED")
        self.assertEqual(x["task_id"], "ERDOS-PV-0002-A")
        pre.assert_called_once()

    def test_prior_exact_return_requires_reconciliation(self):
        with patch.object(d, "candidates", side_effect=offered([candidate(2)])),\
             patch.object(d.lease, "scope", side_effect=scope),\
             patch.object(d.lease, "current_ref", return_value=None),\
             patch.object(d.lease, "preflight",
                          side_effect=ValueError("Exact task already returned; do not duplicate")):
            x = d.select()
        self.assertEqual(x["result"], "RECONCILIATION_REQUIRED")
        self.assertIn("already returned", x["reason"])

    def test_transport_failure_not_swallowed(self):
        with patch.object(d, "candidates", side_effect=offered([candidate(2)])),\
             patch.object(d.lease, "scope", side_effect=scope),\
             patch.object(d.lease, "current_ref",
                          side_effect=RuntimeError("transport failure")):
            with self.assertRaisesRegex(RuntimeError, "transport"):
                d.select()

    def test_selector_identity_drift_rejected(self):
        with patch.object(d, "candidates", side_effect=offered([candidate(2)])),\
             patch.object(d.lease, "scope",
                          return_value={"id": "ERDOS-PV-0002-A", "stage": "A", "issue": 9999}):
            with self.assertRaisesRegex(ValueError, "disagree"):
                d.select()

    def test_empty_scan_is_not_completion(self):
        with patch.object(d, "candidates", return_value=[]) as cand:
            x = d.dispatch("claim")
        self.assertEqual(x["result"], "NO_UNCLAIMED_CANDIDATE_IN_SCAN")
        self.assertFalse(x["mutation"])
        self.assertEqual(cand.call_count, 4)

    def test_inspect_never_creates_claim(self):
        chosen = {"result": "READY_FOR_ATOMIC_CLAIM", "candidate": candidate(2)}
        with patch.object(d, "select", return_value=chosen),\
             patch.object(d.lease, "claim") as claim:
            self.assertEqual(d.dispatch("inspect"), chosen)
        claim.assert_not_called()

    def test_claim_handoff_requires_acquired(self):
        chosen = {"result": "READY_FOR_ATOMIC_CLAIM", "candidate": candidate(2),
                  "next_last_served_phase_if_claimed": "A"}
        with patch.object(d, "select", return_value=chosen),\
             patch.object(d.lease, "scope", side_effect=scope),\
             patch.object(d.lease, "claim", return_value={"result": "ACQUIRED",
                           "claim_sha": "a" * 40}) as claim:
            x = d.dispatch("claim")
        self.assertEqual(x["result"], "CLAIMED_HANDOFF_ONLY")
        self.assertEqual(x["worker_execution"], "NOT_PERFORMED")
        self.assertEqual(x["protected_admission"], "NOT_PERFORMED")
        self.assertTrue(x["mutation"])
        claim.assert_called_once()

    def test_ambiguous_race_does_not_advance_phase(self):
        chosen = {"result": "READY_FOR_ATOMIC_CLAIM", "candidate": candidate(2),
                  "next_last_served_phase_if_claimed": "A"}
        with patch.object(d, "select", return_value=chosen),\
             patch.object(d.lease, "scope", side_effect=scope),\
             patch.object(d.lease, "claim", return_value={
                 "result": "LOST_RACE_OR_UNCERTAIN", "winner_sha": None}):
            x = d.dispatch("claim", last_phase="D")
        self.assertEqual(x["result"], "CLAIM_RACE_OR_UNCERTAIN")
        self.assertEqual(x["mutation"], "UNKNOWN_RECONCILE")
        self.assertEqual(x["next_last_served_phase_if_claimed"], "D")

    def test_claim_transport_error_must_not_assert_no_mutation(self):
        import io, contextlib, json
        with patch.object(d, "dispatch", side_effect=RuntimeError("lost acknowledgment")),\
             patch.object(sys, "argv", ["erdos_pv_dispatch_once.py", "claim"]):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = d.main()
        self.assertEqual(code, 2)
        out = json.loads(buf.getvalue())
        self.assertEqual(out["mutation"], "UNKNOWN_IF_CLAIM_ATTEMPTED")

    def test_inspect_transport_error_marks_no_mutation(self):
        import io, contextlib, json
        with patch.object(d, "dispatch", side_effect=RuntimeError("read failed")),\
             patch.object(sys, "argv", ["erdos_pv_dispatch_once.py", "inspect"]):
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = d.main()
        self.assertEqual(code, 2)
        self.assertIs(json.loads(buf.getvalue())["mutation"], False)


if __name__ == "__main__":
    unittest.main()
