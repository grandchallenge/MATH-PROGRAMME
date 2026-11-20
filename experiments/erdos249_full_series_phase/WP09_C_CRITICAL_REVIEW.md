# Erdős #249 — WP09-C bounded adversarial review

**Review mode:** separate Axiomatist, Verifier, Adversary and Referee logical passes under GCL staffing policy; same assistant, **not** independent authenticated mathematician, independent compiler replay, Lean certification, or MATHCERT.  
**Object:** JOINT_LOCAL_PRIME_LAW_009C.md and joint_local_prime_law.py, on exact topic branch research/erdos249-wp09c-local-joint-law.  
**Disposition:** QUALIFIED_BOUNDED_MANUSCRIPT_REVIEW; no original irrationality or Cook first-harmonic promotion.

## Axiomatist: quantifier and source-scope audit

The theorem fixes finitely many integer-weight triples, X and Q integers with X>=64 and Q>=32X, prime cutoff y>=2. It characterizes the shifted local quantity Z_X(Q), not the exponentially weighted length-L Cook E_(h,N,L). In the limiting rate W and H must remain fixed; the finite explicit error formula remains valid when W,H vary, but (7) cannot silently be invoked uniformly for a growing bundle. The Cook source is pinned to exact 2026 Git revision and the earlier WP09-B second moment is reused as antecedent. No new historical priority is asserted.

## Verifier: independent algebra and constants

1. For m>0, 0<=f_y(m)-f(m)<=sum_(p>y,p|m)1/p by a finite-product union bound.
2. On an X-long shifted interval, number of multiples of p <=X/p+1. Thus average error <=1/y +[1+log(2X+H)]/X.
3. The exact identity phi(n+s)=(n+s)f(n+s) costs at most 2HW in the weighted difference sum. Substituting f_y costs averaged 2W e, multiplied by n/Q<2/rho. The exponential Lipschitz constant 2pi gives 4piHW/Q+8piWe/rho.
4. Delta_y is P_y-periodic and satisfies |Delta_y|<=2W. The derivative bound for the residue-class test function is 4piW/rho. An interval Riemann-sum bound of (2+variation) per class gives the last term of (5).
5. For finite supports y' >=y, a uniformly sampled class modulo P_(y') is divisible by p with probability exactly 1/p. The two shifted arguments and t<=2 give 8piW/(rho y). This is a deterministic CRT identity, **not** a primality-independence assumption about n as a random variable.
6. P_y<=y!<=y^y and y=floor(log X/(4 loglog X)) prove the claimed O(loglog X/log X) rate for fixed terms.
7. In a single (1,h,0) pair, the modular reflection a -> -a-h flips Delta_y. The finite second moment equals WP09-B's product and cos Taylor remainder is at most (4pi/rho)^4/24. The coefficient 14pi²V_h/(3rho²) includes the correct integral 7/3.

## Adversary: attempted falsifications

- Repeated offsets and signed weights: allowed; cancellation only reduces |Delta_y|; the proof uses total absolute weight W.
- Offset n+s rather than n: the error 2HW/Q is retained; ignoring it would invalidate (5).
- Finite y and small X: P_y/X may be large; (5) is still true but is allowed to be vacuous. The resource cap in the Python engine is computational, not a theorem condition.
- Integer class a=0: it represents positive multiples of P_y, not phi(0); the model f_y is a finite divisibility profile only. Exact tests use this convention.
- Growing number of shifts: fixed-W/H corollary does not apply. The explicit bound must be recomputed.
- Prime truncation cannot claim full Cook cancellation: the elementary direct bound for the length-L weighted Cook sum is only O(X/y). It is **not** an established lower bound on its actual error, and the manuscript was corrected to say so.
- Smooth integrals: Python values use ordinary floating point; no rigorous interval arithmetic or certified numerical asymptotic is asserted. The proof is mathematical, not inferred from the decimal.
- Generic rational countermodels from WP07-E can match nearlog finite phases, and the earlier WP09-A rational affine-periodic model has genuine signed contrasts. Neither is contradicted by this local arithmetic law. New results are explicitly restricted to the genuine totient f and its finite-prime divisibility model.

## Referee: admission scope and next gate

A self-contained elementary fixed-order joint local characteristic theorem and its numerical test engine are suitable for a **bounded noncertifying research PR**, subject to clean exact-head CI and actual execution readback. This separate *logical* review does not manufacture human independence. Do not mark the original series irrational, Cook's 10% weighted estimate proved, WP07 issue #3500 complete, the Project #2 worker item Done, or MATHCERT submitted. The next substantive proof objective is arithmetic cancellation across the O(log X)-scale overlapping weighted Cook terms.

**Evidence status when authored:** GitHub source files and appended tests are committed on a topic branch; CHAD tunnel could not be contacted for local test execution, and CI must independently establish replay. Record an exact observed CI result rather than asserting PASS from this review.
