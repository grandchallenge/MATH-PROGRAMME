# WP09-L — source-locked mathematical critical review

**Primary source:** Will Cook, *The Binary Totient Series*, revision 3368d1e69467aec111eb3244843ad3542171ff96, Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*. **Predecessor:** protected WP09-K PR #3678, merge 9ca7784599521f71c9befa4c0c49361f5e732eb9. **Issue:** #3500 OPEN. **Materials:** COFACTOR_TWO_COPY_TRANSFER_009L.md, cofactor_two_copy_transfer.py, registered tests/test_erdos249_full_series_phase.py.

**Review scope:** Distinct Axiomatist, Verifier, Adversary and Referee logical passes conducted within the SAME assistant system. Not independently authenticated mathematical review, a Lean kernel proof or MATHCERT. Claims of protected admission depend on separate exact-head and native merge-group validation.

## Axiomatist: the true quantifiers and phase object

The phase E_N is **Cook's actual complete h-shifted, length-L Euler-totient phase**, not a finite-prime projection or the WP09-K long product. The source sets A and G are reconstructed exactly using largest prime factors p_N, cofactors m_N, the small-cofactor/large-prime conditions, and phi(m_N)>=eta m_N. For a fixed m, the latter includes ALL A_m indices or excludes ALL, so the source's zbar_m over A_m equals the mean over a retained good G_m. Any algorithm averaging over a truncated or weighted subset would break the claimed identity.

Theorem A is a **sufficient conditional criterion**: if true same-cofactor two-copy energy C_E is small enough on an actual source-legal cofinal block, then the source's unresolved weighted first bound follows. WP09-L does NOT prove cofinal smallness. Theorem B translates this into actual original phase spread on pairs with a shared cofactor. Theorem C is a universal *information-boundary* adversarial weight choice, not a claim that actual totient residual weights equal those adversarial weights. Theorem D produces finite exact rational certificates for s=8,12 at X=16384, h=1, not the canonical asymptotic s=26 regime.

## Verifier: exact group identities and threshold audit

1. For each good m, z_N is exactly Cook's extracted source character exp(2pi i (2^h-1) phi(m)(p_N-1)/2^t). Its exact numerator at modulus Q is (2^h-1)*phi(m)*(p_N-1)*2^(s-1), because L-t=s-1.
2. Define group phase sums A_m=sum E_N, Z_m=sum z_N, W_m=sum w_N. Because zbar_m=Z_m/g_m, the unresolved first source term equals **exactly** S=sum_m(A_m-W_m Z_m/g_m). No conjugate is inserted in W_mZ_m: w_N=E_N/z_N, and Cook uses z_N-zbar_m.
3. |W_m|<=g_m, so |S|<=sum|A_m|+sum|Z_m|. Groupwise Cauchy gives sum|A_m|<=sqrt(G*C_E) where C_E=sum |A_m|²/g_m. The source's group-mean input Z1=sum|Z_m|<=X/100 yields sufficient C_E<=((11/20)*X)²/G for the source 14X/25 bound.
4. C_E is the exact two-copy character sum sum_m(1/g_m)sum_{N,M in G_m} exp(2pi i (D_N-D_M)/Q). It is nonnegative real as the sum of squared group character sums. The identity G-C_E=sum_m(1/(2g_m))sum_{N,M}|E_N-E_M|² is exact.
5. The conventional centered-residual covariance S=sum_m sum_N(w_N-wbar_m)(z_N-zbar_m) yields |S|<=sqrt((G-C_W)(G-C_Z)), C_W=sum|sum w|²/g_m, C_Z=sum|sum z|²/g_m. This bound is NOT interchangeable with sqrt(G C_E)+Z1. The latter can succeed while the former is too weak.
6. With adversarial legal unit weights w_N=conj(z_N), E_N^adv=1, S_adv=G-C_Z. Because C_Z=sum g_m|zbar_m|²<=Z1, Cook's cofinal source inputs G>67X/100 and Z1<=X/100 imply S_adv>66X/100>14X/25, while the second source weighted term equals C_Z<=X/100. This is a *genuine algebraic countermodel to source-mean-only inference*, NOT a totient-source E_N.
7. The true finite example X16384,h1,s12 has L20,t9, good G9526 and 64 actual cofactor groups. Correct original D rolling recurrence is checked independently at N=X, X+X/2 and 2X-1. Source group mean Z1, two-copy C_E, weighted first term S and full original harmonic are computed with integer root enclosures.
8. The rigorous root enclosure uses exact alternating Machin pi bounds, certifying floor(10^15*pi)=3141592653589793 and pi<22/7. Centered x quantization changes the true angle by <=2 units of 10^-15. The 13-step cosine/sine integer Taylor recurrences incur <=25 accumulated fixed-point rounding units and tails <1 unit (orders 28 and 29). Hence 32 units/component is strictly conservative.
9. Sum errors on complex group means are <=2*g_m*epsilon in magnitude, with epsilon=32*10^-15. As a result C_E,C_Z,C_W each differ from integer-approximate squared group sums by <=8*G*epsilon. The real first term S differs from its signed integer approximation by <=10*G*epsilon. Z1 lies between the exact integer isqrt floor sum minus 2G epsilon and the floor sum plus one integer unit per group plus 2G epsilon.
10. All original comparisons are performed with exact Fraction arithmetic, including the squared sufficient condition G*C_E_upper <=(14X/25-Z1_upper)^2 with a positive right-hand budget. The generic Cauchy route is labelled insufficient only when a rigorous **lower bound** for (G-C_W)*(G-C_Z) exceeds (14X/25)^2. This does not assert that actual S exceeds the target.

## Adversary: what can still go wrong in an unjustified transfer

- **Cook's canonical fourth bound:** The finite s8/s12 specimens at X16384 do NOT have G>0.67X or Z1<=0.01X. Neither finite s is the canonical s26; none of the source's other three asymptotic estimates is claimed there. A finite h1 harmonic success says nothing about arbitrarily large blocks for every h.
- **Wrong level of independence:** The new sufficient two-copy criterion requires genuine arithmetic cancellation of E_N across numbers with **same cofactor**. It is not supplied by WP09-K's long multiplicative-defect phase-word gap. The previous rational shadow is a direct warning against that extrapolation.
- **Variance-only mistake:** The generic Cauchy upper bound >14X/25 in finite specimens is *not* evidence the actual weighted term is large. The rational interval certificate directly shows that the actual S is small.
- **Group definition mistake:** The group mean of z must be over A_m, not an independent sample of primes. Because G is a union of entire A_m groups the two coincide for kept m; the proof would not hold if the good condition also selected individual primes within a fixed m.
- **No reinterpreted cosine as rational:** Roots of unity are generally transcendental-component complex numbers. The verifier never asserts their cosines or sines are rational. It returns a rational fixed-point approximation with an explicit a priori error strictly smaller than 32/10^15.
- **Taylor/angle rounding:** Negative centered residues use integer floor division, not floating floor; the error bound allows one unit of quantization independent of sign. The 25-unit accumulated recurrence bound is proved by integer induction with multiplier <=10/((2j-1)(2j)) for cos and <=10/((2j)(2j+1)) for sin. Both remainder bounds are verified with exact fractions and the certified pi upper bound.
- **No hidden lpf interpolation:** Largest prime factors are built by a full integer sieve over the actual interval. Totient values are exact integers. There is no learned predictor, average prime heuristic, or synthetic coefficient substitute.
- **No MATHCERT:** Same-agent logical Axiomatist/Verifier/Adversary/Referee passes, local CHAD smoke and green CI cannot be represented as independent mathematical certification.

## Referee disposition and next source-locked proof obligation

Bounded research admission is supported for the exact cofactor two-copy sufficient lemma, its equivalent phase-spread inequality, the sharp adversarial group-mean obstruction, and **finite rigorously enclosed original-totient certificates**, subject to exact-head native required checks, protected merge queue and Git blob/main readback.

The source-locked **next substantive theorem**, still unresolved, is the **cofinal same-cofactor prime-pair original-phase correlation bound**

$$
C_E\le(11X/20)^2/G
$$

at canonical s=26, eta=1/1000, least Cook-legal L, for every fixed h along arbitrarily late X. Cook's source then supplies the remaining bounds. No claim of that result is made. Keep original Erdős #249 and #3500 OPEN, MATHCERT NOT_SUBMITTED.


## Canonical s=26 eight-shift four-bound extension: separate hostile pass

**Axiomatist.** The four source terms are not interchangeable: term 1 is a signed **real-part** inequality, terms 2, 3 and 4 require absolute **complex modulus** inequalities. The finite checker explicitly computes all three real and imaginary component pairs, never substitutes a bound on the real part of those terms. For X=16384, s=26, eta=1/1000, shifts h=1 through 8, the source least depth under L>=s+h is L=26+h, and t=h+1. These depths and the exact original size gate are checked.

**Verifier.** Define B=sum_m W_m Z_m/g_m. Then the source second term is **exactly** B. The approximate rational real and imaginary parts of B are each obtained by exact products of group fixed-point root-component sums. A worst-case **complex-norm** error <8G*epsilon follows from the same per-root component error epsilon=32/10^15, not merely separate real-part control. The root modulus upper bound is computed by applying integer isqrt to the exact squared rational modulus of the approximate B and adding 8G*epsilon. For the original third and fourth source phase sums, an integer isqrt norm upper bound from the real and imaginary fixed-point component sums plus 2n*epsilon is valid. Zero excluded-good indices give third term exactly zero, not a fake numerical tolerance.

**Adversary.** At the canonical finite h=1 specimen, the source's asymptotic unweighted group mean Z1<=X/100 is **false**: the exact lower interval gives Z1>=0.4304X. Yet the actually weighted second term is <=0.0049X, proving >80-fold suppression relative to this crude source absolute sum. This does not contradict Cook's eventual large-X s26 group-mean estimate, and it is NOT evidence of random independence. It exhibits the actual correlation-dependent cancellation in a finite genuine-totient specimen. The missing first bound and the original full first harmonic also pass at this same finite block; that alone does not make any cofinal or all-h statement.

**Referee.** Exactly eight canonical s=26 source four-bound finite cases, for h=1,...,8 and X=16384, are enrolled for independent GitHub CI replay, with each source h,L,t,cofactor partition, signed first term, three complex modulus gates and full original 9X/10 first-harmonic check. They are **finite rational interval certificates** of these claims, subject to the interval arithmetic proof; they are NOT the unresolved claim that all fixed shifts have arbitrarily late successful blocks. Keep #3500 and original Erdős #249 OPEN, MATHCERT NOT_SUBMITTED.

**Operational diagnostic:** The hostile type-gate replay initially exposed a Python lru_cache alias: cached root(0,L) and root(False,L) had equal cache keys, permitting a malformed boolean residue to bypass type validation. The fixed source validates argument types **before entering the cached internal root evaluator**. All nine pre-existing WP09-L tests replayed 9/9 on the repaired head, and the canonical finite extension adds its own independently routed tests. This repair preserves the exact mathematical formula and avoids weakening the negative tests.
