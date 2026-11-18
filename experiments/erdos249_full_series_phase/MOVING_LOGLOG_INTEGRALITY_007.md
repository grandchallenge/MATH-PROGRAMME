# Erdős #249 — WP07-A: logarithmically moving finite-tail integrality

**Programme:** ERDOS-249-S-WP07/1  
**Research issue:** [MATH-PROGRAMME #3500](https://github.com/grandchallenge/MATH-PROGRAMME/issues/3500)  
**Status:** proved manuscript deduction **conditional only on an established classical analytic-number-theory theorem**; original problem OPEN  
**Claim class:** noncertifying; no priority claim, independent mathematical certification, or Lean proof  
**Date:** 2026-11-18 UTC

## Prior work and exact target

The Erdős #249 conjecture asks whether

$$
S=\sum_{n\ge1}\frac{\varphi(n)}{2^n}
$$

is irrational. The source lock is [manifest 0249](../../governance/erdos_proof_verification/manifests/0249.json).

The existing GCL [full-series investigation 001](README.md) proves that for every **fixed** depth $L$, the truncated scaled totient tails are integers at a density-one set of positions, and their phase averages tend to one. The [WP06 rational control](COBOUNDARY_TWO_SCALE_006.md) shows that generic prime-position pulses do not force irrationality. Will Cook, *The Binary Totient Series* (revised 1 October 2026), Theorem 3.5(b), already supplies a stronger **conditional** harmonic saving on the good-base set, whose unproved cofinal estimate would resolve the original question.

This packet extends GCL's **fixed-depth** integrality analysis to certain **moving depths**. The essential new deduction in this packet is elementary once the following classical moment input is granted. It is not a claim that the analytic-number-theory input or the general phenomenon is newly discovered.

**External classical input: Selberg–Delange for the distinct-prime-factor function.** For fixed $0<z<1$ and $Y\ge3$, the standard Selberg–Delange asymptotic for $z^{\omega(n)}$ gives

$$
\sum_{n\le Y}z^{\omega(n)}
\ll_z Y(\log Y)^{z-1}.
\tag{SD}
$$

Here $\omega(n)$ is the number of distinct prime divisors of $n$. The bound follows from the standard Dirichlet-series factorization

$$
\sum_{n\ge1}\frac{z^{\omega(n)}}{n^s}
=
\prod_p\left(1+\frac{z}{p^s-1}\right)
=\zeta(s)^zG_z(s),
$$

where the Euler product for $G_z$ converges absolutely when the real part of $s$ is greater than $1/2$, away from any chosen branch singularities. The asymptotic (SD) is **cited as an external established theorem** and is not formally or independently reproved by this work package. One published discussion of the classical method is the Selberg–Delange literature; its original theorem and attribution are not GCL results.

## Theorem A — moving-depth density-one integrality with a quantitative rate

Fix $0<\alpha<1$. For sufficiently large real $X$, put

$$
\mu_X=\log\log X,\qquad
L_X=\lfloor\alpha\mu_X\rfloor\ge1,
\qquad
I(\alpha)=1-\alpha+\alpha\log\alpha>0.
$$

Let

$$
U_{N,L_X}=\sum_{j=1}^{L_X}\frac{\varphi(N+j)}{2^j},
\qquad
\mathcal B_X=\{N\in\mathbb Z:X\le N<2X,\ U_{N,L_X}\notin\mathbb Z\}.
$$

Then, counting integers in the interval,

$$
\boxed{
\#\mathcal B_X
\ll_\alpha X\log\log X\,(\log X)^{-I(\alpha)}.
}
$$

More strongly, the same bound holds for the exceptional set on which at least one *individual* term $\varphi(N+j)/2^j$ is nonintegral. Consequently

$$
\boxed{
\sup_{h\in\mathbb Z}
\left|
\frac{1}{\#([X,2X)\cap\mathbb Z)}
\sum_{X\le N<2X}
\exp(2\pi i h U_{N,L_X})-1
\right|
\ll_\alpha
(\log\log X)(\log X)^{-I(\alpha)}
\longrightarrow0.
}
$$

The supremum is over **all** integer harmonics simultaneously; it is not restricted to fixed or polynomially growing $h$.

**Proof.** The Euler product formula

$$
\varphi(n)=\prod_{p^a\Vert n}p^{a-1}(p-1)
$$

implies the pointwise, exact arithmetic inequality

$$
\nu_2(\varphi(n))\ge\omega(n)-1
\qquad(n\ge1).
\tag{1}
$$

Every distinct *odd* prime divisor contributes at least one factor of two, and there is at most one distinct even prime divisor. For $n=1$ and $n=2$ the inequality still holds.

Call a position $N$ **termwise exceptional** if some $j\in\{1,\ldots,L_X\}$ satisfies $2^j\nmid\varphi(N+j)$. By (1) this can occur only if $\omega(N+j)\le L_X$. Fix $z=\alpha$, with $0<z<1$. Since $z^{\omega(n)}\ge z^{L_X}$ whenever $\omega(n)\le L_X$,

$$
\#\{n\le 3X:\omega(n)\le L_X\}
\le z^{-L_X}\sum_{n\le3X}z^{\omega(n)}
\ll_\alpha Xz^{-L_X}(\log X)^{z-1}.
\tag{2}
$$

As $L_X\le\alpha\log\log X$ and $\log z<0$,

$$
z^{-L_X}\le
\exp(-\alpha\log\log X\log\alpha)
=(\log X)^{-\alpha\log\alpha}.
$$

Taking a union bound over at most $L_X$ possible shifts $j$ gives

$$
\#\{\text{termwise exceptional }N\}
\ll_\alpha
X L_X(\log X)^{\alpha-1-\alpha\log\alpha}
\ll_\alpha
X\log\log X(\log X)^{-I(\alpha)}.
$$

Since $\log\alpha<\alpha-1$ for $0<\alpha<1$, $I(\alpha)>0$. Outside the termwise exceptional set every $\varphi(N+j)/2^j$ is an integer, so $U_{N,L_X}\in\mathbb Z$. For any integer $h$, its exponential character equals one at every such good $N$. At every bad $N$ the absolute discrepancy from one is at most two. Dividing the sum by the interval length gives the stated uniform estimate. QED.

**Quantifier firewall.** The depth $L_X$ increases to infinity but only at rate proportional to $\log\log X$. The result **does not** apply at $L$ comparable with $\log_2 X$; it does not imply harmonic cancellation for the true infinite scaled tail. It is a quantified obstruction to replacing the required *moving analytic depth* by the density-one fixed-depth calculation.

## Theorem B — divergent actual remainder at the same moving depth

Define the true scaled tail

$$
U_N=\sum_{j\ge1}\frac{\varphi(N+j)}{2^j}.
$$

For all $N\ge X$ and all sufficiently large $X$,

$$
\boxed{
U_N-U_{N,L_X}
\ge\frac{\sqrt{(N+L_X+1)/2}}{2^{L_X+1}}
\ge\frac{\sqrt X}{2\sqrt2\,(\log X)^{\alpha\log2}}
\longrightarrow+\infty.
}
$$

**Proof.** For every $n\ge1$, the elementary multiplicative inequality

$$
2\varphi(n)^2\ge n
$$

follows prime-power by prime-power from $\varphi(p^a)=p^{a-1}(p-1)$. (It was already proved in [GCL full-series 001](README.md); no new claim is made for that inequality.) The omitted tail is **positive**, and its first term alone gives

$$
U_N-U_{N,L_X}
\ge \frac{\varphi(N+L_X+1)}{2^{L_X+1}}
\ge\frac{\sqrt{(N+L_X+1)/2}}{2^{L_X+1}}.
$$

Finally $L_X\le\alpha\log\log X$, so $2^{L_X+1}\le2(\log X)^{\alpha\log2}$, establishing the explicit lower bound. Since any fixed power of $\log X$ grows more slowly than $\sqrt X$, the lower bound tends to infinity uniformly in $N\ge X$. QED.

By contrast, the standard **upper** enclosure from $\varphi(n)\le n$ is

$$
U_N-U_{N,L}\le\frac{N+L+2}{2^L}.
$$

For that particular upper bound to be less than one at $N\ge X$, it is **necessary** that $2^L>X$, or $L>\log_2X$. Thus the density-one integer regime proven in Theorem A is far shallower than the analytic tail-control regime. Neither a large true **positive** remainder nor an all-harmonic phase collapse of the finite front decides the fractional part of the full remainder.

## Finite proof-obligation reduction and exact tests

For any $X,L\ge1$, let $\mathcal E_{X,L}$ count integer starts $N\in[X,2X)$ for which some $2^j\nmid\varphi(N+j)$, $1\le j\le L$. The elementary steps, without Selberg–Delange, give the valid **finite** bound for every rational $0<z<1$:

$$
\mathcal E_{X,L}
\le
Lz^{-L}
\sum_{n\le3X}z^{\omega(n)}
\tag{3}
$$

provided $L\le X$ (so all $N+j\le3X$). This is a deliberately weak bound at moderate finite $X$; it is *not* a numerical substitute for the external asymptotic theorem.

The executable WP07-A module implements distinct-factor counting, independent totient verification, exact two-adic valuations and rational finite Markov envelopes. Hostile tests verify the pointwise premises, the source's modular-integrality equivalence, the finite upper bound (3), the positive remainder lower bound for fixed finite indices, the rational-series comparator, and the absence of any claim of cofinal irrationality.

## Claim ledger and successor

| Claim | Provenance | Status |
| --- | --- | --- |
| WP07-A | Growing-depth termwise integrality and all-harmonic finite Fourier collapse, for $L_X=\lfloor\alpha\log\log X\rfloor$ | Manuscript proof using **external classical** Selberg–Delange moment bound |
| WP07-B | True omitted positive totient tail diverges uniformly for that same moving depth | Elementary manuscript proof; uses already established lower bound for $\varphi$ |
| WP07-C | Finite deterministic Markov/union envelope and exact arithmetic checks | Manuscript proof and executable fixtures |
| WP07-OPEN | Cook's good-base cofinal fixed Fourier saving at genuine analytic depth $L(X)\asymp\log_2X$ | **UNPROVED** |
| ORIGINAL-249 | Irrationality of the full binary totient series | **OPEN** |

**Next substantive producer:** Derive a totient-specific nonconcentration or harmonic saving at $L$ large enough to control the infinite remainder. Cook's already available Theorem 3.5(b) would suffice if one establishes his remaining unproved good-base bound for each integer $h$ on arbitrarily large blocks $X$. A generic inference from irrationality to phase cancellation, a fixed $L$, the present $\log\log X$ theorem, or further finite scanning is invalid; GCL's [irrational sparse orbit](SPARSE_ORBIT_OBSTRUCTION.md) and [rational prime-pulse comparator](COBOUNDARY_TWO_SCALE_006.md) are mandatory hostile controls.

**Governance boundary:** These manuscript deductions are not Lean-checked here, not independently certified, and not mathematical priority claims. A protected PR can admit WP07-A evidence without closing WP07's positive Fourier producer or the original Erdős #249 research programme.
