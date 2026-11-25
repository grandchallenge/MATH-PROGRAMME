# WP09-O — exact multiplicative rational comparisons and denominator escape

Final bounded structural tranche authorized after WP09-N (PR #3730). Original Erdős #249 open; no MATHCERT. Source context: Will Cook, The Binary Totient Series, revision 3368d1e69467aec111eb3244843ad3542171ff96, blob 547ed9ed83500181a2e55047ce5df569b7cb49ac. No priority claim for finite Euler products or classical cyclotomic identities. This is an obstruction analysis, not an irrationality proof.

## 1. Dense prime truncations

Let y≥2 be an integer, P the primes at most y, M their product, and

$$
f_y(n)=n\prod_{p\mid n,\ p\in P}(1-1/p).
$$

This is positive integral, exactly coprime multiplicative, phi(n)≤f_y(n)≤n, equal to phi on all P-smooth n and in particular n≤y. For EVERY prime p and k≥1, f_y(p^{k+1})=p f_y(p^k); f_y(p)=p-1 in P and p otherwise. Thus all prime-step laws of phi at primes in P hold globally, including arbitrary powers and unrestricted other multipliers.

Inclusion-exclusion gives f_y(n)=sum_(d|gcd(n,M)) mu(d)n/d. Absolute convergence permits the finite divisor interchange:

$$
S_y=\sum_{n\ge1}\frac{f_y(n)}{2^n}
=\sum_{d\mid M}\frac{\mu(d)2^d}{(2^d-1)^2}\in\mathbb Q.
$$

For p outside P, f_(P union {p})(n)=f_P(n)-1_(p|n) f_P(n/p); in generating functions F_(P union {p})(z)=F_P(z)-F_P(z^p). These rational truncations decrease to the true S. With r the smallest omitted prime,

$$
2^{-r}\le S_y-S\le (r+1)2^{1-r}.
$$

The lower bound is the exact discrepancy 1 at r; the upper bound uses f_y(n)≤n. These comparisons are NOT bounded additive perturbations: at a fixed omitted p and a distinct unbounded omitted prime q, f_y(pq)-phi(pq)=p+q-1. They fail exact parity at omitted odd primes. With y≥2 the set of odd coefficients has natural density (3/4) product_(3≤p≤y)(1-1/p), by CRT, tending to zero. The exact parity failure cannot be silently discarded.

## 2. Exact carry relations and their limitation

For any nonnegative integral f≤n define T_f(N)=sum_(j≥1) f(N+j)/2^j, c_f(N)=floor(T_f(N)), and d_f(n)=floor(2 frac(T_f(n-1))) in {0,1}. Then

$$
f(n)=2c_f(n-1)-c_f(n)+d_f(n).
$$

If its full sum is rational, d_f is eventually periodic, by binary long division. Put u_f(n)=2c_f(n-1)-c_f(n). For any prime p whose true totient prime-step law holds, set a_p(n)=p-1 for p not dividing n and p otherwise. Exact multiplicativity plus the geometric law yields

$$
u_f(pn)=a_p(n)u_f(n)+a_p(n)d_f(n)-d_f(pn).
$$

In particular if the digit period is h and p=1 modulo h, for all sufficiently large n this gives u_f(pn)=a_p(n)u_f(n)+(a_p(n)-1)d_f(n). For all p in P, f_y obeys these exact identities with its genuine eventual periodic digit sequence. Thus no proof using only a fixed finite set of prime-step laws, these carry identities, positivity and the linear envelope can exclude rationality. The period is not uniform in y. The all-prime exact coefficient values and parity remain genuine additional restrictions.

Quantitative statistical limitation: for any Y≥1,

$$
\sum_{n\le Y}(f_y(n)-\varphi(n))
\le Y^2\sum_{p>y}p^{-2}\le Y^2/y.
$$

Indeed the product loss is at most the sum of omitted reciprocals; count multiples by Y/p and use n≤Y. For any integer X≥1 the mean normalized absolute difference of the integer carries on [X,2X) is at most

$$
\frac{1}{X^2}\sum_{N=X}^{2X-1}|c_{f_y}(N)-c_\varphi(N)|
\le \frac{4X^2+8X+6}{yX^2}+1/X.
$$

Use the preceding prefix bound at Y=2X+j, sum weights 2^(-j), then floor error≤1. Consequently the limsup is ≤4/y. This does not control high bits or exact parity. Local normalized statistics and finite factor identities can be arbitrarily well matched by exactly multiplicative rational comparisons.

## 3. Primitive cyclotomic denominator escape

Let D_y be the reduced positive denominator of S_y, and C=Phi_M(2) the cyclotomic value. Put C_prim=C/gcd(C,M). Then

$$
C_{\mathrm{prim}}^2\mid D_y.
$$

Proof. For an odd prime q dividing C, write t=ord_q(2). Since C divides 2^M-1, t|M. For d|M the valuation v_q(2^d-1) is zero unless t|d, and otherwise equals v_q(2^t-1)+v_q(d/t) by the elementary lifting-the-exponent identity for odd q. Insert these into the cyclotomic product C=product_(d|M)(2^d-1)^mu(M/d). As M is squarefree, write d=t e with e|M/t. If t=M, the valuation is v_q(2^M-1), and q is primitive. If t<M, the constant part cancels; the v_q(e) sum is 1 when M/t=q and 0 otherwise. In the exceptional case t|q-1 implies q is the largest prime factor of M, so q≤y; there is at most one such prime and its valuation in C is exactly 1. Primitive primes do not divide M since M|q-1. Hence C_prim is exactly the primitive part of C. Each primitive q divides no 2^d-1 for any proper d|M. In the rational sum S_y, only the d=M summand has negative q-valuation, equal to -2v_q(C); the others have nonnegative valuation. No cancellation is possible at q. This proves the divisibility.

The cyclotomic product also gives

$$
\log C=\varphi(M)\log 2+
\sum_{d\mid M}\mu(M/d)\log(1-2^{-d}),
$$

and the absolute value of the last sum is ≤2, since -log(1-x)≤2x for 0≤x≤1/2. Thus

$$
D_y\ge \frac{2^{2\varphi(M)}}{e^4 y^2}.
$$

By Bertrand's postulate r≤2y and the largest included prime is > (y-1)/2. Since phi(M)=product_(p≤y)(p-1), its ratio to y tends to infinity (factor out the largest prime and any arbitrarily large fixed product of other prime factors). Therefore

$$
D_y(S_y-S)\ge \frac{2^{2\varphi(M)-r}}{e^4 y^2}
\longrightarrow\infty.
$$

In particular the standard rational-separation proof S_y-S<1/(q D_y) cannot succeed asymptotically for any fixed candidate denominator q. This is a proof of failure of that test, NOT a proof that S is rational or that every denominator-based technique must fail.

## 4. Parity-preserving comparisons and the cost of sparsity

A different exactly multiplicative comparator g_y equals phi on P-smooth numbers and zero otherwise. It preserves evenness for every n≥3 and the geometric prime-power law at every prime (including those with initial value zero). But for nonempty P its binary sum is irrational: up to 2X there are at most product_(p in P)(1+floor(log_p(2X))) supported integers, which is O_P((log X)^|P|). Hence [X,2X] contains arbitrarily long zero intervals of length g≫_P X/(log X)^|P|. At the index N immediately before such an interval, 0<T_g(N)≤(N+g+2)2^(-g) tends to zero; positivity follows from infinite support on powers of any p in P. If S_g were rational of denominator q, every T_g(N) would be an integer multiple of 1/q, a contradiction. Thus this sparse construction is not a rational comparator, and no deduction to true phi follows because phi has full support.

For completeness, exact parity and any finite coefficient prefix can also coexist with a rational exactly multiplicative function: prescribe phi(p^k) for p^k≤B and zero otherwise on prime powers, extend coprime multiplicatively. The support is finite, so the sum is rational; this construction sacrifices positivity and the global geometric law at the last nonzero prime power. It shows why finite data alone cannot certify the all-prime statement.

## 5. Research disposition and restart gate

WP09-H/I excluded bounded rational perturbations by exact multiplication; WP09-J/K amplified and represented this distinction by long phase words. WP09-O establishes a different obstruction: exact coprime multiplication and geometric prime-power laws globally, every true prime-step law on any fixed finite prime set, and arbitrarily small normalized mean carry error are compatible with rational binary sums, while the natural finite-prime rational approximants have provably excessive denominators for direct rational separation.

No new contradiction between eventual periodic binary digits and the complete all-prime totient law plus exact parity has been established. The exact carry network is a necessary restatement, not a sufficient proof or a credible new quantitative producer. The finite-prime comparators do not match every constraint; the result is a barrier to specified methods, not a universal impossibility theorem.

Decision under the authorized bounded tranche: SHELVE active Erdős #249 proof search; preserve original problem OPEN and MATHCERT NOT_SUBMITTED. Stop incremental Fourier refinements and finite denominator scanning. Reopen only on a concrete new result that uses global exact prime values and parity to constrain periodic carries, or proves a source-legal cofinal original Cook cancellation estimate, or gives a genuinely different irrationality criterion with verified hypotheses. Record operational suspension without marking the mathematical problem solved.

## 6. Exact finite evidence

The following reduced denominator bit lengths and primitive cyclotomic bit lengths were calculated with Python arbitrary-precision integer and Fraction arithmetic; no floating-point test determines divisibility. The last column k certifies D_y(S_y-S)≥2^k using the omitted prime lower error bound and D_y≥2^(bit length minus one).

| cutoff y | M | denominator bits | primitive part bits | k |
|---|---|---|---|---|
| 2 | 2 | 4 | 2 | 0 |
| 3 | 6 | 12 | 1 | 6 |
| 5 | 30 | 59 | 9 | 51 |
| 7 | 210 | 417 | 48 | 405 |
| 11 | 2310 | 4616 | 481 | 4602 |
| 13 | 30030 | 60051 | 5760 | 60033 |

The four new registered tests check actual exact rational series versus finite truncation, denominator divisibility, the complete carry network on 700 exact rational tails, multiplicativity and prime-power laws, and hostile parity/sparse/finite-support distinctions. All 157 registered full-series tests passed before the final exact-head replay. CHAD source run 62dfe6c05e704e148b20b12c306736ce, output SHA256 5141a9c7b05e4b46072aeadbd9b56d7b65c3fd89eec2cdbcbc87cf2b9fa9f0a7; finite table run 1cf6a1f7a39343648bc042d569b23b3a, output SHA256 b9c12b8e236c1e66109cacd8c75b3b8a9ae9cce2d40af544bbc2ef5ece257fdf. CHAD OS-only replay, not independent attestation.
