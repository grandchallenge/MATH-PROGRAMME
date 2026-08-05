from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

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
