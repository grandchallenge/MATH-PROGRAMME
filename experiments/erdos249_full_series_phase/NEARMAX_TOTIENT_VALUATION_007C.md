# Erdős #249 — WP07-C: sparse near-maximal two-adic totient valuations

**Research workstream:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500)  
**Record:** ERDOS-249-S-WP07-C/1  
**Date:** 2026-11-18 UTC  
**Claim class:** self-contained elementary manuscript theorem, exact finite adversarial tests, no theorem-priority or certification claim  
**Original Erdős #249 full-series irrationality:** **OPEN**

## 1. Why this is a separate, totient-specific target

The preceding [WP07-A](MOVING_LOGLOG_INTEGRALITY_007.md) shows that actual totient finite tails are termwise integral at almost all starts at depths $L=\alpha\log\log X$, using a classical moment estimate. [WP07-B](NEARLOG_RATIONAL_CONTROL_007B.md) constructs a *synthetic rational* integer-coefficient series in which all finite tails are termwise integral at **every** start and at depths $\lfloor\log_2N\rfloor-5$. A useful positive obligation is therefore to test what actual Euler-totient arithmetic prohibits at such nearly analytic depths.

This packet proves an **unconditional sparsity theorem** for actual $\varphi(n)$, using only prime factorization, a generating-function counting bound, and elementary inequalities. It is not a claim that the complete dyadic totient series is irrational or that integrality of the **sum** of a finite window is rare. Internal cancellation between nonintegral summands is not excluded.

A relevant antecedent is Jun-Jia Zhao, *p-Adic Valuation of Euler's Totient Function* (Bulletin of the Malaysian Mathematical Sciences Society, 2025, DOI: [10.1007/s40840-025-01869-7](https://doi.org/10.1007/s40840-025-01869-7)), which treats extremal prime-adic valuations, including characterization of exact maximum at $p=2$. We do **not** claim novelty or mathematical priority for the present near-extremal counting argument.

## 2. Theorem A — fixed-distance near-maximum valuations are subpolynomially rare

Fix an integer $C\ge0$. For real $X\ge2$ define

$$
E_C(X)=
\left\{
n\in\mathbb Z:
1\le n\le X,\quad
\nu_2(\varphi(n))\ge\lfloor\log_2n\rfloor-C
\right\}.
$$

Let $B=2^{C+1}$ and $R=\lfloor\log_2X\rfloor$. Define the finite constant

$$
D_B=\prod_{\substack{3\le p\le B\\p\text{ prime}}}
\left(2+\lfloor\log_pB\rfloor\right).
$$

**Theorem A (explicit elementary bound).** For every $C\ge0$ and $X\ge2$,

$$
\boxed{
\# E_C(X)\le (R+1)D_B\exp(2\sqrt{BR}).
}
\tag{A}
$$

In particular, for each fixed $C$,

$$
\boxed{\#E_C(X)\le\exp(O_C(\sqrt{\log X}))=X^{o(1)}.}
$$

A harmless logarithmic factor in the first bound is absorbed by the displayed $O_C$ in the exponent.

**Proof, Step 1: bounded odd part.** Let $n\in E_C(X)$, $k=\lfloor\log_2n\rfloor$, $v=\nu_2(\varphi(n))$, and write $\varphi(n)=2^v u$ with $u$ odd and positive. Since $v\ge k-C$ and $\varphi(n)\le n<2^{k+1}$,

$$
1\le u=\frac{\varphi(n)}{2^v}
<2^{C+1}=B.
\tag{1}
$$

Thus *the odd part of the entire totient is bounded uniformly in $n$*.

**Step 2: restricted odd prime factors.** If an odd prime $p$ divides $n$, the factor $p-1$ divides $\varphi(n)$. Write

$$
p-1=2^{r_p}d_p,\qquad r_p\ge1,\quad d_p\text{ odd}.
$$

Then $d_p$ divides $u$ and so $1\le d_p<B$. Hence

$$
\boxed{p=1+d_p2^{r_p},\quad d_p\text{ odd},\quad d_p<B.}
\tag{2}
$$

For each fixed $r\ge1$, (2) allows at most $B$ candidate odd primes, even *before* testing primality.

If an odd prime $p>B$ divides $n$, it does so only to the first power: otherwise the factor $p^{a-1}$ in $\varphi(p^a)$ would divide the bounded odd part $u$, which is impossible. For each smaller odd prime $p\le B$, its exponent $a_p$ in $n$ has at most $2+\lfloor\log_pB\rfloor$ possibilities, including exponent zero. Therefore all small-odd-prime exponents together have at most $D_B$ possible patterns.

The exponent of 2 in $n$ has at most $R+1$ possibilities because $n\le X$.

**Step 3: count permitted large-prime subsets.** Consider the distinct large odd prime factors $p>B$. Since every such $p=1+d_p2^{r_p}>2^{r_p}$,

$$
\sum_{p\mid n,\ p>B}r_p
\le \log_2 n\le R.
\tag{3}
$$

At each level $r$ there are at most $B$ eligible primes. Hence the number of possible subsets satisfying (3) is bounded by the sum of coefficients of degrees at most $R$ in the nonnegative-coefficient generating series

$$
G(t)=\prod_{r\ge1}(1+t^r)^B.
$$

For any real $s>0$, use $t=e^{-s}$ to obtain

$$
\begin{aligned}
\sum_{j=0}^{R}[t^j]G(t)
&\le e^{sR}G(e^{-s})\\
&\le\exp\left(sR+
B\sum_{r\ge1}e^{-sr}\right)\\
&=\exp\left(sR+\frac{B}{e^s-1}\right)
\le\exp\left(sR+\frac Bs\right).
\end{aligned}
$$

Set $s=\sqrt{B/R}$ (valid because $R\ge1$). This gives $\exp(2\sqrt{BR})$.

Multiplying the bounds for the exponent of two, the finitely many small odd primes, and the large-prime subset proves (A). Finally $B$ and $D_B$ are constants depending only on $C$, while $R=O(\log X)$, so the bound is $X^{o(1)}$. QED.

## 3. Corollary B — almost no actual totient windows enjoy termwise near-logarithmic integrality

Fix any integer $C\ge0$ and take sufficiently large $X$ that $L=\lfloor\log_2 X\rfloor-C\ge1$ and $L\le X$. In $[X,2X)$ define the *termwise integral* starting positions

$$
\mathcal G_{X,L}=
\left\{
N\in\mathbb Z\cap[X,2X):
2^j\mid\varphi(N+j)\quad
(1\le j\le L)
\right\}.
$$

Then

$$
\boxed{
\#\mathcal G_{X,L}
\le \# E_{C+2}(3X)
\le \exp(O_C(\sqrt{\log X}))
=X^{o(1)}.
}
\tag{B}
$$

**Proof.** Termwise integrality at $N$ implies in particular

$$
\nu_2(\varphi(N+L))\ge L.
$$

Set $k=\lfloor\log_2X\rfloor$ and $n=N+L$. Since $N<2X$ and $L\le X$, $n<3X$. Also $X<2^{k+1}$ implies $3X<2^{k+3}$, so

$$
\lfloor\log_2n\rfloor\le k+2.
$$

Consequently

$$
\nu_2(\varphi(n))\ge k-C
\ge \lfloor\log_2n\rfloor-(C+2),
$$

hence $n\in E_{C+2}(3X)$. Distinct starting positions give distinct $n=N+L$. Apply Theorem A at $3X$. QED.

**Crucial scope firewall.** This says **termwise** integrality in an almost-logarithmic window is extremely rare for actual totients. It does not assert rarity of an **integral sum** $\sum_{j=1}^L\varphi(N+j)/2^j$: distinct nonintegral rational summands may cancel modulo one. Indeed the previously protected [WP07-A exact tests](../../tests/test_erdos249_moving_loglog_integrality.py) show such cancellation already at $N=1,L=2$. Neither (A) nor (B) establishes a fractional-part gap for the infinite scaled tail.

## 4. Theorem C — rare adjacent integral *finite sums* at near-logarithmic depth

Corollary B concerns individual terms, and by itself does not control cancellation among fractions. The following result directly constrains **integrality of the entire finite sum**.

For $X$ large, fix $C\ge0$ and $L=\lfloor\log_2X\rfloor-C\ge1$. Define the exact integer numerator

$$
A_{N,L}=\sum_{j=1}^{L}2^{L-j}\varphi(N+j),
\qquad U_{N,L}=\frac{A_{N,L}}{2^L}.
$$

**Theorem C (adjacent-integrality obstruction).** Among starting positions $N\in[X,2X)$, the number of indices for which **both** $U_{N,L}$ and $U_{N+1,L}$ are integers is at most

$$
\boxed{
\#E_{C+2}(3X)=X^{o(1)}.
}
\tag{C1}
$$

Consequently the number of starts at which the **whole** finite sum $U_{N,L}$ is an integer satisfies

$$
\boxed{
\#\{N\in[X,2X): U_{N,L}\in\mathbb Z\}
\le\frac X2+X^{o(1)}+O(1).
}
\tag{C2}
$$

Thus at least half of these starting positions, asymptotically, have a **nonintegral finite sum** at the near-logarithmic depth, regardless of cancellation among individual terms.

**Proof.** The numerator has an exact sliding-window recurrence, obtained by multiplying by two and removing the first summand:

$$
\boxed{
A_{N+1,L}=2A_{N,L}-2^L\varphi(N+1)+\varphi(N+L+1).
}
\tag{4}
$$

If both neighboring finite tails are integral, then both numerators are divisible by $2^L$. Reducing (4) modulo $2^L$ gives

$$
2^L\mid\varphi(N+L+1).
$$

Set $k=\lfloor\log_2X\rfloor$ and $n=N+L+1$. Since $N<2X$, and $L+1\le X$ for all sufficiently large $X$, we have $n<3X$ and $\lfloor\log_2n\rfloor\le k+2$. Consequently

$$
\nu_2(\varphi(n))\ge L=k-C
\ge\lfloor\log_2n\rfloor-(C+2).
$$

Thus $n\in E_{C+2}(3X)$ and the map $N\mapsto n=N+L+1$ is injective. Theorem A proves (C1).

For (C2), divide the $X+O(1)$ integer starting positions into disjoint consecutive pairs (and at most one singleton). Each pair contains **at most one** integral sum unless that adjacent pair belongs to the exceptional family counted in (C1). Therefore the total number of integral finite sums is at most $\lceil X/2\rceil+\#E_{C+2}(3X)$ for integer $X$, and the stated asymptotic follows for real $X$ after endpoint adjustment. QED.

**Exact scope and remaining obstruction.** The theorem proves actual **nonintegrality**, not a uniform lower bound on the distance of the finite sum from the nearest integer. The smallest possible nonzero fractional part has denominator $2^L$ and can be as small as $2^{-L}$, which tends to zero at the present depth. The standard bound on the discarded **infinite** tail is not yet smaller than this distance, and no total infinite-tail residue gap has been proved. No all-harmonic Fourier saving follows just from nonintegrality at half the starts.

## 5. Quantitative comparison with the rational control and what remains open

The synthetic rational sequence in [WP07-B](NEARLOG_RATIONAL_CONTROL_007B.md) has coefficient valuations $\nu_2(a_n)\ge\lfloor\log_2n\rfloor-5$ **for all sufficiently large $n$**, and its full sum is rational $2/3$. Theorem A proves that the actual totient function can reach valuations within five of $\lfloor\log_2n\rfloor$ at only $X^{o(1)}$ indices up to $X$.

This is a genuine structural distinction between Euler's totient and the constructed rational sequence, not simply a generic series countermodel. But the original irrationality conjecture concerns the entire value

$$
S=\sum_{n\ge1}\varphi(n)2^{-n},
$$

not the density of isolated high-valuation coefficients. To exploit the distinction, a new argument must transfer sparse high valuations to a **nontrivial cofinal residue gap** for the complete moving-depth sum, or directly to the good-base Fourier cancellation specified in Will Cook's 2026 sufficient conditions. Such a transfer is **not provided** by this theorem and must not be inserted by analogy.

## 6. Executable tests, review and claim ledger

Implementation: [nearmax_totient_valuation.py](nearmax_totient_valuation.py). Tests extend the **already registered** [full-series test module](../../tests/test_erdos249_full_series_phase.py), keeping existing tests intact and avoiding a new full-fanout policy manifest modification. The module uses exact integer arithmetic, independent Euler-totient reconstruction, prime-factor enumeration, finite generating-function counting and explicit hostile bounds. Finite tests do not prove an $X\to\infty$ asymptotic; the manuscript proof does.

| Claim | Authority | Status |
| --- | --- | --- |
| WP07-C-A | Count near-maximal $\nu_2(\varphi(n))$ by bounded odd part and weighted prime-factor choices | Self-contained elementary manuscript theorem |
| WP07-C-B | Actual totient termwise integrality at $L=\lfloor\log_2 X\rfloor-C$ occurs on at most $X^{o(1)}$ starting positions | Consequence of WP07-C-A |
| WP07-C-C | Adjacent integral full finite sums at near-log depth occur at only $X^{o(1)}$ starts; at most half of starts have an integral finite sum asymptotically | Exact sliding-window recurrence plus WP07-C-A |
| WP07-C-N | A nonintegral finite sum may still lie within $2^{-L}$ of an integer; the discarded infinite tail is not controlled to that precision | Explicit mathematical scope qualification |
| WP07-OPEN | Totient-specific cofinal harmonic saving or full infinite-tail residue exclusion | **OPEN** |
| ORIGINAL-249 | Irrationality of original full binary totient sum | **OPEN** |

**Review/claim restrictions:** No claim that this near-extremal theorem is historically novel, formally Lean-verified, independently human-reviewed, externally certified, or that it solves the original problem. Preserve the original source-and-priority record. Close only *bounded evidence admission* after exact protected readback, not parent #3500 or parent #3201.
