# Erdős #41: pointwise competition between off-spectrum correlations

**State:** finite B3 arithmetic theorem with an exact additive-energy consequence. This note is a bounded successor to the fourth-moment audit, NOT a proof of Erdős #41. The core combinatorial arguments are written proofs, not end-to-end Lean formalizations.

## Definitions

Let A be a finite B3/M3 set of integers: unordered three-term multisets, including repetitions, have unique sums. Let X⊆A with n=|X|≥1, and let Y_1,...,Y_k be any pairwise disjoint subsets of A\X. Each Y_j may be empty.

Let P_X be the set of unordered two-term sums from X. M3 implies B2, so each p∈P_X corresponds to one unordered pair {a,b} from X, even when a=b. Write q_X=|P_X|=n(n+1)/2. Define ordered difference multiplicities

$$
r_X(d)=|\{(p,p')∈P_X^2:p-p'=d\}|
$$

and, for the jth external block,

$$
c_j(d)=|\{(p,q)∈P_X\times P_{Y_j}:p-q=d\}|.
$$

Write $D(A)=A-A$. The earlier exact selector theorem shows r_X(d)=n on the n(n−1) nonzero differences of X and zero on other nonzero differences of A. The cross-block exclusion theorem gives c_j(d)=0 for all d∈D(A), including 0.

## The positive-pair matching theorem

**Theorem.** For every nonzero integer d,

$$
\boxed{r_X(d)+\sum_{j=1}^k c_j(d)\le n.}\tag{MATCH}
$$

More precisely, for d∉D(A), take all representations counted by the left-hand side. Associate to each representation its unordered positive pair {a,b}⊆X, whose sum is p. The *supports of these positive pairs are pairwise disjoint*. In particular, a diagonal pair {a,a} occupies one vertex and a nondiagonal pair occupies two. This yields (MATCH). For d∈D(A)\{0}, the external counts vanish and the selector law gives r_X(d)∈{0,n}, establishing (MATCH) there as well.

**Proof of support-disjointness, case by case.**

1. **Two internal representations.** Suppose p₁−q₁=p₂−q₂=d with p₁=a+b, p₂=a+c sharing a∈X, and q₁, q₂ sums of pairs from X. Then b+q₂=c+q₁ is an equality of two three-term multisets in A. If b=c, B2 uniqueness gives q₁=q₂, so the representations coincide. If b≠c, the B3 multiset equality forces q₁=b+t and q₂=c+t for some t∈X, so d=(a+b)−(b+t)=a−t belongs to D(A), contrary to d∉D(A).

2. **One internal and one external representation.** Suppose p₁=a+b (internal) and p₂=a+c (external positive pair) share a. Write their negative pairs q₁∈P_X and q₂∈P_{Y_j}. Equality of differences gives b+q₂=c+q₁. The left triple contains two Y_j elements and one X element, while the right triple contains three X elements. Because X and Y_j are disjoint, the multisets cannot coincide. This contradicts B3.

3. **Two external representations.** Suppose p₁=a+b and p₂=a+c share a, with q₁∈P_{Y_i} and q₂∈P_{Y_j}. Equality gives b+q₂=c+q₁. If i≠j, the left triple contains two Y_j elements while the right contains two Y_i elements, so B3 uniqueness is impossible. If i=j, uniqueness forces b=c (their only X elements), hence q₁=q₂ by B2, so the representations coincide.

In every case, distinct representations for d∉D(A) cannot share a positive X element. A collection of nonempty pair supports with disjoint vertices has at most n members. QED.

The matching proof actually gives a sharper **weighted** inequality. For a fixed difference d outside D(A), let e(d) count representations whose positive unordered pair consists of two *distinct* X elements, and let h(d) count those with a repeated positive element (a diagonal pair). Disjointness of the positive-pair supports forces

$$
\boxed{2e(d)+h(d)\le n,\qquad d\notin D(A).}\tag{WEIGHTED}
$$

The simpler (MATCH) follows because e(d)+h(d) is the sum of all internal and external multiplicities. This distinction matters when attempting to strengthen the local estimate: most nondiagonal representations consume two vertices, not one. An integer d in D(A) is excluded from (WEIGHTED), because its n trivial internal representations share a common anchor and need not be a matching.

This pointwise exclusion is stronger information than bounds derived merely from the lengths of pair-difference intervals.

## Exact mass and quadratic correlation budget

Let $q_j=|P_{Y_j}|=|Y_j|(|Y_j|+1)/2$, taking q_j=0 for an empty block. Since every external correlation is supported off D(A), and r_X(0)=q_X,

$$
\sum_{d\ne0}\left(r_X(d)+\sum_jc_j(d)\right)
=q_X^2-q_X+q_X\sum_j q_j.\tag{MASS}
$$

The selector law also gives the exact **internal off-spectrum first mass**

$$
\boxed{\sum_{d\notin D(A)}r_X(d)
=q_X^2-q_X-n^2(n-1)
=\frac{n(n-1)(n^2-n+2)}4.}\tag{OFF1}
$$

Combining nonnegativity with the pointwise cap yields, for $S(d)=r_X(d)+\sum_jc_j(d)$,

$$
\boxed{\sum_{d\ne0}S(d)^2
\le n\left(q_X^2-q_X+q_X\sum_jq_j\right).}\tag{QUAD}
$$

This is a *joint* fourth-order correlation budget: expanding S(d)² produces the internal pair-sum energy, cross-block pair-difference energies, and nonnegative interaction terms. It is not valid to discard the interactions and then assume all spectra are disjoint.

Moreover every d outside D(A) with S(d)>0 uses at most n representations. Consequently

$$
\boxed{
|\{d\notin D(A):S(d)>0\}|
\ge
\frac{n(n-1)(n^2-n+2)/4+q_X\sum_jq_j}{n}.
}\tag{SUPPORT}
$$

All these are **exact universal finite B3 consequences** with no asymptotic approximations. The support lower bound, when its right-hand side is nonintegral, means the cardinality is at least its ceiling.

## Explicit adversarial union

Let $X=\{1,2,5\}$ and $Y=\{3,4,7\}$. Each block separately satisfies B3, but their union does not. At d=−8, which is **not** in $(X\cup Y)-(X\cup Y)$, the internal spectrum has r_X(−8)=1, from the positive pair 1+1=2 and negative pair 5+5=10. The cross spectrum has c_XY(−8)=3, from

$$
(1+1)-(3+7)=-8,\quad
(1+2)-(4+7)=-8,\quad
(1+5)-(7+7)=-8.
$$

The positive unordered X pairs $\{1,1\},\{1,2\},\{1,5\}$ overlap at vertex 1. Hence r_X(−8)+c_XY(−8)=4>3=|X|. This small case directly falsifies the theorem if B3 uniqueness of the *union* is omitted, and serves as a hostile regression certificate.

## Scaling obstruction to the original density question

For a finite positive B3 carrier A of diameter H, every difference appearing in the full spectrum lies in [-2H,2H], with at most 4H nonzero positions. Thus (MASS), (MATCH) give the weaker but explicit global relation

$$
\boxed{q_X^2-q_X+q_X\sum_jq_j\le4nH.}\tag{CAP}
$$

If the main block and a complementary block both have cardinality proportional to H^(1/3), then the left side is of order H^(4/3), and the right side is also of order H^(4/3). No scale-diverging factor appears. The same limitation holds for the one-sided energy budget (QUAD) without a new independent lower bound on overlap or forced concentration.

**Determination:** we obtained an actual arithmetic *competition law*, not just a synthetic interval comparison. It can rule out finite non-B3 arrangements via matching failure. Nevertheless (MATCH) and (CAP) do NOT establish a collision for every positive critical-density coefficient, and no passage to the required infinite finite-window valley has been proved.

**Research obligation:** prove an additional cross-scale interaction that forces a fixed portion of the off-spectrum mass to compete at the **same** differences across many separated blocks, accumulating a scale-growing loss rather than merely using 4H available positions. Alternatively, identify a counterexample to a proposed higher-order overlap lemma on genuine finite B3 fixtures. This is the boundary between standard local B3 counting and a viable approach to Erdős #41.

Related context: Helm, *On the Distribution of B3-Sequences* (1996), DOI 10.1006/jnth.1996.0069; Táfula, *Infinite Sidon-type sets for zero-sum linear forms* (2026), DOI 10.1007/s00605-026-02211-4. No novelty or publication claim is made for these elementary combinatorial consequences.
