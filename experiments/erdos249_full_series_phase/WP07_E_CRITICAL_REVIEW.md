# Erdős #249 WP07-E — adversarial review of exact residue-mimicking rational countermodel

**Review type:** non-authoring *logical* adversarial pass by the same authenticated GCL agent. **Not** independently credentialed mathematical review, not Lean-checking, not MATHCERT.  
**Workstream:** [#3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500) OPEN; original Erdős #249 OPEN.  
**Exact manuscript SHA-256:** 75fc5b86739f55c5753f041743961be6f511a681ee5c2b0e4569924cc36c85b9.  
**Exact source SHA-256:** 11f09bb1d201d2ef58164c36c94f98398160ce2d6204878d05543b4fc5e8ac5f.  
**Exact registered hostile suite SHA-256:** 561b3f059fafb1ac4a7a44f8b7cc30d9d64c7141038d4bca521747c9fd74f45f.  
**Replayed exact topic head:** f7a20f8012a1672726bd062576b1b3d6e7a0bd07; **31/31 source tests PASS**, source math gate PASS.

## A. Is the modulus interpolation circular, or does it prove rationality independently?

The recurrence **uses** actual $\varphi(n)$ to define the synthetic $b_n$; this is legitimate for a countermodel but not an independent expression for the totient. The generated $a_n$ is a *different* sequence, and its rationality derives from the baseline $c_n=\lfloor n/2\rfloor$ and an exact telescoping coboundary, not from assuming anything about the totient sum. Specifically, the correction through $N$ equals $-b_N/2^N$, and the bound $b_N=O(N)$ makes its limit zero. Thus the full sum is exactly $2/3$ even if the original totient sum is irrational. No finite extrapolation is involved.

## B. Are the all-index coefficient bounds uniform across modulus jumps?

For $n<8$, $M_n=1$, so $b_n=0$ and $a_n=\lfloor n/2\rfloor$. For $n\ge5$, $M_n\le n/4$ and $M_{n-1}\le(n-1)/4$; the least residue choice forces $0\le b_n<M_n$. Hence $a_n>\lfloor n/2\rfloor-n/4+1\ge n/4$ and $a_n<\lfloor n/2\rfloor+(n-1)/2<n$. The $n=4$ boundary is directly included in the $M=1$ case. There is no hidden assumption that successive moduli stay equal; they double at powers of two. Tests cross all such transitions through 12,000.

## C. Are both the coefficient congruence and the finite sum identity exact?

By the definition of $b_n$, $a_n-\varphi(n)$ is divisible by $M_n$ at **every** index. Since $M_n$ is nondecreasing, for $N\ge8$, $L=\lfloor\log_2N\rfloor-2$, and $j\le L$, we have $2^j\mid M_{N+j}$ and therefore $2^j\mid a_{N+j}-\varphi(N+j)$. Thus the difference of **whole finite sums** is an integer term by term. Every integer-harmonic exponential phase and every blockwise Fourier phase average at this common depth are *exactly the same*, regardless of the actual unknown infinite totient sum. Tests use direct exact binary numerators rather than floating phases.

## D. Does the valuation agreement incorrectly claim identity everywhere?

No. Congruence modulo $2^{k_n}$ preserves the exact two-adic valuation when that valuation is **strictly smaller** than $k_n$. The only possible mismatches occur when $\nu_2(\varphi(n))\ge k_n$, which is WP07-D's $E_2$ exceptional set for $n\ge4$. The separately source-proved $O((\log X)^3)$ estimate is used only for the mismatch *count*, not for the central rational sum or all-position finite phase identity. No precise list of mismatches outside the finite checks is alleged.

## E. Can this comparator refute an actual totient-specific proof?

No. The model matches only the selected coefficient residues and the linear envelope. The synthetic function $a_n$ is not asserted to be multiplicative, to be Euler's totient, or to satisfy a higher-depth or cofinal condition. It therefore **does not refute** Cook's actual good-base Fourier hypothesis or any proof using authentic multiplicative correlations. It **does** reject a generic inference that those particular nearlog finite phases, even with positive linear coefficients, imply irrationality. A later positive proof must identify the additional hypothesis the countermodel does not satisfy.

## F. Does the interpolation actually hold for arbitrary integer targets?

Yes. The proof of the carry bound and the rational full sum uses **only** that $b_n$ is a canonical residue modulo $M_n^{(K)}$, not any arithmetic property of the target $t_n$. For each fixed integer deficit $K\ge2$, $M_n^{(K)}\le n/2^K$ once $n\ge2^{K+1}$, and $b_n<M_n^{(K)}$, so $n/4\le a_n\le n$ with the same rational full sum $2/3$. The coefficient congruence and exact complete finite-tail fractional-phase match at depth $\lfloor\log_2N\rfloor-K$ then follow for **every** target. Restricting the target to $|t_n|\le n$ is needed only to know its own complete binary series converges, not for the construction or modular identity. This stronger universal statement avoids falsely attributing the countermodel's behavior to a special coincidence involving totient arithmetic.

The three new hostile tests independently exercise four bounded target classes for deficits 2, 3 and 5, including dyadic boundaries, as well as a deliberately unbounded signed target that tests carry independence from target growth. Exact modulo checks, rational telescoping, linear envelopes and invalid-input guards all pass. This is an algebraic theorem, not an empirical induction.

## G. Are the source claims and execution independent?

The module uses a totient sieve, a separately implemented direct coprime-count oracle, explicit integer modular arithmetic and exact rational arithmetic. The 31/31 tests include all existing WP06/WP07-B regression tests, the original nine WP07-E hostile tests, and three additional universal interpolation tests. They cannot certify an infinite theorem, but both infinite conclusions were proved algebraically in the manuscript. The qualified reviewer is the same agent and no independent theorem-referee identity, novelty or source priority is being manufactured. The underlying dyadic carry method is already present in GCL WP06/WP07-B; the present specialization needs external literature comparison before a novelty claim.

**Disposition:** ACCEPT_WITH_SCOPE for the rational entire-series identity, the all-position exact finite totient-phase mimic, the universal arbitrary-target interpolation theorem, the valuation-exception deduction and its exact tests. The **scientific** cofinal actual-totient residue-vs-remainder separation is still unproved; maintain #3500 and the original #249 OPEN.
