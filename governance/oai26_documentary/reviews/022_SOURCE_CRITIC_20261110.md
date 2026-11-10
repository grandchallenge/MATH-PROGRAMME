# OAI-26 Family 022 — primary-source editorial critic

**Scope:** Original-paper statement fidelity, not a proof or certification.

Pinned upstream: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

Primary PDF: `preprints/The-weak-inhomogeneous-Duffin-Schaeffer-conjecture-September-25-2026/paper.pdf`; Git blob `45c7854d5bb55c1b201bad41c0346d646287b579`, 837,552 bytes, 87 pages; SHA-256 `d91ccb7b68c5b0e2e081710c3c9012d0d790992703fc3609853953c538bc7203`. The GitHub identity was independently compared with the downloaded raw file's Git blob hash.

## Exact claim readback

Page 3, Theorem 1.1: for every **fixed real shift** gamma and every **finite-valued nonnegative** psi on the positive integers, divergence of the series sum(phi(q)psi(q)/q) implies ||qx-gamma|| < psi(q) for infinitely many positive q for **Lebesgue-almost every real x**. The integer numerator is unrestricted, and the theorem imposes no monotonicity or Diophantine condition. Its exceptional null set may depend on gamma and psi. The assertion is a sufficient divergence implication, not a convergence converse.

Page 3, Corollary 1.2: separate Hausdorff-measure divergence statement under explicit restrictions on a dimension function f. Pages 3–5 distinguish the weak unrestricted-numerator theorem from the stronger coprime-numerator variant; the introduction reports counterexamples to that stronger variant.

Edge cases: psi identically zero does not satisfy divergence; large error windows are addressed separately by the small-width reduction in Section 2. The revised six-section exposition preserves the theorem's quantifiers, target, and claim limits.

**Editorial decision: ACCEPTED_EXPOSITION_WITH_LIMITS.** Source-statement fidelity was checked. The 87-page proof itself, overlap estimates, finite-block second-moment argument, partition induction, Hausdorff transference, formal Lean mapping, comparator runs, and independent mathematical validity were **not** verified.

**Claim boundary:** Original-source editorial exposition only. NO_CERTIFICATION. Admission requires an exact article hash, checked generated HTML, affected tests, and protected merge/readback.
