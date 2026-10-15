RESULT/1
ASSIGNMENT_ID: ERDOS-CATALOGUE-0893-S01
PROBLEM_ID: 893
DISPOSITION: BOUNDED_TASK_DESIGNED
CONTEXT_CLASS: ZERO_CONTEXT
TIMEBOX_OBSERVED: NO

## Exact statement and normalization
tau(m)=number of POSITIVE divisors m, including tau(1)=1. For f(n)=sum_{k=1}^n tau(2^k−1), Erdős asks whether f(2n)/f(n) tends to a limit as n->infinity; distinguish a finite REAL limit versus +infinity (extended real). Ratio finite real limit definitively ruled out by an unconditional limsup-infinity theorem; whether the entire sequence tends to +infinity remains OPEN. Individual tau(2^n−1) can fluctuate; no monotonicity of individual terms is assumed.

## Dated status and primary evidence
Erdős 'Some of my new and almost new problems and results in combinatorial number theory', Eger 1996, published 1998 pp169–180, DOI 10.1515/9783110809794.169, original p180 question (full chapter not independently checked page-image). Maintained https://www.erdosproblems.com/893 OPEN (Oct 2026); frozen teorth/erdosproblems@536408716724a2402bdfa7c1d764bf83d64a8c89 earlier OPEN. Vjekoslav Kovač and Florian Luca, 'On the number of divisors of Mersenne numbers', arXiv:2506.04883v4, posted Feb3 2026, primary complete machine-readable article https://arxiv.org/html/2506.04883v4, Theorem 1 UNCONDITIONALLY proves limsup_{n→inf} f(2n)/f(n)=+infinity. Proposition 2 proves a related ratio for f'(n)=sum_{k<=n}2^{tau(k)}, NOT an unconditional divergence theorem for original f. Their Theorem3 proves f(2n)/f(n)->infinity only ASSUMING either a divisor count conjecture for 2^N+1 at record Mersenne indices N, or a cyclotomic-factor omega(Phi_d(2)) logarithmic bound. No independent GCL reproof of their deep asymptotic argument.

## Strongest verified interface
Elementary identity for every k>=1: gcd(2^k−1,2^k+1)=1 because both odd and difference 2, so tau(2^(2k)−1)=tau(2^k−1)*tau(2^k+1). Since tau(2^k+1)>=2, splitting f(2n) into even and odd k shows STRICT universal inequality f(2n)>2f(n) for all n>=1; this is NOT full divergence. CHAD exact finite_892_893.py/json factors all 2^k−1 for k<=64 with SymPy factorint, validates each factor product and primality (all primes <2^64), separate trial division cross-check k<=24, checks tau(2^(2k)−1)=tau(2^k−1)*tau(2^k+1) for k<=32 and exact f ratio samples n<=32. Observed f(64)/f(32) approximately 15.134, finite observation only.

## Proposed bounded successor task
Input n,k positive, divisor count tau, coprime multiplicative lemma, exact factorization receipt. Prove gcd identity and dyadic tau identity for all k, and prove f(2n)>2f(n) for all n, via complete paper proof or pinned no-placeholder Lean compile+literal axiom output, exact finite regression exponent<=64 and independent trial division <=24. Falsify by shared odd prime factor of 2^k−1 and 2^k+1, tau product mismatch, or f(2n)<=2f(n). STOP before inferring full divergence: choose ONE Kovač–Luca conditional hypothesis and produce a separate independent theorem if claiming stronger result.

## Prerequisites and blocker
Original 1998 full page source not independently visually rechecked. Kovač–Luca Theorem1 deep analytic proof NOT independently reconstructed or Lean kernel replayed. Their Theorem3 assumptions not GCL-proved; public formal statement does not establish solved conjecture. No new asymptotic theorem.

## Reuse and claim boundary
Reused primary Feb2026 arXiv v4 theorem and maintained catalogue, elementary coprime arithmetic, exact CHAD finite factorizations. No novel priority, full published proof certification, protected editorial admission, PR merge or live public MathJax verified.
