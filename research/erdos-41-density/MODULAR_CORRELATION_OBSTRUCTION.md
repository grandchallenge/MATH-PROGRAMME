# Erdős #41: modular obstruction to prescribed cross-block overlap

**Disposition (2026-10-15): PROVED finite selector and modular transfer lemmas; conditional infinite obstruction.** The required density-forced overlap lower bound is **NOT proved**. Erdős #41 remains OPEN. No MATHCERT, novelty, or problem-resolution claim.

## Source and precise correlation

Use the repetition-allowed B3/M3 definition: a multiset of three elements of A is uniquely determined by its sum, including repeated elements. Source: https://www.erdosproblems.com/41 .

Let X_1 < ... < X_k be disjoint inner B3 subblocks of A, Y a disjoint outer B3 subset above them, P_i = {a+b: a,b in X_i, unordered with repetitions}, and

$$
R_{ij}(t)=\#\{(p,p')\in P_i\times P_j:p-p'=t\}.
$$

Let H be a set of distinct **positive actual differences** z-z' with z,z' in Y. Orient each edge (i,j) with i>j, since for i<j and h>0 the correlation R_ij(2h) is identically zero by order alone. The aggregate over a graph G on the inner blocks is

$$
S_G(H)=\sum_{(i,j)\in E(G),\,i>j}\sum_{h\in H}R_{ij}(2h).
$$

No quantity at fixed N is counted at multiple cuts. The direct full-outer-center overlap uses both signs; this note focuses on the once-oriented positive-difference sub-sum.

## Theorem 1: universal matching cap

Put X = union_i X_i, n = |X|. For every nonzero h in A-A, **2h is outside A-A**. Otherwise a-b=2(z-z') with z != z' yields a+z'+z'=b+z+z, a forbidden triple-sum coincidence (the repeated z' has multiplicity two on one side and at most one on the other).

For any d outside A-A, consider distinct ordered pair-sum representations p-q=d with p,q in P_X. Their positive unordered pairs have disjoint vertex supports. Indeed, if p_1=a+b and p_2=a+c share a, then B3 applied to b+q_2=c+q_1 forces either b=c (and the representations are equal by B2), or q_1=b+t, q_2=c+t for t in X; in the second case d=a-t belongs to A-A, a contradiction. This also covers diagonal pairs.

Hence R_XX(d) <= n for d outside A-A, and for each h in H the graph-indexed sum is bounded by R_XX(2h). Therefore

$$
\boxed{0\le S_G(H)\le n|H|.}\tag{CAP}
$$

At critical inner and outer occupancies n=O(N^{1/3}) and |H|=O(N^{2/3}), this is O(N) regardless of the number of disjoint inner blocks. A proof claiming a superlinear lower bound for this single-scale aggregate must first refute an exact finite B3 theorem.

## Theorem 2: finite K-color modular annihilation

Let A be **any finite B3 set**, X_1,...,X_k,Y pairwise disjoint subsets, and let G be a graph of inner-block comparisons with a proper coloring e_i in {1,...,K}. Define e(a)=e_i on X_i, e(a)=0 on Y and on all unselected points. Pick a fixed integer q>3K and construct

$$
A'=\{qa+e(a):a\in A\},\quad
X_i'=\{qa+e_i:a\in X_i\},\quad
Y'=\{qy:y\in Y\}.
$$

Then A' is B3, has the same cardinality as A, and for every edge (i,j) of G and every h' in Y'-Y',

$$
\boxed{R_{ij}'(2h')=0.}\tag{ZERO}
$$

Proof of B3 preservation: every e(a) lies in [0,K]. If sums of three lifted elements agree, then q times the difference of the original triple sums lies in [-3K,3K], forcing the original sums to agree because q>3K. B3 of A identifies the original three-multisets, so the lifted multisets agree. The map is injective as q>K.

Proof of ZERO: for p_i' in P_i' and p_j' in P_j',

$$
p_i'-p_j'\equiv 2(e_i-e_j)\pmod q,
\qquad 2h'\equiv0\pmod q.
$$

Proper coloring gives 0<|e_i-e_j|<q/2, making equality impossible. No assumption on the numerical gap sizes or on the number of actual outer differences is needed.

This theorem kills correlations on **any uniformly K-colorable prescribed comparison graph**, including bipartite graphs, matchings, and trees, while preserving exact B3 arithmetic. It does **not** kill all correlations on a complete graph with unbounded chromatic number.

## Theorem 3: persistence of the obstruction at infinitely many scales, conditional on a hypothetical dense B3 set

Assume, only for this theorem, that an infinite B3 set A satisfies A(t) >= c t^(1/3) for all sufficiently large t. Let R=(6/c)^3. The prior density extraction in MULTISCALE_GATE.md and DENSITY_LOCALIZED_ZERO_OVERLAP.md provides at every sufficiently large N a populated outer interval W_N=A intersect (N/R,N], and k(N)=floor(log_R(N)/12) populated, pairwise disjoint geometric inner shells X_1(N),...,X_{k(N)}(N) in (N/R^(2k(N)+1),N/R^2], with k(N) tending to infinity. The previous CROSS_BIN_LOCAL_DIFFERENCE_SUPPLY.md produces H_N of distinct actual positive differences of W_N satisfying

$$
|H_N|\ge \kappa_c N^{2/3},\quad
1\le h\le N/R^2\quad(h\in H_N)
$$

for a positive fixed constant \kappa_c.

Select a subsequence N_m increasing so fast that the entire active interval (N_m/R^(2k(N_m)+1),N_m] lies above N_(m-1). This is possible since k(N)<=log_R(N)/12 and the lower endpoint is at least N^(5/6)/R. On the **single original infinite set A**, define a bounded digit function e(a) by assigning e=1 or e=2 to alternate inner shells in each active interval and e=0 to the corresponding outer W_(N_m), taking e=0 elsewhere. These assignments are consistent because active intervals are disjoint.

Set A'={10a+e(a):a in A}. By Theorem 2, A' is an infinite B3 set. Moreover for t sufficiently large,

$$
A'(t)\ge A\bigl((t-2)/10\bigr)
\ge c((t-2)/10)^{1/3},
$$

so A' **still has positive critical lower density**. At every selected scale m, take X_i'(N_m) as the lifted labeled inner shells, W_m'=10W_(N_m), and H_m'=10H_(N_m). The H_m' are distinct actual outer differences, satisfy |H_m'|>=\kappa_c N_m^(2/3), and remain within the corresponding inner-compatible scale window.

For every oppositely colored pair of shells, the correlation is exactly zero. In particular, the nonredundant matching

$$
E_m=\{(2r,2r-1):1\le r\le\lfloor k(N_m)/2\rfloor\}
$$

has |E_m| tending to infinity but

$$
\boxed{S_{E_m}(H_m')=0\quad\text{for every }m.}\tag{INF-ZERO}
$$

**Logical qualification:** no positive-lower-density infinite B3 set has been constructed. The theorem is a conditional transfer: *if* such an A exists, then a B3 set with the same qualitative density property exists for which a growing nonredundant family of correctly scaled correlations is zero. This is not a counterexample to Erdős #41.

## Falsifiable finite replay

Use the genuine 29-point B3 fixture already recorded in CROSS_SCALE_OVERLAP_ENERGY.md, with four successive 3-point blocks X_0,...,X_3 and the final 17 points as W. Direct exact enumeration finds the **unlifted** positive-difference correlation R_30(2h) summed over W-W positive is 1. Color even-indexed blocks 1 and odd-indexed blocks 2, and lift using q=10, assigning W digit 0. The lifted 29-point set has 4495 unique unordered triple sums; its 17-point W has 136 distinct positive differences; **all four cross-color block-pair correlations vanish**, including the originally nonzero (3,0) correlation. See test_erdos41_modular_overlap_gate.py.

Hostile checks must remove B3 (which invalidates matching or difference uniqueness) and must test both correct and reversed index orientations.

## Consequence for research strategy

The localized difference theorem establishes a reservoir of \Omega_c(N^(2/3)) actual h-values. That cardinality, even together with arbitrarily many populated geometric shells, does **not** imply positive S_G for a fixed bounded-color, nonredundant comparison graph.

Any universal positive-correlation lemma for such a graph family, under hypothetical persistent density, would already imply nonexistence of positive-density infinite B3 sets via the conditional modular transfer. It cannot be treated as a simple consequence of the existing finite counting bounds.

A viable next theorem must instead use a comparison family not uniformly colorable with boundedly many residues (for example a genuinely complete family with growing chromatic number), or select arithmetic correlations adaptively in a way not neutralized by a bounded digit lift. It must also obtain a strictly stronger multiscale deficit than the O(N) single-scale matching budget, without recounting the same positive unordered pair at different cuts.

**Open obligation:** prove a quantitatively accumulating lower bound for the fully specified, oriented, nonredundant complete-family correlation S(H_N), taking into account all inner mixed-color pairs and actual outer differences. No such lower bound is claimed here.

Related source files: [CROSS_BIN_LOCAL_DIFFERENCE_SUPPLY.md](CROSS_BIN_LOCAL_DIFFERENCE_SUPPLY.md), [CROSS_SCALE_OVERLAP_ENERGY.md](CROSS_SCALE_OVERLAP_ENERGY.md), [SPECTRAL_MATCHING_COMPETITION.md](SPECTRAL_MATCHING_COMPETITION.md), [DENSITY_LOCALIZED_ZERO_OVERLAP.md](DENSITY_LOCALIZED_ZERO_OVERLAP.md).
