# Erdős #249 — WP08-B: moving-prime escape and the exact sparse totient pulse

**Research workstream:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500)  
**Programme:** ERDOS-249-S-WP08-B/1  
**Date:** 2026-11-19 UTC  
**State:** noncertifying mathematical source proof plus independent exact-integer arithmetic checks. Original Erdős #249 **OPEN**; MATHCERT **NOT_SUBMITTED**.

## 1. Objective and exact antecedents

Protected [WP08-A](OVERLOG_PHASE_SEPARATION_008.md) proved that each **fixed** omitted prime produces a phase discrepancy between the actual totient and a finite-prime rational Euler approximation. Its constants deteriorate as the prime support grows. This packet attacks precisely that loss by **moving the prime cutoff with the observation scale** and combining *many* omitted primes simultaneously.

The principal output is an explicit, growing-prime, over-logarithmic phase-escape bound on $\asymp X/\log y$ starting positions, with a gap at least $1/(192y)$. It is a quantitative arithmetic result about the **actual** Euler totient. It is not yet a uniform positive constant as $y\to\infty$, not a one-sided gap against the complete infinite tail, and not a proof of original irrationality.

The only external classical inputs to the asymptotic corollary are the well-known prime number theorem and the elementary mean

$$
\sum_{m\le T}\frac{\varphi(m)}m=\frac6{\pi^2}T+O(\log T).
\tag{1}
$$

The exact finite theorem below does not require the prime number theorem, and the mean estimate is proved from the standard divisor identity in [WP08-A](OVERLOG_PHASE_SEPARATION_008.md). No new priority claim is made for the standard prime number theorem, finite Möbius rational approximation, or the method of summing primes.

## 2. Setup, domain and the exact pulse identity

Let $X\ge64$ be an integer, choose an integer $y\ge2$ such that

$$
\boxed{y^2>3X,}
\tag{2}
$$

and put

$$
L=\lfloor\log_2X\rfloor+4,\qquad Q=2^L,\qquad
8X<Q\le16X.
$$

Let $P_y$ be the finite set of primes at most $y$, and set

$$
g_y(n)=n\prod_{\substack{p\mid n\\p\le y}}(1-1/p).
$$

Every $g_y(n)$ is a nonnegative integer, and $g_y(n)\ge\varphi(n)$. The **entire infinite** binary sum of this finite-prime approximation is rational, by the already protected WP08-A finite Euler formula:

$$
\boxed{
S_y=\sum_{n\ge1}\frac{g_y(n)}{2^n}
=\sum_{d\mid\prod_{p\le y}p}\mu(d)\frac{2^d}{(2^d-1)^2}
\in\mathbb Q.
}
\tag{3}
$$

Define the residual coefficient $D_y(n)=g_y(n)-\varphi(n)\ge0$.

**Theorem A (exact sparse large-prime pulse).** If $1\le n<3X$ and (2) holds, then

$$
\boxed{
D_y(n)=
\begin{cases}
\varphi(n/p),&\text{if }n\text{ has a prime divisor }p>y,\\
0,&\text{if all prime divisors of }n\text{ are }\le y.
\end{cases}
}
\tag{4}
$$

The omitted prime $p$ in the first case is unique.

**Proof.** Two distinct omitted primes, or two copies of the same omitted prime, would give $n\ge p_1p_2>y^2>3X$, impossible. Hence any omitted prime $p>y$ occurs to exponent one and is unique. Set $m=n/p$. Then $m<3X/y<y<p$, so every prime divisor of $m$ belongs to $P_y$, and $p\nmid m$. Consequently the finite-prime Euler product for $g_y$ includes **exactly** the Euler factors of $m$:

$$
g_y(pm)=p\varphi(m),\qquad
\varphi(pm)=(p-1)\varphi(m).
$$

Subtracting gives $D_y(pm)=\varphi(m)$. If there is no omitted prime, the full and truncated Euler products agree exactly. QED.

The identity contains **no probability approximation**, no assumption that a particular large integer is prime, and no prime independence hypothesis. It is stronger than merely bounding a missing-prime factor.

## 3. Exact finite effective theorem: simultaneous prime escape

Let

$$
I_X=[X+L+1,\,2X+L-1]\cap\mathbb Z.
$$

For $N\in[X,2X)$ define the complete finite difference of actual totient and the rational finite-prime comparator

$$
W_{N,L}=\sum_{j=1}^{L}\frac{\varphi(N+j)-g_y(N+j)}{2^j}.
$$

Define the set of **good prime pulses**

$$
\mathcal G_{X,y}=
\left\{
n\in I_X:
n=pm,\quad y<p\le2y,\quad p\text{ prime},\quad
2\varphi(m)\ge m
\right\}.
$$

Because $n<3X$ and $y^2>3X$, the representation $n=pm$ above is **unique** for each good endpoint.

**Theorem B (effective all-primes simultaneous phase escape).** For every pair of integers $X,y$ satisfying (2),

$$
\boxed{
\#\left\{
N\in[X,2X):
\|W_{N,L}\|_{\mathbb R/\mathbb Z}
\ge\frac1{192y}
\right\}
\ \ge\ \frac12\,\#\mathcal G_{X,y}.
}
\tag{5}
$$

This is an exact, unconditional finite statement with no asymptotic error or prime-number theorem.

**Proof.** Write the integer numerator of the difference as

$$
A_N=\sum_{j=1}^L2^{L-j}
\bigl(\varphi(N+j)-g_y(N+j)\bigr)
$$

and let $r_N$ be its centered representative modulo $Q$, so $\|W_{N,L}\|_{\mathbb R/\mathbb Z}=|r_N|/Q$. The exact sliding recurrence of WP08-A gives

$$
r_{N+1}-2r_N\equiv\varphi(N+L+1)-g_y(N+L+1)\pmod Q.
\tag{6}
$$

Take $n=pm\in\mathcal G_{X,y}$ and $N=n-L-1$. By Theorem A, its right side is **exactly** $-\varphi(m)$, and

$$
\varphi(m)\ge m/2=\frac{n}{2p}
\ge\frac X{4y}.
\tag{7}
$$

Suppose both $|r_N|<X/(12y)$ and $|r_{N+1}|<X/(12y)$. Then the integer $z=r_{N+1}-2r_N$ satisfies

$$
|z|<\frac X{4y}\le\varphi(m).
$$

The integer $z+\varphi(m)$ is therefore nonzero, yet by (6) is divisible by $Q$. Moreover the exact pulse identity gives

$$
0<|z+\varphi(m)|
\le|z|+\varphi(m)
<\frac X{4y}+\frac{3X}y
<Q,
$$

contradicting divisibility by $Q$. Therefore one of the two adjacent starts has $|r|\ge X/(12y)$, hence fractional distance at least

$$
\frac{X}{12yQ}\ge\frac1{192y}.
$$

The map $n\mapsto(N,N+1)$ produces $\#\mathcal G_{X,y}$ adjacent pairs of starting positions. Every start is covered by **at most two** such pairs, regardless of whether the good endpoints are consecutive. Thus at least half as many distinct starts satisfy the phase-gap inequality. QED.

**Important:** Theorem B concerns differences from a *moving rational comparator*, not the full series itself, and its threshold shrinks when $y$ grows. Its verification does **not** require computing the enormous rational denominator of $S_y$.

## 4. Asymptotic cross-prime amplification

Put

$$
\beta=\frac{12}{\pi^2}-1>0.
$$

For a fixed $\varepsilon$ with $0<\varepsilon<1/4$, choose an integer cutoff $y=y(X)$ in the uniform range

$$
\boxed{
X^{1/2+\varepsilon}\le y\le X^{1-\varepsilon}.
}
\tag{8}
$$

For sufficiently large $X$, this guarantees (2), and every $p\in(y,2y]$ has $X/p\to\infty$ uniformly in the range.

**Theorem C (moving-prime escape at logarithmic-density scale).** Uniformly over (8), as $X\to\infty$,

$$
\boxed{
\#\left\{
N\in[X,2X):
\|W_{N,L}\|_{\mathbb R/\mathbb Z}
\ge\frac1{192y}
\right\}
\ge
\left(
\frac{\beta\log 2}{2}+o(1)
\right)\frac{X}{\log y}.
}
\tag{9}
$$

The asymptotic leading constant is approximately $0.0748$.

**Proof.** Fix a prime $p\in(y,2y]$. The indices $m$ with $pm\in I_X$ form a consecutive integer interval of length $X/p+O(1)$, whose upper endpoint is $O(X/p)$. From (1), subtracting the two summatory estimates gives

$$
\sum_{\substack{m\\pm\in I_X}}
\frac{\varphi(m)}m
=\frac6{\pi^2}\frac Xp+O(\log X).
$$

Let $h_p$ be the number of these $m$ satisfying $\varphi(m)/m\ge1/2$. Since $\varphi(m)/m\le1$, while every other ratio is below $1/2$, we get

$$
h_p\ge \beta\frac Xp-O(\log X).
\tag{10}
$$

Uniqueness of the large prime in Theorem A means these good endpoint sets for distinct $p$ do not overlap. Hence

$$
\#\mathcal G_{X,y}
\ge\beta X\sum_{y<p\le2y}\frac1p
-O\bigl(\pi(2y)\log X\bigr).
\tag{11}
$$

The **classical prime number theorem** gives

$$
\sum_{y<p\le2y}\frac1p
=\frac{\log2+o(1)}{\log y},
\qquad
\pi(2y)=O(y/\log y).
$$

The error in (11) is $O(y\log X/\log y)$, which is $o(X/\log y)$ because $y\le X^{1-\varepsilon}$. Therefore

$$
\#\mathcal G_{X,y}
\ge\bigl(\beta\log2+o(1)\bigr)\frac X{\log y}.
$$

Apply the exact finite Theorem B to get (9). This argument is **uniform** over the stated moving range; no additional hypothesis about independent prime events was used. QED.

**What improved relative to WP08-A:** A single missing prime near $y$ contributes only about $X/y$ local witnesses. Counting all primes in $(y,2y]$ and exploiting the exact unique-pulse decomposition increases the provable count to order $X/\log y$. Furthermore the phase-gap threshold is explicitly $1/(192y)$ rather than the weaker $c_{P_y}/(96y)$ obtained by applying WP08-A to one missing prime and discarding its precise residual structure. This is a simultaneous growing-support theorem; it is **not** a fixed positive-density theorem independent of $y$.

## 5. Rational approximation and hostile scope checks

**Theorem D (strict finite-prime rational upper approximation).** For every finite integer $y\ge2$,

$$
\boxed{
S<S_y<S+\frac{y+2}{2^y}.
}
\tag{12}
$$

**Proof.** $g_y(n)=\varphi(n)$ for all $n\le y$, and $0\le g_y(n)-\varphi(n)<n$ for all $n$. For every prime $p>y$, $g_y(p)=p$ and $\varphi(p)=p-1$, so the total difference of the infinite series is strictly positive. The upper bound follows from the elementary geometric identity

$$
\sum_{n>y}\frac n{2^n}=\frac{y+2}{2^y}.
$$

Together with the exact rationality of $S_y$ in (3), this is a complete infinite approximation statement, but the denominator of $S_y$ is **not** bounded at a useful scale for a rationality contradiction. QED.

**Hostile rational patch.** For any fixed finite $X,y$, define a comparator $a^{X,y}_n$ equal to $\varphi(n)$ on the finite index interval $[X+1,\,2X+L]$ and equal to $g_y(n)$ elsewhere. It differs from the **rational** $g_y$ sequence at only finitely many indices, so the full series $\sum_n a^{X,y}_n2^{-n}$ is still rational. Yet all length-$L$ finite tails starting at $N\in[X,2X)$ agree with those of the **actual** totient **exactly as real numbers**, not only in phase. This adversary depends on $X,y$ and does **not** disprove a single cofinal all-$X$ irrationality criterion; it prevents the finite-block observation (9) from being promoted to an unconditional irrationality proof.

## 6. Remaining genuine boundary

The relevant actual infinite-tail estimate remains

$$
0<\sum_{j>L}\frac{\varphi(N+j)}{2^j}
<\frac{N+L+2}{2^L}.
$$

Theorem C forces a **growing number** of large-prime phase discrepancies at over-logarithmic depth, but their guaranteed magnitude is only $1/(192y)$, which tends to zero, while the generic omitted-tail bound remains of constant order at $L=\lfloor\log_2X\rfloor+4$. The growing finite-prime comparator $S_y$ is rational for each $y$ and its denominator grows without a usable uniform bound. This does **not** produce the denominator-uniform, one-sided cofinal separation necessary for the original irrationality proof.

The next positive task is to combine the exact pulse decomposition with a **joint distributional bound** on the *discarded* prime-pulse tail, or extract a phase-sign condition that survives the full shifted totient remainder for **each hypothetical rational denominator**. This must be proved for the actual full sequence and checked against the rational patch and WP07-E universal phase mimic. Only then could one promote beyond WP08-B.

## 7. Claim ledger

| Claim | Disposition |
| --- | --- |
| WP08-B-A: exact large-prime pulse $g_y(n)-\varphi(n)=\varphi(n/p)$ in the single-large-prime regime | Elementary manuscript proof |
| WP08-B-B: exact effective finite-phase escape at threshold $1/(192y)$ on at least half the good prime-pulse endpoints | Elementary manuscript proof, exact integer checks |
| WP08-B-C: moving support $X^{1/2+\varepsilon}\le y\le X^{1-\varepsilon}$ supplies $\Omega(X/\log y)$ phase-separated starts | Classical totient mean plus prime number theorem, no novelty claim |
| WP08-B-D: finite-prime rational sums approximate actual full sum strictly from above with error below $(y+2)/2^y$ | Elementary exact generating-function argument |
| WP08-B-N: phase escape alone implies irrationality | **FALSE as a generic inference**; exact finite rational patch |
| Original Erdős #249, cofinal full-series one-sided denominator-uniform separation | **OPEN** |
| Independent authentication, external theorem priority, Lean/MATHCERT certification | **NOT_CLAIMED / NOT_SUBMITTED** |

The executable artifact [moving_prime_escape.py](moving_prime_escape.py) and hostile tests extend the existing governed [full-series test file](../../tests/test_erdos249_full_series_phase.py). Tests supply exact finite reproduction, not certification of an infinite asymptotic. No new CI route, branch-protection rule, role, reviewer identity or workflow is required.

**Governance:** On protected merge only, record a bounded WP08-B admission receipt on the existing research [issue #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500); leave issue, GCL Project #2, parent #3201 and original Erdős #249 OPEN/In Progress; MATHCERT NOT_SUBMITTED.
