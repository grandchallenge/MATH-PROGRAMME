# CM5 R0: stable additivity and natural lattice stabilization

The genuine reduced integral homology functor in degree n+k of the
Dold–Kan Eilenberg–MacLane model is additive whenever k < n, for
all abelian groups and all their homomorphisms.

## Proof

For a group A let R(A) be the reduced free integral module, with
generator [a] and [0]=0. The reduced basis supplies the linear maps
q: R(A) -> R(A) tensor R(A) and c: R(A) tensor R(A) -> R(A)
defined on generators by q([a])=[a] tensor [a] and
c([a] tensor [b])=[a+b]-[a]-[b]. Both are natural for group maps,
including maps that kill a generator.

For f,g:A->B the exact defect R(f+g)-R(f)-R(g) is the composite
q, R(f) tensor R(g), c. This identity extends to actual simplicial
objects, then to alternating chains. The signed Eilenberg–Zilber
comparison identifies the intermediate diagonal tensor chain
homology with ordinary tensor-complex homology. Both reduced
complexes are supported from n, so the tensor complex is supported
from 2n. Its homology is zero below 2n. The defect therefore
vanishes in homology in the stable range. Additivity of the actual
Dold–Kan Eilenberg–MacLane functor follows from the earlier natural
finite simplex decomposition. No additivity of reduced free chains
is presumed.

## Finite lattice naturality

For any additive functor F from abelian groups to integer modules,
preservation of finite biproducts gives a coordinate isomorphism
F(Z^r) -> F(Z)^r. The i-th component is F applied to the i-th
coordinate projection. For any integer matrix f: Z^r -> Z^s,
the induced map in these coordinates is the very same integer
matrix acting on F(Z). This is proved by expanding each coordinate
of f as a finite linear combination of the standard projections.

Thus stable homology on the finite lattice category is determined
naturally by its rank-one coefficient. The actual rank-one stable
suspension isomorphism from reconstruction 026, applied
coordinatewise and conjugated by the coordinate isomorphisms,
gives a natural isomorphism of successive stable homology functors
on that category. The proof uses the matrix action, not a choice
of unrelated objectwise isomorphisms.

## Verified scope and remaining work

Five Lean modules establish the cross-effect identity, its
simplicial and homological transport, the finite lattice
coordinate comparison, the natural matrix action, and a natural
stabilization on the finite lattice skeleton. All audited
declarations use only the standard Lean axioms.

The natural stabilization is transported from the actual rank-one
map. Equality with the earlier geometric suspension at every rank
is a separate obligation. This construction suffices to identify
successive stable coefficient functors on the lattice skeleton.

Finite generation of the rank-one coefficient groups remains the
next substantive obligation: establish the finite homology of the
circle model at n=1 and propagate finite generation through the
genuine reduced bar filtration and its tensor columns. Then
construct the finite presentation of the stable coefficient
module and the pseudocoherence approximate-resolution induction.
The derived real and circle cohomology comparisons and independent
CM5 certification remain open. The genuine solid analytic bridge
of PR #3785 is already protected-admitted.
