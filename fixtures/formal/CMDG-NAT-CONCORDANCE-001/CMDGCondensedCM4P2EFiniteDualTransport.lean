import CMDGCondensedCM4P2EFiniteTransport
import Mathlib.Algebra.Category.ModuleCat.Biproducts
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
  funext y
  simp only [ModuleCat.comp_apply, Finset.sum_apply]
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

#check finiteFamilyInternalHom
#check finiteCoordinateInclusion
#check finiteCoordinateProjection
#check finiteCoordinateInclusion_projection_self
#check finiteCoordinateInclusion_projection_ne
#check finiteCoordinate_resolution
#check finiteCoordinateEvaluation
#check finiteCoordinateExtension
#check MonoidalClosed.pre_map

#print axioms finiteCoordinateInclusion
#print axioms finiteCoordinateProjection
#print axioms finiteCoordinateInclusion_projection_self
#print axioms finiteCoordinateInclusion_projection_ne
#print axioms finiteCoordinate_resolution
#print axioms finiteCoordinateEvaluation
#print axioms finiteCoordinateExtension

end CMDG.CondensedCM4P2E.FiniteDualTransport
