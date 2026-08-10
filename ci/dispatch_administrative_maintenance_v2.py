from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import dispatch_administrative_maintenance as legacy
from administrative_automation import (
    AutomationError,
    apply_completion_to_registry,
    derive_completion_state,
    load_json,
    parse_datetime,
    validate_completion_state,
    validate_config,
)

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "governance" / "administrative_maintenance_automation.json"
STATE_PATH = ROOT / "governance" / "administrative_maintenance_completion_state.json"
UTC = timezone.utc


def superseded_cancelled_pr_run(run: dict[str, Any]) -> tuple[bool, list[str]]:
    """Return true only when the event payload proves a cancelled PR run is obsolete."""
    if str(run.get("conclusion") or "").lower() != "cancelled":
        return False, []

    run_head = str(run.get("head_sha") or "").strip()
    pull_requests = run.get("pull_requests")
    if not run_head or not isinstance(pull_requests, list) or not pull_requests:
        return False, []

    current_heads = sorted(
        {
            str((pull_request.get("head") or {}).get("sha") or "").strip()
            for pull_request in pull_requests
            if isinstance(pull_request, dict)
        }
        - {""}
    )
    if not current_heads:
        return False, []

    return all(current_head != run_head for current_head in current_heads), current_heads


def reconcile_workflow_run_liveness(
    event_name: str,
    event: dict[str, Any],
    dispatches: list[legacy.Dispatch],
    now: datetime,
) -> list[legacy.Dispatch]:
    """Replace only demonstrably superseded cancellation P1s with evidence-only P3s."""
    if event_name != "workflow_run":
        return dispatches

    run = event.get("workflow_run") or {}
    superseded, current_heads = superseded_cancelled_pr_run(run)
    if not superseded:
        return dispatches

    run_id = str(run.get("id") or "unknown")
    workflow_name = str(run.get("name") or "required workflow")
    run_head = str(run.get("head_sha") or "unknown")
    failure_key = f"event:workflow-failure:{run_id}"
    filtered = [dispatch for dispatch in dispatches if dispatch.key != failure_key]
    current_head_text = ", ".join(f"`{head}`" for head in current_heads)
    body = f"""## Superseded required-workflow cancellation evidence

- workflow: `{workflow_name}`
- run id: `{run_id}`
- conclusion: `cancelled`
- cancelled run head: `{run_head}`
- associated current PR head(s): {current_head_text}
- observed at: `{legacy.iso_z(now)}`
- classification: `P3` evidence only; the cancelled exact head is no longer the live PR evidence lane

This downgrade is permitted only because the workflow-run payload itself proves that every associated current PR head differs from the cancelled run head. It does not treat a current-head cancellation, an unbound cancellation, or any other non-success conclusion as non-failing.
"""
    filtered.append(
        legacy.Dispatch(
            kind="event",
            key=f"event:workflow-superseded-cancellation:{run_id}",
            title=f"superseded required-workflow cancellation {workflow_name} #{run_id}",
            body=body,
            severity="P3",
            due_at=None,
            source_event=event_name,
        )
    )
    return legacy.deduplicate(filtered)


def main(argv: list[str] | None = None) -> int:
    args = legacy.parse_args(sys.argv[1:] if argv is None else argv)
    config = load_json(CONFIG_PATH)
    errors = validate_config(config)
    if errors:
        raise AutomationError("; ".join(errors))
    head = os.environ.get("GITHUB_SHA") or subprocess_head()
    derived = derive_completion_state(ROOT, config, head)
    previous = load_json(STATE_PATH) if STATE_PATH.exists() else None
    errors = validate_completion_state(derived, previous)
    if errors:
        raise AutomationError("; ".join(errors))
    registry = apply_completion_to_registry(legacy.load_registry(), derived)
    event = legacy.load_event(args.event_path)
    event_name = legacy.event_name_from_environment()
    now = parse_datetime(args.now) if args.now else datetime.now(UTC)

    allowed = {"auto", *(item["id"] for item in registry["procedures"])}
    if args.procedure not in allowed:
        raise SystemExit(f"unsupported procedure: {args.procedure}")

    dispatches = legacy.build_dispatches(registry, event_name, event, now, args.procedure)
    dispatches = reconcile_workflow_run_liveness(event_name, event, dispatches, now)
    disposition = "dry_run" if args.dry_run else "emitted"
    results = [{**asdict(dispatch), "disposition": disposition} for dispatch in dispatches]
    severity_counts = {
        severity: sum(item.severity == severity for item in dispatches)
        for severity in ("P1", "P2", "P3")
    }
    report = {
        "schema_version": "2.0.0",
        "control_id": registry["control_id"],
        "trigger_id": registry["trigger_id"],
        "evaluated_at": legacy.iso_z(now),
        "event_name": event_name,
        "source_schedule": event.get("schedule"),
        "manual_procedure": args.procedure,
        "dry_run": args.dry_run,
        "dispatch_count": len(results),
        "severity_counts": severity_counts,
        "dispatches": results,
        "completion_state": derived,
        "delivery_channels": registry["dispatch"]["delivery_channels"],
        "authority_boundary": {
            "workflow_signal_is_evidence_only": True,
            "candidate_creation_allowed_here": False,
            "protected_record_required": True,
            "schedule_anchor_reset": False,
            "claim_promotion": False,
        },
    }
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    summary_path_raw = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path_raw:
        legacy.write_summary(Path(summary_path_raw), report)
    legacy.emit_annotations(dispatches)
    output = os.environ.get("GITHUB_OUTPUT")
    if output:
        with Path(output).open("a", encoding="utf-8") as handle:
            handle.write(f"dispatch_count={len(results)}\n")
            handle.write(f"p1_count={severity_counts['P1']}\n")
            handle.write(f"p2_count={severity_counts['P2']}\n")
            handle.write(f"p3_count={severity_counts['P3']}\n")
            handle.write(f"report={args.report.as_posix()}\n")
    print(json.dumps(report, indent=2))
    return 0


def subprocess_head() -> str:
    import subprocess

    return subprocess.run(["git", "rev-parse", "HEAD"], check=True, text=True, capture_output=True).stdout.strip()


if __name__ == "__main__":
    raise SystemExit(main())