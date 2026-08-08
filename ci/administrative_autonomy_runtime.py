from __future__ import annotations

import administrative_autonomy_runtime_github as runtime_github
from administrative_autonomy_runtime_contract import (
    ALLOWED_REPOSITORIES, ROOT, RUNTIME_PATH, build_record, load_json,
    record_path_for, repository_state, validate_activation, validate_record,
    validate_runtime_contract,
)
from administrative_autonomy_runtime_github import check_runs_state
from administrative_autonomy_runtime_late_recovery import (
    eligible_candidates as late_recovery_eligible_candidates,
)
from autonomy_github import AutonomyError

runtime_github.eligible_candidates = late_recovery_eligible_candidates

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
