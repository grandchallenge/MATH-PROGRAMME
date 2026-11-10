# OAI26 Family 052 — bounded review of both primary source statements

**Scope:** Source-to-article statement fidelity; not independent proof verification, a Lean declaration audit, or mathematical certification.

**Pinned upstream:** `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

The two source files were downloaded independently and their raw-byte Git blob hashes matched the pinned GitHub contents identities:

- `preprints/Universal-cover-splitting-for-compact-Kahler-manifolds-September-23-2026/paper.pdf`: Git blob `4869a892ebd2192cf9acb780d8263179f78255bf`, 479,820 bytes, 33 pages, SHA-256 `14d3e3f23539fd98735adb5042214f7f6eac9499a47e3303018932e00d29d333`.
- `preprints/Integrability-of-split-tangent-bundles-on-rationally-connected-manifolds-September-23-2026/main.pdf`: Git blob `e07d0c5e6ad37a020f67fca8c10c770ae00fb9fd`, 362,906 bytes, 16 pages, SHA-256 `cb23bde917710f73321f4342b88dba8135aeb84b4c553f57df7d5532de73c01d`.

## Primary-source comparison

Kähler manuscript, page 3, Theorem 1.1: for a compact **connected** Kähler manifold of complex dimension at least two, a *specified* split tangent bundle with exactly two **integrable holomorphic positive-rank subbundles** yields a compatible product of **connected simply connected complex manifolds** on the **ordinary universal cover**. The factors need not be compact. This does not assert a product of the original X or of a finite cover. Compatibility means that the lifted specified subbundles are identified by the differential with the two factor tangent bundles.

Rationally connected manuscript, page 1, Theorem 1.1: for a **smooth connected projective complex** manifold of dimension at least two where two general points are joined by a rational curve, every *specified* holomorphic splitting into two positive-rank subbundles has **both summands integrable**. Page 2, Corollary 1.2 uses **Höring's earlier product theorem** to obtain the stronger conclusion that **X itself** is a product of smooth projective manifolds, identifying the specified summands with its factor tangent bundles. The original article must not reduce this to only a universal-cover result or attribute the product implication solely to the automatic-integrability theorem.

The two manuscripts make different claims under different hypotheses. A general compact Kähler tangent splitting without integrability is not covered. An arbitrary-number-of-summands conclusion is not checked.

**Verdict: ACCEPTED_EXPOSITION_WITH_LIMITS.** Both manuscript statements and their differing product conclusions have been compared with the article. Unverified: global continuation/path rectangles in the 33-page Kähler proof; tangent-box construction, formal extension, bracket-tensor vanishing and two-point rational curves in the 16-page rationally connected proof; the cited earlier Höring theorem itself; full formal declaration/axiom mapping; proof correctness and mathematical certification.

**Claim boundary:** Source-grounded editorial fidelity only. NO_CERTIFICATION. Exact-hash article admission, mathematical Markdown, compendium tests, generated HTML and protected merge/readback are separate requirements.
