RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0879-S01
PROBLEM_ID: 879
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
For positive n, G(n) is the greatest sum of a pairwise coprime set S subset [1,n], including the legal singleton 1. Define H(n)=sum over primes p<n of p+n*pi(sqrt n). Erdős asks whether H(n)-G(n)=n^(1+o(1)) in the appropriate lower-estimate sense, specifically G(n)>H(n)-n^(1+o(1)), and whether every maximizing set for sufficiently large n must contain an integer with at least k DISTINCT prime factors for each fixed k>=2. The original 1984 paper uses STRICT a_i<n, in contrast to inclusive <=n in maintained formulation; numerical and formal versions must explicitly distinguish this endpoint convention. This is NOT Problem #878 F(n), whose allowable primes must divide n.

## Dated status and primary evidence
P. Erdős, 'On Two Unconventional Number Theoretic Functions and on Some Related Problems', Calcutta Mathematical Society jubilee volume part I (1984), printed p120, https://users.renyi.hu/~p_erdos/1984-16.pdf, poses both questions and cites joint work with van Lint. Maintained https://www.erdosproblems.com/879 (checked October 14, 2026) OPEN. Quoted established bounds H(n)-n^(3/2-o(1))<G(n)<H(n) and (H(n)-G(n))/n tends to infinity do not give requested n^(1+o(1)) error. Original text gives stronger claim only under prime distribution assumptions, not unconditionally. The k=2 question is recorded as resolved; general fixed k>=3 remains open. Frozen teorth catalogue @536408716724a2402bdfa7c1d764bf83d64a8c89 OPEN. No admitted protected formal theorem checked.

## Strongest verified interface
An exact disjoint-prime-support dynamic optimizer computes inclusive G(n) for all n<=70, independently cross-checked via direct gcd subset enumeration n<=14; optimized witnesses verify pairwise coprimality. G(30)=193, H(30)=219, witness {1,11,13,17,19,23,25,27,28,29}; G(60)=594,H(60)=680, witness {1,17,23,29,31,37,41,43,47,49,52,53,55,57,59}. At n=30, restricting all chosen elements to at most one distinct prime factor (PRIME POWERS allowed) yields only 188; thus any maximizing set there contains a member with two distinct prime factors. This finite result does NOT settle eventual k>=3 or the asymptotic G-H error.

## Proposed bounded successor task
Input n, the complete prime-support table for integers 1..n, and per-support maximal element. Target: prove that G(n)=1+maximum weight disjoint support packing, with a separate simplification for primes p>n/2, and establish exact correctness against brute gcd tests through n=14. Acceptance: complete finite proof or pinned no-sorry Lean with literal axiom output and matching n30,n60 witnesses. Falsify by a legal pairwise-coprime set exceeding the optimizer or a prime support mismatch; stop before promoting finite evidence to an infinite asymptotic theorem.

## Prerequisites and blocker
The van Lint joint analytic argument and conditional strengthened estimate not independently re-derived. Original strict inequality a_i<n differs from the present inclusive fixture; that semantic difference must be preserved when formalized. No new mathematical certification or non-author review.

## Reuse and claim boundary
Reused original 1984 Erdős text, maintained source status and previously independently replayed exact finite research fixture. No novelty or protected admission asserted.
