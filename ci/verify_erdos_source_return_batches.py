#!/usr/bin/env python3
"""Fail-closed, pure aggregate readback of all source-return batch artifacts."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path

try:
    from ci.erdos_catalogue_queue_projection import (
        eligible_issue_ids, select_source_batch, source_batch_manifest,
        validate_receipt, persist_projection_receipt,
    )
except ModuleNotFoundError:
    from erdos_catalogue_queue_projection import (
        eligible_issue_ids, select_source_batch, source_batch_manifest,
        validate_receipt, persist_projection_receipt,
    )


def verify(report: dict, *, report_digest: str, manifest: dict,
           root: Path, run_id: str, run_attempt: str, protected_head: str) -> dict:
    expected = source_batch_manifest(report, 64, report_digest)
    if manifest != expected:
        raise ValueError("manifest partition, count or captured report identity drift")
    if not run_id.isdecimal() or not run_attempt.isdecimal():
        raise ValueError("GitHub run/attempt identity missing")
    if len(protected_head) != 40 or any(c not in "0123456789abcdef" for c in protected_head):
        raise ValueError("protected workflow source head missing")
    if not root.is_dir():
        raise ValueError("no archived batch evidence")
    actual_dirs = sorted(x for x in root.iterdir() if x.is_dir())
    expected_dirs = sorted(
        root / f"gcl-source-return-batch-{item['index']}-{run_id}-{run_attempt}"
        for item in expected["include"]
    )
    if actual_dirs != expected_dirs:
        raise ValueError(
            f"batch artifact census mismatch: expected {len(expected_dirs)}, "
            f"got {len(actual_dirs)}"
        )
    all_ids = eligible_issue_ids(report)
    seen: list[int] = []
    totals = {"returned_readbacks": 0, "preserved_done": 0, "changed_source_fields": 0}
    evidence: list[dict] = []
    for item in expected["include"]:
        index = item["index"]
        path = root / f"gcl-source-return-batch-{index}-{run_id}-{run_attempt}" / "projection.json"
        if not path.is_file():
            raise ValueError(f"batch {index}: missing projection.json")
        receipt = json.loads(path.read_text(encoding="utf-8"))
        selected, scope = select_source_batch(report, size=64, index=index)
        if (receipt.get("schema") != "GCL-ERDOS-SOURCE-RETURN-PROJECTION/1"
                or receipt.get("status") != "VERIFIED_BATCH"
                or receipt.get("verified") is not True
                or receipt.get("applied") is not True
                or receipt.get("complete") is not True
                or receipt.get("dry_run") is not False
                or receipt.get("blocker") is not None
                or receipt.get("in_flight_issue") is not None
                or receipt.get("batch") != scope
                or receipt.get("report_sha256") != report_digest
                or receipt.get("protected_head") != protected_head
                or receipt.get("workflow_run") != f"https://github.com/grandchallenge/MATH-PROGRAMME/actions/runs/{run_id}"
                or receipt.get("expected_issue_count") != len(selected)
                or receipt.get("processed_count") != len(selected)):
            raise ValueError(f"batch {index}: nonterminal, unbound, or incomplete receipt")
        rows = receipt.get("results")
        if not isinstance(rows, list) or [row.get("issue") for row in rows] != selected:
            raise ValueError(f"batch {index}: exact issue partition/readbacks do not match")
        completed = preserved = 0
        for row in rows:
            n = row["issue"]
            # Authenticate selected comment identity against the immutable intake.
            if row.get("comment_id") != validate_receipt(report, n)["comment_id"]:
                raise ValueError(f"#{n}: batch comment identity changed")
            if row.get("target") == "PRESERVE_DONE":
                if (row.get("verified_status") != "Done"
                        or row.get("historical_terminal") is not True):
                    raise ValueError(f"#{n}: terminal custody unverified")
                preserved += 1
            elif row.get("target") == "RETURNED":
                if (row.get("verified_status") != "RETURNED"
                        or row.get("verified_gcl_state") != "RETURNED"
                        or row.get("available_removed") is not True):
                    raise ValueError(f"#{n}: authoritative return surfaces not verified")
                completed += 1
                if row.get("gcl_state_before") == "AVAILABLE":
                    totals["changed_source_fields"] += 1
            else:
                raise ValueError(f"#{n}: unknown terminal source projection disposition")
        if (receipt.get("verified_returned") != completed
                or receipt.get("preserved_done") != preserved):
            raise ValueError(f"batch {index}: claimed counters differ from evidence")
        totals["returned_readbacks"] += completed
        totals["preserved_done"] += preserved
        seen.extend(selected)
        evidence.append({"batch_index": index, "issue_count": len(selected),
                         "returned_readbacks": completed, "preserved_done": preserved,
                         "receipt_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    if seen != all_ids or sum(totals[k] for k in ("returned_readbacks", "preserved_done")) != len(all_ids):
        raise ValueError("global source-return partition or terminal evidence incomplete")
    return {
        "schema": "GCL-ERDOS-SOURCE-RETURN-AGGREGATE/1",
        "status": "VERIFIED",
        "verified": True,
        "complete": True,
        "applied": True,
        "claim_scope": "All single-valid-return source tasks in one captured report; NOT full queue closure, theorem certification or editorial acceptance",
        "run_id": run_id,
        "run_attempt": run_attempt,
        "protected_head": protected_head,
        "report_sha256": report_digest,
        "eligible_issue_count": len(all_ids),
        "verified_issue_count": len(seen),
        "batch_count": len(expected_dirs),
        **totals,
        "batch_evidence": evidence,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--report", required=True, type=Path)
    p.add_argument("--manifest", required=True, type=Path)
    p.add_argument("--receipts-root", required=True, type=Path)
    p.add_argument("--receipt", required=True, type=Path)
    args = p.parse_args()
    record = {"schema": "GCL-ERDOS-SOURCE-RETURN-AGGREGATE/1",
              "status": "BLOCKED", "verified": False,
              "complete": False, "applied": False, "blocker": None}
    try:
        report_bytes = args.report.read_bytes()
        record = verify(
            json.loads(report_bytes), report_digest=hashlib.sha256(report_bytes).hexdigest(),
            manifest=json.loads(args.manifest.read_text()),
            root=args.receipts_root,
            run_id=os.environ.get("GITHUB_RUN_ID", ""),
            run_attempt=os.environ.get("GITHUB_RUN_ATTEMPT", ""),
            protected_head=os.environ.get("GITHUB_SHA", ""),
        )
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
        record["blocker"] = f"{type(exc).__name__}: {exc}"
    persist_projection_receipt(args.receipt, record)
    print(json.dumps({k:v for k,v in record.items() if k!="batch_evidence"},sort_keys=True),flush=True)
    return 0 if record["verified"] is True else 1


if __name__ == "__main__":
    raise SystemExit(main())
