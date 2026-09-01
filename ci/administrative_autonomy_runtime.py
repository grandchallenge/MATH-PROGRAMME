from __future__ import annotations

import importlib.util
import json
import os
import sys
import unittest
from concurrent.futures import ThreadPoolExecutor
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
# instead of adding another privileged scheduler. The bounded routine lane and
# ordinary administrative lane are launched independently inside each heartbeat
# so failure or latency in either lane cannot make the other lane unreachable.
# Both still use the existing separated credentials and fail closed together.
import administrative_autonomy_low_friction as low_friction
import administrative_autonomy_low_friction_persistent_sync as low_friction_persistent_sync

# GitHub's pull-request mergeable_state is not a reliable base-drift signal: a
# branch can be mergeable/clean while protected main has advanced. Bind the
# low-friction runtime to exact protected-base ancestry instead. All existing
# low-friction state-machine checks consume current_pull(), so this one bounded
# overlay makes base drift visible as BEHIND throughout checking and stabilization.
# Importing this runtime both as __main__ and as a module is supported by the
# repository validators; install the overlay idempotently so those imports never
# stack ancestry wrappers or duplicate protected-main reads.
_existing_base_aware_current_pull = (
    low_friction.current_pull
    if getattr(low_friction.current_pull, "_mp_low_friction_base_aware", False)
    else None
)
_low_friction_current_pull = (
    getattr(
        _existing_base_aware_current_pull,
        "_mp_low_friction_original",
        low_friction.current_pull,
    )
    if _existing_base_aware_current_pull is not None
    else low_friction.current_pull
)


def _new_base_aware_low_friction_current_pull(client, pr: int) -> dict[str, object]:
    pull = _low_friction_current_pull(client, pr)
    if pull.get("state") != "open" or pull.get("merged") is True:
        return pull
    base_ref = str(pull.get("base", {}).get("ref") or "")
    head_sha = str(pull.get("head", {}).get("sha") or "")
    if base_ref != low_friction.EXPECTED_BASE or not low_friction.SHA_RE.fullmatch(head_sha):
        return pull

    branch_path = (
        f"/repos/{low_friction.EXPECTED_REPOSITORY}/branches/"
        f"{low_friction.EXPECTED_BASE}"
    )
    base = client.get(branch_path)
    base_sha = str(base.get("commit", {}).get("sha") or "")
    if not low_friction.SHA_RE.fullmatch(base_sha):
        raise AutonomyError("low-friction protected-base SHA readback is invalid")

    compare = client.get(
        f"/repos/{low_friction.EXPECTED_REPOSITORY}/compare/{base_sha}...{head_sha}"
    )
    compare_base = str(compare.get("base_commit", {}).get("sha") or base_sha)
    if compare_base != base_sha:
        raise AutonomyError("low-friction protected-base comparison identity drift")
    try:
        behind_by = int(compare.get("behind_by") or 0)
    except (TypeError, ValueError) as exc:
        raise AutonomyError("low-friction protected-base behind count is invalid") from exc
    if behind_by < 0:
        raise AutonomyError("low-friction protected-base behind count is negative")

    # Re-read protected main after the comparison. A movement during comparison
    # is conservatively treated as BEHIND so the state machine re-enters sync.
    base_after = client.get(branch_path)
    base_after_sha = str(base_after.get("commit", {}).get("sha") or "")
    if not low_friction.SHA_RE.fullmatch(base_after_sha):
        raise AutonomyError("low-friction protected-base post-compare SHA is invalid")
    base_moved = base_after_sha != base_sha

    if behind_by == 0 and not base_moved:
        return pull
    value = dict(pull)
    value["mergeable_state"] = "behind"
    value["_low_friction_base_drift"] = {
        "protected_base_sha": base_sha,
        "protected_base_sha_after": base_after_sha,
        "candidate_head": head_sha,
        "compare_status": str(compare.get("status") or "unknown"),
        "behind_by": behind_by,
        "base_moved_during_compare": base_moved,
    }
    return value


if _existing_base_aware_current_pull is None:
    _new_base_aware_low_friction_current_pull._mp_low_friction_base_aware = True
    _new_base_aware_low_friction_current_pull._mp_low_friction_original = (
        _low_friction_current_pull
    )
    low_friction.current_pull = _new_base_aware_low_friction_current_pull
    _base_aware_low_friction_current_pull = _new_base_aware_low_friction_current_pull
else:
    _base_aware_low_friction_current_pull = _existing_base_aware_current_pull

# A synchronization can occur in one protected heartbeat and terminal admission
# in a later heartbeat. Persist and recover that event history so the final
# receipt cannot lose already-performed internal head updates when process memory
# is reset between scheduled runs.
low_friction_persistent_sync.install(low_friction)

_base_execute = protected_behind_execute
_base_validate_command = protected_behind_validate_command


def _load_test_module(path: Path, module_name: str):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load low-friction adversarial matrix: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _validate_low_friction_matrix() -> int:
    errors = low_friction.validate_control(
        low_friction.load_json(low_friction.CONTROL_PATH)
    )
    if errors:
        for error in errors:
            print(error)
        return 1
    suite = unittest.TestSuite()
    test_paths = (
        ROOT / "tests" / "test_administrative_autonomy_low_friction.py",
        ROOT / "tests" / "test_administrative_autonomy_low_friction_base_drift.py",
        ROOT / "tests" / "test_administrative_autonomy_low_friction_persistent_sync.py",
    )
    try:
        for index, test_path in enumerate(test_paths):
            module = _load_test_module(
                test_path, f"mp_admin_low_friction_matrix_{index}"
            )
            suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(module))
    except Exception as exc:
        print(exc)
        return 1
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
    _bind_existing_ruleset_token()
    low_report = report_path.with_name("administrative-low-friction-sweep.json")
    low_state = "LOW_FRICTION_NOT_RUN"
    low_error: str | None = None

    # Liveness invariant: neither administrative lane is downstream of the
    # other. Each heartbeat starts both lanes before waiting on either result.
    with ThreadPoolExecutor(
        max_workers=2,
        thread_name_prefix="mp-admin-heartbeat",
    ) as executor:
        low_future = executor.submit(low_friction.sweep, low_report)
        base_future = executor.submit(_base_execute, report_path)

        try:
            outcome = low_future.result()
            low_state = str(outcome.get("state") or "SWEEP_COMPLETE")
        except Exception as exc:
            low_state = "LOW_FRICTION_FAILED_CLOSED"
            low_error = str(exc)
            print(
                f"low-friction routine lifecycle failed closed: {exc}",
                file=sys.stderr,
            )

        # Preserve the ordinary lane's historical exception semantics while
        # ensuring it was already started even if low-friction failed closed.
        base_result = int(base_future.result())

    _attach_low_friction_summary(
        report_path,
        state=low_state,
        low_report=low_report,
        error=low_error,
    )
    if base_result != 0:
        return base_result
    if low_error is not None:
        return 1
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
