# CM5 R0: integer rank-one homology and stable finite generation (041)

## Disposition

The integral rank-one homology base is now kernel-checked.
The actual reduced Dold–Kan chain model of the integer group in
degree one has homology the integers in degree one and zero in
all other degrees. Every homology group of every positive-stage
rank-one Eilenberg–Mac Lane model is finitely generated. The actual
stable homology functor evaluated at the integer group is finite.

Parent PR #3853 merged at
1aef34aea4e3f3d8a8a133c825a369674a97e418.
This completes the rank-one finite-generation input for the
approximate-resolution induction in 016 and 030. It does not
construct LatticeBD.

## Equivariant integer-line comparison

Let V_n be the free integer module on (n+1)-tuples of integer
vertices. The simplicial vertex functor pulls back tuples along
ordinal maps; the actual alternating face differential deletes
vertices. Simultaneous translation commutes with the differential.
Prepending a chosen vertex a defines a cone c_a. For positive
degree its boundary identity is

$$
d c_a+c_a d=1.
$$

Translation carries this cone to the cone based at the translated
vertex. These statements are checked as maps, not just on a
chosen homology representative.

The two-term line resolution can be realized directly inside V,
avoiding the group-ring and representation-theoretic dependency.
The finite signed chain of unit edges P(a,b) from a to b is
defined by the coefficient at k of the step indicator at b
minus the step indicator at a. The support lies between a and b.
The following identities hold for arbitrary integers, including
negative endpoints and reversed paths:

$$
d P(a,b)=[b]-[a],\quad
P(a,b)+P(b,c)=P(a,c),\quad
T_s P(a,b)=P(a+s,b+s).
$$

Define the straightening map E to be identity on vertices,
the signed path map on edges, and zero in higher degrees.
The triangle identity establishes that E is a chain map,
and the translation identity makes E equivariant. This is the
oriented line model of the two-term resolution with differential
t-1 in Laurent-polynomial coordinates.

A direct all-degree construction provides the equivariant
homotopy, with H_0 zero. At degree n+1 the difference of the
identity, E, and the already constructed lower homotopy applied
to the boundary is a cycle. Fill it by the cone based at the first
vertex of the generator tuple. Extend linearly. The previous-degree
homotopy equation implies the cycle condition, and the cone
identity supplies the primitive. Translation equivariance follows
by induction from the equivariance of the residual and of the
cone at the translated vertex. In every positive degree,

$$
dH+Hd=1-E.
$$

No assertion about the group-ring resolution is needed as an axiom.

## Descent to the actual additive bar

Adjacent differences give a natural simplicial map from the
homogeneous vertex tuples to the actual additive group bar.
Partial sums give representatives with first vertex zero.
Their composite on a homogeneous tuple is the translation by
the negative of its first vertex. The section followed by the
quotient map is identity in every degree.

Every equivariant map of homogeneous free modules therefore
descends to the corresponding orbit modules: precompose with
the partial-sum section and postcompose with the edge quotient.
The quotient is split epi, and the square for each descended map
commutes. Consequently the actual alternating differential and
the descended homotopy satisfy the same identity.

In degrees at least two the descended E vanishes. Every cycle
there is a boundary, with its primitive given by the descended H.
In degree one the differential is zero, and the descended
straightening sends a generator indexed by an integer x to x
times the unit-edge generator. Displacement vanishes on
boundaries, by the triangle formula. Every degree-one class is
an integer multiple of the unit-edge class.

The natural free-abelian-group to integer-finitely-supported-module
isomorphism identifies these orbit chains with the actual
unreduced free chains of the bar. The existing natural reduced-free
inclusion and projection give a retract on actual chain complexes.
Thus all positive higher homology vanishes in the reduced complex
and finite generation follows from the orbit calculation.

The protected barEMIso and barReducedIso transport these conclusions
to the degree-one Eilenberg–Mac Lane model. Degree zero vanishes by
the existing support theorem. The canonical bottom homology
comparison, transported through the integer-module equivalence,
identifies degree one with the integers themselves. This avoids
assuming that a cyclic group has no torsion simply because it has
one generator.

## All positive stages and the stable lattice input

Apply the checked finite_from_bar theorem of 040 to the actual
integer bar. It uses degreewise finite free replacement, tensor
homotopy invariance, and the finite bar filtration in each degree.
The result integer_em_finite proves finite generation of every
homology group at every positive Eilenberg–Mac Lane stage.

The endpoint stable_rank_one_finite identifies the actual stable
functor evaluated on the rank-one lattice with this finite
homology. In the stable range, the existing additive matrix theorem
then describes its entire restriction to finite free lattices.
A finite free presentation of the coefficient gives a short exact
sequence of additive lattice functors with finite sums of the
identity lattice functor as the first two terms. The remaining
formal work is to realize this natural presentation, prove the
FP closure and approximate-resolution induction, and extract a
coherent infinite resolution by finite polynomial terms in the
lifted lattice category. The already checked extension 039 then
constructs UniversalBD from that resolution.

## Evidence

Lean v4.33.0-rc1, mathlib
79d0395a1825a6264ad5d269e35e60537518955e.
Exact 82-module source closure, including toolchain and manifest,
matched to the candidate repository: capture
23f03ce228f24c78b710827edcc35331.

| Module suffix | Final local capture |
| --- | --- |
| BreenDeligneIntegerVertices | afecf476255d4ad0868f1bdef72d9591 |
| BreenDeligneIntegerLine | a1a710432c1e4481915233778dce7653 |
| BreenDeligneIntegerStraightening | 566c956df26c4ba9a921704878ff30f9 |
| BreenDeligneIntegerOrbits | aa3a5811758c43c881642cb9ac62f3c3 |
| BreenDeligneIntegerOrbitHomology | b1414dcc772c4300ac402d00f520795d |
| BreenDeligneIntegerReducedHomology | 428d9e809dd94810a140e51cdafb023d |
| BreenDeligneRankOneFinite | d0deeaffbabe4fa5a1d24f6f3fc6b566 |

All checked endpoints report only propext, Classical.choice and
Quot.sound. Initial elaboration, scalar-instance, and rewrite
diagnostics were repaired and replayed. One overly broad
integer induction simplification timed out; explicit integer
equalities removed that issue. No new external package, Mathlib
source patch, HDD fallback, or manual CI duplication was used.
Local captures are not independent attestations.

No inhabitant of LatticeBD or unconditional canonical comparison
is claimed. No independent certification has been issued.
