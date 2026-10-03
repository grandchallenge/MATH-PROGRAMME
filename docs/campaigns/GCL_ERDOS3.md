# GCL-ERDOS3

GCL-ERDOS3 is the standalone successor research campaign promoted from the OPENMATH-2026 H7 corpus.

## Current protected result

Protected Solve evidence: `6c39975864788f27aea1f0da50fa409625bd5bd6`.

The first research tranche has completed:

- **E3-F01 — FORMALIZED.** The exact current `H7_D5.lean` blob is byte-identical to the artifact successfully compiled in the organizer-pinned Lean 4.33.1 image. Finite deletion, tail preservation and divergent residue-fibre lemmas are now proof-receipted. `E3-F-D5` is closed and has no replay successor.
- **E3-B01 — PROVED, pending one independent verification.** For normalized dyadic block densities (delta_j), reciprocal divergence is equivalent up to a factor-two blockwise comparison to divergence of (sum_jdelta_j). Every summable threshold is therefore exceeded infinitely often.
- **E3-B01 extremal reduction.** If (sum_j r_k(2^j)/2^j<infty), then every reciprocally divergent set contains a non-trivial (k)-term arithmetic progression.
- **E3-A01 — BOUNDARY_SHARPENED.** For every nonsummable threshold sequence (	heta_jin[0,1]), an explicit reciprocally divergent set can be built with dyadic density never exceeding (	heta_j). Thus summability is qualitatively sharp for density-only threshold forcing.
- **E3-S01 — SOURCE_INTERFACE_FOUND.** Exact Mathlib residue/summability interfaces, Formal Conjectures AP-free extremal interfaces, and the quantitative three-term source are bound.

## Quantitative calibration

Bloom–Sisask's three-term estimate (r_3(N)ll N/(log N)^{1+c}) crosses the dyadic summability barrier and reproduces the known three-term case.

For four-term progressions, the current cited Green–Tao bound (r_4(N)ll N(log N)^{-c}) for a small (c>0) does not cross that barrier. The maintained Erdős Problems record gives (N/[(log N)(loglog N)^2]) as an example of a sufficient scale.

This does not show the dyadic route is necessary. It identifies exactly what is missing from that route.

## Active frontier

1. `E3-V-B01`: one independent, protected-packet-only verification of the new bridge. Issue #762.
2. `E3-B-AP`: for fixed (kge4), obtain a summable dyadic AP-free density envelope or find a stronger cross-scale mechanism.

The operational contribution lifecycle remains separate from the mathematical frontier. `Next residual` is evidence, not scheduling authority. No result here proves Erdős Problem 3.
