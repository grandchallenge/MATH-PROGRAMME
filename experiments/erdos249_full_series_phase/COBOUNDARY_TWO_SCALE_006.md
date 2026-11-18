# Erdős #249 — WP06: dyadic coboundary rational controls and moving-depth feasibility

**Work package:** ERDOS-249-S-WP06/1  
**Issue:** [MATH-PROGRAMME #3495](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3495)  
**Record date:** 2026-11-18  
**Original problem status:** OPEN  
**Certification:** NOT_SUBMITTED  
**Research class:** bounded mathematical negative control and necessary-depth theorem, without novelty or independent-human-review claims.

## Source custody and relationship to prior results

Erdős #249 asks whether

$$
S=\sum_{n=1}^{\infty}\frac{\varphi(n)}{2^n}
$$

is irrational. The source lock is [manifest 0249](../../governance/erdos_proof_verification/manifests/0249.json). Previous GCL [WP04](MOBIUS_SIGNED_TAIL_DENOMINATOR_004.md) and [WP05](MOVING_DEPTH_CRT_PULSE_005.md) concern, respectively, a signed Möbius rational approximation barrier and an obstruction to using the same depth for forced congruence and infinite-tail certification.

Will Cook, *The Binary Totient Series* (2026, revised 1 October 2026), gives a conditional prime-pulse route in Proposition 6.70 and an *equivalent cofinal quantified condition* in Proposition 6.71. Those are existing contributions; neither the source's open arithmetic input nor the full irrationality conjecture is proved by GCL here. The paper also develops several rational controls, including parity and carry-rank negative examples. This packet supplies an explicit **additional bounded-coefficient coboundary control for prime pulses**, without claiming independent priority or novelty. See [Cook's long paper](https://wcook04.github.io/plectis/maths/papers/erdos249-totient-reasoning-surface--chapter-f5a03d171ab5.html), [existing GCL WP05](MOVING_DEPTH_CRT_PULSE_005.md), and the source catalogue [#249](https://www.erdosproblems.com/249).

## Theorem A — a rational full series with cofinal prime pulses

**Statement.** Fix any nonempty finite set $\mathcal H$ of positive integers. There is a sequence of nonnegative integers $(a_n)_{n\ge1}$ with

$$
0\le a_n\le n\qquad(n\ge1),
$$

whose full dyadic sum is the **exact rational number**

$$
\boxed{\sum_{n=1}^{\infty}\frac{a_n}{2^n}=\frac8{255},}
$$

and such that for infinitely many arbitrarily large primes $p\equiv3\pmod4$,

$$
\boxed{
a_{p+4h}-a_p\equiv2\pmod4
\qquad\text{simultaneously for all }h\in\mathcal H.
}
$$

In particular, cofinal prime-position modulo-four pulses, nonnegative integer coefficients and an upper coefficient bound by $n$ **do not together imply irrationality** of a binary series. This does not refute any totient-specific condition in Cook's work; its stronger test controls candidate infinite-tail integer values, not only finite pulses.

**Proof.** Let $H_*=\max\mathcal H$. Choose an infinite increasing sequence of primes $p_j\equiv3\pmod4$, each greater than 11, with

$$
p_{j+1}>p_j+4H_*+8.
$$

There are infinitely many primes congruent to three modulo four (by the elementary Euclidean argument, or Dirichlet's theorem), hence this sparse selection is possible.

Define a binary support sequence $b_0=0$ and, for $n\ge1$, let

$$
b_n=
\begin{cases}
1 &\text{if }n=p_j+4h-1\text{ for some }j\ge1,\ h\in\mathcal H,\\
0 &\text{otherwise.}
\end{cases}
$$

All support indices satisfy $n\equiv2\pmod4$ and are at least 14. The chosen gaps make each pulse position isolated from the other prime windows. Put

$$
\boxed{a_n=4\left\lfloor\frac n8\right\rfloor+2b_{n-1}-b_n.}
$$

For $n<8$ the base term is zero and both binary terms vanish, so $a_n=0$. For $n\ge8$, the base term is at least four and at most $n/2$, while $-1\le2b_{n-1}-b_n\le2$. Consequently $0\le a_n\le n$. These bounds do not use the prime property.

The infinite series converges absolutely because $a_n\le n$. The coboundary partial sums telescope **exactly**:

$$
\begin{aligned}
\sum_{n=1}^{N}\frac{2b_{n-1}-b_n}{2^n}
&=\sum_{n=0}^{N-1}\frac{b_n}{2^n}
-\sum_{n=1}^{N}\frac{b_n}{2^n}\\
&=b_0-\frac{b_N}{2^N}
=-\frac{b_N}{2^N}.
\end{aligned}
$$

Since $0\le b_N\le1$, the infinite coboundary contribution is zero. Independently, the standard generating-function identity

$$
\sum_{n\ge1}\left\lfloor\frac n8\right\rfloor x^n
=\frac{x^8}{(1-x)(1-x^8)}
$$

at $x=1/2$ gives

$$
\sum_{n\ge1}\frac{4\lfloor n/8\rfloor}{2^n}
=\frac8{255}.
$$

Finally, fix one selected prime $p=p_j$. Because $p\equiv3\pmod4$, no supported binary index equals $p$ or $p+4h$; the construction and prime-window separation give $b_{p-1}=0$. By construction $b_{p+4h-1}=1$ for every $h\in\mathcal H$. Thus

$$
a_p=4\lfloor p/8\rfloor,
\qquad
a_{p+4h}=4\lfloor(p+4h)/8\rfloor+2,
$$

and their difference is congruent to two modulo four. This holds simultaneously for all $h$ in the finite set and for infinitely many prime positions $p_j$. QED.

**Epistemic boundary:** The sequence depends on the *chosen finite family* $\mathcal H$. No single universal sequence with this construction is claimed to exhibit all shifts simultaneously. In particular it does not satisfy the additional high-two-adic totient divisibilities required in WP05, and is not a counterexample to Cook's sufficient criterion.

## Theorem B — necessary separation of congruence and analytic depths

Suppose $N\ge0$, $H\ge1$, $L,K\ge1$ and the **positive** totient endpoint satisfies

$$
2^K\mid\varphi(N+L).
$$

Then the totient bound $0<\varphi(n)\le n$ gives

$$
N+L\ge\varphi(N+L)\ge2^K.
$$

For the full shifted totient-tail difference

$$
V_{H,N}
=\sum_{j\ge1}\frac{\varphi(N+H+j)-\varphi(N+j)}{2^j},
$$

truncation at depth $L$ gives the standard analytic error enclosure

$$
\left|V_{H,N}
-\sum_{j=1}^{L}\frac{\varphi(N+H+j)-\varphi(N+j)}{2^j}\right|
\le \frac{N+H+L+2}{2^L}.
$$

The inequality follows from $|\varphi(N+H+j)-\varphi(N+j)|\le N+H+j$ (both terms are nonnegative and at most their respective arguments), together with the elementary geometric sums.

**No-go corollary.** If $L\le K$, the displayed *analytic upper bound* satisfies

$$
\boxed{
\frac{N+H+L+2}{2^L}
\ge\frac{2^K+H+2}{2^L}>1.
}
$$

So any proof strategy requiring the **standard upper bound** to be less than one is impossible at the same or shallower depth, even when the prime position and the depth move together to infinity. This does **not** imply the actual tail is larger than one. The failure concerns this specific sufficient upper-bound criterion, not all conceivable sharper analytic methods.

More generally, this standard upper bound can be less than one only if

$$
2^L>N+H+L+2.
$$

This requires $L>K$ under the endpoint-divisibility premise, and asymptotically demands that $L$ exceed $\log_2 N$ by a margin. This condition is **sufficient for that particular upper bound to be less than one** but is **not sufficient for irrationality**, nor for the finite residue to lie away from all integers.

The finite depth and the congruence-forcing depth must therefore be separated. In WP05's forward CRT construction, the finite front was deliberately made integral when $K\ge L$. Theorem B explains why the *same setup* cannot simultaneously make the trivial infinite-tail error bound small.

## A quantitative exact two-scale residue test (known source logic)

For integer coefficients with $0\le a_n\le n$, write

$$
D(H,N,L)=
\sum_{j=1}^{L}2^{L-j}
(a_{N+H+j}-a_{N+j})\in\mathbb Z,
$$

and let $r$ be its least residue modulo $2^L$. If

$$
N+H+L+2<\min(r,2^L-r),
$$

then the **full infinite shifted-tail difference is nonintegral**, because the finite rational part is farther from every integer than the proven error. This is an elementary symmetric sufficient test, and a weaker version of Cook's optimized directed criterion; it is included only as a reference implementation contract. Its universal cofinal occurrence for the actual totient coefficients is **unproved**, and repeating it does not count as a new theorem.

For the rational control constructed in Theorem A, any proposed shift compatible with the rational denominator must ultimately **fail** a genuinely sound exclusion criterion. A passing comparator cannot be inferred from a single arbitrary finite-window pulse.

## Executable verification and claim ledger

Source: [rational_pulse_coboundary.py](rational_pulse_coboundary.py).  
Hostile tests: [test_erdos249_rational_pulse_coboundary.py](../../tests/test_erdos249_rational_pulse_coboundary.py).

The deterministic test suite uses independent trial-division primality checks, exact fractions, rational generating-function identity, full coefficient bound over multiple sparse prime windows, telescoping partial sums, overlapping finite shift families, invalid-input rejection, and explicit two-scale arithmetic conditions. It does **not** use finite sampling to prove the infinite Dirichlet consequence.

| ID | Result | Evidence and limit |
| --- | --- | --- |
| WP06-A | Cofinal finite-family prime pulses compatible with rational full value $8/255$ and $0\le a_n\le n$ | Complete manuscript proof; finite exact fixtures; no novelty asserted |
| WP06-B | A positive totient endpoint divisible by $2^K$ forces the standard tail bound above one if $L\le K$ | Complete elementary proof; not a lower bound on actual tail |
| WP06-C | Exact binary coboundary partial sum $-b_N/2^N$ | Telescoping equality; exact-fraction checks |
| WP06-D | Universal cofinal shifted-tail residue exclusion for the **actual totient** series | **NOT PROVED** |
| ORIGINAL-249 | Irrationality of $S$ | **OPEN** |

**Next substantive producer (WP07 or continuing WP06 arithmetic phase):** Find a **totient-specific** finite-to-infinite bridge at depth $L>K$ with $2^L>N+H+L+2$ and a nontrivial, cofinal lower bound on the *distance of the exact finite residue to the nearest multiple of $2^L$*. The quantifiers must cover every hypothetical rational denominator period. Compare against Cook's existing equivalent condition and refute all proposed generic implications using the bounded rational prime-pulse construction. This is a substantive evidentiary gap, not an infrastructure or administrative issue.
