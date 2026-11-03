# OAI26 Family 081 — bounded primary-source critic

**Source:** `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`, `preprints/Riesz-transforms-and-uniform-rectifiability-in-higher-codimension-September-24-2026/paper.pdf`.

## Source evidence inspected

The primary `build/paper.tex` abstract and `build/sections/00-introduction.tex` definitions, full main theorem and methodological overview were read. The pinned `lean/docs/081.md` explains the publisher's claimed formal scope.

## Claim boundaries

The manuscript asserts a quantitative uniform rectifiability conclusion for n-Ahlfors–David regular Radon measures in Euclidean dimension d, integers d at least four and n between two and d minus two. Its hypothesis is a single uniform scalar L² to vector L² operator bound on **every positive hard truncation** of the n-dimensional Riesz transform. It does not require principal values or a variation bound. The claimed conclusion is big pieces of Lipschitz images at every support point and admissible radius, constants depending only on d, n, Ahlfors–David regularity and the transform bound. The empty and unbounded support conventions should be preserved.

The formal-scope description explicitly excludes the variation and principal-value corollaries, which must not be promoted through the main comparator alone.

## Open critical obligations

Independently check the global growth and tail pairings, bilateral flat-ball packing, planar compactness limits, normal-height normalization and fractional-energy estimates, limiting affine rigidity and growth class, relative excess improvement, dyadic endpoint packing, and invocation of the David–Semmes theorem. Verify formal comparator statement parity, nonvacuity and all imported axioms against the exact publisher revision. Source reading is not independent proof replay.

**Verdict: SOURCE_SCOPE_REVIEWED_WITH_LIMITS; NO_CERTIFICATION.** Editorial admission is appropriate only on exact SHA-256 registration, reproducible compendium regression, strict rendering, required CI and protected-merge readback.
