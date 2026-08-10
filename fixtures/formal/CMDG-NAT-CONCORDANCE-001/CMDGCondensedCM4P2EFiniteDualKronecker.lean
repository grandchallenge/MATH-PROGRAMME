import CMDGCondensedCM4P2EFiniteDualTransport

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

lemma finiteCoordinatePre_projection_inclusion_self
    (X : FintypeCat.{u}) (x : X.obj) :
    (MonoidalClosed.pre (finiteCoordinateProjection X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf =
      𝟙 CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom := by
  rw [finiteCoordinatePre_projection_inclusion]
  rw [finiteCoordinateInclusion_projection_self]
  simp

lemma finiteCoordinatePre_projection_inclusion_ne
    (X : FintypeCat.{u}) {x y : X.obj} (hxy : x ≠ y) :
    (MonoidalClosed.pre (finiteCoordinateProjection X y)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf = 0 := by
  rw [finiteCoordinatePre_projection_inclusion]
  rw [finiteCoordinateInclusion_projection_ne X hxy]
  rw [monoidalClosed_pre_zero]
  rfl

#check finiteCoordinatePre_projection_inclusion_self
#check finiteCoordinatePre_projection_inclusion_ne

#print axioms finiteCoordinatePre_projection_inclusion_self
#print axioms finiteCoordinatePre_projection_inclusion_ne

end CMDG.CondensedCM4P2E.FiniteDualTransport
