import CMDGCondensedCM4P2E
import CMDGCondensedCM4P2EAlgebraic
import Mathlib.Algebra.Algebra.Bilinear

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
  let Y : CompHaus.{u} := k.right.unop
  let a' : LocallyConstant Y R := coefficientPresheaf.map k.hom a
  let h' : LocallyConstant Y R := h
  exact LinearMap.mul R (LocallyConstant Y R) a' h'

/-- Pullback along the coefficient presheaf preserves pointwise multiplication. -/
lemma coefficientMap_mul
    {A B : CompHaus.{u}ᵒᵖ} (f : A ⟶ B)
    (x y : coefficientPresheaf.obj A) :
    coefficientPresheaf.map f (x * y) =
      coefficientPresheaf.map f x * coefficientPresheaf.map f y := by
  rfl

/-- Pullback along a morphism in the slice carries the coefficient pulled back from the base to the
same coefficient section pulled back along the target leg. -/
lemma coefficientPullback_triangle
    (X : CompHaus.{u}) {i j : Under (op X)} (f : i ⟶ j) :
    coefficientPresheaf.map i.hom ≫ coefficientPresheaf.map f.right =
      coefficientPresheaf.map j.hom := by
  rw [← coefficientPresheaf.map_comp, Under.w f]

/-- Pointwise multiplication by a coefficient section pulled back from the slice base is natural
under every morphism of the slice. -/
lemma rankOneSectionMul_naturality
    (X : CompHaus.{u}) {i j : Under (op X)} (f : i ⟶ j)
    (a : coefficientAt X) (h : coefficientPresheaf.obj i.right) :
    coefficientPresheaf.map f.right (rankOneSectionMul X i a h) =
      rankOneSectionMul X j a (coefficientPresheaf.map f.right h) := by
  have ha :
      coefficientPresheaf.map f.right (coefficientPresheaf.map i.hom a) =
        coefficientPresheaf.map j.hom a := by
    have htriangle := congrArg
      (fun q : coefficientAt X ⟶ coefficientPresheaf.obj j.right => q a)
      (coefficientPullback_triangle X f)
    simpa only [ModuleCat.comp_apply] using htriangle
  change
    coefficientPresheaf.map f.right
        (coefficientPresheaf.map i.hom a * h) =
      coefficientPresheaf.map j.hom a * coefficientPresheaf.map f.right h
  rw [coefficientMap_mul, ha]

/-- Multiplication by a section pulled back from the base of a slice object, packaged directly in
the categorical Hom carrier underlying the internal Hom. This uses the ambient `R`-linear category
structure and therefore does not introduce a second scalar-action requirement on the coefficient
module. -/
noncomputable def rankOneMultiplicationToEndomorphism
    (X : CompHaus.{u}) (k : Under (op X)) :
    coefficientAt X ⟶
      (ihom (coefficientPresheaf.obj k.right)).obj (coefficientPresheaf.obj k.right) := by
  let Y : CompHaus.{u} := k.right.unop
  let A := LocallyConstant Y R
  let pull : coefficientAt X →ₗ[R] A := (coefficientPresheaf.map k.hom).hom
  let mul : A →ₗ[R] A →ₗ[R] A := LinearMap.mul R A
  let pack : (A →ₗ[R] A) →ₗ[R]
      (coefficientPresheaf.obj k.right ⟶ coefficientPresheaf.obj k.right) :=
    { toFun := fun f => ModuleCat.ofHom f
      map_add' := by
        intro f g
        rfl
      map_smul' := by
        intro r f
        apply ModuleCat.hom_injective
        rfl }
  exact ModuleCat.ofHom (pack.comp (mul.comp pull))

#check rankOneInternalHom
#check rankOneInternalHom_eq_functorEnrichedHom
#check RankOneTarget
#check coefficientAt
#check rankOneIdentityProjection
#check rankOneEndomorphismEvalOne
#check rankOneEvaluationApp
#check rankOneSectionMul
#check coefficientMap_mul
#check coefficientPullback_triangle
#check rankOneSectionMul_naturality
#check rankOneMultiplicationToEndomorphism
#check LinearMap.mul
#check ModuleCat.homLinearEquiv
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
#print axioms coefficientMap_mul
#print axioms coefficientPullback_triangle
#print axioms rankOneSectionMul_naturality
#print axioms rankOneMultiplicationToEndomorphism

end CMDG.CondensedCM4P2E.InternalHom
