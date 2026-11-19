# Erdős #249 — WP07-E: an exact near-logarithmic totient-residue mimic with a rational full sum

**Workstream:** [#3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500)  
**Programme:** ERDOS-249-S-WP07-E/1 (bounded negative-control theorem)  
**Date:** 2026-11-18 UTC  
**Status:** noncertifying manuscript proof, exact integer-source tests; original Erdős #249 **OPEN**, MATHCERT **NOT_SUBMITTED**

## 1. Motivation and source discipline

The protected WP07-C theorem and [WP07-D candidate #3520](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3520) analyze actual Euler-totient coefficients modulo powers of two. A remaining logical danger is that the resulting finite-sum residue and finite Fourier-phase behavior could be generic for a sequence with an **entirely rational** binary sum.

This packet constructs such a sequence. It matches the *actual totient coefficients modulo a power of two comparable to the index* at **every** index, while retaining nonnegative coefficients in the same linear envelope as the earlier rational controls. Thus it replicates **the exact fractional parts of all near-logarithmic finite totient tails at every start**. It does not replace actual totients beyond the specified modular precision, is not a multiplicative function, and does not refute Will Cook's stronger, already source-locked full-series conditional criteria.

This construction is a direct extension of elementary dyadic carry/coboundary methods used in protected [WP06](COBOUNDARY_TWO_SCALE_006.md) and [WP07-B](NEARLOG_RATIONAL_CONTROL_007B.md). **No historical novelty claim is made** for modular carry interpolation itself, and it should not be presented as the original solution to Erdős #249.

## 2. Explicit construction

Let $\varphi$ be the ordinary Euler totient, independently defined from prime factorization. For each integer $n\ge1$, set

$$
c_n=\left\lfloor n/2\right\rfloor,
\qquad
k_n=\max(0,\lfloor\log_2n\rfloor-2),
\qquad
M_n=2^{k_n}.
$$

Choose $b_0=0$ and then the **unique** integer $0\le b_n<M_n$ satisfying

$$
b_n\equiv c_n+2b_{n-1}-\varphi(n)\pmod{M_n}.
$$

Finally define the integer coefficient

$$
\boxed{a_n=c_n+2b_{n-1}-b_n.}
\tag{1}
$$

The recurrence explicitly uses the *actual* totient values to construct a **different** coefficient sequence; no approximation or search is involved. By design,

$$
\boxed{a_n\equiv\varphi(n)\pmod{M_n}\qquad(n\ge1).}
\tag{2}
$$

The modulus is nondecreasing, and for $n\ge4$ it obeys $M_n\le n/4$.

## 3. Theorem A — rationality, positivity and global linear bounds

For the sequence (1),

$$
\boxed{
a_1=0,\qquad
\frac n4\le a_n\le n\quad(n\ge2),\qquad
\sum_{n\ge1}\frac{a_n}{2^n}=\frac23.
}
\tag{A}
$$

**Proof of bounds.** For $1\le n<8$, the modulus $M_n$ equals one, so $b_n=0$ and $a_n=c_n$; in particular, the small-index bounds are immediate. More generally, for $n\ge5$ we have

$$
0\le b_n<M_n\le n/4,
\qquad
0\le b_{n-1}<M_{n-1}\le(n-1)/4.
$$

Here and below $M_n$ is a positive power of two, and the last inequality holds for $n-1\ge4$. Therefore

$$
a_n\ge\lfloor n/2\rfloor-(M_n-1)
\ge n/2-1/2-n/4+1>n/4,
$$

and

$$
a_n\le\lfloor n/2\rfloor+2b_{n-1}
< n/2+(n-1)/2<n.
$$

For $n=1,2,3,4$, $M_n=1$ and $b_n=0$, so $a_n=\lfloor n/2\rfloor$, satisfying the asserted bounds. This completes the all-index inequalities.

**Proof of exact full rational sum.** Every $b_n$ is bounded by $M_n\le\max(1,n/4)$, hence $b_n/2^n\to0$. For each positive integer $N$, the **telescoping identity**

$$
\sum_{n=1}^{N}\frac{2b_{n-1}-b_n}{2^n}=-\frac{b_N}{2^N}
$$

holds, since $b_0=0$. The correction series is absolutely convergent, because $b_n=O(n)$. Separately,

$$
\sum_{n\ge1}\left\lfloor n/2\right\rfloor x^n
=\frac{x^2(1+x)}{(1-x^2)^2},
$$

which evaluates to $2/3$ at $x=1/2$. Equation (1) therefore gives the **exact infinite** binary sum $2/3$. No numerical truncation or eventual-periodicity assertion is needed. QED.

## 4. Theorem B — reproduce the *entire* finite totient phase at near-log depth

For any integer $N\ge8$, set

$$
L_N=\lfloor\log_2N\rfloor-2\ge1
$$

and define the two full finite scaled tails

$$
U_{N,L_N}^{\varphi}=
\sum_{j=1}^{L_N}\frac{\varphi(N+j)}{2^j},
\qquad
U_{N,L_N}^{a}=
\sum_{j=1}^{L_N}\frac{a_{N+j}}{2^j}.
$$

Then

$$
\boxed{
U_{N,L_N}^{a}-U_{N,L_N}^{\varphi}\in\mathbb Z
\quad\text{for every }N\ge8.
}
\tag{B1}
$$

In particular, for **every** integer harmonic $h$,

$$
\boxed{
\exp(2\pi i hU_{N,L_N}^{a})
=\exp(2\pi i hU_{N,L_N}^{\varphi}).
}
\tag{B2}
$$

**Proof.** The modulus $M_n=2^{k_n}$ is nondecreasing. For $1\le j\le L_N$,

$$
M_{N+j}\ge M_N=2^{L_N}\ge2^j.
$$

By (2), $2^j\mid a_{N+j}-\varphi(N+j)$. Every summand in the difference of the complete finite tails is therefore an integer, proving (B1). The Fourier equality (B2) follows because each exponential character has integer period one. QED.

**Blockwise exact identity.** For any integer $X\ge8$, one may instead take a common depth $L=\lfloor\log_2X\rfloor-2$ for **every** $N\in[X,2X)$. The identical argument proves **termwise equality of all finite Fourier phases** and thus exact equality of their averages on the whole block, for every integer harmonic simultaneously. The equality is not a numerical approximation or merely an equality of magnitudes.

**Immediate scientific limitation.** This counterfeit sequence has a *rational full binary sum*, despite agreeing with the true totient sequence on every piece of finite residue data through this depth and obeying $n/4\le a_n\le n$. Thus no argument using **only these finite fractional parts, their all-harmonic phase averages, and this common linear coefficient envelope** can distinguish the actual totient from an exactly rational binary series.

## 5. Theorem C — match even the exact two-adic valuation almost everywhere

For every $n\ge4$ satisfying

$$
\nu_2(\varphi(n))<\lfloor\log_2n\rfloor-2,
$$

the congruence (2) is modulo $2^{\lfloor\log_2n\rfloor-2}$, so it implies

$$
\boxed{\nu_2(a_n)=\nu_2(\varphi(n)).}
\tag{C}
$$

Indeed, if $v=\nu_2(\varphi(n))$ is strictly less than $k_n$, then $a_n/2^v\equiv\varphi(n)/2^v\pmod2$.

Therefore the mismatch set is contained in the nearmaximal exceptional set $E_2(X)$, up to finitely many small indices. The Fermat/odd-budget estimate for fixed $C$ proved in [WP07-D PR #3520](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3520) gives, **subject to the separately governed WP07-D admission and its self-contained proof**,

$$
\boxed{
\#\{2\le n\le X:\nu_2(a_n)\ne\nu_2(\varphi(n))\}
=O((1+\log X)^3).
}
\tag{C2}
$$

Here $B=2^{2+1}=8$, $K_B=1$, and the exponent from the explicit WP07-D bound is $K_B+2=3$. The core modular identity (B1) and rationality (A) do **not** depend on this count.

## 6. Where this comparator stops

The high-precision modular match is only guaranteed through

$$
k_n=\max(0,\lfloor\log_2n\rfloor-2).
$$

It does **not** give matching coefficients modulo $2^L$ at $L-\log_2N\to+\infty$ while keeping the same linear coefficient envelope. Nor does it establish that the infinite scaled totient tail has the periodic fractional parts of the rational comparator.

For a hypothetical rational denominator $q$, the elementary **strict dyadic residue-versus-analytic-tail** test would require the centered numerator residue to exceed $q(N+L+2)$, while every such numerator residue is at most $2^{L-1}$. At the present depth $L\le\lfloor\log_2N\rfloor$, the strict test is therefore impossible even in principle. To produce a positive irrationality result one must control genuine **over-logarithmic analytic depth**, or exploit extra arithmetic information not preserved by this bounded carry interpolation, such as multiplicativity/prime-factor correlations across a large range.

**No claim here:** irrationality of $\sum\varphi(n)2^{-n}$, proof of Cook's good-base cofinal Fourier bound, exact totient multiplicativity for $a_n$, mathematical priority, independent theorem certification, or MATHCERT submission.

## 7. Reproducibility and claim ledger

The standard-library [module](totient_residue_rational_mimic.py) uses an independent totient sieve and deterministic least-nonnegative modular remainders. The hostile tests extend the already protected, registered rational-control test suite [here](../../tests/test_erdos249_rational_pulse_coboundary.py), without modifying a policy component or inventing a CI route. Tests check congruence for thousands of indices, coefficient bounds, full-series telescoping on independent exact rational fractions, exact fractional-phase matching through dyadic boundaries, no wrongly inferred full-tail irrationality, valuation mismatch set containment and malformed arguments.

| Claim | Status |
| --- | --- |
| WP07-E-A: positive linear coefficients and rational full sum $2/3$ | Elementary exact manuscript proof |
| WP07-E-B: same actual-totient finite fractional parts at $L_N=\lfloor\log_2N\rfloor-2$ for every $N\ge8$ | Elementary exact manuscript proof |
| WP07-E-C: exact valuation agreement outside $E_2(X)$ | Elementary deduction from congruence; count conditional only on separate proven WP07-D lemma |
| WP07-E-N: shallow finite-sum residue or phase criterion forces original irrationality | **Refuted** as a generic implication |
| Original Erdős #249, cofinal quantitative actual-totient Fourier/residue producer | **OPEN** |
| Formal Lean checking, external review, mathematical priority | **NOT_SUBMITTED / NOT_CLAIMED** |

**Next productive target:** a true totient-specific identity involving global multiplicative structure or an over-logarithmic residue estimate. Extend or adapt a proposed positive criterion only after showing why this **exact phase mimic** cannot reproduce its hypotheses. Close neither research issue #3500 nor the original Erdős #249 problem on the basis of this negative-control result.
