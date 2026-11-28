# CM5-R0: finite-torus boundary and canonical shifted unit (038)

## Disposition

The genuine canonical all-integer-shifts comparison is kernel-checked
relative to the explicit UniversalBD package. No independent
certification or claim of an internally constructed UniversalBD
inhabitant is made. This is the existing protected comparison,
not a replacement map. Parent PR #3842 is merged at
d5f97c2e2c0033a7c4d9a14cf6e5cc72613233ea.

## Finite-torus boundary and scalar vanishing

Use the genuine integer-real-circle short exact sequence. By 036,
the real product has zero scalar Ext in all degrees, conditional
on UniversalBD. Its actual Yoneda boundary is consequently an
additive equivalence in each degree. The reindex morphism of
short exact sequences proves naturality of this equivalence.

The discrete integer coefficient object is projective: locally
constant condensation is left adjoint to evaluation at the point,
which preserves epimorphisms by the Stonean evaluation criterion.
The rank-one module is projective by lifting the value at one.
For a finite index set, the actual integer-product fan is a
bilimit bicone. Its Ext decomposition and projectivity give zero
positive Ext. The boundary identifies degree-one circle Ext with
the product of the rank-one degree-zero Ext groups. Its inverse
description is the sum of actual coordinate boundaries
(finiteCircleExtOne_eq_sum), not an abstract dimension count.

By 037, every class of degree at least two for the full circle
product is the pullback of a finite-stage class, hence zero.
The actual boundary gives

$$
\mathrm{Ext}^{q}(\mathbb Z^I,\mathbb Z)=0
\qquad(q>0).
$$

In degree zero the same naturality and finite-stage descent show
that each genuine morphism from the integer product to the scalar
coefficient factors through a finite-coordinate projection.

## Product target detection

For any categorical product of condensed modules, every Ext
class is detected jointly by its projections. In degree zero
this is the product universal property. In positive degree take
a projective presentation of the source, lift the class by the
Yoneda boundary from its kernel in one lower degree, and project
to each coefficient. Exactness and the vanishing projected
original classes imply that each projected lift extends across
the projective. In positive lower degree these extensions vanish,
so induction detects the lift as zero. In lower degree zero the
extensions are genuine morphisms and the product universal
property assembles them. Exactness then kills the original class.
No exchange of products with derived functors is assumed.

## Genuine canonical comparison

The protected solidIntegerIso identifies the genuine source G_T
with an integer product. The protected
gsFreeSolidToCoefficientProductIso identifies the genuine target
G_S with a product of scalar coefficient sheaves. The two results
above therefore give

$$
\mathrm{Ext}^{q}(G_T,G_S)=0
\qquad(q>0).
$$

Apply the existing protected theorem
shiftedComparisonCandidate_iff_genuineSolidSourceExtZero.
This proves canonicalUnit_allShifts_of_UniversalBD for every
profinite S. Its conclusion is the existing ShiftedComparisonBijectiveCandidate,
which uses precomposition by the actual canonical solidification
unit in every integer source shift.

This route bypasses a separate formalization of internal derived
Hom. It does not claim a new internal-Hom object isomorphism.
The published existence theorem (Scholze, Lectures on Condensed
Mathematics, arXiv:2605.03658v1, Theorem 4.10) supplies the
universal finite-type package at source level. The remaining
kernel-level obligation is to construct an inhabitant of UniversalBD
in the required universe, not to assume one by an axiom or
replace the analytic calculation by an external duality theorem.

## Evidence

Lean v4.33.0-rc1, mathlib
79d0395a1825a6264ad5d269e35e60537518955e.
Exact 216-module source closure and pinned manifest/toolchain
matched the candidate repository. All new modules passed locally.

| Endpoint module suffix | Local capture |
| --- | --- |
| FiniteTorusBoundary | 204fc55c03594c2ca96bd90af6f882f9 |
| ProductExtDetection | 608be420192046ababb43eacf219c864 |
| CanonicalUnitBD | 608be420192046ababb43eacf219c864 |

The pre-existing UniformDerivedUnitExtCriterion was replayed
in capture 9912764ec2084c5fbc3e3f97b151d50c.
All printed axioms are propext, Classical.choice and Quot.sound.
The explicit UniversalBD parameter remains in the theorem.
Initial diagnostics concerned a missing local Mathlib olean and
the lifted scalar action; the rank-one proof uses ext_ring
and the existing span-singleton linear map to avoid that
unneeded import. The final modules passed fresh local replay.
Local captures are not independent attestations. Protected native
exact-head replay is the admission requirement.

## Residual

Construct UniversalBD internally. Independent review and
certification remain governed separately. No promotion beyond
the actual checked conditional theorem.
