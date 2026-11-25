# CM5 R0: canonical positive-degree bottom homology

This advances the actual reduced Dold-Kan chain construction
of PR 3710 and canonical augmentation of PR 3725. The finite
projective lattice terms are already protected. No stable
higher-homology or final CM5 claim is made.

For a simplicial abelian group whose degree k term is zero,
the degree k+2 simplex obtained by summing the first degeneracy
of a and the second degeneracy of b has faces a, a+b, b,
then zero. This is verified using the simplicial identities,
including the tail index bounds. The natural reduced generator
is the free generator minus the identity generator, so the
alternating differential produces the additive boundary relation
on reduced generators.

For the actual Eilenberg-MacLane object in degree k+1, the
outgoing bottom differential vanishes. The bottom homology
quotient map is therefore an epimorphism from the reduced chain
group. Its value on reduced generators is additive by the
explicit boundary relation. This produces a homomorphism
from the original bottom simplex group onto bottom homology.
The quotient factors through the actual evaluation map, checked
by the free group universal property and natural reduced
projection.

The Moore projector is the identity in the first nonzero
simplex degree. The normalization map there is consequently an
isomorphism. Its composite with the actual Dold-Kan counit
and single-complex identification is an isomorphism onto the
input group. The composite of the additive homology class map
and the previously defined bottomHomologyToGroup equals exactly
this comparison. Since the additive class map is epi and its
composite is iso, it is iso, and so is the canonical bottom
homology map. Naturality follows from the chain augmentation
and the single-complex homology isomorphism.

The two Lean modules BreenDeligneAdditiveBoundary and
BreenDeligneBottomInjectivity establish witness_boundary,
class_factor, classHom_epi, bottomHomologyToGroup_iso,
and bottomHomologyNaturalIso. The local SSD replays report
only propext, Classical.choice and Quot.sound. The statement
is for positive degrees, parametrized by k+1. Degree zero
is not covered by this isomorphism.

Remaining substantive obligations: higher stable suspension
and finite generation in the genuine model, finite-projective
approximate-resolution induction, extension from lattices
to general condensed inputs, compact cohomology comparison,
and canonical shifted solidification. Native exact-head
validation and protected admission are separate from local
compiler checks; no independent certification is claimed.
