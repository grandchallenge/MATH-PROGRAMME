import CMDGCondensedCM4P2EFiniteDualKronecker

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

lemma finiteCoordinateExtension_evaluation_self
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinateExtension X x ≫ finiteCoordinateEvaluation X x =
      𝟙 CMDG.CondensedCM4P2D.coefficientPresheaf := by
  have hExt :
      finiteCoordinateExtension X x =
        CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.inv ≫
          finiteCoordinatePreProjectionNamed X x := rfl
  have hEval :
      finiteCoordinateEvaluation X x =
        finiteCoordinatePreInclusionNamed X x ≫
          CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.hom := rfl
  rw [hExt, hEval, Category.assoc]
  rw [finiteCoordinatePreNamed_self_assoc]
  simp

lemma finiteCoordinateExtension_evaluation_ne
    (X : FintypeCat.{u}) {x y : X.obj} (hxy : x ≠ y) :
    finiteCoordinateExtension X y ≫ finiteCoordinateEvaluation X x = 0 := by
  have hExt :
      finiteCoordinateExtension X y =
        CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.inv ≫
          finiteCoordinatePreProjectionNamed X y := rfl
  have hEval :
      finiteCoordinateEvaluation X x =
        finiteCoordinatePreInclusionNamed X x ≫
          CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHomNatIso.hom := rfl
  rw [hExt, hEval, Category.assoc]
  rw [finiteCoordinatePreNamed_ne_assoc X hxy]
  simp

#check finiteCoordinateExtension_evaluation_self
#check finiteCoordinateExtension_evaluation_ne

#print axioms finiteCoordinateExtension_evaluation_self
#print axioms finiteCoordinateExtension_evaluation_ne

end CMDG.CondensedCM4P2E.FiniteDualTransport
