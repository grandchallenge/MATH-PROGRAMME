# Erdős #41: exact cross-scale mixed-lag overlap energy

**Disposition:** exact finite B3 collision-energy identities, a conditional overlap inequality, a multiscale counting obstruction, and genuine B3 adversarial examples. No proof that persistent positive B3 lower density forces excessive overlap. Erdős #41 remains OPEN.

## 1. Same-lag families with a shared outer block

Let A be a finite repetition-permitted B3 set. Let X_1,...,X_k be pairwise disjoint nonempty inner blocks, all strictly below a common nonempty outer block Y, all subsets of A. Write n_i=|X_i|, y=|Y|, q_i=binom(n_i+1,2), and P_i={a+b:a,b∈X_i}. B3 implies B2, so P_i has q_i distinct unordered pair sums.

For every integer lag d, define the unweighted centered fiber

$$
f_i(d)=|\{(p,z)\in P_i\times Y:p-2z=d\}|.
$$

Each unordered positive pair is counted **once**. For every i its total is

$$
\boxed{T_i=\sum_d f_i(d)=q_i y.}\tag{T}
$$

The families refer to the **same actual lag integer**, not separately recentered coordinates. Since X_i<Y, their support lies at strictly negative lags.

Let F(d)=Σ_i f_i(d), T=Σ_i T_i and let L be an upper bound on the number of integer lag locations occupied by F. When every block lies in [1,H], one can take L=2H, since each lag lies in [−2(H−1),−1].

## 2. Exact overlap identity

Define the pair-sum cross-difference correlation and the outer-set difference multiplicity by

$$
R_{ij}(h)=|\{(p,p')\in P_i\times P_j:p-p'=h\}|,
\qquad
r_Y(h)=|\{(z,z')\in Y^2:z-z'=h\}|.
$$

**Theorem 1 (exact overlap energy).** For all i,j,

$$
\boxed{\sum_d f_i(d)f_j(d)=\sum_h R_{ij}(2h)\,r_Y(h).}\tag{ENERGY}
$$

For i≠j, B2 uniqueness forces P_i∩P_j=∅, eliminating the h=0 term. Hence

$$
\boxed{O_{ij}:=\sum_d f_i(d)f_j(d)
=\sum_{\substack{z,z'\in Y\\ z\ne z'}}
R_{ij}(2(z-z')).}\tag{CROSS}
$$

This counts genuine four-versus-four relations

$$
a+b+2z'=a'+b'+2z
$$

with a,b in X_i, a',b' in X_j and z≠z' in Y. These equalities are NOT prohibited by uniqueness of three-term sums.

**Proof.** Expand the left side as the number of quadruples (p,z,p',z') satisfying p−2z=p'−2z'. Rearranging gives p−p'=2(z−z'), then sorting by h proves (ENERGY). If i≠j, h=0 requires equal pair sums from disjoint X_i and X_j, impossible because B3 implies B2.

**Further B3 restriction (cross-pair matching).** For i≠j and any integer h, the representations counted by $R_{ij}(h)$ have pairwise disjoint positive unordered-pair supports in $X_i$, and pairwise disjoint negative unordered-pair supports in $X_j$. Indeed, if two positive pairs share a, write them $a+b$ and $a+c$. Equal differences imply $b+u'+v'=c+u+v$, with b,c from Xi and u,v,u',v' from Xj. B3 uniqueness forces b=c and the unordered negative pairs equal; the representations coincide. The same argument works with the roles reversed. Therefore

$$
\\boxed{R_{ij}(h)\\le\\min(n_i,n_j)\\quad (i\\ne j).}\\tag{MATCH-R}
$$

Furthermore nonzero ordered differences in Y are distinct because B3 implies B2, so $r_Y(h)=1$ for every nonzero h belonging to Y−Y. The cross-energy identity consequently becomes

$$
\\boxed{O_{ij}=\\sum_{h\\in(Y-Y)\\setminus\\{0\\}}R_{ij}(2h)
\\le y(y-1)\\min(n_i,n_j).}\\tag{MATCH-O}
$$

At critical-size finite scales where $n_i,n_j,y=O(H^{1/3})$, this upper bound is O(H): the same leading scale as the total cross-family representation count. It does not force an overload. An overlap **lower** bound must use additional arithmetic correlations that this upper bound does not supply.

The within-family excess is similarly

$$
\boxed{\sum_d f_i(d)(f_i(d)-1)
=\sum_{\substack{z,z'\in Y\\z\ne z'}}R_{ii}(2(z-z')).}\tag{SELF}
$$

Indeed equal-center solutions are exactly identical pair sums, because P_i has no duplicated members.

## 3. Correct quantitative overlap pressure

Let E_i=Σ_d f_i(d)^2 and O=Σ_{i<j}O_ij. Since F has support in at most L integer positions, Cauchy–Schwarz gives

$$
\boxed{2O=\sum_dF(d)^2-\sum_i E_i
\ge\frac{T^2}{L}-\sum_iE_i.}\tag{PRESSURE}
$$

Substituting (SELF) yields the entirely explicit bound

$$
\boxed{O\ge\frac12\left[
\frac{T^2}{L}-T-
\sum_i\sum_{\substack{z,z'\in Y\\z\ne z'}}R_{ii}(2(z-z'))
\right].}\tag{P2}
$$

The right-hand side may be negative; then only O≥0 follows. (P2) is an *exact necessary pressure inequality* conditional on the real within-family energies. It does **not** automatically imply any positive overlap from positive lower density.

The B3 fixed-lag matching theorem gives f_i(d)≤ceil(n_i/2) for every nonzero lag, and hence E_i≤ceil(n_i/2)T_i, but this crude replacement in (PRESSURE) is too weak to generate a divergent scale factor.

## 4. No counterfeit logarithmic accumulation

Let n=Σ_i n_i. The total number of representations from all these one-color positive-pair families is

$$
\boxed{
T=y\sum_i\binom{n_i+1}{2}
=\frac y2\left(\sum_i n_i^2+n\right)
\le y\binom{n+1}{2}.}\tag{PART}
$$

**Proof.** The first equality is (T); the second expands each binomial. The difference between the final right-hand side and T is $y\sum_{i<j}n_i n_j\ge0$, exactly the positive pairs with their two elements in *different* inner blocks that have been omitted from these families.

By the finite B3 triple-sum bound, if all sets lie in [1,H], the cardinalities n and y are O(H^(1/3)). Thus T=O(H), while the available number of negative lag positions is O(H). Subdividing into arbitrarily many geometric blocks does not produce an additional logarithmic factor in T. More splits remove positive pairs; recounting one mixed representation in several cuts does not create new demand.

This defeats the naive argument: "each scale contributes its own large independent mass to one common lag window, so enough scales must overload B3 matching." The same-scale families are **not independent**, their counts have the exact constraint (PART), and the available window remains of critical size.

Even when the nested infinite positive-lower-density assumption supplies blocks at every sufficiently large scale, these identities do **not** imply that O>0 or that the pointwise matching budget is exceeded. A real proof would need an extra density-sensitive statement controlling the actual r_Y and R_ij correlations, or a genuinely smaller admissible common lag support.

## 5. Genuine B3 adversarial checks

Use the previously authenticated finite B3 set

$$
A=\{1,2,5,14,33,72,125,219,376,573,745,1209,1557,2442,
3098,4048,5298,6704,7839,10987,12332,15465,19144,
24546,28974,34406,37769,45864,50877\}.
$$

For X0={1,2,5} and X1={14,33,72}, let Y contain the remaining 23 members. Exact integer enumeration yields **138 distinct negative lags in each family and zero cross-family overlap**: O_01=0. If the first three consecutive 3-element blocks are used as inner blocks and the remaining 20 elements as Y, all three families have 120 distinct lags and all pairwise O_ij=0. With four such blocks and a 17-element outer block, a single shared lag does appear.

These are genuine B3 configurations with both zero and nonzero inter-family lag overlap. They do **not** disprove a theorem whose hypothesis is persistent positive *infinite* lower density. They demonstrate that a single-scale "B3 plus critical cardinality forces cross-family overlap" premise is unsound.

The sparse infinite B3 base-16 construction previously admitted provides a second adversarial boundary: many widely separated centered lag families can share one nonzero value without producing a B3 collision. Consequently neither universal spectral disjointness nor indiscriminate overlap multiplication can be assumed.

## 6. Research disposition

**Proved:** the exact cross-scale mixed-family overlap identity (ENERGY/CROSS), exact within-family excess (SELF), rigorous pressure lower bound (PRESSURE/P2), and partition budget (PART). These account for representation multiplicity, distinct lag locations, and the same-center exclusion.

**Not proved:** persistent positive lower density forces O>0 for these particular families at every large scale, forces O to exceed a matching budget, localizes all mixed lag support to o(N^(2/3)), or resolves Erdős #41.

**Next falsifiable lemma:** find a nontrivial relation between pair-sum cross-difference spectra R_ij(2h) and the actual outer difference multiplicities r_Y(h), valid *only under nested persistent positive B3 lower density*, that supplies an accumulating positive lower bound beyond the Cauchy and partition identities. This is genuinely additional number theory, not an algebraic consequence of the present finite counts.

Literature boundary: C. Táfula, *Infinite Sidon-type sets for zero-sum linear forms*, Monatsh. Math. 211 (2026), 315–327, DOI 10.1007/s00605-026-02211-4, identifies the odd-order Sidon density question as open and establishes general zero-sum results under added gap conditions. Its pairwise-distinct ordered representation convention must not be confused with these unordered repetition-allowed B3 pairs. No novelty priority or mathematical solution certification claimed.
