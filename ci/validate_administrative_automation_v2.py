from __future__ import annotations

from pathlib import Path

import administrative_automation as automation
import administrative_receipts as receipts

automation.derive_completion_state = receipts.derive_completion_state

import validate_administrative_automation as implementation

ROOT = Path(__file__).resolve().parents[1]
EXTRA_PATHS = [
    ROOT / "ci" / "administrative_receipts.py",
    ROOT / "ci" / "dispatch_administrative_maintenance_v3.py",
    ROOT / "ci" / "prepare_administrative_candidate_v2.py",
    ROOT / "ci" / "synchronize_administrative_completion_v2.py",
]
FORBIDDEN = (
    "/merges",
    "merge_pull_request",
    "enable_auto_merge",
    "dismiss_pull_request_review",
    "branch_protection_rule",
)


def main() -> int:
    result = implementation.main()
    if result:
        return result
    errors: list[str] = []
    for path in EXTRA_PATHS:
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in text:
                errors.append(f"{path.name}: forbidden authority capability token {token}")
    if errors:
        for error in errors:
            print(error)
        return 1
    print("MP-ADMIN-AUTOMATION-CLOSURE-001: protected receipt routing valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
