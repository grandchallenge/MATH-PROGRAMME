# EC-BULK-007 critical sample #1087 — primary definition resolved; proof review pending

**Status:** REVIEW_PENDING_ASYMPTOTIC_PROOF_AND_EXPOSITION. Primary six-distance definition resolved by the authenticated REVISE result; this is NOT a completed critical review.

- Source return: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2358#issuecomment-6162306382
- Original source: Erdős and Purdy, Some extremal problems in geometry, JCTA 10 (1971), pp.246–252.
- Unaccepted draft: governance/erdos_compendium/editorial/1087.md

## Source-fidelity obligation

The original Erdős–Purdy 1971 source, section 4, printed p. 251, defines the relevant quadruples by requiring that the six pairwise distances are *not all different*. Thus equal-length segments sharing an endpoint **are included**; there is no disjoint-pair-only restriction. Source-critical REVISE result: https://github.com/grandchallenge/MATH-PROGRAMME/issues/2684#issuecomment-6387995206 . A reproduced copy of the original text is at https://paperzz.com/doc/7349569/some-extremal-problems-in-geometry-let-there-be-given-n-p... . For collinear points at positions 0,1,3,6, the squared distances are 1,4,9,9,25,36. The equal length-three segments (0,3) and (3,6) share one endpoint, and no two disjoint segments have the same length. This exact witness tests the definition, not either asymptotic estimate.

The square example is degenerate under either convention, so cannot adjudicate the ambiguity. Reproducible script ci/erdos_compendium_007_phase8_checks.py separately counts disjoint and shared-endpoint equal segments for these witnesses, with exact integer arithmetic.

## Required before critical approval

Obtain a provenance-locked copy of the original 1971 article, including a content hash and page-image verification. The statement's meaning has been resolved from printed p. 251, but that paragraph states the historical $n^3\log n$ and $n^{7/2}$ bounds without displaying derivations. Locate and critically verify those derivations (in that article or explicitly identified companion sources); check the counting convention and asymptotic constants; then conduct independent mathematical and exposition review. The registered immutable manuscript SHA belongs to the *earlier* candidate and is not silently rewritten by this successor editorial correction. Do not count this as a completed review, admit protected publication, or claim a solution to the open $n^{3+o(1)}$ question.
