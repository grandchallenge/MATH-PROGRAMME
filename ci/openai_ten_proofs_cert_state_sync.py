#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "governance/validators/openai_ten_proofs_cert_state_sync.py"
SPEC = importlib.util.spec_from_file_location("openai_ten_proofs_cert_state_sync", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

if __name__ == "__main__":
    raise SystemExit(MODULE.main())
