from __future__ import annotations

import importlib.util
import json
import os
import sys
import unittest
from functools import partial
from pathlib import Path

import administrative_autonomy_receipt_stage as receipt_stage
import administrative_autonomy_runtime_github as runtime_github
import administrative_autonomy_runtime_receipt_behind_resume as receipt_resume
from administrative_autonomy_runtime_contract import (
    ALLOWED_REPOSITORIES, ROOT, RUNTIME_PATH, build_record, load_json,
    record_path_for, repository_state, validate_activation, validate_record,
    validate_runtime_contract,
)
from administrative_autonomy_runtime_github import check_runs_state
from administrative_autonomy_runtime_mirror_sync import (
    wait_mirror_sync as provenance_bound_wait_mirror_sync,
)
from administrative_autonomy_runtime_queue_starvation import (
    pending_closures as nonblocking_pending_closures,
)
from administrative_autonomy_runtime_receipt_behind_resume import (
    stage_completion_receipt as resumable_stage_completion_receipt,
)
from administrative_autonomy_runtime_structural_2033_recovery import (
    eligible_candidates as structural_2033_recovery_eligible_candidates,
)
from administrative_autonomy_runtime_structural_2257_recovery import (
    eligible_candidates as structural_2257_recovery_eligible_candidates,
)
from administrative_autonomy_runtime_structural_0833_recovery import (
    eligible_candidates as structural_0833_recovery_eligible_candidates,
)
from administrative_autonomy_runtime_structural_0121_recovery import (
    advance_completion_state as structural_0121_hole_advance_completion_state,
    eligible_candidates as structural_0121_recovery_eligible_candidates,
    wait_mirror_sync as structural_0121_hole_wait_mirror_sync,
)
from administrative_autonomy_runtime_post_receipt_closure_resume import (
    pending_closures as resumable_post_receipt_pending_closures,
    stage_completion_receipt as stable_post_receipt_stage_completion_receipt,
    wait_mirror_sync as descendant_post_receipt_wait_mirror_sync,
)
from administrative_autonomy_runtime_post_receipt_current_frontier import (
    pending_closures as current_frontier_post_receipt_pending_closures,
    stage_completion_receipt as current_frontier_post_receipt_stage_completion_receipt,
    wait_mirror_sync as current_frontier_post_receipt_wait_mirror_sync,
)
from administrative_autonomy_runtime_structural_1809_recovery import (
    advance_completion_state as structural_1809_collision_advance_completion_state,
    eligible_candidates as structural_1809_recovery_eligible_candidates,
    synchronize_eligible_candidate as structural_1809_synchronize_eligible_candidate,
    wait_mirror_sync as structural_1809_collision_wait_mirror_sync,
)
from administrative_autonomy_runtime_administrative_review_0121_recovery import (
    eligible_candidates as administrative_review_0121_recovery_eligible_candidates,
)
from autonomy_github import AutonomyError

receipt_stage.pending_closures = nonblocking_pending_closures
receipt_stage.advance_completion_state = structural_0121_hole_advance_completion_state
receipt_resume.advance_completion_state = structural_0121_hole_advance_completion_state
receipt_stage.stage_completion_receipt = resumable_stage_completion_receipt
RECOVERY_ELIGIBILITY_CHAIN = (
    structural_2033_recovery_eligible_candidates,
    structural_2257_recovery_eligible_candidates,
    structural_0833_recovery_eligible_candidates,
    structural_0121_recovery_eligible_candidates,
    structural_1809_recovery_eligible_candidates,
    administrative_review_0121_recovery_eligible_candidates,
)
runtime_github.eligible_candidates = RECOVERY_ELIGIBILITY_CHAIN[-1]
runtime_github.wait_mirror_sync = provenance_bound_wait_mirror_sync
runtime_github.wait_mirror_sync = structural_0121_hole_wait_mirror_sync

# Exact #515 terminal-debt overlay. These assignments deliberately occur after
# all durable compatibility bindings above and before the executor import below.
receipt_stage.pending_closures = resumable_post_receipt_pending_closures
receipt_stage.stage_completion_receipt = stable_post_receipt_stage_completion_receipt
runtime_github.wait_mirror_sync = descendant_post_receipt_wait_mirror_sync

# Exact #515 current-frontier successor. The predecessor overlay remains visible
# as durable history; this later binding changes only the exact target path.
receipt_stage.pending_closures = current_frontier_post_receipt_pending_closures
receipt_stage.stage_completion_receipt = current_frontier_post_receipt_stage_completion_receipt
runtime_github.wait_mirror_sync = current_frontier_post_receipt_wait_mirror_sync

# Exact #520 collision/historical-hole recovery. Ordinary allocator, BEHIND,
# receipt, and mirror mechanics remain the base; only the exact target path is
# normalized and re-admitted through the bounded protected control.
receipt_stage.advance_completion_state = partial(
    structural_1809_collision_advance_completion_state,
    base=structural_0121_hole_advance_completion_state,
)
receipt_resume.advance_completion_state = receipt_stage.advance_completion_state
runtime_github.wait_mirror_sync = partial(
    structural_1809_collision_wait_mirror_sync,
    base=current_frontier_post_receipt_wait_mirror_sync,
)

# Historical compatibility-test marker only; this symbol is not imported or called.
# administrative_review_0813_receipt_pending_closures
# The generic receipt integration supersedes the authority-sensitive Aug13
# import-time recovery overlay. Administrative-review candidate, closure, and
# receipt transitions now use the protected generic runtime without the former
# qualification-only suspension wrappers.
import administrative_autonomy_runtime_execute as runtime_execute

import administrative_autonomy_runtime_behind_sync as behind_sync
from administrative_autonomy_runtime_behind_sync import (
    execute as protected_behind_execute,
    main as protected_behind_main,
    validate_command as protected_behind_validate_command,
)

behind_sync.synchronize_eligible_candidate = partial(
    structural_1809_synchronize_eligible_candidate,
    base=behind_sync.synchronize_eligible_candidate,
)

# MP-ADMIN-LOW-FRICTION-001 deliberately reuses this already-protected heartbeat
# instead of adding another privileged scheduler. The bounded routine lane runs
# only after the ordinary administrative executor returns successfully. It has
# no new token, cadence, ruleset mutation, direct-push, or Human-Steward route.
import administrative_autonomy_low_friction as low_friction

_base_execute = protected_behind_execute
_base_validate_command = protected_behind_validate_command


def _validate_low_friction_matrix() -> int:
    errors = low_friction.validate_control(
        low_friction.load_json(low_friction.CONTROL_PATH)
    )
    if errors:
        for error in errors:
            print(error)
        return 1
    test_path = ROOT / "tests" / "test_administrative_autonomy_low_friction.py"
    spec = importlib.util.spec_from_file_location(
        "mp_admin_low_friction_matrix", test_path
    )
    if spec is None or spec.loader is None:
        print(f"cannot load low-friction adversarial matrix: {test_path}")
        return 1
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    suite = unittest.defaultTestLoader.loadTestsFromModule(module)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if not result.wasSuccessful():
        return 1
    print("MP-ADMIN-LOW-FRICTION-001 state-machine adversarial matrix: valid")
    return 0


def validate_command() -> int:
    base_result = _base_validate_command()
    low_result = _validate_low_friction_matrix()
    return 0 if base_result == 0 and low_result == 0 else 1


def _bind_existing_ruleset_token() -> None:
    # The protected candidate heartbeat already mints ADMIN_TOKEN for ruleset
    # readback. Low-friction uses it only through GET operations and creates no
    # new credential or administration mutation path.
    if not os.environ.get("ADMIN_READ_TOKEN") and os.environ.get("ADMIN_TOKEN"):
        os.environ["ADMIN_READ_TOKEN"] = os.environ["ADMIN_TOKEN"]


def _attach_low_friction_summary(
    report_path: Path,
    *,
    state: str,
    low_report: Path,
    error: str | None = None,
) -> None:
    if not report_path.exists():
        return
    try:
        report = json.loads(report_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return
    summary: dict[str, object] = {
        "control_id": low_friction.EXPECTED_CONTROL_ID,
        "state": state,
        "report": low_report.name,
        "human_steward_checkpoint_requested": False,
    }
    if error is not None:
        summary["error"] = error
    report["low_friction_routine_lifecycle"] = summary
    report_path.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def execute(report_path: Path) -> int:
    result = _base_execute(report_path)
    if result != 0:
        return result
    _bind_existing_ruleset_token()
    low_report = report_path.with_name("administrative-low-friction-sweep.json")
    try:
        outcome = low_friction.sweep(low_report)
    except Exception as exc:
        _attach_low_friction_summary(
            report_path,
            state="LOW_FRICTION_FAILED_CLOSED",
            low_report=low_report,
            error=str(exc),
        )
        print(f"low-friction routine lifecycle failed closed: {exc}", file=sys.stderr)
        return 1
    _attach_low_friction_summary(
        report_path,
        state=str(outcome.get("state") or "SWEEP_COMPLETE"),
        low_report=low_report,
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    args = behind_sync.parse_args(sys.argv[1:] if argv is None else argv)
    if args.command == "validate":
        return validate_command()
    return execute(args.report)


__all__ = [
    "ALLOWED_REPOSITORIES", "ROOT", "RUNTIME_PATH", "AutonomyError",
    "build_record", "check_runs_state", "execute", "load_json", "main",
    "record_path_for", "repository_state", "validate_activation",
    "validate_command", "validate_record", "validate_runtime_contract",
]

if __name__ == "__main__":
    raise SystemExit(main())
