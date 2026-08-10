import CMDGCondensedCM4P2E
import CMDGCondensedCM4P2EAlgebraic

/-!
# CMDG CM4-P2-E internal-Hom bridge

This auxiliary fixture isolates the sole remaining E1 construction: comparison of the protected
P2-D sheaf-level internal Hom with the discrete algebraic dual on finite modules.

The first checkpoint freezes only the rank-one target and the identity-arrow projection from the
enriched end. It does not assert the rank-one isomorphism or the final finite comparison.
-/

namespace CMDG.CondensedCM4P2E.InternalHom

universe u

open CategoryTheory Opposite
open CategoryTheory.Enriched.FunctorCategory
open scoped CategoryTheory.MonoidalClosed

abbrev R := CMDG.CondensedCM4P2E.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule.{u}

noncomputable abbrev coefficientPresheaf : PresheafModule :=
  CMDG.CondensedCM4P2D.coefficientPresheaf

noncomputable local instance : MonoidalClosed PresheafModule :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- Rank-one specialization of the protected P2-D internal-Hom construction. -/
noncomputable def rankOneInternalHom : PresheafModule :=
  (MonoidalClosed.internalHom.obj (op coefficientPresheaf)).obj coefficientPresheaf

lemma rankOneInternalHom_eq_functorEnrichedHom :
    rankOneInternalHom =
      functorEnrichedHom (ModuleCat.{u + 1} R) coefficientPresheaf coefficientPresheaf := rfl

/-- The rank-one theorem target. This is a type alias only; no inhabitant is asserted here. -/
abbrev RankOneTarget := rankOneInternalHom ≅ coefficientPresheaf

/-- At a test object `X`, project the enriched end defining the internal Hom to the identity object
of `Under (op X)`. This is the canonical observation point for the evaluation-at-one inverse. -/
noncomputable def rankOneIdentityProjection (X : CompHaus.{u}) :=
  CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
    (ModuleCat.{u + 1} R)
    (Under.forget (op X) ⋙ coefficientPresheaf)
    (Under.forget (op X) ⋙ coefficientPresheaf)
    (Under.mk (𝟙 (op X)))

#check rankOneInternalHom
#check rankOneInternalHom_eq_functorEnrichedHom
#check RankOneTarget
#check rankOneIdentityProjection
#check CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
#check CategoryTheory.Presheaf.functorEnrichedHomCoyonedaObjEquiv
#check CategoryTheory.presheafHom
#check CondensedMod.LocallyConstant.fullyFaithfulFunctor
#check CondensedMod.LocallyConstant.functorIsoDiscrete

#print axioms rankOneInternalHom_eq_functorEnrichedHom
#print axioms rankOneIdentityProjection

end CMDG.CondensedCM4P2E.InternalHom
