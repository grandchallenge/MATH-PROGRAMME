# OAI26 Family 005 — pinned source PDF and bounded editorial critique

**Evidence class:** source-fidelity audit and distinct logical editorial critic (not mathematical certification). Source `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`; PDF `preprints/Catalans-constant-is-irrational-September-24-2026/paper.pdf`, Git blob `ecbe60eb89d2d25c1d07da6232f8d9869e6c0c1d`, 574,388 bytes, 44 pages.

## Source readback

Direct PDF extraction of physical pp. 1–6 confirms: Theorem 1.1, p. 1, states that Catalan's constant `G=beta(2)` is irrational. The introduction carefully distinguishes earlier family-wise irrationality results (at least one among a set of even beta values) from the present claim about **this individual** value. The claimed new proof is a determinant/finite-prime-versus-real-place comparison, not merely faster numerical convergence.

The manuscript describes determinants `Delta_N` of size `48N`, mixed moments initially involving `1,G,zeta(2)`, and Taylor-contact cancellation removing `zeta(2)` from the entries. Under the rationality hypothesis for G it concludes rationality of determinants. Its introductory summary on p. 3 defines the same normalized logarithm and asserts: Proposition 3.4 gives `liminf L_N > -2.29084` on nonzero determinants; Proposition 4.1 supplies nonvanishing for unbounded prime N; Proposition 7.1 gives `limsup L_N <= -2.290939875 < -2.2909`. The displayed numerical bounds would be mutually incompatible **if** all the source's hypotheses, normalizations, and limiting estimates were independently established.

Physical pp. 4–6 introduce polynomial rows `P_r,D_r`, the determinant's mixed moments, and claimed coefficient cancellation. These source-level objects are reflected in the updated six-section editorial manuscript, without presenting any of them as externally established proof.

## Separate editorial critic verdict

**`ACCEPTED_EXPOSITION_WITH_PROOF_LIMITS`** for a six-section explanation of exactly what the pinned PDF claims and the broad mathematical mechanism claimed in its introduction. Editorial admission makes no finding that the proposed irrationality proof is correct. The prior draft's assertion that the paper's internal strategy had not been inspected was corrected: its p. 1–6 statement and summary were directly read.

Unresolved mathematical duties: replicate the rational finite certificates for determinant nonvanishing, evaluate denominator bounds including the prime-2 contribution, check uniform holomorphic interpolation and both real branches, and verify the potential-theory energy estimates/limit interchanges. No proof replay, formal Lean binding, Comparator verdict or MATHCERT certificate was performed. In particular no independent verification of Propositions 3.4, 4.1, or 7.1 is asserted. This is **not** a full line-by-line mathematical audit of 44 pages.

**Critic scope:** claim attribution, correct relative order of bounds, distinct role of prime subsequences and conditional contradiction, limits of GCL evidence, and plain-language exposition. The article must retain `NO_CERTIFICATION` and exact immutable PDF link. Admission can proceed only for the hash-bound article after successful Markdown, generated HTML and protected main readback. Parent #2901 remains open.
