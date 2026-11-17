# Erdős source-return late-exception custody

Control: ERDOS-LATE-SOURCE-EXCEPTION-CUSTODY-001.

## Exact incident

On 2026-10-20 the source-audit issue [#1836](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1836)
was closed at 09:10:57 UTC. The Council Clerk posted
[exception 6288214238](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1836#issuecomment-6288214238)
at 09:49:43 UTC, saying SOURCE_INTEGRITY and NO SOURCE ACCEPTANCE.
The [original result](https://github.com/grandchallenge/MATH-PROGRAMME/issues/1836#issuecomment-6287257066)
remains evidence, not an accepted proof.

## Prevention through the admitted controller

The existing one-issue return-fastpath workflow now accepts both normal
RESULT/1 comments and Clerk-authored GCL-RETURN-EXCEPTION/1 comments.
The second case runs ci/erdos_late_exception_recovery.py with the existing
Council Clerk App token, not a new automation or authorization service.

The event and current comment must agree byte for byte and match the
original issue and registry. A closed Done issue is reopened and the Project
status restored to RETURNED, with exact readback. Repeated invocations are
idempotent. The unchanged source-integrity review remains required.

The ordinary return projector also checks an exact, complete live comment
census before preserving Done. Any unresolved source-exception comment
blocks that terminal disposition. A census with 100 or more comments fails
closed; do not truncate. No worker result is edited or deleted.

## Reproduction, review, and claim boundary

Replay the 2026-10-20 post-closure exception case, a clean historical Done,
an incomplete comment census, and idempotent recovery. Run unit tests,
workflow routing and Markdown checks against the exact candidate.

Use the original issue for source-semantic review and record a protected
disposition before further terminal closure. No part of this control grants
mathematical acceptance, proof certification or automatic source approval.

The related #566/#567 incorrect formal Ramsey invariant requires its own
source-bound semantic repair, not a global silent provider update.
