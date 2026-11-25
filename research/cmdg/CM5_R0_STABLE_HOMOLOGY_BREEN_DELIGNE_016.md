# CM5 R0 — reduced bar stable range and the finite-type obstruction

## Disposition

Source-relative reconstruction of the stable-homology input in Scholze,
arXiv:2605.03658v1, Lecture IV, Theorems 4.14 and 4.16.
The new EilenbergMacLaneModel Lean module constructs the Dold–Kan
simplicial group and reduced free integral chain functor. Its exact-head
replay is required. The topological filtration and homology calculations
below are not asserted as Lean theorems.

## Stable homology from the reduced bar filtration

Take a well-pointed CW model of the simplicial abelian group
$K(L,n)$, for a finite free lattice $L$ and $n\geq 1$.
Use the usual realization of the simplicial group bar construction
with simplices $G^p$ in degree $p$, where $G=K(L,n)$.
Its degeneracy subspace consists of tuples having an identity entry.
The reduced skeletal bar filtration has cofibers
$\Sigma^p G^{\wedge p}$ for $p\geq1$; equivalently one can use
the normalized simplicial-direction bar spectral sequence.
This assertion uses the proper/well-pointed bar realization and
the product latching-cofibration theorem, not arbitrary quotient
homology of noncofibrant spaces.

Since $G$ has connectivity at least $n-1$, its reduced integral homology vanishes
in degrees below $n$. The reduced Künneth theorem gives vanishing of
$\widetilde H_i(G^{\wedge p};\mathbb Z)$ for $i<pn$,
including the Tor terms, whose least possible degree is higher.
Consequently the cofibers in filtration $p\geq2$ have zero
reduced homology below $2n+2$. The first filtration is $\Sigma G$.
The exact sequences of successive filtration pairs, followed by
the increasing skeletal colimit, give the natural suspension map

$$
\widetilde H_{n+j}(K(L,n);\mathbb Z)
\longrightarrow
\widetilde H_{n+j+1}(K(L,n+1);\mathbb Z)
$$

as an isomorphism for $0\leq j<n$.
In this degree the source degree plus one is at most $2n$,
so neither the relative group nor its next-degree group can obstruct
the comparison. The identification $BG\simeq K(L,n+1)$ uses the
contractible universal bar bundle and its homotopy exact sequence.

For fixed $j$, choose $n>j$ and define
$M_j=\widetilde H_{n+j}(K(\mathbb Z,n);\mathbb Z)$.
The suspension maps identify this definition for every larger $n$.
$M_0=\mathbb Z$ by Hurewicz.

Finite generation follows separately, without presuming stability:
$K(\mathbb Z,1)$ has the homotopy type of the circle, so every
integral homology group is finitely generated. If $G$ has
finitely generated integral homology in every degree, the finite
smash powers have the same property by reduced Künneth.
The reduced bar spectral sequence has finitely generated entries
in every bidegree and a finite filtration in each total degree;
hence $BG$ has finitely generated homology in each degree.
Induction proves the desired finite generation for $M_j$.

## Naturality in the lattice

For $L,L'$ finite free, the model sends their direct sum to the
product of Eilenberg–MacLane spaces, up to the natural equivalence.
The quotient of the product by the wedge is the smash product.
Its reduced homology vanishes below $2n$; more precisely the
Künneth decomposition in degrees below $2n$ consists exactly of
the two individual reduced homology groups, via the inclusions
and projections. Thus in degree $n+j<2n$ the functor on lattices
preserves biproducts. It is additive: addition of maps factors
through the diagonal and codiagonal, which become the diagonal
and codiagonal of the homology biproduct.
Evaluating at rank one therefore gives the canonical natural
identification

$$
\widetilde H_{n+j}(K(L,n);\mathbb Z)\cong M_j\otimes_{\mathbb Z}L.
$$

The map sends a simple tensor $m\otimes x$ to the image of $m$
under the homology map induced by $\mathbb Z\to L,1\mapsto x$.
A finite basis proves invertibility, but the map does not depend
on that basis. This is the actual natural stable-range input,
not just an equality of ranks.

## Consequence for the lattice functor

Use the reduced bar complexes shifted down by $n$.
Each chain term is a finite sum of polynomial free functors or
a direct summand of one (reduction at the basepoint). The
augmentation at degree zero must be the canonical Hurewicz
identification with $L$. The stable-range homology above provides
the approximate-resolution input in Scholze Lemma 4.15.
For finitely generated $M$, choose an exact finite free presentation
$0\to\mathbb Z^a\to\mathbb Z^b\to M\to0$.
Tensoring objectwise with the free lattice $L$ gives a short exact
sequence of functors. The pseudocoherence closure properties and
the approximate-resolution lemma give the induction of Theorem 4.14.
They still require realization in Lean.

The Dold–Kan chain model is an alternative to the iterated multisimplicial
bar model. To use it in the induction formally, establish the comparison
of their integral chains or prove the corresponding bar filtration
for the Dold–Kan model itself; no such identification is assumed in
the new Lean module. Likewise finite simplex coproducts alone do not
prove the finite-projective chain term statement for the reduced free
functor. The natural splitting of its augmentation must be transported
to the lattice functor category, and the universal matrix formulas
must subsequently be extended to arbitrary abelian groups and
sheafified. No new foundational axiom or MATHCERT claim.

## Explicit approximate-resolution induction

Write FP(k) for an object admitting a partial resolution through
degree k by finitely generated projectives, with FP(0) meaning
finitely generated. Use the category of lattice functors, with
finite direct sums of the actual free representables and their
retracts as the finite projectives.

The two closure rules are proved by the ordinary horseshoe
construction for extensions and by the mapping cone of a lift
of the map in a short exact sequence:
- If both outer terms of a short exact sequence are FP(k),
  then so is the middle term.
- If the middle term is FP(k) and the left term is FP(k-1),
  then the right term is FP(k), for k at least one.
  In degree zero only finite generation of the middle term is needed.

For the second rule, a resolution of the left term lifted into
one of the middle term produces a cone resolution of the right
term. In degree k the new term is the sum of the middle
degree k term and the left degree k-1 term, exactly the stated
finite-type requirements. These constructions can first extend
the partial resolutions by arbitrary projectives without a
finiteness condition beyond the required degrees. The first rule
uses projective lifts against the right-hand surjections at
each degree, and the kernel short exact sequences from the
snake lemma, so the finite-type requirement is preserved.

Consider an augmented complex of finite projectives

$$
P_n\longrightarrow\cdots\longrightarrow P_0\longrightarrow X\longrightarrow0.
$$

Let $Z_i$ denote the kernel of the outgoing differential from
$P_i$, including the augmentation at zero, and let $B_i$ be
the image of the next differential. Let $H_i=Z_i/B_i$.
Suppose $H_i$ is FP(n-i-1) for $0\leq i<n$.
Because $B_{n-1}$ is a quotient of $P_n$, it is FP(0).
The sequence $0\to B_{n-1}\to Z_{n-1}\to H_{n-1}\to0$
makes $Z_{n-1}$ FP(0).
Descend from i+1 to i. From the exact sequence

$$
0\to Z_{i+1}\to P_{i+1}\to B_i\to0
$$

and the second closure rule, $B_i$ is FP(n-i-1).
The first closure rule applied to $0\to B_i\to Z_i\to H_i\to0$
gives $Z_i$ FP(n-i-1). Finally,
$0\to Z_0\to P_0\to X\to0$ makes X FP(n).
This is the exact degree accounting in the approximate-resolution lemma.

For the identity lattice functor U, the rank-one free
representable maps onto U by evaluation, and the rank-two term
generates the kernel by the additivity relations
$[a+b]-[a]-[b]$. Thus U is FP(1). For the induction to FP(n),
take the reduced n-fold bar complex shifted down by n. The
Hurewicz augmentation is onto with zero augmented H(0).
The remaining H(i), for i<n, are naturally $M_i\otimes U$.
By the finite presentation of $M_i$ and the second closure rule,
they are FP(n-1) when U is FP(n-1), hence satisfy the weaker
FP(n-i-1) hypotheses above.

Reduction and simplicial normalization are natural split summands
of finite sums of free representables. If a finite projective
resolution term is only a retract of such a sum, add the
complement as a contractible pair in that degree and the next
degree. Starting at degree zero and iterating constructs a
resolution whose terms themselves are finite sums of the actual
representables, without an infinite sum at any fixed degree.
The exact augmentation is unaffected. Equivalently one can use
Schanuel's lemma to prolong any previously fixed finite free
partial resolution.

This establishes the finite-type conclusion in source mathematics
conditional only on the stated standard bar, connectivity and
Künneth inputs, and on the standard projective resolution
constructions. It is not a formal proof that the new Lean
Dold–Kan complex has these homology objects.

## Explicit remaining Lean obligations

- Actual reduced bar filtration, latching cofibers and homology
  comparison with the Dold–Kan model.
- Connectivity/Künneth, finite generation and stable suspension
  in the actual models, including naturality in lattice maps.
- Pseudocoherence approximation and finite projective resolution
  extraction; extension to arbitrary groups and condensed sheaves.
- Derived condensed cohomology comparison and exact shifted
  solidification endpoint.
