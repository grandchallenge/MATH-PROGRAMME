# WP09-H — qualified exact mathematical adversarial review

**Source lock:** Will Cook paper/249 revision 3368d1e69467aec111eb3244843ad3542171ff96, Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac. Previous actual-totient result is protected WP09-G PR #3631, merge 95fdf1224077e6935cbbb00c6427149b8ea4d60b.  
**Material:** BOUNDED_DYADIC_SHADOW_009H.md; bounded_dyadic_shadow.py; tests/test_erdos249_full_series_phase.py.  
**Epistemic status:** The following are **distinct logical Axiomatist, Verifier, Adversary and Referee passes performed by one agent**, not independently authenticated mathematical refereeing, not a Lean proof, not MATHCERT, and not a claimed resolution of the open Erdős problem.

## Axiomatist: sharpen the objects and quantifiers

The actual, unknown-status real number is alpha = sum phi(n)/2^n. The construction of a rational **different coefficient sequence** a_K uses only its explicitly convergent arithmetic tail, not a hypothesis that alpha is irrational. K is any integer >=6, and the shadow agrees with phi through index 2K and at every odd index. Its difference eta(n) is always one of 0,2,4,6.

The chosen target beta_K is **explicitly dyadic rational** with denominator dividing 2^(3K), not merely an arbitrary rational with unknown denominator. This enables the all-shift integer-tail argument for N>=3K, independently of h. The Cook phase bound is for **every** late legal block and **every** shift, not just h=1.

The actual Euler-totient WP09-G imaginary two-prime theorem is invoked unchanged. The shadow inherits its order-X contrast because a perturbation bounded by six changes each **one-step** cocycle by O(1/Q), and Q is order X at the cofinal legal depth.

The multistep comparison treats only **externally fixed weights** and bounded k-step cocycle characters; weights that depend on coefficients or on original Cook phases are **excluded**. The logarithmic scale is a threshold of the displayed perturbative estimate, not a sweeping impossibility theorem for all mathematical arguments at shorter scales.

## Verifier: exact arithmetic identity audit

1. With M=3K, beta_K=sum_(n<=M)phi(n)/2^n+(M+2)/2^M. Since the geometric envelope identity is sum_(n>M)n/2^n=(M+2)/2^M, delta_K=beta_K-alpha=sum_(n>M)(n-phi(n))/2^n is **strictly positive** and bounded by (M+2)/2^M.
2. Capacity B_K=2*4^(-K) gives 0<x_K=delta_K/B_K <=(3K+2)/2^(K+1)<1 for K>=6. This last numerical gate is strict and checked by exact integer arithmetic.
3. The floor digit formula e_j=floor(4^j*x)-4 floor(4^(j-1)*x) is in {0,1,2,3}, even at finite base-four endpoints. Its partial-sum reconstruction is floor(4^J*x)/4^J and converges to x without a hidden choice of expansion.
4. Adding 2e_j at n=2(K+j) changes phi by at most six, only on even n>=14. For even n, phi(n)<=n/2 and six<=n/2, so 0<=a(n)<=n; parity at n>=3 is unchanged. The complete infinite correction is 2*4^(-K)*x=delta_K, so sum a(n)/2^n=beta_K with denominator dividing 2^(3K).
5. For every N>=M, the infinite *single* shifted tail R_N=2^N*beta_K - finite integer prefix is integral, and so are all h-difference tails. The omitted complete Cook window is bounded by (N+h+L+2)/Q, strictly below 1/16 under the exact source-size inequality. Thus every original shadow phase has Re>cos(pi/8)>0.9. No numerical cosine sample is needed for the all-scale result.
6. With eta in [0,6], the **difference** eta(n+h)-eta(n) lies in [-6,6], not [-12,12]. Consequently every terminal source moment differs by at most 6 per summand, every one-step cocycle by at most 12*pi/Q, and WP09-G's signed imaginary modulus-six contrast differs by at most 12*pi*X/Q.
7. WP09-G gives U_phi>=pi X^2/(64Q). Therefore U_shadow>=pi X(X-768)/(64Q). At X>=1536 this is >=pi X^2/(128Q); at L=L_1(X)+1 with Q<256X it is >=pi X/32768. The signed actual source contrasts also persist up to O(X).
8. In the k-step exact integer recurrence, the total dyadic coefficient is 2^k-1. Hence the shadow/truth **complex** character difference is bounded pointwise by 12*pi*(2^k-1)/Q, and externally weighted sums obey the same bound multiplied by their number of terms. At Q~X, the normalized difference vanishes whenever 2^k=o(X). The proof does not assume fixed L or independent source increments.
9. For fixed n, if b is coprime-multiplicative and uniformly B-close to phi, primes p not dividing n yield |b(n)-phi(n)|(p-1)<=B(1+|b(n)|). Sending p to infinity forces exact equality. For our shadow specifically, odd prime values remain exactly phi(p)=p-1, so at any modified even n its multiplicative defect along coprime odd p is at least 2(p-1)-6.

## Adversary: hostile cases and failed inferences

- **No disguised irrationality claim:** alpha may or may not be rational. The construction works either way, because it only computes a nearby rational target beta_K and adds exact base-four digits of a positive arithmetic tail. It does not assert beta_K differs from alpha by an irrational amount.
- **No reliance on a computability oracle:** the mathematical digits are explicitly defined through floors of a convergent positive real series. The finite verifier uses integer lower/upper intervals to certify any requested prefix; if a base-four boundary cannot be resolved, it fails closed without guessing digits. Nontermination in a hypothetical exact boundary case would not invalidate the mathematical definition.
- **No false parity at n=1:** phi(1)=1 is retained and may be odd. The parity invariant is n>=3, as with actual phi.
- **No negative coefficients:** eta is nonnegative, and every modified even index n>=14 has at least six units of room under n because phi(n)<=n/2. This avoids a false arithmetic positivity claim.
- **Original Cook denominator rather than unwrapped energy:** the integer-tail proof is for the exact full D/Q, not a proxy normalized ratio, finite shifted covariance, or merely a cocycle. Cook's real first harmonic fails strongly for the shadow at every admissible late block.
- **Prime source and WP09-G signal preserved, not exact phi:** all fixed-prime and composite-modulus leading source sums survive with O(X) errors; no equality of exact totient multiplicative structure, exact value phi(n), or high-frequency phase is asserted.
- **Externally weighted k-step limitation:** w_N depending on a versus phi cannot be held fixed in the comparison. In particular Cook's w_N(z_N-zbar) is not covered by the bounded-coefficient formula unless independently controlled.
- **No full-source theorem transfer:** the shadow's rational first-harmonic failing does not refute the actual totient's as-yet-unproved tenth-saving. It refutes only an inference relying on observables insensitive to bounded per-coefficient changes.
- **Multiplicative rigidity does not prove irrationality:** eliminating nonmultiplicative shadows still leaves the open problem of using phi's exact multiplicativity to derive phase cancellation. Theorem D is an exact discriminator, not a final Cook inequality.
- **Source proof versus numerical verification:** the all-n no-go and all-X stability are proved analytically; finite exact digits, rational enclosures and integer centered residues validate only chosen sample instances. No floating cosine or source tests are represented as a mathematical certification.

## Referee disposition and next substantive mathematical obligation

**Bounded research admission is justified only upon exact-head CI and governance-compliant protected merge/readback.** Keep MATH-PROGRAMME issue #3500 and original Erdős #249 open, MATHCERT NOT_SUBMITTED. No claim of independent human specialist certification or Lean kernel verification.

Scientific next task is **multiplicativity-sensitive two-adic carry escape**. In practical terms, find a theorem that uses coprime product identities of genuine phi to rule out near-integer complete dyadic tails, or establish the source-locked prime/cofactor weighted exponential bound. Another fixed-prime moment, fixed-frequency characteristic, or sublogarithmic k-step cocycle signal alone is insufficient, by Theorems A–C. The targeted proof must cross the O(1)-coefficient sensitivity barrier rather than reconfirm it.
