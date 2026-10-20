# Erdős #41 — Four-route first falsification tranche: finite overlap is not a future shortage; weak Fourier profiles erase B3

**Date:** 20 October 2026. **Programme:** #2789; specialist tasks #2790 (A), #2793 (D); parent #2622. **Disposition:** two rigorously delimited negative theorems. Neither result disproves Erdős #41, establishes positive lower density for one infinite B3 set, certifies novelty, or supplants the separate independent reviewer #2792.

Throughout, **B3 means uniqueness of sums of unordered three-element multisets, with repetitions allowed**. A pair-sum uniqueness property B2 follows.

## A. Arbitrarily distant, critically populated finite extensions survive an old fourth-order defect

### A1. Exact extension lemma, with all mixed three-sum classes

**Lemma A1 (no finite B3 prefix creates an absolute far-future density shortage).** Let $S\subseteq[1,U]$ and $T\subseteq[1,W]$ be any two nonempty finite, repetition-permitted B3 sets. Set the integer parameters

$$
M=8U+1,\qquad H=8MW+8U,\qquad
Z=\{H+Mt:t\in T\}.
$$

Then $S\cup Z$ is B3. Its new elements lie in the consecutive integer interval $J=[H+1,H+MW]$, which has $L=MW$ integer positions, and $|Z|=|T|$.

**Proof.** Every three-sum has an unambiguous number $r\in\{0,1,2,3\}$ of members drawn from $Z$: terms with $r$ new elements lie in a short interval about $rH$, and $H>3MW+3U$ makes these four ranges disjoint. For a fixed $r$:

- $r=0$: the original B3 property of S applies.
- $r=3$: subtracting $3H$ and dividing by M reduces equality to the B3 property of T.
- $r=1$: equality gives $M(t-t')=(s'_1+s'_2)-(s_1+s_2)$. The right side has absolute value below $2U<M$, forcing $t=t'$ and equality of the two unordered S-pairs by B2.
- $r=2$: equality gives $M[(t_1+t_2)-(t'_1+t'_2)]=s'-s$, whose right side has magnitude below $U<M$; hence the two unordered T-pairs coincide and $s=s'$.

All equality cases are therefore trivial. QED.

### A2. Uniform critical-size descendants from the finite-field moment alphabet

For any prime $p\ge5$, set $B=3p+1$ and

$$
W_p=p(1+B+B^2)+1,\qquad
e_i=1+i+B(i^2\bmod p)+B^2(i^3\bmod p)
\quad(0\le i<p).
$$

The $p$-element set $T_p=\{e_i\}$ is B3: triple sums have no base-$B$ carries; equality of the first three power sums modulo $p$ identifies the underlying triple multiset by Newton identities (division by 2 and 3 is allowed for $p>3$). Since $W_p<12p^3$, its size satisfies $p>(W_p/12)^{1/3}$.

Apply Lemma A1 to **any fixed** finite B3 $S\subseteq[1,U]$ and $T=T_p$, with the same $M=8U+1$ for every p. It produces an interval $J_p$ of $L_p=MW_p$ consecutive integer positions, with $L_p\to\infty$ and

$$
\boxed{
C(S,J_p)\ge |Z_p|=p>
\left(\frac{L_p}{12M}\right)^{1/3}.
}\tag{CRITICAL-FAR-FUTURE-ESCAPE}
$$

Here $C(S,J)$ is the **maximum genuine B3-compatible batch size**, not an entropy surrogate. Thus no theorem involving *only a fixed finite older B3 configuration*, including its mixed-four-sum overlap count, can assert that all sufficiently distant future windows have $o(L^{1/3})$ true extension capacity. Any correct density-shortage theorem must quantify the changing older prefix, the ratio of future location to previous scale, and/or infinitely many stages. The coefficient $(12M)^{-1/3}$ depends on the original S and may become arbitrarily small as S grows; this is **not an infinite fixed-c construction**.

### A3. Direct overlap stress test

For the genuine B3 blocks

$$
P=\{1,2,5,14\},\qquad Y=\{1033,1072,1125,1219\},
$$

put $S=P\cup Y$ and define $T(V)=V+V-V$. The two near reciprocal bands are $Y-T(P)$ and $T(Y)-P$. Their overlap contains $Y-P$ and **11 additional values** (the candidate Xi4 defect). Lemma A1 allows a critical-order genuine future batch at infinitely many growing finite widths without changing any arithmetic relation inside $P\cup Y$. Thus the existence of nonzero Xi4 **by itself** has no universal coercive effect on the maximum far-future batch size. This does NOT rule out a three-block theorem with fixed comparable widths, a bounded separation factor, or an evolving positive-density hypothesis.

## D. A first no-go for weak renormalized spectral measures

### D1. Exact harmonic rigidity at the integer scale

For any finite set $E\subseteq\mathbb Z$, with $n=|E|$, let

$$
F_E(\theta)=\sum_{a\in E} e^{2\pi ia\theta}.
$$

Orthogonality gives that $\int_0^1|F_E|^6$ is the number of ordered pairs of ordered three-term selections with equal integer sums. If E is B3, each unordered three-multiset with three distinct, exactly two equal, or all equal entries has respectively 6, 3 or 1 orderings. Therefore

$$
\boxed{
\int_0^1|F_E(\theta)|^6\,d\theta
=36\binom n3+9n(n-1)+n
=6n^3-9n^2+4n.
}\tag{EXACT-SIXTH-MOMENT}
$$

If E is not B3, the same moment is **strictly larger**, because different unordered triple multisets with equal sum contribute additional positive cross-terms.

### D2. Weak-limit nonidentifiability despite critical endpoint populations

For each prime $p\ge5$ let $T_p$ be the genuine $p$-point B3 moment alphabet above. Define a second set

$$
T'_p=\{1,2,3\}\cup\{e_i:3\le i<p\}\subseteq[1,W_p].
$$

It also contains **exactly p distinct integers**, because $e_i\ge i+1\ge4$ for $i\ge3$. But it is **not** B3: the two different repeated-summand triples $(1,1,3)$ and $(1,2,2)$ both have sum 5.

Define the normalized empirical probability measures

$$
\mu_p=\frac1p\sum_{a\in T_p}\delta_{a/W_p},\qquad
\nu_p=\frac1p\sum_{a\in T'_p}\delta_{a/W_p}.
$$

The two sets differ in at most three points on either side. Thus for **every** bounded Borel test function $\varphi:[0,1]\to\mathbb C$ with $|\varphi|\le1$,

$$
\boxed{
\left|\int\varphi\,d\mu_p-\int\varphi\,d\nu_p\right|
\le\frac6p\longrightarrow0.
}\tag{WEAK-PHASE-NONIDENTIFIABILITY}
$$

This holds in particular for *all* rescaled continuous Fourier modes $\varphi(x)=e^{2\pi itx}$, uniformly in real t. Every weak-* accumulation point of the genuine B3 measures $\mu_p$ is also an accumulation point of the non-B3 measures $\nu_p$, even though exact integer Fourier sixth moments distinguish them for **every p**. Both endpoints have the same critical-order population $p>(W_p/12)^{1/3}$.

**Negative conclusion:** A renormalized argument that remembers **only a weak limit of normalized occupation measures** cannot preserve or recover the exact B3 condition. Consequently a putative spectral proof using only that limit and scale-invariant density has an irreparable identifiability gap unless it adds a discrete defect, a scale-sensitive phase observable, or exact noncommuting integer-frequency data. This does **not** rule out Fourier methods that retain the full integer trigonometric polynomial or an appropriately stronger topology.

## Shared next gate

- **Track A (#2790):** impose an actual c-persistent, scale-comparable next-window hypothesis; determine whether Xi4 raises a *conditional* lower bound on the additional six-variable collision hypergraph beyond the ordinary Q(P)-Q(P) conflicts. Seek a theorem about a third block that is forced to be populated, not an arbitrary far translate.
- **Track B (#2791):** attempt transport and scale ownership for a true cardinality-capacity observable; the new far-future extension lemma is a required hostile control.
- **Track C (#2792):** independently audit both lemmas and the prior source PRs with repetition-permitted triples; author's tests do not constitute independent review.
- **Track D (#2793):** retain full integer phases or an explicitly error-controlled discrete arithmetic defect in the renormalized state; seek a quantitative nonstationary transfer obstruction, not a fixed weak empirical measure alone.

**Disposition:** BOUNDED-NEGATIVE for the precise finite-Xi4-only and weak-measure-only inference classes. No universal density dip, novelty claim, MATHCERT status, or protected-admission assertion. Source: GCL #2789 and parent #2622; public Erdős #41 status OPEN.
