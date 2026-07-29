# Lean Formalization Handoff

## Obligation

Use this lane to transfer a normalized theorem statement and its exact assumptions into a reproducible Lean package with pinned dependencies and an explicit build target.

## MATHFORGE

MATHFORGE contributes source reconstruction, equivalent formulations, examples, and candidate formal definitions. It does not treat a plausible formal statement as source correspondence.

## MATHSOLVE

MATHSOLVE fixes the normalized proposition, assumption ledger, imports, theorem name, target file, and correspondence argument. It rejects hidden strengthening, weakening, or carrier changes.

## MATHCERT

MATHCERT checks out the pinned commit, scans for prohibited placeholders and local axioms, runs the declared build, and confirms that the exported declaration matches the normalized claim.

## Allowed statuses

`normalized`, `formalization_ready`, `build_passed`, `ready_for_mathcert`, `rejected`.

## Rejection policy

Reject source mismatch, unpinned dependencies, unspecified build commands, `sorry`, local axioms, and claims broader than the named declaration.

## Package

The package root is `lanes/lean_formalization_handoff`. Its toy fixture normalizes and prepares the natural-number theorem `a + 0 = a` without claiming certification.

## Claim boundary

A successful Lean build certifies only the named declaration under its imported foundations and verified source correspondence.
