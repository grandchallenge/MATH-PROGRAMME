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
with $p$-simplices $G^p$, where $G=K(L,n)$.
Its degeneracy subspace consists of tuples having an identity entry.
The reduced skeletal bar filtration has cofibers
$\Sigma^p G^{\wedge p}$ for $p\geq1$; equivalently one can use
the normalized simplicial-direction bar spectral sequence.
This assertion uses the proper/well-pointed bar realization and
the product latching-cofibration theorem, not arbitrary quotient
homology of noncofibrant spaces.

Since $G$ is $(n-1)$-connected, its reduced integral homology vanishes
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

## Explicit remaining Lean obligations

- Actual reduced bar filtration, latching cofibers and homology
  comparison with the Dold–Kan model.
- Connectivity/Künneth, finite generation and stable suspension
  in the actual models, including naturality in lattice maps.
- Pseudocoherence approximation and finite projective resolution
  extraction; extension to arbitrary groups and condensed sheaves.
- Derived condensed cohomology comparison and exact shifted
  solidification endpoint.
