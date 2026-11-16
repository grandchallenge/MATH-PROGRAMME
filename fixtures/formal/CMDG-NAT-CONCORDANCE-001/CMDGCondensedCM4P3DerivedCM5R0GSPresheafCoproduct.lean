import CMDGCondensedCM4P3DerivedCM5R0GSCoordinateEquiv
import Mathlib.CategoryTheory.Limits.FunctorCategory.Basic

/-!
# CMDG CM5: the Nöbeling basis-source presheaf is an actual coproduct

This file closes the presheaf (not merely condensed-sheaf) coproduct
obligation. The legs are the actual Finsupp.lsingle rank-one presheaf
inclusions already used by the canonical G_S coefficient comparison.

At each compact Hausdorff test X, the protected compact-test coordinate
equivalence identifies the evaluated source with the actual module Finsupp
coproduct. Compatibility of this isomorphism with every inclusion makes
an isomorphism of evaluated cocones, rather than just of objects.
Joint reflection of colimits by evaluation then gives the full presheaf
coproduct universal property. No finiteness hypothesis on the index type.

This is a colimit statement in the presheaf category. The enriched
internal-Hom coproduct-to-product isomorphism, identification with the
canonical G_S coefficient comparison, and the Ext¹ consequence remain
separate obligations.
-/

noncomputable section

universe u

open CategoryTheory Limits Opposite

namespace CMDG.CondensedCM5R0

private abbrev R : Type (u + 1) := CMDG.CondensedCM4P2D.R.{u}

/-- The actual rank-one inclusion cocone in the full presheaf category.
This is not a sheaf-only coproduct witness. -/
noncomputable def gsBasisDiscreteSourcePresheafCofan
    (S : Profinite.{u}) :
    Cofan (fun _ : LiftedSourceBasisIndex S =>
      CMDG.CondensedCM4P2D.coefficientPresheaf) :=
  Cofan.mk (gsBasisDiscreteSourcePresheaf S)
    (gsBasisCoefficientInclusionPresheaf S)

/-- The compact-test coordinate equivalence carries each actual rank-one
presheaf inclusion to the corresponding Finsupp.lsingle injection. -/
theorem gsBasisCoordinateLinear_comp_single
    (X : CompHaus.{u}) (I : Type (u + 1)) (i : I) :
    (gsLocallyConstantFinsupp_coordinateLinear X I).comp
      (LocallyConstant.mapₗ R.{u}
        (Finsupp.lsingle i : R.{u} →ₗ[R.{u}] (I →₀ R.{u}))) =
      (Finsupp.lsingle i : LocallyConstant X R.{u} →ₗ[R.{u}]
        (I →₀ LocallyConstant X R.{u})) := by
  classical
  have h := gsLocallyConstantFinsupp_coordinate_assemble X I
  have hi := congrArg
    (fun (φ : (I →₀ LocallyConstant X R.{u}) →ₗ[R.{u}]
        (I →₀ LocallyConstant X R.{u})) =>
      φ.comp (Finsupp.lsingle i)) h
  simpa [gsLocallyConstantFinsupp_assembleLinear, LinearMap.comp_assoc] using hi

/-- At each test space, the actual evaluated presheaf cocone is
isomorphic as a cocone to the canonical Finsupp coproduct cocone. -/
noncomputable def gsBasisPresheafEvaluatedCofanIso
    (S : Profinite.{u}) (X : CompHaus.{u}) :
    ((evaluation (CompHaus.{u}ᵒᵖ) (ModuleCat.{u + 1} R.{u})).obj
      (op X)).mapCocone (gsBasisDiscreteSourcePresheafCofan S) ≅
      ModuleCat.finsuppCocone R.{u} (LocallyConstant X R.{u})
        (LiftedSourceBasisIndex S) := by
  refine Cocone.ext
    ((gsLocallyConstantFinsupp_coordinateEquiv X
      (LiftedSourceBasisIndex S)).toModuleIso) ?_
  rintro ⟨i⟩
  apply ModuleCat.hom_injective
  change (gsLocallyConstantFinsupp_coordinateLinear X
      (LiftedSourceBasisIndex S)).comp
      (LocallyConstant.mapₗ R.{u}
        (Finsupp.lsingle i : R.{u} →ₗ[R.{u}]
          (LiftedSourceBasisIndex S →₀ R.{u}))) =
        (Finsupp.lsingle i : LocallyConstant X R.{u} →ₗ[R.{u}]
          (LiftedSourceBasisIndex S →₀ LocallyConstant X R.{u}))
  exact gsBasisCoordinateLinear_comp_single X (LiftedSourceBasisIndex S) i

/-- The actual Nöbeling basis source is a coproduct of rank-one
coefficient presheaves in the complete presheaf category, by pointwise
reflection of the colimit property. -/
noncomputable def gsBasisDiscreteSourcePresheafCofanIsColimit
    (S : Profinite.{u}) :
    IsColimit (gsBasisDiscreteSourcePresheafCofan S) := by
  apply evaluationJointlyReflectsColimits
  intro X
  exact (ModuleCat.finsuppCoconeIsColimit R.{u}
    (LocallyConstant X.unop R.{u}) (LiftedSourceBasisIndex S)).ofIsoColimit
      (gsBasisPresheafEvaluatedCofanIso S X.unop).symm

/-- A bounded witness of the arbitrary coproduct in the actual presheaf
category, built from the verified colimiting inclusion cocone. -/
noncomputable instance gsBasisPresheafCoeffHasCoproduct
    (S : Profinite.{u}) :
    HasCoproduct (fun _ : LiftedSourceBasisIndex S =>
      CMDG.CondensedCM4P2D.coefficientPresheaf) :=
  HasColimit.mk
    ⟨gsBasisDiscreteSourcePresheafCofan S,
      gsBasisDiscreteSourcePresheafCofanIsColimit S⟩

/-- Canonical categorical coproduct of coefficient presheaves is the
exact source presheaf used in the protected enriched internal Hom. -/
noncomputable def gsBasisDiscreteSourcePresheafCoproductIso
    (S : Profinite.{u}) :
    (∐ (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2D.coefficientPresheaf)) ≅
      gsBasisDiscreteSourcePresheaf S :=
  IsColimit.coconePointUniqueUpToIso
    (colimit.isColimit (Discrete.functor
      (fun _ : LiftedSourceBasisIndex S =>
        CMDG.CondensedCM4P2D.coefficientPresheaf)))
    (gsBasisDiscreteSourcePresheafCofanIsColimit S)

#check gsBasisDiscreteSourcePresheafCofan
#check gsBasisCoordinateLinear_comp_single
#check gsBasisPresheafEvaluatedCofanIso
#check gsBasisDiscreteSourcePresheafCofanIsColimit
#check gsBasisPresheafCoeffHasCoproduct
#check gsBasisDiscreteSourcePresheafCoproductIso

#print axioms gsBasisCoordinateLinear_comp_single
#print axioms gsBasisPresheafEvaluatedCofanIso
#print axioms gsBasisDiscreteSourcePresheafCofanIsColimit
#print axioms gsBasisPresheafCoeffHasCoproduct
#print axioms gsBasisDiscreteSourcePresheafCoproductIso

end CMDG.CondensedCM5R0
