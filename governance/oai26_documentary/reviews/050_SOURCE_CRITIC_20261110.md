# OAI-26 Family 050 — bounded primary-source editorial critic

**Scope:** Source-statement fidelity, not independent construction or curvature proof review, source-to-Lean equivalence, or MATHCERT certification.

Pinned upstream: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

Exact primary PDF: `preprints/ample-rank-two-bundles-on-the-quadric-surface-without-griffiths-positive-metrics-September-24-2026/paper.pdf`. Git blob `3df7e220f480a17f408b5a1c99b0f56483a2384e`, 389,997 bytes, 18 pages; SHA-256 `af1c052828ec09138c76a64edeed05edd429e4634bf61a4fecdda9d86fd1eb9b`. Raw PDF bytes independently reproduce the exact pinned Git blob.

## Source-claim and qualification check

Pages 1–2, Theorem 1.1: on the quadric S = P^1 x P^1, choose one algebraic rank-two vector bundle G, the coordinatewise m-th power map f_m, and P = O_S(1,1). For **every positive integer m**, the bundle E_m = f_m^*G tensor P is **ample**. There exists an integer m_0 such that for **every m >= m_0**, E_m has **no smooth Hermitian metric with strictly Griffiths-positive Chern curvature**. This is not a claim about every positive m lacking a metric. The source says the threshold m_0 is ineffective.

Proposition 3.1 gives a quantitative ampleness certificate: the tautological O_{P(E_m)}(n) is very ample for every even n with n-1 >= 3m. It is distinct from asking whether the original vector bundle E_m admits strictly Griffiths-positive curvature.

Pages 3–4 describe the proof's two parts: a bundle G obtained from line bundles glued along three graphs; and a limiting plurisubharmonic **Hermitian quadratic** form whose nonzero invariant measure would be incompatible with two projective transformations. The paper distinguishes smooth strict Hermitian curvature from weaker metric conditions, determinant twists, symmetric powers, or more general Finsler norms.

**Verdict: ACCEPTED_EXPOSITION_WITH_LIMITS.** The six-section article describes the source-claimed existence family and retains the logically essential all-m versus sufficiently-large-m quantifier distinction. No independent checking of bundle local freeness, ampleness filtration, measure obstruction, complete 18-page argument, source-to-Lean semantic match, Comparator replay, or mathematical correctness has been performed.

**Claim boundary:** Primary-source editorial fidelity only; NO_CERTIFICATION. Admission requires exact article SHA-256, mathematical Markdown/compendium checks, rendered HTML, and protected merge/readback.
