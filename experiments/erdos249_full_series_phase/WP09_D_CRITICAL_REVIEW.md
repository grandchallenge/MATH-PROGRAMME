# Erdős #249 — WP09-D: independent logical critical review

**Object:** JOINT_COVARIANCE_GAP_009D.md, joint_covariance_gap.py and the appended governed full-series tests.  
**Review protocol:** separate Axiomatist, Verifier, Adversary and Referee **logical** passes by one agent. Not an independent human mathematician, MATHCERT, or Lean formalization.  
**Scope:** bounded conditional CRT covariance, fixed-order actual-totient local Fourier deficit. No original irrationality, Cook first harmonic or source-priority promotion.

## Axiomatist — exact quantifiers

- Offsets and coefficients are fixed for the limiting $X\to\infty$ result. Inputs are a nonzero integer zero-sum signature. Real coefficients also obey the analytic conditional-variance proof.
- $p>H$ is necessary for the simple isolated-coordinate projection; an arbitrary smaller prime can alias two shifts and invalidate the displayed $\ell^2$ lower bound.
- The finite-CRT inequality is unconditional for every $y\ge p$ and does not require $P_y\ll X$. The actual-asymptotic variance uses the previously proved WP09-B fixed-shift pair-correlation estimate.
- The actual phase gap is valid uniformly in the modulus only when $Q_X\ge6BX$ and $X\ge H$. It is **not** the original Cook depth-$L$ weighted phase.

## Verifier — arithmetic and constants

1. On a uniformly sampled finite CRT residue, conditioning modulo p makes each other prime q's residue uniform exactly. Each q contributes factor $1-q^{-2}$ to the conditional mean.
2. Zero-sum coefficients eliminate the common conditional mean. Because $p>H$, all shifts are distinct modulo p; squaring then averaging yields $\mu_{y,p}^2\sum c_s^2/p^3$ **without any off-diagonal terms**.
3. Jensen/Cauchy–Schwarz makes this conditional variance a lower bound on the full variance. $\mu_{y,p}\ge6/\pi^2>3/5$ supplies the simple uniform numerical constant.
4. Expand $\Delta_y^2$: each pair has the exact finite Euler factor $(1-2/q^2+1/q^3)$ when q divides the shift difference and $(1-2/q^2)$ otherwise. This is the already pinned two-point method, not an unverified prime-independence heuristic.
5. Chord inequality $1-\cos(2\pi u)\ge8u^2$ applies on the centered interval $|u|\le1/2$. With $|\Delta_y|\le B$, $1\le t\le2$, $\rho\ge4B$, and $\int_1^2t^2dt=7/3$, the constant is $56/3$. Multiplication by $9/25$ gives $168/25$.
6. For actual unscaled coefficients, $\varphi(n+s)=(n+s)f(n+s)$ and $|R_c|\le BH$; summing the cross-term correction is $O_{c,H}(X^2)$. Partial summation turns a constant second-moment density into $(7/3)V_cX^3+O(X^2\log^2(2X))$.
7. $|A_c(n)|\le B(2X+H)\le3BX$, so $Q_X\ge6BX$ centers every actual phase. Multiplying the exact finite cos bound by $(Q_X/X)^2$ eliminates the modulus, proving uniformity even if $Q_X/X$ grows.

## Adversary — failure modes actively checked

- **Zero signature by cancellation:** e.g. $(1,3,1)+(1,1,3)$ must be rejected. The theorem is strictly about *nonzero* signatures; a list of nonzero terms can still cancel.
- **Prime alias:** select p greater than every occupied offset, not merely a prime not dividing one fixed h.
- **Finite models versus actual totient:** exact CRT identities alone do not prove the limit without the genuine WP09-B shifted correlation and partial summation. Both are cited explicitly.
- **Small denominator phases:** no bound without the Q condition. The finite harmonic engine guards $Q\ge6BX$ rather than silently centering by mod Q.
- **Infinite-dimensional promotion:** formally encoding Cook's weighted length-L phase makes the signature weight norm grow with $2^L$, while its scale parameter $2^L/X$ stays bounded. Both Theorems B and C become inapplicable. The true first-harmonic $\le0.9X$ and Cook weighted prime/cofactor bound stay OPEN.
- **Rational adversary:** $\sum_{n\ge1}\lfloor n/2\rfloor\,2^{-n}=2/3$ exactly, despite locally varying shifted differences and nontrivial finite Fourier phases. Generic positive local variance does not entail irrationality.
- **Scientific numerical precision:** exact CRT fractions and product identities are authoritative finite checks; optional Python complex phase diagnostics are not interval certificates. Neither finite data nor an unexecuted test counts as an all-X proof.
- **Novelty:** the correlation products have established classical antecedents. No independent source-level priority adjudication or new MATHCERT claim.

## Referee disposition

The algebraic implication and its explicit constants survive the logical attack. Bound the admission to **WP09-D finite-dimensional nondegeneracy and actual local phase-gap theorem** only. Retain exact primary Cook source lock and protected WP09-B/C dependencies; use the already governed test module, no new routing or policy surface. Do not certify the original irrationality, modify issue #3500's open state, or claim the mathematical result has independent human specialist review.

**Execution at time of writing:** manuscript/source/test committed on a topic branch; no full exact-head CI replay, merge queue evidence, or protected admission yet. These remain independent operational gates. The next *substantive research* objective is a uniform quantitative Cook weighted prime/cofactor correlation across the full logarithmic window.
