# WP09-E — qualified mathematical critical review, four logical passes

**Material object:** FULL_WINDOW_PRIME_PROJECTION_009E.md, full_window_prime_projection.py, and the appended governed full-series tests.  
**Basis:** exact protected WP09-B/C/D and source-locked Will Cook 2026 first-harmonic setup at commit 3368d1e69467aec111eb3244843ad3542171ff96.  
**Reviewer identity:** same agent performing separate Axiomatist, Verifier, Adversary and Referee **logical** passes; NOT an independent human mathematician, external source-priority determination, Lean kernel proof, or MATHCERT.

## Axiomatist — scope and quantifiers

The theorem applies to the **actual** Euler totient and **actual complete Cook numerator**, not a truncated finite-prime surrogate. Fix shift h, choose one prime p not dividing h, allow arbitrary depth L subject only to L+h<=X and the explicit integer threshold X>=40*p^2*max(E_X,h+4). Thus the result applies at Cook's least logarithmic depth, and the prime p stays fixed rather than growing with L.

The conclusion is a lower bound on the squared magnitude of the full normalized-totient weighted window and the **unwrapped** phase argument D/2^L. It does NOT bound distances from integers, Fourier amplitudes, wrapped phase dispersion, or the irrationality of the original full series.

## Verifier — reconstruct every coefficient

1. Verify the exact divisor identity phi(m)/m=sum_{d|m}mu(d)/d. On n congruent r mod p, count d prime to p with density 1/(pd), and d divisible by p with compatible residue with density 1/d. Multiplying by mu(d)/d yields the conditional mean mu_p/p(1-1/p*indicator). The absolutely convergent infinite main-series tail costs <=X/M<=1 with M=2X+H, and the sum of O(1) weighted count errors costs <=1+log M. The published integer E_X strictly exceeds this sum.
2. Independently confirm the correct **sign** in the weighted conditional mean: t_u=q_(u-h)-q_u, therefore summing the common-zero signed coefficient signature gives -X*mu_p*t_(-r)/p^2. Incorrectly reversing t would reverse the predicted positive/negative conditional classes.
3. For p not dividing h, the residues 1,1+h,1-h are distinct from residue 1. The first dyadic weight at j=1 contributes 1/2 to q_1; all other residue classes begin at j>=2 and recur every p>=2 places, giving q_other<=1/3. Thus t_(1+h)>=1/6 and t_1<=-1/6 for **every** L, even when p is smaller than the number of shifts.
4. The absolute signed coefficient mass of G is less than two independently of L. Each of the two selected N residues has true block sum magnitude at least X/(10p^2)-2E_X, hence >=X/(20p^2) after the exact threshold. Every residue has no more than X/p+1<=2X/p terms. Two separate Cauchy–Schwarz inequalities yield sum G²>=X/(400p³).
5. Because phi(n)=n*f(n), the **entire** phase argument D/2^L=N*G+R, not a local proxy. The remainder R is bounded by sum_j 2^-j(h+2j)<=h+4, uniformly even at growing depth. Finite Euclidean reverse triangle yields RMS(D/2^L)>=X/(20p^(3/2))-(h+4)>=X/(40p^(3/2)); the final implication uses X>=40p²(h+4). Multiplying its square by X proves the cubic bound.
6. |G|<=1 and |D/2^L|<=2X+h+4<=3X. The positive-density corollary follows from a bounded-second-moment threshold, not from treating moment bounds as probability distributions of fractional parts.
7. The least Cook-admissible L_h(X) is O_h(log X), so H<=X eventually, and the finite threshold is O_h(log X). The cofinal statement follows without a quantitative prime-number theorem.

## Adversary — attacks and necessary limitations

- **Prime aliasing:** WP09-D required p>H. This proof deliberately permits p<=H, but exactly aggregates all coefficients in each mod-p residue. Merely reusing the WP09-D coordinate-isolation argument for small p would be wrong; the dyadic alias calculation repairs it.
- **Period wrap and zero-sum:** If p divides h then t_u=0 identically; p must be a prime NONDIVISOR of h. The executable rejects p|h, composite p, invalid h, and missing required finite CRT primes.
- **Low-X vacuity:** An asymptotic O(log X) error does not license the lower bound for a small finite X. The implementation returns eligible=False with no numeric theorem lower when the integer threshold fails. Real tested pairs include (h,X)=(1,4096),(2,8192),(6,32768), each with genuine minimum Cook depth.
- **CRT target:** The actual finite-prime CRT oracle must handle overlapping shifts modulo p and return exact rational conditional means. It must not silently assume p>H or infer an infinite-prime limit from a finite period.
- **Coefficient recurrence:** The actual D_(N+1)-2D_N identity equals d_h(N+L+1)-2^L d_h(N+1), not only its modular residue. The rolling implementation is checked against an independently summed direct numerator on all N in multiple blocks.
- **Big integers, precision:** The finite actual energy checker compares 1600*p^3*sum(D^2) against X^3*(2^L)^2 as integers; it does not rely on floating trigonometric estimates for its conclusion. An optional small finite harmonic observation would not prove arbitrarily late blocks.
- **Fundamental modular alias:** A_N=N has cubic unwrapped energy but exp(2*pi*i*A_N)=1 identically. This counterexample disproves any abstract claim that the new cubic energy forces 10% cancellation. It is deliberately not presented as an Euler-totient or bounded-coefficient mimic. The existing WP07-E rational controls and WP09-B ceiling additionally constrain false promotion.
- **Prior art:** Normalized shifted totient correlations appear in Balasubramanian–Giri–Srivastav (2017). The new proof uses a direct arithmetic-progression count and dyadic residue aliasing. Do not assert independent novelty/priority or imply an independent external proof review.

## Referee disposition

Admit only a **bounded, actual full-Cook-growing-window UNWRAPPED energy** theorem if candidate source checks, registered exact tests, native protected merge queue and merge material identity all pass. Keep the original irrationality OPEN and issue #3500 in progress. Do not release MATHCERT, report independent specialist certification, or claim Cook's 10% first-harmonic sum or prime/cofactor weighted cancellation.

**Next independent research obligation:** move from the real unwrapped conditional prime projection to a **modulo-one** conditional exponential-characteristic or genuinely multi-step Cook cocycle bound. A successful proof must distinguish near-integer winding from large real arguments and produce a fixed positive phase deficit strong enough for Cook's source-locked 9X/10 threshold.

**Checkpoint status:** written on topic branch before candidate CI, exact merge-group replay or protected admission. These are later operational evidence gates, not proof steps.
