# OAI26 Family 083: bounded source critic

**Primary revision:** `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.
**Primary source:** `preprints/A-uniform-Hilbert-transform-estimate-for-Lipschitz-directions-September-25-2026/main.pdf`.

## Inspected evidence

The pinned manuscript's `build/sections/01-introduction.tex` includes the main theorem, definitions, comparison to preceding work, explanation of band reduction and proof mechanism. The publisher's `lean/docs/083.md` records the claimed formal scope.

## Claim and exclusion audit

For any unit Lipschitz field in two spatial coordinates with Lipschitz seminorm at most one, the manuscript claims a common L2 bound on the short directional Hilbert transform at all positive hard inner truncations below one fixed universal outer length. Its supremum over truncations is outside the operator norm; do not promote this to an L2 maximal-hard-truncation bound. Its output-point direction convention is part of the statement. The symmetric principal-value, bounded extension and weak-(2,2) assertions are source corollaries. For positive Lipschitz seminorm K, the short outer scale is proportional to 1/K; constant fields use a separate argument. No statement for arbitrary long outer lengths is licensed.

The source identifies Lacey-Li's short popularity maximal theorem and Lepingle's martingale 3-variation theorem as specialized imported inputs. The rest of the outlined analytic proof includes frequency reassembly, a logarithmic restricted estimate, packet forests, exactly-one Fourier inequality, and angular mass-telescoping. Each requires independent proof-body and hypothesis review.

The pinned Lean scope states a quantified radius at most 1/(1000000 K) for K positive. It is not sufficient evidence of exact formal replay, axiom cleanliness, nonvacuity, or statement equivalence. Prior annular, analytic, one-coordinate and rounded directions results must not be conflated with the full planar Lipschitz result.

**Critical verdict: SOURCE_SCOPE_REVIEWED_WITH_LIMITS; NO_CERTIFICATION.** Article SHA registration, regression tests, strict docs build, required exact-head CI, protected merge and main readback remain documentary admission obligations.
