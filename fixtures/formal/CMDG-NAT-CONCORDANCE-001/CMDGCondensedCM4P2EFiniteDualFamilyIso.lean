import CMDGCondensedCM4P2EFiniteDualResolution

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

/-- Aggregate the coordinate evaluations into the canonical finite-family evaluation. -/
noncomputable def finiteFamilyEvaluation (X : FintypeCat.{u}) :
    finiteFamilyInternalHom X ⟶
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X :=
  ∑ x, finiteCoordinateEvaluation X x ≫ finiteCoordinateInclusion X x

/-- Aggregate the coordinate extensions into the canonical finite-family extension. -/
noncomputable def finiteFamilyExtension (X : FintypeCat.{u}) :
    CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X ⟶
      finiteFamilyInternalHom X :=
  ∑ x, finiteCoordinateProjection X x ≫ finiteCoordinateExtension X x

lemma finiteCoordinateExtension_familyEvaluation
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinateExtension X x ≫ finiteFamilyEvaluation X =
      finiteCoordinateInclusion X x := by
  classical
  unfold finiteFamilyEvaluation
  rw [Preadditive.comp_sum Finset.univ]
  rw [Finset.sum_eq_single x]
  · rw [← Category.assoc, finiteCoordinateExtension_evaluation_self]
    simp
  · intro y hy hyx
    rw [← Category.assoc, finiteCoordinateExtension_evaluation_ne X hyx]
    simp
  · simp

lemma finiteFamilyExtension_evaluation
    (X : FintypeCat.{u}) :
    finiteFamilyExtension X ≫ finiteFamilyEvaluation X =
      𝟙 (CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X) := by
  classical
  unfold finiteFamilyExtension
  rw [Preadditive.sum_comp Finset.univ]
  have hterm :
      (∑ x,
          (finiteCoordinateProjection X x ≫ finiteCoordinateExtension X x) ≫
            finiteFamilyEvaluation X) =
        ∑ x, finiteCoordinateProjection X x ≫ finiteCoordinateInclusion X x := by
    apply Finset.sum_congr rfl
    intro x hx
    rw [Category.assoc, finiteCoordinateExtension_familyEvaluation]
  rw [hterm, finiteCoordinate_resolution]

lemma finiteCoordinateInclusion_familyExtension
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinateInclusion X x ≫ finiteFamilyExtension X =
      finiteCoordinateExtension X x := by
  classical
  unfold finiteFamilyExtension
  rw [Preadditive.comp_sum Finset.univ]
  rw [Finset.sum_eq_single x]
  · rw [← Category.assoc, finiteCoordinateInclusion_projection_self]
    simp
  · intro y hy hxy
    rw [← Category.assoc, finiteCoordinateInclusion_projection_ne X hxy]
    simp
  · simp

lemma finiteCoordinateEvaluation_extension_pre
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinateEvaluation X x ≫ finiteCoordinateExtension X x =
      finiteCoordinatePreInclusionNamed X x ≫ finiteCoordinatePreProjectionNamed X x := by
  have hEval :
      finiteCoordinateEvaluation X x =
        finiteCoordinatePreInclusionNamed X x ≫
          CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.hom := rfl
  have hExt :
      finiteCoordinateExtension X x =
        CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.inv ≫
          finiteCoordinatePreProjectionNamed X x := rfl
  rw [hEval, hExt, Category.assoc]
  simp

lemma finiteFamilyEvaluation_extension
    (X : FintypeCat.{u}) :
    finiteFamilyEvaluation X ≫ finiteFamilyExtension X =
      𝟙 (finiteFamilyInternalHom X) := by
  classical
  unfold finiteFamilyEvaluation
  rw [Preadditive.sum_comp Finset.univ]
  have hterm :
      (∑ x,
          (finiteCoordinateEvaluation X x ≫ finiteCoordinateInclusion X x) ≫
            finiteFamilyExtension X) =
        ∑ x, finiteCoordinateEvaluation X x ≫ finiteCoordinateExtension X x := by
    apply Finset.sum_congr rfl
    intro x hx
    rw [Category.assoc, finiteCoordinateInclusion_familyExtension]
  rw [hterm]
  have hdiag :
      (∑ x, finiteCoordinateEvaluation X x ≫ finiteCoordinateExtension X x) =
        ∑ x, finiteCoordinatePreInclusionNamed X x ≫ finiteCoordinatePreProjectionNamed X x := by
    apply Finset.sum_congr rfl
    intro x hx
    exact finiteCoordinateEvaluation_extension_pre X x
  rw [hdiag, finiteFamilyPre_resolution]

/-- Fixed-finite-set internal duality, constructed canonically from coordinate maps. -/
noncomputable def finiteFamilyInternalHomIso (X : FintypeCat.{u}) :
    finiteFamilyInternalHom X ≅
      CMDG.CondensedCM4P2E.FiniteTransport.finiteCoefficientFamilyPresheaf X where
  hom := finiteFamilyEvaluation X
  inv := finiteFamilyExtension X
  hom_inv_id := finiteFamilyEvaluation_extension X
  inv_hom_id := finiteFamilyExtension_evaluation X

#check finiteFamilyEvaluation
#check finiteFamilyExtension
#check finiteCoordinateExtension_familyEvaluation
#check finiteFamilyExtension_evaluation
#check finiteCoordinateInclusion_familyExtension
#check finiteCoordinateEvaluation_extension_pre
#check finiteFamilyEvaluation_extension
#check finiteFamilyInternalHomIso

#print axioms finiteFamilyEvaluation
#print axioms finiteFamilyExtension
#print axioms finiteCoordinateExtension_familyEvaluation
#print axioms finiteFamilyExtension_evaluation
#print axioms finiteCoordinateInclusion_familyExtension
#print axioms finiteCoordinateEvaluation_extension_pre
#print axioms finiteFamilyEvaluation_extension
#print axioms finiteFamilyInternalHomIso

end CMDG.CondensedCM4P2E.FiniteDualTransport
