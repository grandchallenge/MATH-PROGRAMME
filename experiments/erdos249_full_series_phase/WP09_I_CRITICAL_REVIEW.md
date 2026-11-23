# WP09-I — role-scoped mathematical review and hostile audit

**Exact source:** Will Cook, *The Binary Totient Series*, Git revision 3368d1e69467aec111eb3244843ad3542171ff96 and Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac. Previous admitted actual-totient two-prime result: WP09-G PR #3631, protected merge 95fdf1224077e6935cbbb00c6427149b8ea4d60b. Distinct predecessor WP09-H six-unit shadow: PR #3648.  
**Files:** TWO_UNIT_PARITY_SHADOW_009I.md, two_unit_parity_shadow.py, and tests/test_erdos249_full_series_phase.py.  
**Authority and status:** separate same-agent Axiomatist, Verifier, Adversary and Referee logical passes. NOT independently authenticated human mathematical refereeing, not Lean kernel proof, not theorem-priority adjudication, not MATHCERT.

## Axiomatist: what is actually proved

For each fixed K>=6, a real tail defined by the **positive** actual Euler-totient values beyond index 3K is expanded into canonical base-two digits. Subtracting twice those digits from actual phi after index K creates an integer coefficient sequence within distance **two** at every n, with exact even parity for n>=3, and 0<=a(n)<=n. Its full binary series equals the **explicit finite dyadic rational** gamma_K=sum_(n<=3K)phi(n)/2^n. There is no assumption or claim that the original real sum alpha is irrational.

All sufficiently late source-legal complete Cook phases for this distinct sequence, for **every h**, are within 1/16 of integers and have real part >0.9. The actual WP09-G two-prime imaginary cocycle U is stable within 4*pi*X/Q under these bounded coefficient changes; the rational shadow therefore has an order-X imaginary U contrast. Short k-step complex cocycles remain close for 2^k=o(Q) under externally fixed weights only.

The parity-preserving constant two is optimal for any nonzero difference at an index n>=3: both original and shadow coefficients are even. Unlike WP09-H's six-unit shadow, this construction does **not** claim to leave all odd-prime coefficients or all odd indices unchanged.

## Verifier: independent mathematical reconstruction

1. The exact dyadic rational gamma_K is a finite sum with denominator dividing 2^(3K). The difference alpha-gamma_K is the positive actual totient tail, bounded by (3K+2)/2^(3K).
2. Dividing by B_K=2^(1-K) yields x in (0,1) since (3K+2)/2^(2K+1)<1 for K>=6. Its floor digits b_j=floor(2^j x)-2 floor(2^(j-1)x) lie in {0,1} and telescope without a noncanonical boundary choice.
3. For n>=K+1>=7, phi(n) is a positive even integer of size >=2. Subtracting zero or two preserves nonnegativity, integrality, parity and the n envelope. The all-index error is exactly either zero or -2.
4. Summing the adjustment gives 2^(1-K) sum_j b_j 2^(-j)=B_K*x=alpha-gamma_K. Hence the *entire infinite* series is gamma_K, not just a finite truncation. Since gamma_K has dyadic denominator, every shifted infinite tail at N>=3K is an integer after multiplying by 2^N.
5. The universal omitted Cook tail has size <=(N+h+L+2)/Q<1/16 at every source-admissible block. Thus the original full-length *shadow* Cook phases have real part >cos(pi/8)>9/10 for all h, N and legal L at X>=3K. No floating diagnostic is needed to prove the cofinal claim.
6. Eta(n) in {-2,0} gives shifted source differences differing by <=2, not <=4. Every full one-step Cook cocycle differs in complex value by <=4*pi/Q. The two WP09-G residue source sets together have <=X indices, so their imaginary U contrast changes by <=4*pi X/Q.
7. Protected actual-phi WP09-G U>=pi X^2/(64Q) leads to U_shadow>=pi X(X-256)/(64Q)>=pi X^2/(128Q) for X>=512. At legal least+1 Cook depth Q<256X, so U_shadow>=pi X/32768 cofinally, *while* the shadow real complete-phase mean remains >0.9.
8. Iterating the exact full Cook recurrence for k steps weights shifted source deltas by 2^(k-1-i), whose sum is 2^k-1. The sine/chord difference bound gives <=4*pi(2^k-1)/Q per cocycle, and <=that times the count for fixed external bounded weights. Uniform normalized differences tend to zero if 2^k=o(X) at Q~X.
9. Exact bounded-error multiplicative rigidity, proved in WP09-H, applies also at B=2. For any index with eta(n)=-2, the explicit coprime product defect at prime p not dividing n has magnitude >=2(p-1)-2(n+1), eventually positive and growing with p. A purported rational comparator identical to true phi in all normalized local prime tests need not satisfy global coprime multiplicativity.

## Adversary: scope and failure modes

- **Denominator:** gamma_K is an explicit **DYADIC** rational, not merely a generic quotient with odd denominator. This is essential to integer shifted tails at all late N for all h.
- **Parity:** phi(1)=1 and phi(2)=1 are exceptions to the even-totient statement. This construction leaves n<=K untouched and only asserts parity preservation for n>=3.
- **Different exact-source constraints:** WP09-H preserves all odd coefficients, including all odd primes, but uses a six-unit maximum gap. WP09-I preserves parity with the best two-unit max gap, but it can alter odd-prime coefficients. The two theorems have different strengths; no claim combines both to say all odd primes unchanged at two-unit gap.
- **No reliance on unknown alpha status:** the floor digits are exact definitions using a positive convergent tail. The finite producer certifies digits using an exact interval for alpha's tail; unresolved binary boundaries fail closed. The mathematical existence proof does not need termination of a binary digit-decider at exceptional rational endpoints.
- **Cofinal phase transfer:** the near-integer phase bound applies to the **shadow**, not to the actual Euler totient. A bounded O(2) change per coefficient is *not* small at original phase scale because binary carries can amplify it.
- **Bounded weighted phase class only:** the stability theorem compares externally specified bounded weights and specified k-step cocycles, not weights themselves depending on phi, a, Cook's z_N or cofactor m_N. The source-locked prime/cofactor estimate remains OPEN.
- **Phase signature versus original real 10%:** a strong imaginary contrast of two *cocycle* sums does not yield a real original-phase sum <=0.9X. The explicit rational shadow disproves any such inference from that observable alone.
- **Arithmetic rigidity not irrationality:** exact multiplicativity detects the shadow but does not automatically transform into quantitative near-integer frequency avoidance for true phi. The required high-frequency, coprime-product-to-phase bridge remains the open research problem.
- **Finite tests are not certification:** exact integer arithmetic tests confirm finite digit prefixes, dyadic tail enclosures, centered phase representative inequalities, k-step coefficient bounds and explicit multiplicative defects. They do not prove new asymptotic phi cancellation.

## Referee: bounded admission and required next result

The theorems are self-contained and eligible for bounded research admission only after exact candidate-head replay, source-math Markdown validation, the native protected GitHub merge queue, exact merge-group required checks, four-file Git blob identity readback, and durable issue #3500 receipt. One reviewer system can staff distinct logical passes but may not pretend independent human review or provide MATHCERT.

**Next decisive substantive proof obligation:** a genuine multiplicativity-sensitive two-adic carry-escape result for the actual Euler totient at scale L~log X, or Cook's unresolved 14X/25 weighted prime/cofactor cancellation. Both WP09-H and the sharper WP09-I establish quantitatively why bounded fixed-prime/short-time source signatures are insufficient. Preserve Erdős #249 OPEN and issue #3500 OPEN/In Progress until the source-locked actual-phi criterion is proved.
