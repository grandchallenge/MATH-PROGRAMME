#!/usr/bin/env python3
"""Read-only, source-locked Erdős evidence coverage inventory.

No issue metadata, formal replay file, or queue status proves the main conjecture.
Records distinguish catalogue coverage from adjudicated mathematical conclusions.
"""
from __future__ import annotations
import argparse
import collections
import json
import re
from pathlib import Path

EXPECTED_PHASES = frozenset("ABCD")
EVIDENCE_ROOT = "governance/erdos_proof_verification/evidence/"
ADMISSIONS_ROOT = "governance/erdos_proof_verification/admissions/"
VALID_IDS = set(range(1, 1222))

def reconcile(registry: dict, pv_registry: dict, packets: list[dict],
              admissions: dict, files: set[str], activity: dict) -> dict:
    rows = registry.get("issues")
    if not isinstance(rows, list) or len(rows) != 1221:
        raise ValueError("catalogue registry not source-locked")
    ids = [x["problem_id"] for x in rows]
    if set(ids) != VALID_IDS or len(set(ids)) != len(ids):
        raise ValueError("catalogue identities missing/duplicated")
    population = pv_registry.get("population", {})
    if population.get("count") != 1221 or len(pv_registry.get("cohorts", [])) != 13:
        raise ValueError("proof-verification inventory identity drift")
    if len(packets) != 13:
        raise ValueError("missing proof-verification cohort packet")
    catalog = {}
    for cohort, packet in zip(pv_registry["cohorts"], packets):
        if packet.get("cohort_id") != cohort.get("cohort_id"):
            raise ValueError("cohort packet identity/order drift")
        range_info = packet.get("range", {})
        first, last = cohort["first"], cohort["last"]
        if (range_info.get("first"), range_info.get("last")) != (first, last):
            raise ValueError("cohort range identity drift")
        items = packet.get("items")
        if not isinstance(items, list) or len(items) != last - first + 1:
            raise ValueError("cohort count mismatch")
        for x in items:
            n = x["problem_id"]
            if n in catalog or n not in VALID_IDS or not first <= n <= last:
                raise ValueError(f"duplicate/out-of-range cohort record {n}")
            stages = x.get("stage_work_items")
            if not isinstance(stages, dict) or set(stages) != EXPECTED_PHASES:
                raise ValueError(f"stage identities incomplete {n}")
            catalog[n] = x
    if set(catalog) != VALID_IDS:
        raise ValueError("1221-item PV coverage incomplete")

    # Count only identifiable, committed evidence paths. This is evidence
    # presence, never a claim that the evidence proves its declared target.
    evidence = collections.defaultdict(list)
    for name in files:
        m = re.match(r"^"+EVIDENCE_ROOT+r"(\d{4})/(.+)$", name)
        if m and int(m.group(1)) in VALID_IDS:
            evidence[int(m.group(1))].append(name)
    admitted = set()
    for row in admissions.get("admissions", []):
        admitted.add(row["problem_id"])
    for batch in admissions.get("batches", []):
        admitted.update(row["problem_id"] for row in batch["entries"])
    if admitted - VALID_IDS:
        raise ValueError("editorial admission outside locked catalogue")
    events = collections.defaultdict(list)
    if activity.get("record_type") != "ERDOS_COMPENDIUM_RECENT_RESEARCH_ACTIVITY/1":
        raise ValueError("research activity source missing")
    for row in activity.get("activity_candidates", []):
        n = row.get("problem_id")
        if n in VALID_IDS and row.get("mathematical_authority") is False:
            events[n].append(row)
    if activity.get("truncated_input"):
        # A sample is still a useful lead but is not exhaustive.
        sample_truncated = True
    else:
        sample_truncated = False
    stages = collections.Counter()
    stale = []
    missing = []
    active = []
    for n in sorted(catalog):
        entry = catalog[n]
        for ph, slot in entry["stage_work_items"].items():
            stages[f"{ph}:{slot.get('work_status','MISSING')}"] += 1
        paths = sorted(evidence.get(n, []))
        stage_unexecuted = all(
            x.get("work_status") == "UNEXECUTED"
            for x in entry["stage_work_items"].values()
        )
        if paths and stage_unexecuted:
            stale.append({
                "problem_id": n,
                "evidence_file_count": len(paths),
                "sample_evidence_paths": paths[:4],
                "reason": "RETAINED_EVIDENCE_WITH_UNEXECUTED_COHORT_STAGE_SNAPSHOT",
                "scope": "QUEUE_RECONCILIATION_NOT_PROOF_CERTIFICATION",
            })
        if not paths:
            missing.append(n)
        if events.get(n):
            active.append({
                "problem_id": n,
                "recent_issue_count": len(events[n]),
                "editorial_admitted": n in admitted,
                "retained_evidence_file_count": len(paths),
                "queue_stage_snapshot_unexecuted": stage_unexecuted,
                "recent_issue_urls": [e["source_url"] for e in events[n]][:4],
                "action": "SOURCE_REVIEW_AND_EDITORIAL_DELTA_ASSESSMENT",
                "public_mathematical_status_inferred": False,
            })
    # Do not fabricate completeness: separate source-file presence, source
    # replay, actual adjudication and public editorial admission.
    return {
        "record_type": "ERDOS_COMPENDIUM_PROOF_EVIDENCE_COVERAGE/1",
        "authority": "READ_ONLY_TRIAGE_NO_MATHEMATICAL_OR_PUBLICATION_PROMOTION",
        "catalogue_id_count": len(catalog),
        "cohort_packet_count": len(packets),
        "stage_slots_count": sum(stages.values()),
        "stage_status_counts": dict(sorted(stages.items())),
        "editorially_admitted_problem_count": len(admitted),
        "retained_pv_evidence_problem_count": len(evidence),
        "without_retained_pv_evidence_count": len(missing),
        "without_retained_pv_evidence_sample": missing[:25],
        "retained_evidence_vs_unexecuted_snapshot_count": len(stale),
        "retained_evidence_vs_unexecuted_snapshot": stale[:60],
        "recent_activity_problem_count": len(active),
        "recent_activity_sample_truncated": sample_truncated,
        "active_editorial_delta_candidates": sorted(
            active, key=lambda e: (-e["recent_issue_count"], e["problem_id"]))[:60],
        "evidence_inventory_is_proof_verification": False,
        "automatic_publication": False,
        "historical_catalogue_mutated": False,
        "actual_pv_receipt_efficacy_assessed": False,
    }

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    p.add_argument("--activity", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    a = p.parse_args()
    root = a.root.resolve()
    def load(rel):
        path = root / rel
        if not path.is_file():
            raise ValueError(f"missing protected source: {rel}")
        return json.loads(path.read_text(encoding="utf-8"))
    pv = load("governance/erdos_proof_verification/coverage/REGISTRY.json")
    result = reconcile(
        load("governance/erdos_catalogue/REGISTRY.json"), pv,
        [load(c["packet"]) for c in pv["cohorts"]],
        load("governance/erdos_compendium/EDITORIAL_ADMISSIONS.json"),
        {p.relative_to(root).as_posix() for base in
         ("governance/erdos_proof_verification/evidence",
          "governance/erdos_proof_verification/admissions")
         for p in (root/base).rglob("*") if p.is_file()},
        json.loads(a.activity.read_text(encoding="utf-8")),
    )
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    print("Erdos PV:", result["catalogue_id_count"], "records,",
          result["stage_slots_count"], "phase slots;",
          result["retained_pv_evidence_problem_count"], "with retained evidence;",
          result["retained_evidence_vs_unexecuted_snapshot_count"], "stale-stage leads")
    if result["recent_activity_sample_truncated"]:
        print("::warning::Recent issue sampling is truncated; not exhaustive")
    for x in result["retained_evidence_vs_unexecuted_snapshot"][:8]:
        print(f"::warning title=Erdos {x['problem_id']} stage drift::Retained evidence with UNEXECUTED historical cohort stages")

if __name__ == "__main__":
    main()
