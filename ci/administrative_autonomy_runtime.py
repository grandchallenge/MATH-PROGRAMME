from __future__ import annotations

from functools import partial

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

behind_sync.synchronize_eligible_candidate = partial(
    structural_1809_synchronize_eligible_candidate,
    base=behind_sync.synchronize_eligible_candidate,
)

# Preserve the durable executor-import boundary relied on by certification tests.
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
