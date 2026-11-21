# Erdős #249 — WP09-D: strict joint covariance and universal local phase gap

**Research issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500).  
**Status:** bounded noncertifying manuscript result; original Euler-totient series irrationality OPEN; MATHCERT NOT_SUBMITTED.  
**Date:** 2026-11-21.  
**Previous exact admitted material:** WP09-C [protected PR #3590](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3590) at merge e50de5c801dc0e3f1d366839eb7d2d588075dcc7; WP09-B [PR #3541](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3541).  
**Cook source lock:** Will Cook, *The Binary Totient Series* (2026), exact [revision 3368d1e69467aec111eb3244843ad3542171ff96](https://github.com/wcook04/plectis-erdos/blob/3368d1e69467aec111eb3244843ad3542171ff96/paper/249/erdos-249-binary-totient-series.tex), Git blob 547ed9ed83500181a2e55047ce5df569b7cb49ac, section *An exponential-sum question*.

## 1. Claim and intended advance

WP09-C characterized the limiting characteristic of every **fixed finite bundle** of shifted totient differences, but did not establish that its characteristic is nontrivial for every nonzero bundle. This note supplies a quantitative nondegeneracy result, including a completely explicit lower bound and an unconditional Fourier-phase deficit for the **actual** totient at all sufficiently large scales. It generalizes the one-shift WP09-B variance argument to **all** nonzero finite difference signatures and proves strict positive definiteness on the entire finite shift-difference space.

Fix an integer $H\ge1$ and integers $c_0,\dots,c_H$ satisfying

$$
\sum_{s=0}^{H}c_s=0,\qquad
B=\sum_{s=0}^{H}|c_s|>0,\qquad
M_2=\sum_{s=0}^{H}c_s^2>0.
\tag{1}
$$

Missing offsets have coefficient zero. The exact same setup arises by consolidating any finite list of weighted differences
$\sum_iw_i[\varphi(n+u_i)-\varphi(n+v_i)]$.
Let

$$
f(n)=\frac{\varphi(n)}n,\quad
F_c(n)=\sum_{s=0}^H c_s f(n+s),\quad
A_c(n)=\sum_{s=0}^H c_s\varphi(n+s).
\tag{2}
$$

An integer prime $p>H$ will be called a **separating prime**. It distinguishes all occupied offsets modulo $p$. This p can be chosen explicitly by finding the first prime exceeding H. There is no need for an unproved assertion about prime gaps.

## 2. Exact arithmetic nondegeneracy

For $y\ge p$ define $P_y=\prod_{q\le y}q$, $f_y(a)=\prod_{q\le y,q\mid a}(1-1/q)$ and
$\Delta_{c,y}(a)=\sum_sc_sf_y(a+s)$.
The finite averages below are exactly rational. Set

$$
\mu_{y,p}=\prod_{\substack{q\le y\\q\ne p}}\left(1-\frac1{q^2}\right),
\qquad
V_{c,y}=\frac1{P_y}\sum_{a\bmod P_y}\Delta_{c,y}(a)^2.
\tag{3}
$$

**Theorem A (single-prime conditional variance).** For every nonzero zero-sum integer signature (1), every separating prime $p>H$, and every $y\ge p$,

$$
\boxed{
V_{c,y}\ge\frac{\mu_{y,p}^2}{p^3}M_2
\ge\frac9{25p^3}M_2>0.
}
\tag{4}
$$

The limit $V_c=\lim_{y\to\infty}V_{c,y}$ exists, equals the limiting actual shifted-totient variance, and obeys the same lower bound:

$$
\boxed{
\sum_{n\le T}F_c(n)^2=V_cT+O_{c,H}((\log(2T))^2),
\qquad
V_c\ge\frac9{25p^3}M_2>0.
}
\tag{5}
$$

No generic assertion of prime independence is used. The proof conditions on one actual CRT residue and integrates all remaining finite primes **exactly**.

### Proof of Theorem A

Equip the residue classes modulo $P_y$ with the uniform average. For fixed $a\bmod p$, the CRT identifies all other prime residues independently **as an exact finite-product identity**. For each $q\ne p$,

$$
\frac1q\sum_{r\bmod q}
\left(1-\frac1q\mathbf 1_{\{q\mid r+s\}}\right)
=1-\frac1{q^2}.
$$

Hence the conditional mean of the product $f_y(a+s)$ is

$$
\mathbb E_y[f_y(a+s)\mid a\bmod p]
=\mu_{y,p}
 \left(1-\frac1p\mathbf 1_{\{a+s\equiv0\pmod p\}}\right).
\tag{6}
$$

Summing with the coefficients $c_s$ cancels the constant term because $\sum c_s=0$. Distinct occupied shifts $s\in[0,H]$ are distinct modulo $p>H$, so for each class $a$ at most one coefficient survives. Thus

$$
\mathbb E_y[\Delta_{c,y}\mid a\bmod p]
=-\frac{\mu_{y,p}}p
\sum_{\substack{0\le s\le H\\a+s\equiv0\pmod p}}c_s.
\tag{7}
$$

Taking the square and averaging $a$ modulo $p$ gives the **exact identity**

$$
\boxed{
\mathbb E_y\bigl[
 \mathbb E_y[\Delta_{c,y}\mid a\bmod p]^2\bigr]
=\frac{\mu_{y,p}^2}{p^3}\sum_sc_s^2.
}
\tag{8}
$$

Conditional-expectation contraction (or simply the elementary Cauchy–Schwarz inequality in each of the $p$ classes) implies
$V_{c,y}\ge\mathbb E_y[\mathbb E_y[\Delta\mid a\bmod p]^2]$.
Since

$$
\mu_{y,p}\ge\prod_q(1-q^{-2})
=\frac6{\pi^2}>\frac35,
$$

we obtain (4). The lower bound is uniform in $y$.

Existence of $V_c$ follows by expanding its square into finitely many pair correlations. The exact finite CRT computation gives

$$
\begin{aligned}
V_{c,y}&=\sum_{s,t=0}^Hc_sc_t C_{|s-t|,y},\\
C_{0,y}&=\prod_{q\le y}\left(1-\frac2{q^2}+\frac1{q^3}\right),\\
C_{d,y}&=\prod_{\substack{q\le y\\q\mid d}}
 \left(1-\frac2{q^2}+\frac1{q^3}\right)
 \prod_{\substack{q\le y\\q\nmid d}}
 \left(1-\frac2{q^2}\right),\qquad d\ge1.
\end{aligned}
\tag{9}
$$

The products converge absolutely. The corresponding **actual** shifted-totient correlations with error $O_H(\log^2(2T))$ were already proved and independently test-replayed in WP09-B. Apply them to each of finitely many pairs $(s,t)$ to obtain (5). No theorem originality is asserted for these classical pair correlations. QED.

**Corollary (strict covariance matrix).** On the real vector space

$$
\left\{c\in\mathbb R^{H+1}:\sum_sc_s=0\right\},
$$

the matrix with entries $C_{|s-t|}$ is strictly positive definite. Indeed the finite CRT proof works with arbitrary real coefficients and (5) shows its quadratic form is at least $(9/(25p^3))\|c\|_2^2$.

This is stronger than proving strict variance only for a selected shift $h$; it rules out *any* nontrivial finite signed combination of shifted totient ratios becoming asymptotically deterministic.

## 3. Effective local Fourier deficit

Let $\rho\ge4B$. The WP09-C finite-prime local characteristic for this signed profile is

$$
C_{c,y}(\rho)=\frac1{P_y}\sum_{a\bmod P_y}
\int_1^2\exp\left(\frac{2\pi it}{\rho}
 \Delta_{c,y}(a)\right)\,dt.
\tag{10}
$$

**Theorem B (strict local Fourier gap).** For all $y\ge p$ and $\rho\ge\max(32,4B)$,

$$
\boxed{
1-\operatorname{Re} C_{c,y}(\rho)
\ge\frac{56 V_{c,y}}{3\rho^2}
\ge\frac{168 M_2}{25p^3\rho^2}>0.
}
\tag{11}
$$

The same inequality holds for $C_c(\rho)=\lim_{y\to\infty}C_{c,y}(\rho)$.

**Proof.** We have $|\Delta_{c,y}(a)|\le B$ because $0\le f_y\le1$. For $1\le t\le2$ and $\rho\ge4B$, the centered real argument satisfies $|t\Delta_{c,y}/\rho|\le1/2$. Apply the elementary chord bound

$$
1-\cos(2\pi u)\ge8u^2\qquad (|u|\le1/2),
$$

average residues and integrate $\int_1^2t^2dt=7/3$. This gives the first bound; Theorem A gives the second. Passage to $y\to\infty$ is justified by WP09-C's uniform finite-prime characteristic limit and Theorem A's convergent products. QED.

The lower bound is an *absolute* nonzero Fourier deficit for every fixed nontrivial local bundle, not merely a moment statement. The frequencies and offsets are not allowed to grow unrestricted while invoking the fixed-parameter limit.

## 4. True actual-totient phase gap, uniform in its modulus

Define the actual finite harmonic, for integers $X,Q\ge1$,

$$
Z_{c,X}(Q)=\frac1X\sum_{n=X}^{2X-1}
 \exp\left(\frac{2\pi i A_c(n)}Q\right).
\tag{12}
$$

**Theorem C (an unconditional actual-totient local gap).** For every fixed nonzero zero-sum integer coefficient vector (1),

$$
\boxed{
\sum_{n=X}^{2X-1}A_c(n)^2
=\frac73V_cX^3+O_{c,H}\bigl(X^2\log^2(2X)\bigr).
}
\tag{13}
$$

For **every** sequence of integer moduli $Q_X\ge6BX$, with $X\ge\max(64,H)$, this implies

$$
\boxed{
\liminf_{X\to\infty}
\left(\frac{Q_X}{X}\right)^2
\left(1-\operatorname{Re} Z_{c,X}(Q_X)\right)
\ge\frac{56}{3}V_c
\ge\frac{168M_2}{25p^3}>0.
}
\tag{14}
$$

No upper bound on $Q_X/X$ is needed. The gain is in the **actual** Euler totient, not a finite-prime surrogate.

**Proof.** The identity
$\varphi(n+s)=(n+s)f(n+s)$
gives

$$
A_c(n)=nF_c(n)+R_c(n),\qquad
|R_c(n)|=\left|\sum_s sc_sf(n+s)\right|\le BH.
\tag{15}
$$

Also $|F_c(n)|\le B$. Therefore
$A_c(n)^2=n^2F_c(n)^2+O_{c,H}(n+1)$.
Partial summation applied to (5), on $[X,2X)$, yields

$$
\sum_{n=X}^{2X-1}n^2F_c(n)^2
=V_c\int_X^{2X}t^2\,dt
+O_{c,H}(X^2\log^2(2X))
=\frac73V_cX^3+O_{c,H}(X^2\log^2(2X)).
$$

This proves (13). For $n\in[X,2X)$, $X\ge H$, the elementary coefficient envelope
$0\le\varphi(n+s)\le n+s\le3X$
implies $|A_c(n)|\le3BX\le Q_X/2$. The same chord bound used in Theorem B now applies **pointwise**:

$$
1-\operatorname{Re} Z_{c,X}(Q_X)
\ge\frac8{XQ_X^2}\sum_{n=X}^{2X-1}A_c(n)^2.
\tag{16}
$$

Multiply by $(Q_X/X)^2$ and substitute (13), obtaining the stronger asymptotic estimate
$\ge56V_c/3+O_{c,H}(\log^2(2X)/X)$ for the scaled deficit.
The error is uniform in all admissible $Q_X$, proving (14). QED.

## 5. Adversarial boundary: why this is not Cook's 10% saving

The genuine problem in the pinned Cook paper is the length-$L$ phase

$$
E_{h,N,L}=
\exp\left(2\pi i\sum_{j=1}^L
\frac{\varphi(N+h+j)-\varphi(N+j)}{2^j}\right),
\quad L\asymp\log_2X,
\tag{17}
$$

at $2^L\ge16(2X+h+L+2)$. It is NOT the fixed-shift local phase in (12).

If one formally rewrites Cook's numerator as a single bundle of shifted totient differences with weights $w_j=2^{L-j}$, then its coefficient norm is $B\asymp2^L$ (unless exact cancellations occur), while $\rho=2^L/X$ is bounded at the least admissible depth. Thus the hypotheses $\rho\ge4B$ or $Q\ge6BX$ **fail by an unbounded factor**. In addition, the number and maximum offset of terms grow with $L$, making the fixed-parameter constants ineffective. No application of (11) or (14) to Cook's full phase is legitimate.

There is also a generic rational control. The integer sequence $a_n=\lfloor n/2\rfloor$ has the exact rational binary sum
$\sum_{n\ge1}a_n2^{-n}=2/3$, yet its first shifted difference $a_{n+1}-a_n$ alternates between 0 and 1 and therefore has positive variance and a strict local-phase gap for suitable moduli. Any argument turning **local difference variance alone** into irrationality is false. This control does not share Euler totient's multiplicative structure or the prime-conditional projection (6).

**Open work:** a totient-specific cancellation or correlation bound involving the **entire exponentially weighted phase** in (17), or Cook's source-locked prime/cofactor *weighted* correlation
$\operatorname{Re}\sum_{N\in\mathcal G}w_N(z_N-\bar z_{m_N})\le14X/25$
on arbitrarily late admissible blocks. The present fixed-order covariance theorem supplies arithmetic input but does not deliver that bound. Do not close #3500, certify the original Erdős #249 irrationality, or claim theorem priority.

## 6. Evidence and reproducibility

The exact rational engine [joint_covariance_gap.py](joint_covariance_gap.py) constructs canonical zero-sum signatures, finite CRT conditional means, the exact single-prime $L^2$ projection, the independent finite Euler-pair product, and a finite actual-totient phase-energy check. The already governed full-series test suite covers independent CRT recomputation, variance inequalities, offset-cancellation rejection, positive-definite matrix identities, actual phase-energy checks and rational full-series adversaries.

Classical source context: Balasubramanian, Giri and Srivastav, *On correlations of certain multiplicative functions*, J. Number Theory 174 (2017), 221–238, DOI 10.1016/j.jnt.2016.10.001. The finite-dimensional positive-definiteness deduction and the phase inequalities are presented with elementary proofs; the underlying classical shifted correlation results are **not newly attributed to GCL**. Dedicated literature comparison is needed before any originality assertion.

| Claim | Governing disposition |
| --- | --- |
| Exact conditional CRT projection, Theorem A | Self-contained bounded proof; independent finite checks required |
| Local positive-definite covariance and Fourier-gap Theorems B/C | Mathematical manuscript proof; proof replay not a MATHCERT certification |
| Weighted Cook 10% saving for all fixed shifts | OPEN |
| Cook good-base 603X/1000 estimate, original full irrationality | OPEN |
| Independent human theorem review, formal Lean replay, MATHCERT | NOT_SUBMITTED |

**Research consequence:** Every finite local shifted-totient difference observable is nondegenerate, but Cook's irrationality strategy demands *nonlocal*, multiscale weighted cancellation. The next substantive producer must make this transition, not silently reuse fixed-dimensional estimates at growing depth.
