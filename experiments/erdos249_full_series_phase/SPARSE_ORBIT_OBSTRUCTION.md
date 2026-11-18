# Erdős #249 — sparse irrational doubling-orbit obstruction 002

**Research status:** a rigorous elementary manuscript theorem and exact-integer executable checks. **Not Lean-formalised here, not independently human-reviewed, not a novel-priority claim, and not a proof of the original Erdős #249 conjecture.** This work qualifies the scope of the previously merged [full-S Fourier pilot](README.md) under [programme #3201](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3201).

## A stronger negative control from GCL's own verified auxiliary theorem

The protected Lean proof in [PR #3446](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3446), merged at exact SHA \`62ffaa1db3e2d1a5d120611e86fc189f1c24b50e\`, establishes irrationality of the lacunary totient subseries

$$
T=\sum_{m=0}^{\infty}2^{-e_m},
\qquad e_m=2^{m+1}-m.
$$

The source definition is \`Erdos249Bounded.exponent\`; its exact exponent list begins 2, 3, 6, 13, 28, 59, 122. The Lean proof is **only** about T, while the original question for the full totient generating value S remains open. Here we reuse the earlier theorem as a known source-locked fact; the statements below are **new manuscript deductions in this work packet**, not additional Lean-checked theorems.

Let $e(t)=\exp(2\pi i t)$ and consider the doubling orbit $\{2^N T\}$. Its irrationality does **not** force the Fourier averages of that orbit to decay. In fact, the averages approach 1 extremely quickly, even when the range of harmonics grows polynomially.

## Sparse-support lemma (quantitative elementary proof)

Let $(e_m)_{m\ge0}$ be any increasing sequence of positive integers, and define

$$
\alpha=\sum_{m\ge0}2^{-e_m},
\qquad A(Y)=\#\{m:e_m\le Y\}.
$$

Suppose $A(Y)$ is finite for each Y, as follows from strict increase. For integers X, K at least 1 and any nonnegative integer H, define

$$
F_{h,X}(\alpha)=
\frac1X\sum_{N=X}^{2X-1}e(h2^N\alpha).
$$

**Lemma (explicit uniform estimate).** Simultaneously for every integer h with $|h|\le H$,

$$
\left|F_{h,X}(\alpha)-1\right|
\le \frac{2\pi H}{2^K}+\frac{2K A(2X+K)}{X}.
$$

**Proof.** Modulo integers, $2^Nlpha$ equals the sparse binary suffix

$$
2^N\alpha\equiv\sum_{e_m>N}2^{N-e_m}\pmod{\mathbb Z}.
$$

All support exponents are distinct, so this suffix lies in $[0,1]$ (with 1 possible for eventually complete support). The exponential character depends only on this suffix modulo integers. Call N **exceptional** if some $e_m$ lies in $(N,N+K]$. A fixed supported exponent e makes at most K indices N exceptional; and only exponents at most $2X+K$ can appear. Hence at most $KA(2X+K)$ indices in $[X,2X)$ are exceptional.

For any nonexceptional N, all nonzero fractional binary digits of the suffix start strictly after position K. Consequently

$$
0\le\sum_{e_m>N}2^{N-e_m}\le\sum_{j=K+1}^{\infty}2^{-j}=2^{-K}.
$$

Using $|\exp(2\pi i t)-1|\le 2\pi|t|$, the phase discrepancy is at most $2\pi|h|2^{-K}$ for each nonexceptional N. For the exceptional indices, it is at most 2. Summing these two contributions and dividing by X proves the estimate, **uniformly in h**. No ergodic theorem, conjecture or asymptotic assumption is needed.

## Specialization to the Lean-verified irrational T

Since $e_m=2^{m+1}-m\ge2^m$, we have, for $Y\ge1$,

$$
A(Y)\le 1+\lfloor\log_2 Y\rfloor.
$$

For every fixed integer $c\ge0$, take X at least 2 and choose

$$
K=(c+2)\lceil\log_2 X\rceil,\qquad H=X^c.
$$

Then $H2^{-K}\le X^{-2}$, so the lemma yields

$$
\sup_{\lvert h\rvert\le X^c}
\left|F_{h,X}(T)-1\right|
\le
\frac{2\pi}{X^2}+
\frac{2(c+2)\lceil\log_2 X\rceil
(1+\lfloor\log_2(2X+K)\rfloor)}{X}.
$$

The right-hand side tends to zero as $X\to\infty$, at rate at most $O_c((\log X)^2/X)$.

**Conclusion (quantitative obstruction):** $T$ is irrational by the already-admitted Lean theorem, but its doubling-orbit Fourier means approach 1 uniformly over **every fixed polynomial range of integer frequencies**. It is therefore false that irrationality generally entails decay of these means, even at many frequencies and large sampling scales.

This does not refute the existing S-specific sufficient Fourier criteria: their arithmetic hypotheses may be much stronger. It establishes that their required cancellation cannot be justified by irrationality or digit sparsity alone.

## Relation to the original totient-tail shift problem

For an integer coefficient sequence $(a_n)$ with a convergent base-two series $A=\sum_{n\ge1}a_n2^{-n}$, define its scaled tail $U_N^A=\sum_{j\ge1}a_{N+j}2^{-j}$. Since $2^NA\equiv U_N^A\pmod{\mathbb Z}$,

$$
U_{N+r}^A-U_N^A\equiv(2^r-1)2^N A\pmod{\mathbb Z}.
$$

For the lacunary coefficient sequence defining T, this turns the **first-harmonic phase of a shift difference** into one of the polynomially many ordinary orbit harmonics if $r\le c\log_2 X$. Thus even for shift sizes growing logarithmically in X, the phase averages of T converge to 1 instead of showing uniform cancellation. This directly demonstrates that a general shift-based Fourier saving would be substantially stronger than mere irrationality. It does **not** refute the S-specific good-base, prime or totient hypotheses in the conditional reductions of Will Cook, *The Binary Totient Series* (revised October 2026), or their associated Lean consumer declarations. Those hypotheses remain unproved for the actual totient series.

## Executable falsification and source custody

The source-locked prototype is \`sparse_orbit.py\`: integer powers, exponents, truncated dyadic binary residues, exact exceptional-index enumeration, and analytic error bounds are computed without floating-point arithmetic until the final bound or finite trigonometric samples. The ordinary double-precision trigonometric values are descriptive checks, **not certified interval arithmetic**. The required bound itself follows from the written proof, not these computations.

For the fixed polynomial harmonic exponent c = 1, the elementary uniform bound for **all** integer $|h|\le X$ gives:

| X | Chosen K | Exact exceptional indices in [X,2X) | Universal upper bound |
| ---: | ---: | ---: | ---: |
| 2,048 | 33 | 33 | 0.418947 |
| 8,192 | 39 | 39 | 0.142823 |
| 65,536 | 48 | 48 | 0.026368 |

For X = 8,192, L = 48, the directly computed $|M_{h,X,L}(T)-1|$ values are approximately 0.0005133, 0.0007112, 0.0007813, 0.0008191, 0.0005133 for h = 1, 3, 7, 31, 64 respectively. Each has an additional analytical approximation error at most $2\pi|h|2^{-48}$. Again, small errors are compatible with **irrational T** and therefore are not evidence for rationality.

The seven hostile tests \`tests/test_erdos249_sparse_orbit.py\` verify the first source-locked exponents, consecutive gaps and $e_m\ge2^m$, dyadic residue reconstruction against a separately written exact integer sum, nested 24/48-bit truncations using Python rational fractions, exact exceptional-index counts, polynomial bound decay, observed phase means within their analytical bounds, and a rational 4/3 control. They explicitly do **not** infer irrationality from numerical cancellation or infer rationality from phase concentration.

**Research disposition:** Proof in manuscript, runtime numerics and source-locked Lean reference; no theorem-level novelty claim, no distinct independent human mathematical review, no new Lean formalization, no MATHCERT request, and **original Erdős #249 remains OPEN**. The necessary new producer remains totient-specific: derive a cofinal arithmetic phase or residue separation that the lacunary and rational countermodels do not satisfy, and compare it to Cook's prior exact sufficient criteria. Additional polynomial frequency sweeps alone will not address that obligation.
