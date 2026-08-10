import CMDGCondensedCM4P2EFiniteTransport
import Mathlib.Algebra.Category.ModuleCat.Biproducts
import Mathlib.CategoryTheory.Adjunction.Additive
import Mathlib.CategoryTheory.Monoidal.Preadditive
import Mathlib.CategoryTheory.Preadditive.FunctorCategory

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

noncomputable def finiteFamilyInternalHom (X : FintypeCat.{u}) :
    CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u} :=
  (MonoidalClosed.internalHom.obj
      (op (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X))).obj
    CMDG.CondensedCM4P2D.coefficientPresheaf

noncomputable def finiteCoordinateInclusion
    (X : FintypeCat.{u}) (x : X.obj) :
    CMDG.CondensedCM4P2D.coefficientPresheaf ⟶
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X := by
  classical
  refine
    { app := fun S => ModuleCat.ofHom
        { toFun := fun h y => if y = x then h else 0
          map_add' := ?_
          map_smul' := ?_ }
      naturality := ?_ }
  · intro a b
    funext y
    by_cases hy : y = x <;> simp [hy]
  · intro c a
    funext y
    by_cases hy : y = x <;> simp [hy]
  · intro S T f
    apply ModuleCat.hom_injective
    apply LinearMap.ext
    intro h
    funext y
    change
      (if y = x then CMDG.CondensedCM4P2D.coefficientPresheaf.map f h else 0) =
        CMDG.CondensedCM4P2D.coefficientPresheaf.map f (if y = x then h else 0)
    by_cases hy : y = x <;> simp [hy]

noncomputable def finiteCoordinateProjection
    (X : FintypeCat.{u}) (x : X.obj) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X ⟶
      CMDG.CondensedCM4P2D.coefficientPresheaf where
  app S := ModuleCat.ofHom
    { toFun := fun a => a x
      map_add' := by intro a b; rfl
      map_smul' := by intro c a; rfl }
  naturality S T f := by
    apply ModuleCat.hom_injective
    apply LinearMap.ext
    intro a
    rfl

lemma finiteCoordinateInclusion_projection_self
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinateInclusion X x ≫ finiteCoordinateProjection X x =
      𝟙 CMDG.CondensedCM4P2D.coefficientPresheaf := by
  classical
  ext S h
  change (if x = x then h else 0) = h
  simp

lemma finiteCoordinateInclusion_projection_ne
    (X : FintypeCat.{u}) {x y : X.obj} (hxy : x ≠ y) :
    finiteCoordinateInclusion X x ≫ finiteCoordinateProjection X y = 0 := by
  classical
  have hyx : y ≠ x := fun h => hxy h.symm
  ext S h
  change (if y = x then h else 0) = 0
  simp [hyx]

lemma finiteCoordinate_resolution
    (X : FintypeCat.{u}) :
    (∑ x, finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x) =
      𝟙 (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X) := by
  classical
  apply NatTrans.ext
  funext S
  simp only [NatTrans.app_sum, NatTrans.id_app]
  apply ModuleCat.hom_injective
  apply LinearMap.ext
  intro a
  rw [ModuleCat.hom_sum]
  simp only [ModuleCat.hom_id, LinearMap.id_apply]
  let evalAtA :
      (↑((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X).obj S) →ₗ[
        CMDG.CondensedCM4P2D.R.{u}]
        ↑((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X).obj S)) →+
        ↑((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X).obj S) :=
    { toFun := fun f => f a
      map_zero' := rfl
      map_add' := by intro f g; rfl }
  change
    evalAtA
        (∑ i : X.obj,
          ModuleCat.Hom.hom
            ((finiteCoordinateProjection X i ≫ finiteCoordinateInclusion X i).app S)) = a
  rw [map_sum]
  funext y
  let evalAtY :
      ↑((CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X).obj S) →+
        LocallyConstant S.unop CMDG.CondensedCM4P2D.R.{u} :=
    { toFun := fun b => b y
      map_zero' := rfl
      map_add' := by intro b c; rfl }
  change
    evalAtY
        (∑ c : X.obj,
          (ModuleCat.Hom.hom ((finiteCoordinateInclusion X c).app S))
            ((ModuleCat.Hom.hom ((finiteCoordinateProjection X c).app S)) a)) = a y
  rw [map_sum]
  change (∑ c : X.obj, if y = c then a c else 0) = a y
  rw [Finset.sum_eq_single y]
  · simp
  · intro c _ hcy
    have hyc : y ≠ c := fun h => hcy h.symm
    simp [hyc]
  · simp

noncomputable def finiteCoordinateEvaluation
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteFamilyInternalHom X ⟶ CMDG.CondensedCM4P2D.coefficientPresheaf :=
  (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
      CMDG.CondensedCM4P2D.coefficientPresheaf ≫
    CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.hom

noncomputable def finiteCoordinateExtension
    (X : FintypeCat.{u}) (x : X.obj) :
    CMDG.CondensedCM4P2D.coefficientPresheaf ⟶ finiteFamilyInternalHom X :=
  CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.inv ≫
    (MonoidalClosed.pre (finiteCoordinateProjection X x)).app
      CMDG.CondensedCM4P2D.coefficientPresheaf

lemma monoidalClosed_pre_zero
    (A B : CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :
    MonoidalClosed.pre (0 : B ⟶ A) = 0 := by
  apply NatTrans.ext
  funext X
  apply MonoidalClosed.uncurry_injective
  simp

lemma monoidalClosed_pre_add
    (A B : CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u})
    (f g : B ⟶ A) :
    MonoidalClosed.pre (f + g) = MonoidalClosed.pre f + MonoidalClosed.pre g := by
  apply NatTrans.ext
  funext X
  apply MonoidalClosed.uncurry_injective
  simp [Preadditive.add_comp]

lemma finiteCoordinatePre_projection_inclusion
    (X : FintypeCat.{u}) (x y : X.obj) :
    (MonoidalClosed.pre (finiteCoordinateProjection X y)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf =
      (MonoidalClosed.pre
          (finiteCoordinateInclusion X x ≫ finiteCoordinateProjection X y)).app
        CMDG.CondensedCM4P2D.coefficientPresheaf := by
  have h := congrArg
    (fun η => η.app CMDG.CondensedCM4P2D.coefficientPresheaf)
    (MonoidalClosed.pre_map
      (finiteCoordinateInclusion X x) (finiteCoordinateProjection X y))
  simpa only [NatTrans.comp_app] using h.symm

#check finiteFamilyInternalHom
#check finiteCoordinateInclusion
#check finiteCoordinateProjection
#check finiteCoordinateInclusion_projection_self
#check finiteCoordinateInclusion_projection_ne
#check finiteCoordinate_resolution
#check finiteCoordinateEvaluation
#check finiteCoordinateExtension
#check monoidalClosed_pre_zero
#check monoidalClosed_pre_add
#check finiteCoordinatePre_projection_inclusion

#print axioms finiteCoordinateInclusion
#print axioms finiteCoordinateProjection
#print axioms finiteCoordinateInclusion_projection_self
#print axioms finiteCoordinateInclusion_projection_ne
#print axioms finiteCoordinate_resolution
#print axioms finiteCoordinateEvaluation
#print axioms finiteCoordinateExtension
#print axioms monoidalClosed_pre_zero
#print axioms monoidalClosed_pre_add

end CMDG.CondensedCM4P2E.FiniteDualTransport
