# Erdős #41 — zero-sum fibers, matching bounds and a cross-scale obstruction

**Status:** Complete finite-combinatorial statements with hostile tests; the requested infinite collision theorem remains **OPEN**. Do not mistake an admissible overlap of four-term relations for a B3 collision.

## 1. Exact translation-invariant fiber matching

Let (A) be a finite, repetition-permitted B3 set. Let (X\subseteq A), (n=|X|\ge1), and let (q=\binom{n+1}{2}). Define the **unordered-positive-pair** fiber

$$
\rho_X(d)=\#\{(\{a,b\},c):a,b,c\in X,\ a+b-2c=d\}.
$$

Every positive pair is counted once, including diagonal pairs (a=b). For any integer (d\ne0), classify representations into those with (a\ne b), counted by (e_X(d)), and diagonal representations, counted by (h_X(d)).

**Theorem 1 (zero-sum matching).** For every (d\ne0), the positive unordered pairs in distinct representations of (a+b-2c=d) have pairwise disjoint supports in (X). Consequently

$$
\boxed{2e_X(d)+h_X(d)\le n,\qquad h_X(d)\le1,\qquad \rho_X(d)\le\lceil n/2\rceil.}\tag{ZF}
$$

Also

$$
\boxed{\rho_X(0)=n.}\tag{ZERO}
$$

**Proof.** Suppose two distinct representations share a positive-pair element (a), so they can be written (a+b-2c=a+b'-2c'). Then (b+c'+c'=b'+c+c). Three-sum uniqueness forces equality of the multisets (\{b,c',c'\}=\{b',c,c\}). If (c\ne c'), the left has two copies of (c') but the right has at most one (the entry (b')); contradiction. Hence (c=c'), and then (b=b'), so the representations were identical. Each off-diagonal positive pair consumes two distinct vertices; each diagonal one consumes one. Diagonal solutions at nonzero (d) satisfy (a-c=d/2), and B3 implies the Sidon/B2 property and uniqueness of a nonzero ordered difference, hence (h_X(d)\le1). If (d=0), (a+b=2c) gives (a+b+c=3c), so B3 forces (a=b=c), yielding precisely n representations.

**Multiscale corollary.** For any finite family of pairwise disjoint subsets (X_i\subseteq A), the same matching is valid across all their zero-sum fibers, viewed as representations from their union. Thus for every (d\ne0),

$$
\boxed{\sum_i(2e_{X_i}(d)+h_{X_i}(d))\le |\bigcup_iX_i|.}\tag{MULTI}
$$

This inequality is valid for arbitrarily many finite blocks, but **its within-block sum alone is not a new cross-scale deficit**: it also follows immediately by adding the individual bounds $2e_{X_i}(d)+h_{X_i}(d)\le|X_i|$. It does not force spectral supports to be disjoint, and cannot be converted into a logarithmically growing contradiction by summing the same local budget repeatedly.

A genuinely joint *colored* version includes representations with a positive pair drawn from **different** blocks, or with center c from another block. If $A=\bigsqcup_i X_i$, decompose $\rho_A(d)$ by the colors of its two positive summands and its center. For every $d\ne0$,

$$
\boxed{2\sum_{a<b,\ c\in A}\boldsymbol1_{a+b-2c=d}
+\sum_{a\in A,\ c\in A}\boldsymbol1_{2a-2c=d}\le |A|.}\tag{COLORED}
$$

Here $a<b$ selects distinct positive elements and the second sum selects diagonal positive pairs $\{a,a\}$; the center $c$ is unrestricted. In (COLORED) the mixed-block positive pairs compete for the same vertices as the within-block pairs, which is real cross-block arithmetic information. However the theorem supplies no lower bound on how frequently the mixed-block terms must occur at a given d under positive lower density; that missing input is exactly the unresolved step.

## 2. An actual B3 counterexample to cross-scale spectral disjointness

The eight-element set

$$
A=\{1,2,5,14,33,72,125,219\}
$$

is B3: its 120 unordered triples with repetition have 120 different sums (a deterministic exact regression verifies this). Partition it into (X=\{1,2,5,14\}) and (Y=\{33,72,125,219\}). Both blocks have the same nonzero centered zero-sum output,

$$
1+5-2\cdot2=2=33+219-2\cdot125.
$$

The two representations have disjoint positive-pair supports, exactly as (ZF) requires. Their common value is a permitted **four-term** relation, not a collision of unordered triples. Therefore the proposed assertion (\mathrm{supp}\rho_X\cap\mathrm{supp}\rho_Y=\varnothing) away from 0 is **false on a genuine B3 set**. An argument that accumulates disjoint zero-sum spectra across scales would be invalid.

## 3. Arbitrarily many scales can have the same nonzero fiber

The preceding overlap is not confined to two blocks or to a single finite example.

**Theorem 2 (explicit infinite B3 overlap construction).** Put $B=16$. For every integer $j\ge0$ define

$$
T_j=B^{2j+2},\qquad k_j=B^{2j+1},\qquad
X_j=\{T_j,\ T_j+k_j,\ T_j+2k_j+1\}.
$$

Then the infinite set $A_* = \bigcup_{j\ge0} X_j$ is B3, the blocks $X_j$ are pairwise disjoint and separated by geometric gaps, and yet

$$
\boxed{\rho_{X_j}(1)=1\text{ for every }j\ge0.}\tag{INF-OVERLAP}
$$

In particular, for every integer $K\ge1$, the first K geometrically separated blocks have **at least K representations of the same nonzero centered value 1**. There is no universal bound, independent of the number of scales, on the sum of the centered-fiber multiplicities for disjoint B3 blocks.

**Complete proof of B3 uniqueness.** Represent any member of $X_j$ by one of three types $t\in\{0,1,2\}$:

$$
a_{j,t}=B^{2j+2}+tB^{2j+1}+\boldsymbol1_{t=2}.
$$

For a multiset of exactly three such elements, write $x_{j,t}$ for the number of occurrences of type t from block j. In base B, its sum has digit

$$
c_j=x_{j,0}+x_{j,1}+x_{j,2}
\quad\text{at place }2j+2,
$$

$$
w_j=x_{j,1}+2x_{j,2}
\quad\text{at place }2j+1,
$$

and units digit $Q=\sum_j x_{j,2}$. There are **no carries**: each $c_j\le3$, $w_j\le6$, and $Q\le3$, all smaller than 16; different j use disjoint digit places. Consequently equality of two three-term sums implies equality of all $c_j$, all $w_j$, and Q.

Let $x$ and $y$ be the two multisets, and set $\delta_j=x_{j,2}-y_{j,2}$. The equalities of $c_j$ and $w_j$ force

$$
(x_{j,0}-y_{j,0},\ x_{j,1}-y_{j,1},\ x_{j,2}-y_{j,2})
=(\delta_j,-2\delta_j,\delta_j).
$$

If $\delta_j\ne0$, then each of the two three-term multisets uses **at least two elements from block j**: one side contains two copies of type 1 (or more), while the other contains at least one of each types 0 and 2. Because each multiset has only three terms globally, there can be **at most one** block j with $\delta_j\ne0$. Equality of Q requires $\sum_j\delta_j=0$, excluding that possibility. Therefore every $\delta_j=0$ and all $x_{j,t}=y_{j,t}$, so the two triples are identical. This proves B3 for the entire infinite set (any triple involves finitely many blocks).

The centered relation follows immediately from

$$
T_j+(T_j+2k_j+1)-2(T_j+k_j)=1.
$$

**Exact common-fiber multiplicity.** The explicit construction is nearly saturating the available matching budget, not merely sharing a single accidental relation. For the first m blocks put $A_m=\bigcup_{0\le j<m}X_j$. The equality $a+b-2c=1$ is $a+b=2c+1$. In base 16 there are again no carries on either side: the high block digit of $2c+1$ is 2, so the two positive elements a,b must lie in the same block as c. Their local type digits satisfy $t_a+t_b=2t_c$, and their units digits satisfy $\boldsymbol1_{t_a=2}+\boldsymbol1_{t_b=2}=2\boldsymbol1_{t_c=2}+1$. A case check shows the **only** solution up to interchanging a,b is $(t_a,t_b,t_c)=(0,2,1)$. Therefore

$$
\boxed{\rho_{A_m}(1)=m\quad\text{for every }m\ge1.}\tag{EXACT-M}
$$

The general matching bound for this B3 set with $3m$ elements is $\rho_{A_m}(1)\le\lceil3m/2\rceil$, so these explicit examples achieve an asymptotic **two-thirds of the maximal matching capacity at the same lag**, with the representations dispersed over m geometric scales. No proposed argument may claim a lower uniform multiplicity threshold than this merely from B3 and scale separation.

Each $X_j$ lies on scale $T_j=16^{2j+2}$, with $T_{j+1}/T_j=256$. The infinite set has $A_*(N)=O(\log N)$, hence $A_*(N)/N^{1/3}\to0$. It is therefore **not** a counterexample to Erdős #41. What it definitively refutes is a disjointness or uniformly bounded-overlap lemma for these translation-invariant fibers which does not use a lower-density hypothesis.

## 4. Exact fiber mass and the dimension barrier

There are (nq) total positive-pair/center representations. Exactly n have output zero, by (ZERO). Among the remaining representations, the off-diagonal positive pairs account for (n\binom n2) representations and the diagonal pairs for (n(n-1)). Consequently

$$
\boxed{\sum_{d\ne0}\rho_X(d)=n(q-1)=\frac{n(n-1)(n+2)}2.}\tag{MASS}
$$

and the **weighted** multiplicity sum is

$$
\boxed{\sum_{d\ne0}[2e_X(d)+h_X(d)]=n(n^2-1).}\tag{WEIGHT}
$$

For a set (X) of diameter (D), every centered output lies in ([-2D,2D]). There are at most (4D) nonzero integer slots. Using (ZF) on (WEIGHT) gives

$$
n(n^2-1)\le 4Dn,\qquad\text{hence}\qquad
\boxed{n^2-1\le4D.}\tag{B2-SCALE}
$$

This is only a **quadratic** diameter bound. It is weaker than the already admitted cubic-shadow bound (n^3-n^2+2n\le6D+2). Crucially, the translation-invariant expression keeps the desirable common origin but loses enough injectivity that this straightforward matching/capacity argument drops from cubic to quadratic power. This gives a precise obstruction to the naive phase-free, logarithmically accumulating strategy.

## 5. Critical literature boundary

Christian Táfula, *Infinite Sidon-type sets for zero-sum linear forms* (Monatshefte für Mathematik 211, 315–327, 2026; DOI 10.1007/s00605-026-02211-4) establishes an even-order density theorem by nonnegative Fourier methods, and conditional results for general zero-sum forms under assumptions on consecutive gaps. It explicitly identifies the odd-order Sidon density problem as open. Our matching theorem uses **unordered positive pairs with repetitions**, whereas Táfula's representation function uses tuples of pairwise distinct elements; these must not be conflated when comparing multiplicity bounds.

The infinite construction shows that even an arbitrary number of geometric B3 blocks may have the same nonzero anchored fiber; any theorem forcing a scale-growing deficit must use **positive lower density**, stronger interaction data, or both. The present result does not disprove the existence of such a density-sensitive inequality. It **does** refute automatic disjointness of centered fibers and shows that naive fixed-lag weighted matching recovers only a quadratic, not cubic, diameter bound. The next mathematical obligation is to find a new inter-scale *joint distribution* restriction that survives the displayed genuine-B3 overlap witness, or to use a source-grounded irregular-gap constraint to extract a density valley. Erdős #41 remains OPEN. No novelty priority or mathematical certification is asserted.
