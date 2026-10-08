#!/usr/bin/env bash
# Reproduce the bounded CM4 integer/module theorem on the repository's exact pins.
# No protected-branch writes, no GitHub credentials, no claim promotion.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
cd "$ROOT"
PACKAGE="fixtures/formal/CMDG-NAT-CONCORDANCE-001"
THEOREM="$PACKAGE/CMDGCondensedCM4Blocker.lean"
BRIDGE="$PACKAGE/CMDGCondensedCM4P3GPointFunctional.lean"

verify_blob() {
    local path="$1" expected="$2" observed
    observed="$(git hash-object "$path")"
    if [[ "$observed" != "$expected" ]]; then
        printf 'Source-lock mismatch for %s: %s != %s\n' "$path" "$observed" "$expected" >&2
        exit 2
    fi
}
verify_blob "$THEOREM" "8ab0051746507099f7321460fe091e56a84b57bb"
verify_blob "$BRIDGE" "d3ef22a2ad2d9c0af6982773d0a24b715e61f5a7"

command -v lake >/dev/null || { echo 'Lean/lake is required (install elan and use the pinned lean-toolchain)' >&2; exit 2; }
command -v python3 >/dev/null || { echo 'Python 3 is required' >&2; exit 2; }
command -v git >/dev/null || { echo 'Git is required' >&2; exit 2; }

echo "CM4 protected source-lock PASS. The workspace HEAD need not equal the source-baseline commit provided both blobs match."
echo "Lean toolchain: $(cat "$PACKAGE/lean-toolchain")"
echo 'Policy dependencies must already be installed: python3 -m pip install -r requirements/policy.txt'

python3 ci/formal_validation.py validate

# Uses the pinned, manifest-resolved mathlib dependency; NEVER call 'lake update' here.
(cd "$PACKAGE" && lake exe cache get)

# The runner refuses drift of the exact mathlib commit/tree and compiles the
# complete local import closure in promotion mode, rather than only changed files.
python3 ci/formal_validation.py run --lane cmdg-cm4 --mode promotion --changed-paths-json '[]'
python3 ci/formal_validation.py run --lane cmdg-cm4-p3 --mode promotion --changed-paths-json '[]'

# The JSON receipts are generated locally; this does not independently certify
# theorem semantics, reviewer independence, upstream novelty or publication.
python3 - <<'PY'
import json
from pathlib import Path
for lane in ("cmdg-cm4", "cmdg-cm4-p3"):
    file = Path(".formal-validation") / lane / "result.json"
    data = json.loads(file.read_text(encoding="utf-8"))
    if data.get("status") != "FORMAL_VALIDATION_SUCCEEDED" or data.get("mode") != "promotion":
        raise SystemExit(f"{lane}: no successful promotion-mode receipt")
    print(f"{lane}: {data['status']} ({len(data['compiled_local_lean_closure'])} local Lean files)")
print("CM4 protected source and pinned formal-lane replay completed.")
PY
