RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0459-S01
PROBLEM_ID: 459
DISPOSITION: SOURCE_LOCK_READY
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For integers u>=2, let f(u) be the largest integer v such that no integer m with u<m<v has all prime factors dividing uv. Equivalently, f(u) is the smallest v>u whose prime factors all divide u. The original 1980 question is open-ended: "Estimate f(u)." SOLVED is an editorial classification of substantial bounds and typical behavior, not a unique complete asymptotic for every u.

## Dated status and primary evidence
Primary statement visually checked 2026-10-13: P. Erdős and R. L. Graham, Old and New Problems and Results in Combinatorial Number Theory (1980), printed p.91, https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf, SHA256 0cbf0c32f0ab1e1c71db5121a88bac905bf976c4a6ab6bb6d7d9cf9ddd184ed3. Maintained #459 tracker (indexed read 2026-10-13; direct HTTP 403) reports SOLVED (LEAN), observations attributed to Stijn Cambie, and a 2026-03-11 update in pinned catalogue. Cambie's density-one proof sketch appears in the public #459 discussion.
External Lean file: https://github.com/Woett/Lean-files/blob/main/ErdosProblem459.lean (blob badf8b38dbcad590e2228f3c41a9ab7d523557b5, 725 lines). It includes f_bounds, f_prime, two infinite-extreme families, and main_theorem (density one) at line 672. No active proof holes were found in the text. Declared Lean 4.24.0 and mathlib f897ebcf72cd16f89ab4577d0c826cd14afaafc7. NOT GCL-compiled.
Pinned Google DeepMind formal provider at commit 85f863718beeec7b58a3a1926ee92e3472bc2020, FormalConjectures/ErdosProblems/459.lean, blob 3a9d2a22e098be253c452b4df46bc4ce0023df4d, has placeholder declarations for bounds and prime equality, and no density-one theorem. Issue says formal-statement metadata YES; maintained tracker indexed page says NO. This metadata drift is not a proof-status determination.

## Strongest verified interface
For every u>=2, u+2<=f(u)<=u^2. The lower bound follows because u+1 is coprime to u, so cannot be u-smooth; the upper bound follows because u^2 is u-smooth. If u=p is prime, the next p-smooth integer after p is p^2, giving equality at the upper bound for infinitely many primes. If u=2^k-2 (k>=2), u is even and 2^k=u+2 is u-smooth, giving equality at the lower bound for infinitely many k. Finite exact checks: f(2)=4, f(3)=9, f(6)=8, f(14)=16, f(30)=32, f(31)=961, f(62)=64, f(126)=128. No single pointwise growth rate is possible.
Cambie's stronger typical-value statement is: for every epsilon,delta>0, sufficiently large x have at least (1-delta)x integers n<=x with f(n)<(1+epsilon)n. Outline checked: choose M such that density of integers with at least two distinct prime divisors <=M exceeds 1-delta/2 (the divergence of sum_p 1/p and CRT independence suffice). For any fixed distinct p,q<=M, log p/log q is irrational, so the semigroup {p^a q^b:a,b>=0} meets every interval (t,(1+epsilon)t) for all sufficiently large t. Taking the maximum threshold over finitely many pairs, any sufficiently large n divisible by two such primes has a smooth successor below (1+epsilon)n. This proves the stated density-one result, not a pointwise asymptotic. External Lean source includes a formalization; its compilation remains unverified by GCL.

## Proposed bounded successor task
EC004-0459-DENSITY-REPLAY. Inputs: 1980 printed p.91, Cambie's 2026 discussion proof, exact external Lean blob badf8b38dbcad590e2228f3c41a9ab7d523557b5. Target: independently verify the quantified density-one theorem and its finite-prime covering lemma. Method: check the CRT density estimate and irrational-rotation finite-net argument on paper, then compile external Lean in isolated Lean 4.24.0/mathlib f897ebcf72cd16f89ab4577d0c826cd14afaafc7; capture #print axioms, source hash and replay logs. Accept if all hypotheses match, build succeeds without holes/unexpected axioms, and deterministic replay agrees. Falsify on missing uniform threshold, invalid density quantifiers, or compile failure. Stop after one proof audit and one replay, or record exact dependency blocker.

## Prerequisites and blocker
SOURCE_LOCK_READY for documentary exposition of the original open-ended question, exact extrema, and typical-density estimate. Explicit exceptions: editorial SOLVED is not a complete pointwise estimate, formal metadata drifts, and external Lean has not been locally compiled. Direct live tracker read is blocked (HTTP 403). Do not claim MathCert.

## Reuse and claim boundary
Reused the pinned catalogue and primary 1980 page, Cambie's public comment, the pinned provider and external Lean source. Independently reconstructed the elementary extrema, the density-one argument, and finite examples. No sibling issue returns, new solution, issue-comment posting, protected merge, or independent formal certification claimed. This file remains UNPOSTED until authenticated issue-comment readback.
