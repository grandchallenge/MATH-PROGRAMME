# Erdős #249 WP07-D — source-critical logical adversarial review

**Role:** distinct non-authoring logical Adversary/Referee pass by the *same* authenticated GCL agent, not independently credentialed or a MATHCERT mathematical certification.  
**Workstream:** [#3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500) OPEN; original full Erdős #249 OPEN.  
**Exact manuscript SHA-256:** 19aa6355ea93e7fa60307079fb6c0856324528c4990f8c5c8705b2c7af4737d2.  
**Exact module SHA-256:** 8e12dd5480d13046530b392635b7a7161848fa414b13498874ed776341aff305.  
**Exact registered suite SHA-256:** 30b8263cf8b8858c4dcca37ba84d07b27e610e452faa0e3e23f98c2ef146923d.  
**Affected head of source replay:** c14182d9baec9fcaa55ff43d5f3e25bc30c1ffd9; 27/27 whole full-series suite PASS; manuscript math source gate PASS.

## 1. Check the quantitative factor-budget count

For a near-maximal witness, oddpart(phi(n)) is less than B=2^(C+1). Multiplicativity of phi(n) makes the **product** of d_p=oddpart(p-1) over all distinct odd p|n divide the same oddpart(phi(n)). Thus there can be at most K_B=max{k:3^k<B} prime factors with d_p>=3. This count is for distinct primes, not their exponents, and the small-prime exponents are handled separately.

For d_p=1, a prime p=2^r+1 forces r to be a power of two by the elementary factorization of x^m+1 when m is odd. The number of *candidate* r's at most R=floor(log2X) is at most 1+floor(log2R); subsets are bounded by 2^(1+floor(log2R))<=2R. This does **not** assume there are infinitely many Fermat primes.

For d_p>=3 and p>B, the distinct factor p is determined by a pair (odd d_p<B, integer r<=R). There are fewer than BR pairs. Repeated p>B are excluded by the p^(a-1) contribution to the odd totient part. Enumerating at most K_B such factors by sum_j<=K_B binom(BR,j), with independent small odd prime-power patterns D_B and the possible 2-exponent a=0..R, yields the stated rigorous upper bound. Overlapping candidate inventories only **overcount**, which is safe. The conclusion O_C((log X)^(K_B+2)) is valid with fixed C.

## 2. Is the growing-deficit statement uniform?

The right side is explicit for B varying with X, not only a hidden-C asymptotic. If B<=R^(1-delta), then log D_B<=B log(2+log_3 B)=o(R), and the remaining binomial contribution has log size O((log R)^2)=o(R). Therefore the count is exp(o(R)) uniformly in the stated range. This does not extend unchanged to C comparable with log2 R or larger; no such assertion is made.

## 3. Does the C=0 classification duplicate a known theorem?

Yes. Zhao (2025), *p-Adic Valuation of Euler's Totient Function*, explicitly reports the equality characterization by squarefree products of distinct Fermat primes. The packet gives an elementary self-contained proof using the finite product identity, but **claims no novelty or priority**. Independent exact tests match the 17 known qualifying integers through 100000, and check the factorization predicate on each integer in that range. No unproved Fermat-prime infinitude hypothesis was used.

## 4. Does this establish the needed fractional-part separation?

No. The WP07-C sliding-window recurrence gives only rarity of **adjacent integral whole finite sums**; replacing the sparse nearmax count by a polylogarithmic one does not establish a lower bound on the distance of **nonintegral** finite sums from integers. The rational full series with coefficients floor(n/2) has even *fewer* integral finite windows, so the generic implication is false. WP07-D also records the elementary depth firewall: if L<=floorlog2X, the proposed sufficient separation min(r,2^L-r)>q(N+L+2) is impossible because its left side is at most 2^(L-1)<=X/2 while q(N+L+2)>X. A positive result requires new totient-specific correlation at a deeper length or a fundamentally different analytic-tail argument.

## 5. Correct scope of numerical evidence

The exact tests cover independent totient sieves/factorization, the Fermat integer product identity, the C=0 classified witnesses through 100000, the explicit upper-bound oracle for several fixed C, the prior WP07-C adjacent-sum regression, and the rational full-series control. These tests are **not** a finite proof of an asymptotic or independent mathematical certification. The restricted exact evaluator caps C at 10 solely to avoid excessive memory usage; the manuscript theorem has no such restriction.

**Disposition:** ACCEPT_WITH_SCOPE for the elementary polylogarithmic upper bound, the explicit growing-deficit consequence, the non-novel equality proof and the strengthened adjacent-integrality estimate. Original Erdős #249, the positive cofinal residue-distance producer, MATHCERT and external priority remain OPEN/NOT_SUBMITTED.
