# GCL-GHOS-INTELLECT-PROFILE-RECONCILIATION-001 — Phase B operator record

## Purpose

This protected workflow performs only the live INTELLECT profile reconciliation authorized under `grandchallenge/gcl-standards#12` after protected Phase A merge `eaa87bfebab9adbfd39778364aac89aa8c479297`.

## Authorized mutations

The `apply` mode may:

1. add `Constitutional` to the existing `constitutional_profile` single-select vocabulary;
2. add `constitutional` to the existing `authority_scope` single-select vocabulary;
3. apply the six admitted values to `grandchallenge/INTELLECT`;
4. rename the existing active default-branch ruleset to `Constitutional profile - main`.

The property-definition update preserves every field other than the two authorized `allowed_values` extensions. The ruleset update is read-modify-write. Every ruleset field other than `name` must compare equal before and after. The workflow fails closed on bypass actors, missing strict checks, altered review controls, force-push or deletion exposure, malformed property schemas, missing owner proof, or protected-main movement.

## Execution

From `grandchallenge/MATH-PROGRAMME`:

1. Open **Actions**.
2. Select **INTELLECT profile administration**.
3. Select **Run workflow** on protected `main`.
4. Choose `apply`.
5. Approve the `release-trust` environment gate when prompted.

A preliminary `verify` run is safe and read-only but will fail until the live drift is repaired.

## Evidence

A successful run uploads:

- `intellect-profile-admin-evidence.json`;
- `intellect-profile-admin-evidence.json.sha256`.

The evidence binds owner identity, protected-main stability, pre/post organization property schemas, pre/post repository values, complete pre/post ruleset details, exact mutations, API version `2026-03-10`, Phase A identities, and closed claim boundaries.

The artifact must be admitted through a separate independently reviewed evidence PR before issue #12 or `INTELLECT-P0-001` can close.
