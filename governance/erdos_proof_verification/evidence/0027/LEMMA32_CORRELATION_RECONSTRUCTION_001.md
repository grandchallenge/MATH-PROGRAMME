# Erdős 27 — Lemma 3.2 finite correlation reduction and analytic dependency ledger

Supplementary research under ERDOS-PV-0027-B, whose original unique RESULT/1 (#3225 comment 7148323057) and evidence PR #3720 remain unchanged. This is not a second typed return, a new task lease, or an admission change. FFKPY manuscript, 21 Dec 2006, DOI 10.1090/S0894-0347-06-00549-2, printed pp.6,10–12, Lemmas 2.1, 3.1 and 3.2; primary source https://ford126.web.illinois.edu/wwwpapers/coverings.pdf, visually reread in this session. Reuse earlier acquired-source SHA256 aabca6f856644c89826e9f9c8c46f03a92c9f3e46c41ee443b4d6670463014e9; no new byte acquisition claimed. The target is the exact finite correlation reduction followed by a reconstruction conditional on explicitly named classical analytic estimates.

## Finite result

Let C be a finite set of pairs (n_i,r_i), with positive integral moduli. Factor n_i=a_i b_i by the prime cutoff Q>=2, where a_i is Q-smooth and b_i has no prime factor <=Q. Set M=lcm_i a_i, with empty LCM 1. For each h mod M let C_h be the set of pairs (b_i,r_i) with h=r_i mod a_i. Write beta(D) for the sum of 1/(uv) over unordered distinct pairs of entries of D whose moduli u,v share a prime factor. Then

mean_h beta(C_h) <= sum_{i<j, gcd(b_i,b_j)>1} [gcd(a_i,a_j) | r_i-r_j] / (lcm(a_i,a_j) b_i b_j).

For each h, choose one preimage index for each distinct projected pair in C_h, e.g. the least index. This gives an injection from unordered pairs of distinct projected entries to unordered pairs of active original indices, preserving the rough moduli and weights. Extra original-index pairs have nonnegative weight. Sum this inequality over h and exchange finite sums. By the generalized CRT, simultaneous membership in two smooth congruences occurs in zero fibres if the residues disagree modulo gcd(a_i,a_j); otherwise the solutions form one residue class modulo lcm(a_i,a_j), which divides M, so occur in exactly M/lcm(a_i,a_j) fibres. Dividing by M gives the claim. The same argument works if projected pairs are normalized modulo b_i, since this may only cause further collisions. Equality holds when every active projection is injective; that is sufficient, not necessary.

Dropping the compatibility indicator gives a weaker universal upper bound. It is important not to assert equality after deduplicating the projected system.

## Conditional analytic continuation

Assume N>0, K>1, each original n_i lies in (N,KN], multiplicity at most s. Group original indices by smooth part a|M and rough part b. Let S_a be the set of distinct rough parts for smooth part a. For each fixed (a,b) there are at most s residues. Enlarge the unordered distinct pair sum to an ordered sum including diagonal pairs (all weights nonnegative), and drop compatibility. Then

mean beta <= s^2 sum_{a,c|M} 1/lcm(a,c) *
             sum_{b in S_a,d in S_c,gcd(b,d)>1} 1/(bd).

Every contributing pair has at least one common prime p>Q. Its contribution is bounded by the sum over such primes, and the two sums factor for each p. Enlarge S_a to all Q-rough integers in (N/a,KN/a]. This enlargement is an INEQUALITY in general; the displayed source equality after enlargement must be read as an upper bound. Example: C={(6,0),(10,0)}, Q=2, N=2, K=10 has S_2={3,5}, strictly smaller than the allowed interval. No adverse effect on the conclusion.

Analytic inputs, with absolute implied constants:

(H1) F_Q(x)=# {positive t<=x with no prime factor <=Q} <= C1(x/log Q+1) for x>=1, Q>=2. This is the standard upper-bound sieve estimate used in FFKPY, citing Halberstam–Richert, Sieve Methods (1974), Theorem 3.3. Exact original cited theorem and proof are not independently replayed here.

(H2) pi(x)<=C2 x/log x for x>=2 (e.g. Chebyshev). Dyadic intervals p in (2^j Q,2^(j+1)Q] give sum_{p>Q} p^-2 <= 2C2/(Q log Q) sum_{j>=0}2^-j = 4C2/(Q log Q). No full prime number theorem is needed for this step.

(H3) Mertens product upper bound product_{p<=Q}(1-1/p)^-1 <= C3 log Q. A classical cited input, not independently rederived.

For p>Q, writing b=pt preserves roughness. With A=N/(ap)>0, the reciprocal sum over relevant b is at most 1/p times the rough reciprocal sum over A<t<=KA. By partial summation, if A>=1, the latter is bounded by F_Q(KA)/(KA)+integral_A^{KA} F_Q(t)/t^2 dt <= C1((1+log K)/log Q+2). If A<1 and KA>=1, separate t=1 then apply the A=1 case on (1,KA] with log(KA)<=log K; if KA<1 the sum is zero. Thus uniformly it is O(log(QK)/log Q). This handles endpoints below one explicitly. Consequently the sum over common rough primes is O(log^2(QK)/(Q log^3 Q)) by (H2).

Finally the divisor kernel has the exact identity

D(M)=sum_{a,c|M}1/lcm(a,c)
    = product_{p^e || M} sum_{j=0}^e (2j+1)/p^j.

Proof: valuations at each prime vary independently, and exactly (j+1)^2-j^2=2j+1 ordered pairs of exponents have maximum j. Equivalently, the number of divisor pairs with lcm u is tau(u^2). Since all primes dividing M are <=Q, extend each geometric series to infinity and use (1+x)/(1-x)^2=(1-x^2)/(1-x)^3 <=(1-x)^-3, then (H3). This gives D(M)=O(log^3 Q), uniformly in M and its prime powers.

Combining the estimates yields the published mean beta(C_h)=O(s^2 log^2(QK)/Q). The proof is a reconstruction of the source argument and explicitly conditional on H1–H3. No novel asymptotic theorem, complete independent analytic proof, Lean replay or certification is claimed. The finite bound and Euler identity are unconditional.

## Separate critical pass and tests

The critical pass is role-separated, not externally independent. The finite bound uses ordinary pairs, NOT independent rough events; the shared-prime sum may count a pair several times, so is an upper bound. Retaining compatibility uses the smooth CRT even when the rough gcd is nontrivial. Dropping the multiplicity cap invalidates the stated uniform s-bound. Projected residue collisions must be deduplicated before computing beta, and the enlargement from S_a to the full rough interval is not exact.

Hostile examples (Q=2):
- C={(3,0),(6,0)}: active projection collisions yield actual mean 0, compatibility bound 1/18.
- C={(6,0),(6,1)}: incompatible smooth residues yield mean and compatibility bound 0, unconditional coarse bound 1/18.
- C={(6,0),(9,0)}: injection and compatibility yield exact mean 1/54.

The standard-library checker check_correlation_fibres.py enumerates all distinct pairs from moduli 1..6, families of size 0..3, four cutoffs, plus 200 deterministic mixed/negative residue families. It compares direct per-fibre beta with both pair sums and separately compares direct divisor-pair summation with the Euler factorization. 6,448 exact cases passed, including 61 strict projection losses and 185 strict compatibility losses, digest 1a96eb9560f0f206b921e4eebbfe3d5bc5c91f8fb7a4bd0893df06380042a0af, CHAD capture 5e58c7075fe44730add6fe97c831cc49. Finite checks validate edge cases; the proof establishes the general identities and bound.

## Next obligation

Reconstruct H1 from a pinned upper-bound sieve proof (or supply a self-contained alternative), and independently source/verify H2–H3. Then combine with Lemma 3.3 (geometric mean over fibres without modulus-one projections) and Lemma 4.1 (smooth-number reciprocal tail). Phase C remains a separate formalization obligation after the protected Phase B custody transaction.
