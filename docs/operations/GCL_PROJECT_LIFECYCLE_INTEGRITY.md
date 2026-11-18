# GCL Project #2 lifecycle integrity

## Source of authority

The ordinary Project V2 Status options are Todo, In Progress, Done, RETURNED.
AVAILABLE is not and must not be added to Status.

GCL State is an organization Issue Field, with its own option values,
independent of Project V2. The homonymous Project V2 GCL State field
is an empty, unused duplicate (all 1,449 entries unpopulated on
2026-11-18). Never read or write it as execution authority.
It must remain empty until separately governed removal after every
consumer is migrated. Do not add options to this duplicate.

The global AVAILABLE view uses the exact filter
is:open label:gcl-state:available. A matching label is only a
discovery signal. An actual worker must additionally pass the protected
dispatch, active lease, and authenticated pickup/custody rules. No
Project field, label, or audit result grants execution or certification.

## Integrity audit

Run: python ci/gcl_project_lifecycle_integrity.py
Requires authenticated GitHub CLI token with organization Project
read permission. Traverses all Project #2 pages and verifies project
identity, Status schema, available-view filter, absence of duplicate
Project GCL State values/options, lifecycle label consistency,
closed/active mismatches, and truncation.

An open GitHub issue does not imply unfinished mathematical work:
OPEN+Done is a review notice only if the issue is not labeled returned.
A returned worker dispatch can remain OPEN for controlled intake while its
Project workflow is Done. Neither case authorizes automatic mutation.

Tests: python -m unittest ci.test_gcl_project_lifecycle_integrity -v

CI runs tests on source changes. Weekly/manual live observations require
the already configured Council Clerk GitHub App credential with Projects access and fail closed
if missing. No recurring mutation is permitted.

## 2026-11-18 exact inventory

1,449 Project items; 130 issues with gcl-state:available label;
502 closed issues. Closed MATHSOLVE #1218 was Todo and was
corrected to Done with exact item/state readback. MATHSOLVE #1082 is an OPEN+Done staged, returned QFT dispatch with
RESULT/1 and an intake receipt; this is a legitimate terminal worker
projection, not an outstanding mismatch. Preserve its return custody.

The generic queue-class audit reporting zero semantic changes
is not a complete lifecycle-integrity audit. Use both checks.
