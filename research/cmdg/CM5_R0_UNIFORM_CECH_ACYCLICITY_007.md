# CMDG CM5-R0 — degree-uniform finite closed-cover Cech acyclicity

**Status:** MATHEMATICAL ARGUMENT / FORMALIZATION CANDIDATE. NOT LEAN-VERIFIED; NOT MATHCERT-CERTIFIED; NOT DERIVED SOLIDITY.
**Evidence anchor:** CMDG CM5 Ext^5 capstone [MATH-PROGRAMME PR #3561](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3561), exact source head \`5cae71f38568377d7bfd4b6756e8563f4ebbd901\`. The separately protected sixth-to-fifth relation result is [PR #3560](https://github.com/grandchallenge/MATH-PROGRAMME/pull/3560).
**Purpose:** Replace separately hand-built finite closed-family H2/H3/H4/H5 inductions by one theorem quantified over every nonnegative cochain degree. This note does not alter any admitted proof.

## 1. Precise degree-uniform claim

Let $X$ be a profinite space, let $I$ be a finite linearly ordered set, and let $E_i\subseteq X$ be closed for all $i\in I$. Set $F(D)=C(D,\mathbb Z)$, the abelian group of continuous integer-valued functions on a closed subspace $D$ (with $\mathbb Z$ discrete). Define the **increasing-index** finite closed-family Cech cochains by

$$
C^q(\mathcal E)=\prod_{i_0<\cdots<i_q}F(E_{i_0}\cap\cdots\cap E_{i_q}),\qquad q\geq 0,
$$

with differential given by the alternating sum of restrictions to the intersection of length $(q+2)$. Claim:

$$
H^0(C^\bullet(\mathcal E))\cong F\left(\bigcup_{i\in I}E_i\right),
\qquad H^q(C^\bullet(\mathcal E))=0\quad(q>0).
$$

The same claims hold when $\mathbb Z$ is replaced *coordinatewise* by an arbitrary product of discrete copies of $\mathbb Z$, without a shared finite observation across coordinates. Empty intersections contribute the zero group.

## 2. Closed extension lemma

If $D\subseteq Y$ is closed and $Y$ is profinite, every continuous $f:D\to\mathbb Z$ extends to a continuous $\widetilde f:Y\to\mathbb Z$.

Indeed $D$ is compact, so $f(D)$ is a finite subset of the discrete integers. The fibres are finitely many pairwise-disjoint clopen subsets of $D$. Zero-dimensionality and compact Hausdorff normality separate each such fibre from its complement by a clopen of $Y$; successive set differences give a disjoint clopen partition of $Y$ whose intersections with $D$ are exactly the fibres. Assign the fibre values on their ambient parts and zero elsewhere. This works also when $D$ is empty. In particular $F(Y)\to F(D)$ is surjective.

## 3. Induction on the number of closed sets, uniformly in degree

For zero or one index, positive-degree cochains vanish and degree-zero gluing is immediate. Suppose the assertion is established for families of fewer than $m$ sets, in **all** degrees. Let

$$
\mathcal A=(E_1,\ldots,E_{m-1}),\qquad
\mathcal B=(E_1\cap E_m,\ldots,E_{m-1}\cap E_m),
\qquad Z=E_m\cap\bigcup_{i<m}E_i.
$$

Restriction to the cochains with indices below $m$ is a surjective cochain map $C^\bullet(\mathcal E)\to C^\bullet(\mathcal A)$. Let $K^\bullet$ be its kernel. On increasing-index tuples, the components containing $m$ give

$$
K^0=F(E_m),\qquad K^q\cong C^{q-1}(\mathcal B)\quad(q\geq1),
$$

where the differential from $K^0$ is the simultaneous restriction to the $E_i\cap E_m$, and subsequent differentials are the signed differentials of $\mathcal B$. The sign difference is removed by degreewise multiplication by $-1$ as appropriate; it has no effect on exactness.

By induction, $H^{>0}(C^\bullet(\mathcal B))=0$ and $H^0(C^\bullet(\mathcal B))=F(Z)$ (gluing on a finite closed cover). Hence $H^q(K^\bullet)=0$ for $q\geq2$, while

$$
H^1(K^\bullet)
\cong \mathrm{coker}\left(F(E_m)\longrightarrow F(Z)\right)
=0
$$

by the closed extension lemma. The long exact sequence for

$$
0\longrightarrow K^\bullet\longrightarrow C^\bullet(\mathcal E)
\longrightarrow C^\bullet(\mathcal A)\longrightarrow0
$$

now gives $H^q(C^\bullet(\mathcal E))=0$ for **every** $q>0$, simultaneously. In degree zero, compatible continuous functions on the $E_i$ glue to a continuous function on their finite closed union by the closed pasting lemma. This establishes the stated ordinary abelian-group theorem.

For an arbitrary family of product coordinates, apply the argument to each integer coordinate. Products are exact in abelian groups; no common finite quotient of the profinite test space is required.

## 4. Transport to genuine closed fibre relations: distinct obligations

For a profinite map $p:P\to T$, write $R_k=\{(x_1,\ldots,x_k)\in P^k:p(x_1)=\cdots=p(x_k)\}$. For each *fixed* degree $q$, a locally constant integer cochain on the closed $R_{q+1}$ extends to $P^{q+1}$; compactness yields a single finite observation $a:P\to J$ sufficient for its $q+1$ coordinates. Each $E_j=p(a^{-1}(j))$ is closed in $T$. The cocycle condition on genuine $R_{q+2}$ transfers to the appropriate finite closed family; the theorem above then produces a locally constant primitive on $R_q$, with no global section of $p$.

**This paragraph is a mathematical transport outline, not yet a proved categorical or Lean bridge.** It must explicitly establish the common finite-coordinate observation for arbitrary fixed $q$, compatible restriction and sign formulas, empty cases, and coordinatewise product transport.

## 5. Formalization and adversarial gates

1. Define the finite increasing-index cochain complex, its differential, and a real chain-level kernel decomposition when adjoining a last index. Prove $d^2=0$ and the corresponding long exact sequence, not just numerical degree calculations.
2. Prove the closed extension lemma on the exact pinned Profinite/LocallyConstant API, including empty domains. Establish finite-closed gluing in degree zero.
3. Prove the all-degree acyclicity as a Lean theorem quantified over $q:\mathbb N$. Avoid any new axioms, \`sorry\`, or unsound cast of classical topological cohomology into condensed Ext.
4. **Separate normalization:** the current CMDG formal files use tuples with repetitions and all index orders. Construct a verified chain comparison between that actual unnormalized Cech object and the increasing-index complex. Do not equate them by notation or assume alternation of arbitrary cochains.
5. For each positive integer degree, prove the genuine closed-relation scalar Hom, arbitrary-product Hom, all face maps and relations, Stonean-probe exactness, sheafification compatibility, and epimorphism of the true relation morphism in the next Cech degree.
6. Only after those genuine categorical steps and the exact Ext dimension-shifting argument may a statement of all-positive-degree Ext vanishing be proposed. The source-compatible **derived mapping comparison**, solid-side higher Ext control, and MATHCERT/source-semantic authority are separate further gates.

## Disposition

The finite closed-family result in section 3 is a mathematical argument for **all degrees**. Its exact Lean theorem, normalization, categorical transport, all-positive Ext claim, and derived-solidity comparison remain **OPEN**. The next substantive compiler target is the degree-uniform finite closed-family cochain complex and induction, not another bespoke H6 construction.

