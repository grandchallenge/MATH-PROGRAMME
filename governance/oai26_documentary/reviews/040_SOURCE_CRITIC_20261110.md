# OAI-26 Family 040 — bounded primary-source editorial critic

**Scope:** Checking what the pinned manuscript actually asserts, not independently verifying its proof or certifying Bloch's conjecture.

Pinned upstream: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

Exact source: `preprints/Blochs-Conjecture-for-Surfaces-with-pg-equals-q-equals-0-September-24-2026/paper.pdf`. Git blob `1d0ec7929de8830b03ed264ac44ea9c375d0a96b`, 606,566 bytes, 45 pages; SHA-256 `afb7bf56f8d97111983646a0791ef45c85cfa64dbc1fb3b2ebd7cff24170a0aa`. Independently retrieved raw bytes produce the pinned Git blob identity.

## Source-statement comparison

Page 1, Theorem 1.1: for every smooth connected projective surface over C with geometric genus p_g=0 and irregularity q=0, the **integral** degree homomorphism CH_0(S) to Z is an isomorphism. It assumes no minimality, fundamental-group, or special-construction condition.

Page 1, Corollary 1.2: for every smooth connected projective complex surface with p_g=0, the Albanese homomorphism from **integral degree-zero zero-cycles** CH_0(S)^0 to Alb(S)(C) is an isomorphism. The paper invokes the fact that general-type p_g=0 surfaces have q=0 and the classical Bloch–Kas–Lieberman theorem for the non-general-type cases; the introduction places the classical result at Kodaira dimension less than two. This is a source-claimed deduction, not an independent replay of the classical result.

Pages 2–4 sketch a determinant-fixed Quot-scheme localization and Chow correspondence approach, with rational Chow diagonal identity, nonzero coefficient for K^2 <= 8 and K^2 = 9 by separate arguments, then Roitman's torsion theorem to recover the **integral** conclusion. Merely obtaining rationally trivial degree-zero cycles would be weaker than Theorem 1.1. We have not verified these calculations or cited theorems independently.

**Verdict: ACCEPTED_EXPOSITION_WITH_LIMITS.** The six-section article correctly distinguishes Theorem 1.1 (p_g=q=0) from Corollary 1.2 (all p_g=0), maintains integral coefficients and the classical dependency. No complete proof audit, literature-source check of BKL or Roitman, exact Lean/Comparator replay, manuscript-semantic formal equivalence or MATHCERT certification has been performed.

**Claim boundary:** Source-statement editorial fidelity only; NO_CERTIFICATION. Acceptance requires exact-hash article registry, mathematical Markdown and compendium tests, rendered HTML inspection, and protected merge/readback.
