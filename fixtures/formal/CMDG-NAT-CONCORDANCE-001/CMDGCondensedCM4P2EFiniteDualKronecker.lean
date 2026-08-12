import CMDGCondensedCM4P2EFiniteDualTransport

namespace CMDG.CondensedCM4P2E.FiniteDualTransport

universe u
open CategoryTheory Opposite
open scoped CategoryTheory.MonoidalClosed BigOperators
attribute [local instance] FintypeCat.fintype

noncomputable local instance : MonoidalClosed
    (CompHaus.{u}ᵒᵖ ⥤ ModuleCat.{u + 1} CMDG.CondensedCM4P2D.R.{u}) :=
  MonoidalClosed.FunctorCategory.monoidalClosed

@[reassoc]
lemma finiteCoordinatePre_projection_inclusion_self
    (X : FintypeCat.{u}) (x : X.obj) :
    (MonoidalClosed.pre (finiteCoordinateProjection X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf =
      𝟙 CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom := by
  rw [finiteCoordinatePre_projection_inclusion]
  rw [finiteCoordinateInclusion_projection_self]
  rw [MonoidalClosed.pre_id]
  unfold CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom
  rfl

@[reassoc]
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

/-- The coordinate `pre` map with its rank-one source kept explicit. -/
noncomputable def finiteCoordinatePreProjectionNamed
    (X : FintypeCat.{u}) (x : X.obj) :
    CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom ⟶ finiteFamilyInternalHom X :=
  (MonoidalClosed.pre (finiteCoordinateProjection X x)).app
    CMDG.CondensedCM4P2D.coefficientPresheaf

/-- The coordinate `pre` map with its rank-one target kept explicit. -/
noncomputable def finiteCoordinatePreInclusionNamed
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteFamilyInternalHom X ⟶ CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom :=
  (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
    CMDG.CondensedCM4P2D.coefficientPresheaf

@[reassoc]
lemma finiteCoordinatePreNamed_self
    (X : FintypeCat.{u}) (x : X.obj) :
    finiteCoordinatePreProjectionNamed X x ≫ finiteCoordinatePreInclusionNamed X x =
      𝟙 CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom := by
  change
    (MonoidalClosed.pre (finiteCoordinateProjection X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf =
      𝟙 CMDG.CondensedCM4P2E.InternalHom.rankOneInternalHom
  exact finiteCoordinatePre_projection_inclusion_self X x

@[reassoc]
lemma finiteCoordinatePreNamed_ne
    (X : FintypeCat.{u}) {x y : X.obj} (hxy : x ≠ y) :
    finiteCoordinatePreProjectionNamed X y ≫ finiteCoordinatePreInclusionNamed X x = 0 := by
  change
    (MonoidalClosed.pre (finiteCoordinateProjection X y)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf ≫
        (MonoidalClosed.pre (finiteCoordinateInclusion X x)).app
          CMDG.CondensedCM4P2D.coefficientPresheaf = 0
  exact finiteCoordinatePre_projection_inclusion_ne X hxy

#check finiteCoordinatePre_projection_inclusion_self
#check finiteCoordinatePre_projection_inclusion_self_assoc
#check finiteCoordinatePre_projection_inclusion_ne
#check finiteCoordinatePre_projection_inclusion_ne_assoc
#check finiteCoordinatePreProjectionNamed
#check finiteCoordinatePreInclusionNamed
#check finiteCoordinatePreNamed_self
#check finiteCoordinatePreNamed_self_assoc
#check finiteCoordinatePreNamed_ne
#check finiteCoordinatePreNamed_ne_assoc

#print axioms finiteCoordinatePre_projection_inclusion_self
#print axioms finiteCoordinatePre_projection_inclusion_ne
#print axioms finiteCoordinatePreNamed_self
#print axioms finiteCoordinatePreNamed_ne

end CMDG.CondensedCM4P2E.FiniteDualTransport
