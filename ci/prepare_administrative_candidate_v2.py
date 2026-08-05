from __future__ import annotations

import administrative_automation as automation
import administrative_receipts as receipts

automation.derive_completion_state = receipts.derive_completion_state

import prepare_administrative_candidate as implementation


if __name__ == "__main__":
    raise SystemExit(implementation.main())
