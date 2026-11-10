# OAI26 Family 078 — bounded primary-source editorial critic

**Scope:** Statement fidelity to the pinned 3D Bochner–Riesz manuscript, not an independent proof audit, formalization replay, or certification.

Pinned upstream: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

Exact PDF: `preprints/Bochner-Riesz-Multipliers-in-Three-Dimensions-September-24-2026/Bochner-Riesz-Multipliers-in-Three-Dimensions-September-24-2026.pdf`. Git blob `2dd11d2a25a1d2fc0dd86bfca549162f970d8d5b`, 1,044,335 bytes, 114 pages, SHA-256 `ea18d159eefcdc7fff031ab14035ecba7205de156a7fcd747a6a9c6bd0d6762a`. Independently retrieved bytes reproduce the pinned Git blob hash.

## Source theorem and logical limitations

Page 2, Theorem 1.1: for each **fixed order delta > 0**, the Bochner–Riesz multiplier `T_delta` with symbol `(1-|xi|^2)_+^delta` has a finite L^3(R^3) operator norm, with a constant depending on delta. The paper defines the transform with the phase `exp(-2*pi*i*x.xi)` and states the bound first for Schwartz functions, extending uniquely to L^3.

Page 2, consequence (1.3): by the interpolation and duality argument, for **all 1 <= p <= infinity**, the fixed-order multiplier is bounded on L^p(R^3) when
`delta > max{ 3*|1/p - 1/2| - 1/2, 0 }`.
The inequality is **strict**: the source does not establish the equality threshold. At p=2 the printed sufficient criterion is delta>0; for p=1 or infinity it is delta>1. The paper says constants may depend on p and delta. The order is fixed before choosing constants.

Page 2 additionally says scaling supplies the same operator bounds for the dilation family with symbol `(1-|xi|^2/R^2)_+^delta` for each R>0, and for finite p the means converge in L^p to the original function as R tends to infinity. This should not be confused with a maximal theorem over all radii or endpoint-equality boundedness.

Sections 2–12 outline entropy/projection estimates, extremal transport, packet decompositions, oscillatory integrals and interpolation. These are proof dependencies, not results independently replayed here.

**Verdict: ACCEPTED_EXPOSITION_WITH_LIMITS.** The article faithfully states the pinned source's main L^3 theorem and all-p strict-range consequence. Not established: 114-page proof correctness, complex-order interpolation and endpoint extension, detailed packet uncertainty or restriction estimates, named Lean declarations, Comparator acceptance or independent mathematical certification.

**Claim boundary:** Documentary statement fidelity only; NO_CERTIFICATION. Exact article SHA-256, mathematical Markdown and compendium tests, generated HTML, and protected merge/readback remain mandatory.
