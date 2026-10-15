# Erdős #41: cubic difference shadows and a second-moment exclusion principle

**Status:** bounded additive-combinatorial research results, not an Erdős #41 solution. The cubic shadow and moment inequalities below are proved in ordinary mathematics. Selected algebraic identities and finite certificates are checked by Lean; the general set-injection proofs are *not* presented as an end-to-end Lean formalization.

Throughout, M3 means that every unordered triple from a set, **with repeated summands permitted**, has a unique sum. A subset of an M3 set is M3. Repeated entries in a triple are essential in the arguments.

## 1. Exact cubic difference shadow

For any finite set X of integers, write

$$
P_X=\{a+b:a,b\in X\},
\qquad
T_X=P_X-X=\{a+b-c:a,b,c\in X\}.
$$

The unordered pairs in P_X allow a=b. Let n=|X|.

**Cubic shadow theorem.** If X is M3, then

$$
\boxed{|T_X|=f(n):=n+\frac{n^2(n-1)}2
=\frac{n^3-n^2+2n}{2}.}\tag{SH1}
$$

**Proof.** Consider the triples (unordered pair {a,b}, distinguished subtraction term c). There are n binom(n+1,2) such triples. A representation is called *trivial* when c equals a or b. For any x in X, the n trivial representations with output x are exactly ({x,c},c), one for each c in X. No nontrivial representation outputs an element x of X: equality a+b-c=x implies a+b=c+x, and M3 implies the B2 property by padding both two-term sums with a common term. The B2 property then forces c∈{a,b}.

Two nontrivial representations (pair {a,b},c) and (pair {d,e},f) cannot have the same output unless they are identical. Indeed equality a+b-c=d+e-f rearranges to a+b+f=d+e+c. By M3 the triples {a,b,f} and {d,e,c} agree as multisets. Because c∉{a,b}, the copy of c on the left must be f, so f=c, and therefore {a,b}={d,e}. Thus the remaining n binom(n+1,2)-n²=n²(n-1)/2 nontrivial representations all yield different values outside X, proving (SH1).

For n=0 the statement is 0=0; for n=1 it gives one shadow element. No density assumptions enter this theorem.

**The shadow is genuinely cubic.** For X with minimum a, maximum b, and diameter D=b-a,

$$
T_X\subseteq[2a-b,\,2b-a],\qquad
|T_X|\le3D+1.
$$

Consequently, for every finite M3 set X,

$$
\boxed{n^3-n^2+2n\le6D+2.}\tag{SH2}
$$

This gives an elementary cubic cardinality bound sensitive to the *actual diameter*, rather than to a presumed sum-range interval. For X inside [1,N], it gives n³-n²+2n≤6N-4.

## 2. Cubic shadows of disjoint blocks do not intersect

**Cross-block shadow theorem.** If X and Y are disjoint subsets of one M3 set, then

$$
\boxed{T_X\cap T_Y=\varnothing.}\tag{SH3}
$$

**Proof.** If a+b-c=d+e-f with a,b,c in X and d,e,f in Y, then a+b+f=d+e+c. The left triple has two entries from X and one from Y; the right has one from X and two from Y. Because X∩Y is empty, they cannot be the same multiset, contradicting M3.

For a family of pairwise disjoint nonempty finite subsets Xi of one M3 set, (SH1)-(SH3) give an injective **cubic footprint packing** bound:

$$
\boxed{
\sum_i f(|X_i|)
\le\left|\bigcup_i
[2\min X_i-\max X_i,\ 2\max X_i-\min X_i]\cap\mathbb Z\right|.
}\tag{SH4}
$$

For dyadic shell pieces $X_j=A\cap[2^j,2^{j+1})$, any finite collection whose largest index is K consequently obeys

$$
\boxed{\sum_j f(|X_j|)\le 3\cdot 2^K-2.}\tag{SH5}
$$

The shadow intervals lie in [1,3·2^j−2], and are therefore contained in [1,3·2^K−2]. This improves the leading cubic coefficient of ordinary within-shell triple-sum range packing by a factor of three. It does *not* by itself force the original density dip: sufficiently small positive normalized shell occupancies can still satisfy these volume constraints.

## 3. Difference shadows prohibit actual arithmetic shifts

For a finite P define its difference set $D(P)=\{p-p':p,p'\in P\}$.

**Forbidden difference theorem.** For **nonempty** disjoint subsets X,Y of an M3 set, with $P=P_X$,

$$
\boxed{D(P)\cap D(Y)=\{0\}.}\tag{D1}
$$

Indeed, if p-p'=y'-y≠0, then p+y=p'+y' gives two different triples of type XXY. Since X and Y are nonempty, zero belongs to both difference sets. The reverse sign is immaterial because both difference sets are symmetric. A repetition-permitted M3 set is also B2, so the nonzero ordered differences of Y are unique and $|D(Y)|=|Y|(|Y|-1)+1$.

If H=max(Y)-min(Y), counting the forbidden nonzero Y-differences inside [-H,H] yields the *difference-shadow capacity inequality*:

$$
\boxed{
|D(P)\cap[-H,H]|+|Y|(|Y|-1)\le 2H+1.
}\tag{D2}
$$

Unlike the shell-range Hall inequalities, (D2) depends on the **actual gaps** of the pair-sum set P and Y. The particularly useful exact cross-pattern condition is

$$
\boxed{(P_X-X)\cap(P_Y-Y)=T_X\cap T_Y=\varnothing,}\tag{D3}
$$

whose cubic footprint sizes are fixed by (SH1). It is stronger than merely comparing the ranges of XXY and XYY.

## 4. A variance/moment obstruction for actual sum locations

A further necessary constraint uses the actual second moments rather than cardinalities of enclosing intervals.

**Distinct-integer moment lemma.** Let $t_1,\ldots,t_m$ be distinct integers. Then

$$
\boxed{
12\left(m\sum_i t_i^2-\left(\sum_i t_i\right)^2\right)
\ge m^2(m^2-1).
}\tag{V1}
$$

**Proof.** Sort the values so t1<...<tm. Since they are distinct integers, $t_j-t_i\ge j-i$ for i<j. The identity

$$
m\sum_i t_i^2-\left(\sum_i t_i\right)^2
=\sum_{i<j}(t_j-t_i)^2
$$

and the exact square-distance sum $\sum_{i<j}(j-i)^2=m^2(m^2-1)/12$ give (V1). Equality holds for consecutive integers. The cases m=0 or 1 follow directly.

For M3 and disjoint X,Y, form *all* mixed triple sums from both XXY and XYY (including multiplicity if a proposed configuration has collisions). These are required to be distinct under M3, so (V1) applies to their exact values. It is a **joint cross-pattern variance constraint** in addition to all shell-pattern Hall cardinality bounds.

For the XXY pattern alone, let $P=P_X$, $q=|P|=\binom{|X|+1}{2}$, $r=|Y|$, and write $S_P=\sum_{p\in P}p$, $Q_P=\sum_{p\in P}p^2$, with analogous sums $S_Y,Q_Y$. The mixed triple list contains $m=qr$ sums and satisfies

$$
\sum_{p,y}(p+y)=rS_P+qS_Y,\qquad
\sum_{p,y}(p+y)^2=rQ_P+qQ_Y+2S_PS_Y.
$$

Thus the exact M3 constraint is

$$
\boxed{
12\left[qr(rQ_P+qQ_Y+2S_PS_Y)-(rS_P+qS_Y)^2\right]
\ge (qr)^2((qr)^2-1).
}\tag{V2}
$$

A corresponding inequality applies to XYY. For both patterns combined, simply add their exact first and second moments and use the total count in (V1), including the between-pattern shift in their means. This combines the *actual additive locations of both patterns* and can reject a configuration even when their individual variance tests and every Hall volume inequality pass.

## 5. A strict cross-pattern moment witness missed by every Hall bound

Consider the two disjoint blocks

$$
X=\{10,13\}\subset[8,16),\qquad Y=\{16,17\}\subset[16,32).
$$

Each block is M3. The unordered within-block pair sums are

$$
P_X=\{20,23,26\},\qquad P_Y=\{32,33,34\}.
$$

The two *internally collision-free* mixed-pattern sum lists, in increasing order, are

$$
XXY:\quad 36,37,39,40,42,43,
$$

$$
XYY:\quad 42,43,44,45,46,47.
$$

All fifteen nonempty selections of the four full three-shell patterns (XXX, XXY, XYY, YYY) satisfy their shell-range Hall inequalities for occupancies x=y=2 at L=8. The XXY pattern on its own satisfies (V1) with slack +1440, and XYY on its own satisfies (V1) with slack 0. Yet combining them produces twelve purported distinct sums with *negative* moment slack:

$$
12\left(12\sum t_i^2-(\sum t_i)^2\right)-12^2(12^2-1)=-1872.
$$

Therefore the two patterns **cannot simultaneously have distinct sums**, using only the actual moment locations. Indeed 42 and 43 occur in both lists. Equivalently, the cross-block shadows

$$
T_X=\{7,10,13,16\},\qquad T_Y=\{15,16,17,18\}
$$

intersect at 16. This is a minimal, fully explicit example where (i) full shell-range Hall passes, (ii) each mixed pattern separately has unique sums and passes the individual variance lower bound, but (iii) the joint variance and cubic difference-shadow conditions fail.

An even simpler *single-pattern* obstruction is X={9,12,13}, Y={16,20}: both blocks individually M3, but the XXY sum list has twelve entries and only nine distinct values, and the left-hand side of (V1) minus its right-hand side equals -1200. Its mixed-pattern Hall capacity easily permits the count. This demonstrates that actual second moments can exclude arrangements undetected by cardinality/range packing.

## 6. Why the previous adversarial occupancy profile fails this new test

The ungapped synthetic profile in [CROSS_PATTERN_HALL.md](CROSS_PATTERN_HALL.md) chose the **first** b_j positive integers from every occupied dyadic shell. It was deliberately not M3, and it obeyed all triple-sum *interval volume* bounds. The cubic shadow theorem now detects exactly why this particular construction cannot be M3: a block consisting of b consecutive integers has actual diameter b-1, while (SH2) would require

$$
b^3-b^2+2b\le6(b-1)+2.
$$

For b≥3 this is false (with b=3 it says 24≤14). In particular, shell 21 of that synthetic profile contains eight consecutive integers, whose putative cubic shadow would have size f(8)=232 but whose actual shadow is confined to an interval of only 22 integers.

This observation does **not** make all shadow-only counting arguments sufficient for Erdős #41. Small but positively normalized shell occupancies can be widely dispersed inside a shell and satisfy the cubic footprint-volume constraints. The new method adds a *real geometric rigidity*: B3 points cannot cluster as the old Hall counterprofile did. Proving density valleys would still require a cross-scale obstruction to satisfying all these rigidities simultaneously.

## 7. Exact outstanding mathematical obligation

The arithmetic shadow method supplies two independent necessary requirements for an infinite M3 set:

1. Each finite block of size n has a cubic difference shadow of exactly f(n) values, and the shadows of disjoint blocks cannot intersect.
2. Every family of actual mixed triple sums obeys the distinct-integer second-moment bound (V1), including their between-pattern mean separation.

These conditions are now suitable for exact finite feasibility and refutation tests, not for claiming a complete proof. A genuinely consequential successor would bound the *overlap pressure* among shadow intervals at multiple scales or prove an unavoidable collision among cross-pattern sums under a persistent positive normalized density assumption. The exact base-8 finite-window valley criterion remains the mathematical target.

We do not assert that these elementary lemmas are previously unpublished: they are derived directly from unique representation of B3 sums, a standard topic in additive combinatorics. References include the GCL [infinite-source-fidelity audit](../erdos-41-critique/INFINITE_FIDELITY.md), the [previous Hall volume audit](CROSS_PATTERN_HALL.md), and standard background such as K. Soundararajan's additive combinatorics lecture notes (https://www.math.cmu.edu/~af1p/Teaching/AdditiveCombinatorics/Soundararajan.pdf). No claim of a solution, independent referee certification, or publication follows.
