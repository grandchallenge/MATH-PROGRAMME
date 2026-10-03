# GCL-ERDOS3

GCL-ERDOS3 is the standalone successor research campaign promoted from the OPENMATH-2026 H7 corpus.

## Current protected result

Protected Solve adjudication: `20fc4eb4cda683bc07992bd27903e926b190b8b4`.

The first tranche and its single authorized independent replay are complete:

- **E3-F01 — FORMALIZED.** The current `H7_D5.lean` blob is the exact artifact compiled successfully in the pinned Lean 4.33.1 environment. `E3-F-D5` is closed with no replay successor.
- **E3-B01 — PROVED AND INDEPENDENTLY VERIFIED.** Reciprocal divergence is equivalent, up to the factor-two dyadic sandwich, to divergence of the normalized dyadic block-density sum. The AP-free extremal reduction is also verified:
  [
  sum_j r_k(2^j)/2^j<infty
  Longrightarrow
  	ext{every reciprocally divergent set contains a non-trivial }k	ext{-AP}.
  ]
- **E3-A01 — BOUNDARY_SHARPENED.** The nonsummable-threshold construction verifies that summability is qualitatively sharp for arguments using only dyadic density threshold exceedance.
- **E3-S01 — SOURCE_INTERFACE_FOUND.** Exact Lean/Mathlib/AP interfaces and the quantitative extremal-source boundary are bound.
- **E3-V01 — VERIFIED, CLOSED.** The one independent replay authorized by the frontier gate found no defect in the five requested claims.

The authenticated GitHub actor for the E3-V01 return was `fyremael`. GCL records this as transport provenance. The independence claim is limited to the declared zero-context, protected-packet-only execution contract; no distinct-human or distinct-account identity claim is made.

## Active frontier

Only `E3-B-AP` remains active.

For each fixed (kge4), the current route needs either:

[
rac{r_k(2^j)}{2^j}le eta_k(j)
quad	ext{with}quad
sum_jeta_k(j)<infty,
]

or a genuinely stronger cross-scale mechanism not reducible to independent dyadic block densities.

No further equivalent replay of B01 is authorized; its default independent verification budget has been exhausted.

No result here proves Erdős Problem 3.
