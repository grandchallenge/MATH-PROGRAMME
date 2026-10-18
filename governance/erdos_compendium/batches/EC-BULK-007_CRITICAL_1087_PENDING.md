# EC-BULK-007 critical sample #1087 — pending original definition

**Status:** REVIEW_PENDING_PRIMARY_DEFINITION_AND_PROOF. This is NOT a completed critical review.

- Source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2358#issuecomment-6162306382
- Original source: Erdős and Purdy, Some extremal problems in geometry, JCTA 10 (1971), pp.246–252.
- Unaccepted draft: governance/erdos_compendium/editorial/1087.md

## Source-fidelity obligation

The catalogue calls a four-point subset degenerate when among its six pairwise distances two coincide. Primary source must establish whether equal-length segments can SHARE AN ENDPOINT. This changes the result. For collinear points at positions 0,1,3,6, pair squared distances are 1,4,9,9,25,36. The two length-three segments (0,3) and (3,6) share one endpoint, and no two disjoint segments have the same length. Under a disjoint-pair-only definition this quadruple is not degenerate, although it is under the shared-endpoint-inclusive definition.

The square example is degenerate under either convention, so cannot adjudicate the ambiguity. Reproducible script ci/erdos_compendium_007_phase8_checks.py separately counts disjoint and shared-endpoint equal segments for these witnesses, with exact integer arithmetic.

## Required before critical approval

Acquire and hash the original 1971 pages, identify exact definition and original n^3 log n and n^(7/2) proofs, reconcile any incorrect catalogue or draft semantics, then conduct independent mathematical and exposition review. Do not count this as a completed review, admit protected publication, or claim a solution to the open n^(3+o(1)) question.
