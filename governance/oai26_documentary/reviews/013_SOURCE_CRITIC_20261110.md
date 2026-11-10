# OAI26 Family 013 — primary-source statement critic for Ostmann's inverse Goldbach conjecture

**Scope:** Editorial source-to-statement correspondence. NOT independent proof verification, Lean certification, or a proof of the conjecture.

Pinned source: `openai/math@1581d4cbdd69a0faf34b2089614fe2a814316a6a`.

Original PDF: `preprints/the-additive-indecomposability-of-the-primes-September-24-2026/paper.pdf`, 764,239 bytes, 80 pages, Git blob `e9a0bb4bdbf86c71a968416d19c5c20d739d504f`, SHA-256 `2c4ec07457be59763b37d2197852341a7e6615e419982f9f3705c5f3a94c2c3f`. Independently retrieved bytes match the pinned Git blob.

## Main statement and distinction

Page 1, Theorem 1.1 (Ostmann's conjecture): if A and B are subsets of the nonnegative integers, with **at least two elements each**, then the symmetric difference between A+B and P (the set of positive primes) is **infinite**. Thus no set obtained by adding or removing finitely many primes or other nonnegative integers can equal a nontrivial binary sumset. The statement is not merely that the primes themselves cannot be such a sum, nor that they have a density-incompatible representation.

The theorem does NOT assume both summand sets infinite. Page 4, Lemma 2.2 rules out a hypothetical finite summand by a fixed-shift large-sieve argument and prime coverage. Page 5, Theorem 2.3 addresses **two infinite summands**. These two separate results imply Theorem 1.1.

The supposed eventual equality means BOTH that every sufficiently large prime belongs to A+B and that every sufficiently large element of A+B is prime. Only proving one implication, or a generic density bound, is inadequate. Pages 2–3 outline the dependency chain: residue supports, quadratic and higher translated-character decorrelation, additive-transform mass, a finite-field tree comparison, positive-statistic transfers, and final arithmetic contradiction. The authors state they do not prove a general inverse-sieve classification.

**Verdict: ACCEPTED_EXPOSITION_WITH_LIMITS.** The six-section article correctly conveys the original Theorem 1.1 and now explicitly distinguishes the two-infinite-set reduction and the eventual-coverage/exclusion requirements. This critic checked the source's theorem and proof outline; it has NOT checked the 80-page proof, sieve and analytic estimates, citations, logical correctness, formal declarations, Comparator replay, or independent mathematical certification.

**Claim boundary:** Primary-source editorial fidelity only; NO_CERTIFICATION. Exact article hash, mathematical Markdown and compendium tests, rendered HTML, and protected merge/readback are required before an editorial acceptance claim.
