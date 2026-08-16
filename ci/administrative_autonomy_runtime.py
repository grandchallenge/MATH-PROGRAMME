from __future__ import annotations

import administrative_autonomy_receipt_stage as receipt_stage
import administrative_autonomy_runtime_github as runtime_github
import administrative_autonomy_runtime_receipt_behind_resume as receipt_resume
from administrative_autonomy_runtime_contract import (
    ALLOWED_REPOSITORIES, ROOT, RUNTIME_PATH, build_record, load_json,
    record_path_for, repository_state, validate_activation, validate_record,
    validate_runtime_contract,
)
from administrative_autonomy_runtime_github import check_runs_state
from administrative_autonomy_runtime_queue_starvation import (
    pending_closures as nonblocking_pending_closures,
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
from autonomy_github import AutonomyError

receipt_stage.pending_closures = nonblocking_pending_closures
receipt_stage.advance_completion_state = structural_0121_hole_advance_completion_state
receipt_resume.advance_completion_state = structural_0121_hole_advance_completion_state
receipt_stage.stage_completion_receipt = receipt_resume.stage_completion_receipt
RECOVERY_ELIGIBILITY_CHAIN = (
    structural_2033_recovery_eligible_candidates,
    structural_2257_recovery_eligible_candidates,
    structural_0833_recovery_eligible_candidates,
    structural_0121_recovery_eligible_candidates,
)
runtime_github.eligible_candidates = RECOVERY_ELIGIBILITY_CHAIN[-1]
runtime_github.wait_mirror_sync = structural_0121_hole_wait_mirror_sync

from administrative_autonomy_runtime_behind_sync import (
    execute, main, validate_command,
)

__all__ = [
    "ALLOWED_REPOSITORIES", "ROOT", "RUNTIME_PATH", "AutonomyError",
    "build_record", "check_runs_state", "execute", "load_json", "main",
    "record_path_for", "repository_state", "validate_activation",
    "validate_command", "validate_record", "validate_runtime_contract",
]

if __name__ == "__main__":
    raise SystemExit(main())
