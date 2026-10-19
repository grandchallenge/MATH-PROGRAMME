# Erdős catalogue: invalid and competing return handling

This is an extension of the existing protected controller; not a new approval
body, a duplicate task queue, or a scientific certification authority.

## Scope and mechanical repair

A content-addressed source snapshot produces a deterministic exception manifest.
Each worker processes at most **16 source issues**, with no more than **two
workers in parallel**. A fresh Council Clerk token grants issue-comment
permission only. Processing starts after the ordinary source-return aggregate
verifier has passed.

Formatting repair is allowed only when the authenticated original contains all
five correct identity headers, all six nonempty substantive sections, and no
unknown metadata other than the five registered pinned-source audit fields.
The permissible transformation moves extra headers **verbatim** into dated
source evidence, renames an explicit allowlist of equivalent headings, and
reorders complete sections. The original source section text is preserved.

The derived RESULT/1 is an attributed formatting copy carrying the original
comment URL and SHA-256 and an explicit disclaimer of independent authorship
or scientific acceptance. No original worker comment is changed or deleted.

If research is missing, problem identity mismatches, content would be lost, or
multiple invalid source comments conflict, no automatic rewrite occurs. A
GCL-RETURN-EXCEPTION/1 reviewer request is posted once on the **original issue**,
binding exact comment IDs and digests. It is an unresolved specialist obligation,
not acceptance. No separate tickets or Human Steward routine approvals.

## Multiple valid returns

Every contribution remains preserved. Neither first-return nor latest-return
selection is permitted. The protected source-review ledger at
governance/erdos_catalogue/RETURN_ARBITRATIONS.json requires an exact candidate
set of comment IDs and SHA-256 digests, substantive comparative evidence,
specialist identity, a protected review PR, and bounded selection rationale.
Its only authority is selecting a source for queue projection; no theorem
certification or source-semantic acceptance follows. Missing or stale specialist
evidence prevents automatic advancement.

## Evidence and operation

Inspect [the operational workflow](https://github.com/grandchallenge/MATH-PROGRAMME/actions/workflows/erdos-catalogue-queue-projection.yml):

1. The immutable source-return input artifact includes REPORT.json and
   EXCEPTION_MANIFEST.json.
2. Each exception batch artifact includes an exact receipt with its matched
   content hash, issue ID, original source ID and authenticated output readback.
3. The exception aggregate receipt requires all manifest entries. It reports
   mechanical repairs separately from unresolved source/competition reviews.

VERIFIED_WITH_SOURCE_REVIEW_PENDING is not the same as fully remediated.
A missing or BLOCKED receipt is a failed proof of operation. Even a corrected
RESULT/1 must enter the existing source-intake and queue-projection flow before
Project and Issue Field state changes can be claimed.

Read-only verification commands:

    PYTHONPATH=. python3 tests/test_erdos_return_exceptions.py -q
    PYTHONPATH=. python3 tests/test_erdos_catalogue_queue_projection.py -q
    python3 ci/validate_workflow_coverage_v2.py

The initial October 19, 2026 snapshot held 232 rejected comments. A bounded
loss-preservation replay accepted 190 for mechanical repair. The remaining 40
invalid-only issues require source-specialist review; issue #2491 already had a
valid return alongside two rejected comments. These counts are time-bound.
