# Erdős #41 — Reciprocal multiblock capacity, and a finite-horizon escape

**20 October 2026. Research status.** We prove a complete family of **location-aware, size-only Hall inequalities** for three fully compatible B3 blocks, including a genuine cardinality capacity bound independent of block spacing. We then construct **arbitrarily large, actual three-block B3 sets** with critical-order populations that evade a mandatory single-step or two-step shortage, and maintain a finite positive normalized counting lower bound across a factor-17 interval. This does **not** construct an infinite counterexample, decide Erdős #41, or refute any genuinely unbounded multiscale theorem. The point is to eliminate a false finite-window bridge and isolate a precise missing theorem.

## 1. All three-window reciprocal sum capacities, without special locations

Let A be a repeated-summand B3 set and let P, X, Y be its pairwise disjoint subsets, each contained in an integer interval

$$
I_i=[b_i,b_i+R-1]\cap\mathbb Z,\qquad i=0,1,2,
$$

with arbitrary integer starts and length R. Let $m_0=|P|=n$, $m_1=|X|=k$, and $m_2=|Y|=\ell$. A **triple colour type** is $\alpha=(\alpha_0,\alpha_1,\alpha_2)\in\mathbb Z_{\ge0}^3$ with $\alpha_0+\alpha_1+\alpha_2=3$. There are ten types.

For each type define the *exact repeated-summand cardinality*

$$
w_\alpha=\prod_{i=0}^2
\binom{m_i+\alpha_i-1}{\alpha_i},
$$

with the standard convention that the factor for $\alpha_i=0$ is 1. Every selected triple of type $\alpha$ has sum in

$$
J_\alpha=
\left[
\sum_i\alpha_i b_i,\ 
\sum_i\alpha_i b_i+3R-3
\right]\cap\mathbb Z.
$$

**Theorem A (complete family of three-container interval-Hall constraints).** For every nonempty subset $\mathcal F$ of the ten colour types,

$$
\boxed{
\sum_{\alpha\in\mathcal F}w_\alpha
\le
\left|\bigcup_{\alpha\in\mathcal F}J_\alpha\right|.
}\tag{THREE-CONTAINER-HALL}
$$

**Proof.** Each type contains precisely $w_\alpha$ distinct unordered element triples, including repetitions. Distinct colour types have disjoint underlying triple families. All their three-term sums must be distinct because the **whole** P union X union Y is B3. Their integer values belong to the union of the corresponding $J_\alpha$. Comparing counts proves the inequality. QED.

This is the full collection of support-only Hall inequalities at the level of **three colour types**. It is *not* sufficient for B3: internal arithmetic collisions can exist even when every interval-capacity inequality holds. Nor is it a global asymptotic criterion; it is a finite necessary condition.

Choosing the three singleton families PPY, XXY, and PXY gives three separate, **shape-independent reciprocal cardinality constraints**:

$$
\begin{aligned}
\ell\binom{n+1}{2}&\le 2\mathrm{diam}(P)+\mathrm{diam}(Y)+1,\\
\ell\binom{k+1}{2}&\le 2\mathrm{diam}(X)+\mathrm{diam}(Y)+1,\\
nk\ell&\le\mathrm{diam}(P)+\mathrm{diam}(X)+\mathrm{diam}(Y)+1.
\end{aligned}
$$

In particular, for windows of length R and n,k>=1,

$$
\boxed{
\ell\le
\left\lfloor
\frac{3R-2}{
\max\{\binom{n+1}{2},\,nk,\,\binom{k+1}{2}\}}
\right\rfloor.
}\tag{RECIPROCAL-TRUE-CARDINALITY-CAP}
$$

This is an **actual upper bound on the maximum possible future batch cardinality**, valid for every possible arrangement of the future points and every relative spacing of the three occupied windows. If n,k>=c R^(1/3), it implies at most $(3/c^2)R^{1/3}$ future points; the coefficient tightens as the two earlier populations grow. It **does not** improve the *exponent*: the bound remains at precisely the critical order.

For nonuniform widths, the same three inequalities hold with the actual diameters and without the simplifying common-R envelope.

## 2. Finite-field construction: full reciprocal constraints can preserve critical-sized cohorts

The following elementary explicit construction supplies a stringent hostile control, stronger than an abstract scalar occupancy vector. **All points genuinely belong to one repeated-summand B3 set.**

Let p>=5 be a prime. Define

$$
B=3p+1,\quad
R=p(1+B+B^2)+1=9p^3+9p^2+3p+1.
$$

For each integer 0<=i<p, let

$$
e_i=1+i+B(i^2\bmod p)+B^2(i^3\bmod p)\in[1,R].
$$

**Lemma B1 (explicit finite B3 moment code).** $S_p=\{e_i:0\le i<p\}$ is B3 with repeated summands.

**Proof.** Each base-B digit of the sum of ANY three $e_i-1$ values is smaller than B, so there are no carries. An equality of three e-sums implies equality, modulo p, of the first, second and third power sums of the respective three indices in $\mathbb F_p$. Since p>3, Newton's identities recover all three elementary symmetric polynomials, hence the monic cubic polynomial with exactly those three roots including multiplicities. The two index multisets coincide, so the original triples coincide. QED.

Partition the p indices into three consecutive, nonempty groups of sizes

$$
m_0=\lfloor p/3\rfloor,\quad
m_1=\lfloor2p/3\rfloor-\lfloor p/3\rfloor,\quad
m_2=p-\lfloor2p/3\rfloor.
$$

These each contain at least p/5 elements for p>=5. Set M=4R, use the three B3 **colour tags** 0,1,4, and form

$$
\begin{aligned}
P_p&=\{e_i:i\text{ in group 0}\}\subseteq[1,R],\\
X_p&=\{M+e_i:i\text{ in group 1}\}\subseteq[4R+1,5R],\\
Y_p&=\{4M+e_i:i\text{ in group 2}\}\subseteq[16R+1,17R].
\end{aligned}
$$

**Theorem B (three genuine critically populated B3 containers).** The entire $P_p\cup X_p\cup Y_p$ is B3, and for every sufficiently large (indeed every p>=5) prime p each group satisfies

$$
\boxed{m_i\ge\tfrac1{12}R^{1/3}\quad(i=0,1,2).}\tag{CRITICAL-THREE-BLOCKS}
$$

Moreover, writing A_p(N) for the counting function of this finite union,

$$
\boxed{
A_p(N)\ge\tfrac1{21}N^{1/3}
\quad\text{for every real }N\in[R,17R].
}\tag{FINITE-CRITICAL-HORIZON}
$$

**Proof.** The tag set {0,1,4} is itself B3. Any triple's physical sum is $M$ times its tag triple sum, plus a sum of three original e-values. Because the original e-values occupy an interval of diameter below R, two different tag sums differ by at least M=4R>3R, so they cannot collide. With the same tag multiset, equality reduces to a triple-sum equality in the original global B3 set S_p, so the underlying index multisets, and hence the tagged actual triples, coincide. Thus the union is genuinely B3.

For p>=5, R<12p³ and m_i>=p/5; therefore $m_i>R^{1/3}/(5\cdot12^{1/3})>R^{1/3}/12$. In fact the latter inequality follows from 5³·12=1500<12³=1728.

For R<=N<=5R, all of P_p is already counted, so $A_p(N)\ge R^{1/3}/12\ge N^{1/3}/(12\cdot5^{1/3})>N^{1/3}/21$. For 5R<=N<=17R, P_p and X_p are both already counted, so $A_p(N)\ge R^{1/3}/6\ge N^{1/3}/(6\cdot17^{1/3})>N^{1/3}/21$. The strict inequalities follow from $21^3>12^3\cdot5$ and $21^3>6^3\cdot17$. QED.

**Why the type-Hall constraints do not couple these blocks further.** Every colour-tag triple sum from {0,1,4} is different. Thus the ten intervals $J_\alpha$ of ALL three-block triple types are **pairwise disjoint** because their starts differ by at least 4R, while each interval has diameter only 3R−3. The full type-Hall system therefore splits into ten independent per-type range constraints. The original moment-code uniqueness satisfies the *internal* arithmetic restrictions as well. These are complete, unabridged $B_3$ examples: no violated reciprocal signed-sum condition is being concealed.

As p runs through arbitrarily large primes, R tends to infinity. Consequently **no theorem deducing a subcritical future batch solely from three occupied width-R containers of positive critical-order population and their full pairwise reciprocal B3 compatibility can be correct in general**. The construction even supplies a finite factor-17 horizon of genuine positive normalized lower density with c=1/21. A theorem about infinitely many consecutive checkpoints, or a fixed coefficient c over arbitrarily long horizons, is **not refuted**: each constructed set is finite and its normalized counting function becomes zero beyond its last point.

### Arbitrarily many finite compatible containers

**Theorem C (finite-depth escape).** For every integer h>=2, there exist arbitrarily large R and actual finite B3 sets with h disjoint length-R containers, each holding at least $R^{1/3}/(5h)$ members. If N_* is the end of the last container, then

$$
\boxed{N_*\le385h^3R,\qquad
A(N)\ge\frac{N^{1/3}}{40h^2}\quad(R\le N\le N_*).}
$$

**Proof.** Choose arbitrarily large primes p>=2h and the p-point B3 moment code S_p in [1,R], with R<12p³. Split its p indices into h nearly equal groups. Each group contains at least floor(p/h)>=p/(2h)>R^(1/3)/(5h) values.

Choose h increasing, nonnegative integer *tags* forming a B3 set, starting at zero, with largest tag below 96h³. For h>=5, use the same moment-code construction at a prime t with h<=t<2h (Bertrand's theorem), retain h tags and subtract their minimum; the resulting span is below 12t³<96h³. For h=2,3,4 simply use the first h entries of {0,1,4,16}. Translate group j by 4R times its tag. Different tag triple sums are separated by at least 4R, whereas sums of three original baseline values vary by less than 3R. Consequently different colour types cannot collide; within a fixed type the global B3 moment code S_p prevents collisions. The entire union is therefore B3.

Its last element lies before (4·96h³+1)R<=385h³R. At every N>=R, the first block already contributes R^(1/3)/(5h) points. Throughout the stated horizon, N^(1/3)<=385^(1/3)hR^(1/3), and 5·385^(1/3)<40. This proves the finite normalized lower bound. QED.

**Critical limitation:** the certified density coefficient decreases like h^(-2). This DOES NOT refute a theorem asserting impossibility at sufficiently large h for each fixed c>0. It proves that no argument using only a fixed finite number of reciprocal compatibility layers can assume an automatic local shortage without tracking the coefficient and the geometric cost of extending the history.

## 3. The precise unavoidable multiscale difficulty

Theorem A proves that fully reciprocal three-container signed sums impose a **true cardinality cap**, with no alignment assumption. Theorem B shows this cap is of **optimal critical exponent** on arbitrarily large true B3 configurations, even with a substantial finite period of persistent density. Adding container entropy compression cannot turn it into emptiness merely by treating rare choices as impossible.

The refined outstanding bridge is a genuinely **UNBOUNDED, nested-container** statement:

> Fix c>0. Prove that no single infinite repeated-summand B3 carrier can preserve A(N)>=cN^(1/3) at every sufficiently large checkpoint while respecting the exact three-colour Hall and internal signed-code conditions at all scales. The proof must identify an *incremental invariant* or *cross-scale compatibility obstruction* not dischargeable by successive finite-field tagged-block relabellings.

The exceptional finite mechanism is now explicit: the tag sums separate collision types, but to keep all groups from one common finite B3 base alphabet, a growing number of groups would force increasingly large base-code capacity. Whether every general, nonseparable construction faces an analogous growing cost is **not proved**. Inferring it from the tagged construction alone would beg the conjecture.

The full universal density-dip lemma and Erdős #41 remain OPEN. This note is a bounded independent mathematical investigation for GCL issue #2622, not a novelty or protected-release certification.
