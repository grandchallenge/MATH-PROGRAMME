RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0453-S01
PROBLEM_ID: 453
DISPOSITION: SOURCE_LOCK_READY
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization

Let $p_n$ denote the $n$‑th prime, $p_1=2$. Erdős and Straus asked whether there exists $N$ such that for every integer $n\ge N$ there is an integer $1\le i<n$ with $p_n^2<p_{n-i}p_{n+i}$. Pomerance proved the stronger negation: infinitely many $n$ satisfy $p_n^2>p_{n-i}p_{n+i}$ simultaneously for every $1\le i<n$. The strict inequality and the order of quantifiers are essential. An infinite set of such $n$ refutes the eventual-for-all claim.

## Dated status and primary evidence

The original Erdős–Graham volume (1980), printed p. 90, explicitly reports Pomerance's disproof and distinguishes a separate density-zero question: https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf#page=86 . The primary proof is C. Pomerance, *The Prime Number Graph*, Mathematics of Computation 33 (1979), 399–408, DOI 10.1090/S0025-5718-1979-0514836-7. Its p. 399 equation (1.1) states the result; p. 400 Theorem 2.2 and corollary prove it: https://math.dartmouth.edu/~carlp/PDF/paper19.pdf#page=2 . These printed pages were visually inspected. Pinned catalogue: teorth/erdosproblems commit 536408716724a2402bdfa7c1d764bf83d64a8c89, data/problems.yaml blob 4e60263a80af6207aca494d2e1388e44fa372889, DISPROVED, last updated 2026-01-31. Maintained https://www.erdosproblems.com/453 reports DISPROVED (LEAN), edited 2026-04-08. That badge does not constitute GCL formal replay.

## Strongest verified interface

Pomerance Theorem 2.2 (printed p. 400): if $0<a_1<a_2<\cdots$ and $a_n/n\to0$, infinitely many indices $n$ satisfy $2a_n>a_{n-i}+a_{n+i}$ for every integer $1\le i<n$. The paper proves this using infinitely many strict vertices of the concave convex-hull boundary. Set $a_n=\log p_n$. The Chebyshev bound $p_n=O(n\log n)$ implies $\log p_n/n\to0$; exponentiation gives the strict product inequality. Exact finite checks: at $n=3$, $p_n=5$ and $25>3\cdot7=21$, $25>2\cdot11=22$. At $n=5$, $p_n=11$ and $121$ exceeds $91,85,57,46$ for $i=1,2,3,4$. At $n=2$, by contrast, $9<2\cdot5=10$. Finite cases verify indexing and signs, not infinitude.

## Proposed bounded successor task

EC004-0453-LEAN-SEMANTIC-REPLAY. Input: exact pinned provider blob and a fixed Lean/mathlib toolchain. Target: prove the generic strict midpoint-maxima theorem for positive strictly increasing sequences with $a_n/n\to0$, then deduce the negation of the eventual prime-witness proposition. Acceptance: type-checked Lean proof without `sorry` or added axioms; exact toolchain and source hashes; explicit one-based/zero-based prime-index comparison; a negative fixture where the reversed strict inequality fails at $n=3$. Stop after one bounded replay and a separate statement audit. If the strict convex-hull lemma is missing, report that exact blocker instead of claiming certification.

## Prerequisites and blocker

No primary-source or documentary-status blocker. Protected formal provider: google-deepmind/formal-conjectures@85f863718beeec7b58a3a1926ee92e3472bc2020, `FormalConjectures/ErdosProblems/453.lean`, blob `a4313b258228fddfae8e925cd88783ce4a906d7d`. Its theorem `answer(False) ↔ EventuallyHasPrimeWitness` still has `sorry` in the pinned revision. `Nat.nth Nat.Prime` is zero-indexed; syntactic $i=0$ cannot satisfy the strict inequality, so the witness domain matches after index translation. Formal certification is blocked until independent local replay of the external proof. The separate density-zero conjecture in the original 1980 discussion is NOT settled by Pomerance's infinitude result.

## Reuse and claim boundary

Reused evidence: Erdős–Graham printed p. 90, Pomerance's author-hosted printed pp. 399–400, pinned catalogue and Lean file, and the maintained status page. Independently checked: source quantifiers, theorem hypotheses, exponentiation, small integer examples, and formal witness indexing. The 1979 convex-hull theorem is cited, not independently re-proved. No independent-account review, external worker, Lean execution, novelty claim, protected editorial admission, or mathematical certification is asserted.
