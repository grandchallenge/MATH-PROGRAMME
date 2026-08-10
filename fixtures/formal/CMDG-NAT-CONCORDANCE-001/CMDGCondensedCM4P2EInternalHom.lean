import CMDGCondensedCM4P2E
import CMDGCondensedCM4P2EAlgebraic

/-!
# CMDG CM4-P2-E internal-Hom bridge

This auxiliary fixture isolates the sole remaining E1 construction: comparison of the protected
P2-D sheaf-level internal Hom with the discrete algebraic dual on finite modules.

The current checkpoint develops the canonical evaluation direction and the pointwise multiplication
operator needed for its inverse. It does not yet assert the enriched-end lift, the rank-one
isomorphism, or the final finite comparison.
-/

namespace CMDG.CondensedCM4P2E.InternalHom

universe u

open CategoryTheory Limits Opposite
open CategoryTheory.Enriched.FunctorCategory
open scoped CategoryTheory.MonoidalClosed

abbrev R := CMDG.CondensedCM4P2E.R.{u}
abbrev PresheafModule := CMDG.CondensedCM4P2D.PresheafModule.{u}

noncomputable abbrev coefficientPresheaf : PresheafModule :=
  CMDG.CondensedCM4P2D.coefficientPresheaf

noncomputable local instance : MonoidalClosed PresheafModule :=
  MonoidalClosed.FunctorCategory.monoidalClosed

noncomputable def rankOneInternalHom : PresheafModule :=
  (MonoidalClosed.internalHom.obj (op coefficientPresheaf)).obj coefficientPresheaf

lemma rankOneInternalHom_eq_functorEnrichedHom :
    rankOneInternalHom =
      functorEnrichedHom (ModuleCat.{u + 1} R) coefficientPresheaf coefficientPresheaf := rfl

abbrev RankOneTarget := rankOneInternalHom ≅ coefficientPresheaf

noncomputable abbrev coefficientAt (X : CompHaus.{u}) : ModuleCat.{u + 1} R :=
  coefficientPresheaf.obj (op X)

noncomputable def rankOneIdentityProjection (X : CompHaus.{u}) :=
  CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
    (ModuleCat.{u + 1} R)
    (Under.forget (op X) ⋙ coefficientPresheaf)
    (Under.forget (op X) ⋙ coefficientPresheaf)
    (Under.mk (𝟙 (op X)))

noncomputable def rankOneEndomorphismEvalOne (X : CompHaus.{u}) :
    (ihom (coefficientAt X)).obj (coefficientAt X) ⟶ coefficientAt X :=
  ModuleCat.ofHom
    { toFun := fun φ => φ (show coefficientAt X from LocallyConstant.const X (1 : R))
      map_add' := by
        intro φ ψ
        rfl
      map_smul' := by
        intro c φ
        rfl }

noncomputable def rankOneEvaluationApp (X : CompHaus.{u}) :
    rankOneInternalHom.obj (op X) ⟶ coefficientAt X := by
  rw [rankOneInternalHom_eq_functorEnrichedHom]
  exact rankOneIdentityProjection X ≫ rankOneEndomorphismEvalOne X

/-- Pointwise multiplication after pulling the coefficient section to a slice object. -/
noncomputable def rankOneSectionMul
    (X : CompHaus.{u}) (k : Under (op X))
    (a : coefficientAt X) (h : coefficientPresheaf.obj k.right) :
    coefficientPresheaf.obj k.right := by
  let a' : LocallyConstant (unop k.right) R := coefficientPresheaf.map k.hom a
  let h' : LocallyConstant (unop k.right) R := h
  exact a' * h'

/-- Multiplication by a section pulled back from the base of a slice object. -/
noncomputable def rankOneMultiplicationToEndomorphism
    (X : CompHaus.{u}) (k : Under (op X)) :
    coefficientAt X ⟶
      (ihom (coefficientPresheaf.obj k.right)).obj (coefficientPresheaf.obj k.right) :=
  ModuleCat.ofHom
    { toFun := fun a =>
        ModuleCat.ofHom
          { toFun := rankOneSectionMul X k a
            map_add' := by
              intro h₁ h₂
              ext y
              simp [rankOneSectionMul, mul_add]
            map_smul' := by
              intro c h
              ext y
              simp [rankOneSectionMul, mul_comm, mul_left_comm] }
      map_add' := by
        intro a b
        apply ModuleCat.hom_ext
        ext h y
        simp [rankOneSectionMul, add_mul]
      map_smul' := by
        intro c a
        apply ModuleCat.hom_ext
        ext h y
        simp [rankOneSectionMul, mul_assoc] }

#check rankOneInternalHom
#check rankOneInternalHom_eq_functorEnrichedHom
#check RankOneTarget
#check coefficientAt
#check rankOneIdentityProjection
#check rankOneEndomorphismEvalOne
#check rankOneEvaluationApp
#check rankOneSectionMul
#check rankOneMultiplicationToEndomorphism
#check CategoryTheory.Enriched.FunctorCategory.enrichedHomπ
#check CategoryTheory.Presheaf.functorEnrichedHomCoyonedaObjEquiv
#check CategoryTheory.presheafHom
#check CondensedMod.LocallyConstant.fullyFaithfulFunctor
#check CondensedMod.LocallyConstant.functorIsoDiscrete
#check MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerLeft
#check MonoidalClosed.enrichedOrdinaryCategorySelf_eHomWhiskerRight
#check ModuleCat.ihom_map_apply
#check ModuleCat.monoidalClosed_pre_app

#print axioms rankOneInternalHom_eq_functorEnrichedHom
#print axioms rankOneIdentityProjection
#print axioms rankOneEndomorphismEvalOne
#print axioms rankOneEvaluationApp
#print axioms rankOneSectionMul
#print axioms rankOneMultiplicationToEndomorphism

end CMDG.CondensedCM4P2E.InternalHom
