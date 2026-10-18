#!/usr/bin/env python3
"""Governed, actually executed replay of every EC-BULK-007 finite receipt.

The separately captured GitHub issue readback is schema-replayed OFFLINE.
Nothing here makes live GitHub, Project, mathematical-certification, reviewer
approval, or protected-admission claims; no credentials are required.
"""
from __future__ import annotations
import contextlib
import io
import json
from pathlib import Path
import erdos_compendium_007_issue_readback as issue_snapshot
import erdos_compendium_007_finite_checks as phase1
import erdos_compendium_007_phase2_checks as phase2
import erdos_compendium_007_phase3_checks as phase3
import erdos_compendium_007_phase4_checks as phase4
import erdos_compendium_007_phase5_checks as phase5
import erdos_compendium_007_phase6_checks as phase6
import erdos_compendium_007_phase7_checks as phase7
import erdos_compendium_007_phase8_checks as phase8
import erdos_compendium_007_phase9_checks as phase9
import erdos_compendium_007_phase10_checks as phase10
import erdos_compendium_007_phase11_checks as phase11
import erdos_compendium_007_phase12_checks as phase12
import erdos_compendium_007_phase13_checks as phase13
import erdos_compendium_007_phase14_checks as phase14
import erdos_compendium_007_phase15_checks as phase15
import erdos_compendium_007_phase16_checks as phase16
import erdos_compendium_007_phase17_checks as phase17
import erdos_compendium_007_phase18_checks as phase18
import erdos_compendium_007_phase19_checks as phase19
import erdos_compendium_007_phase20_checks as phase20
import erdos_compendium_007_phase21_checks as phase21
import erdos_compendium_007_phase22_checks as phase22
import erdos_compendium_007_phase23_checks as phase23
import erdos_compendium_007_phase24_checks as phase24
import erdos_compendium_007_phase25_checks as phase25

BASE = Path(__file__).resolve().parents[1]
BATCHES = BASE / "governance/erdos_compendium/batches"

PHASES = [
    (1, phase1, "EC-BULK-007_FINITE_CHECKS.json"),
    (2, phase2, "EC-BULK-007_FINITE_CHECKS_PHASE2.json"),
    (3, phase3, "EC-BULK-007_FINITE_CHECKS_PHASE3.json"),
    (4, phase4, "EC-BULK-007_FINITE_CHECKS_PHASE4.json"),
    (5, phase5, "EC-BULK-007_FINITE_CHECKS_PHASE5.json"),
    (6, phase6, "EC-BULK-007_FINITE_CHECKS_PHASE6.json"),
    (7, phase7, "EC-BULK-007_FINITE_CHECKS_PHASE7.json"),
    (8, phase8, "EC-BULK-007_FINITE_CHECKS_PHASE8.json"),
    (9, phase9, "EC-BULK-007_FINITE_CHECKS_PHASE9.json"),
    (10, phase10, "EC-BULK-007_FINITE_CHECKS_PHASE10.json"),
    (11, phase11, "EC-BULK-007_FINITE_CHECKS_PHASE11.json"),
    (12, phase12, "EC-BULK-007_FINITE_CHECKS_PHASE12.json"),
    (13, phase13, "EC-BULK-007_FINITE_CHECKS_PHASE13.json"),
    (14, phase14, "EC-BULK-007_FINITE_CHECKS_PHASE14.json"),
    (15, phase15, "EC-BULK-007_FINITE_CHECKS_PHASE15.json"),
    (16, phase16, "EC-BULK-007_FINITE_CHECKS_PHASE16.json"),
    (17, phase17, "EC-BULK-007_FINITE_CHECKS_PHASE17.json"),
    (18, phase18, "EC-BULK-007_FINITE_CHECKS_PHASE18.json"),
    (19, phase19, "EC-BULK-007_FINITE_CHECKS_PHASE19.json"),
    (20, phase20, "EC-BULK-007_FINITE_CHECKS_PHASE20.json"),
    (21, phase21, "EC-BULK-007_FINITE_CHECKS_PHASE21.json"),
    (22, phase22, "EC-BULK-007_FINITE_CHECKS_PHASE22.json"),
    (23, phase23, "EC-BULK-007_FINITE_CHECKS_PHASE23.json"),
    (24, phase24, "EC-BULK-007_FINITE_CHECKS_PHASE24.json"),
    (25, phase25, "EC-BULK-007_FINITE_CHECKS_PHASE25.json"),
]

def main() -> None:
    verified = []
    for n, module, receipt in PHASES:
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            module.main()
        actual = json.loads(captured.getvalue())
        stored = json.loads((BATCHES / receipt).read_text(encoding="utf-8"))
        if actual != stored:
            raise ValueError(f"phase {n}: retained finite evidence does not replay exactly")
        if actual.get("cohort_id") != "EC-BULK-007" or (actual.get("result") or actual.get("status")) not in {"FINITE_CHECKS_PASS", "FINITE_COUNTEREXAMPLE_PASS"}:
            raise ValueError(f"phase {n}: recorded result is not a passing finite fixture")
        verified.append({"phase": n, "receipt": receipt, "equal": True})
    manifest = json.loads((BATCHES / "EC-BULK-007.json").read_text(encoding="utf-8"))
    saved = json.loads((BATCHES / "EC-BULK-007_QUEUE_READBACK.json").read_text(encoding="utf-8"))
    bound = issue_snapshot.verify_saved_snapshot(manifest, saved)
    sample_ids = json.loads((BATCHES / "EC-BULK-007_QA.json").read_text(encoding="utf-8"))["sample_problem_ids"]
    if len(sample_ids) != 20 or len(set(sample_ids)) != 20:
        raise ValueError("mandatory critical sample registry not exact 20")
    if any(not (BATCHES / f"EC-BULK-007_CRITICAL_{n}_PENDING.md").exists() for n in sample_ids):
        raise ValueError("missing critical sample source dossier")
    result = {"record_type": "EC_BULK_007_GOVERNED_OFFLINE_REPLAY/1",
        "phase_receipts_verified": len(verified), "phase_receipts": verified,
        "historical_authenticated_issue_snapshot": bound,
        "critical_dossiers_prepared": 20, "critical_reviews_approved": 0,
        "source_fidelity_certified": False, "protected_publication_approved": False,
        "result": "OFFLINE_EVIDENCE_REPLAY_PASS"}
    print(json.dumps(result, sort_keys=True))

if __name__ == "__main__":
    main()
