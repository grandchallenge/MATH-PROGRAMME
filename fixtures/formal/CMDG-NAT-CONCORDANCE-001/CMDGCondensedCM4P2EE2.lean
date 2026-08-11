import CMDGCondensedCM4P2EE2Core
import Mathlib.CategoryTheory.Sites.Limits
import Mathlib.Topology.Category.Profinite.Extend
import Mathlib.CategoryTheory.Functor.KanExtension.Pointwise

/-!
# CMDG CM4-P2-E E2 — sheaf lift and right Kan extension certificate

The finite-quotient colimit and internal-Hom limit calculation is frozen in
`CMDGCondensedCM4P2EE2Core`. This layer lifts that certified presheaf limit to condensed modules,
extends it to the structured-arrow cone, and certifies the pointwise and ordinary right Kan
extension statements. E3 uniqueness is not asserted here.
-/

namespace CMDG.CondensedCM4P2E.RightKanReconstruction

universe u

open CategoryTheory Limits Opposite

/-- Forget a condensed `R`-module to its underlying presheaf. -/
noncomputable abbrev condensedModuleToPresheaf : CondensedMod.{u} R ⥤ PresheafModule :=
  ObjectProperty.ι (Presheaf.IsSheaf (coherentTopology CompHaus.{u}))

set_option backward.isDefEq.respectTransparency.types false in
/-- Lift the certified presheaf limit explicitly through the fully faithful sheaf inclusion.
This is the pinned fully-faithful reflection construction specialized to the exact finite-quotient
diagram, avoiding the universe-polymorphic global reflection instance. -/
noncomputable def measureFunctorMapConeIsLimit (S : Profinite.{u}) :
    IsLimit (CMDG.CondensedCM4P2D.measureFunctor.mapCone S.asLimitCone) := by
  let U : CondensedMod.{u} R ⥤ PresheafModule := condensedModuleToPresheaf
  let c := CMDG.CondensedCM4P2D.measureFunctor.mapCone S.asLimitCone
  have hU : IsLimit (U.mapCone c) := by
    change IsLimit
      (CMDG.CondensedCM4P2D.measurePresheafFunctor.mapCone S.asLimitCone)
    exact measurePresheafFunctorMapConeIsLimit S
  exact
    (IsLimit.mkConeMorphism fun _ =>
      (Cone.functoriality
        (S.diagram ⋙ CMDG.CondensedCM4P2D.measureFunctor) U).preimage
          (hU.liftConeMorphism _)) <| by
      apply fun s m =>
        (Cone.functoriality
          (S.diagram ⋙ CMDG.CondensedCM4P2D.measureFunctor) U).map_injective _
      intro s m
      rw [Functor.map_preimage]
      apply hU.uniq_cone_morphism

/-- Extend the canonical finite-quotient limit to the full structured-arrow finite diagram. -/
noncomputable def measureFunctorStructuredArrowIsLimit (S : Profinite.{u}) :
    IsLimit (Profinite.Extend.cone CMDG.CondensedCM4P2D.measureFunctor S) :=
  Profinite.Extend.isLimitCone S.asLimitCone CMDG.CondensedCM4P2D.measureFunctor
    S.asLimit (measureFunctorMapConeIsLimit S)

/-- The right-extension object whose counit is exactly the certified E1 finite comparison. -/
noncomputable def measureRightExtension :
    Functor.RightExtension FintypeCat.toProfinite (Condensed.finFree R) :=
  Functor.RightExtension.mk CMDG.CondensedCM4P2D.measureFunctor
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom

/-- Whisker the certified E1 comparison over the structured-arrow finite diagram. -/
noncomputable def structuredArrowFiniteComparisonIso (S : Profinite.{u}) :
    StructuredArrow.proj S FintypeCat.toProfinite ⋙
        (FintypeCat.toProfinite ⋙ CMDG.CondensedCM4P2D.measureFunctor) ≅
      StructuredArrow.proj S FintypeCat.toProfinite ⋙ Condensed.finFree R :=
  Functor.isoWhiskerLeft
    (StructuredArrow.proj S FintypeCat.toProfinite)
    CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso

/-- Pulling the pointwise right-extension cone back across E1 recovers exactly the structured-arrow
measure cone. -/
noncomputable def structuredArrowMeasureConeIso (S : Profinite.{u}) :
    Profinite.Extend.cone CMDG.CondensedCM4P2D.measureFunctor S ≅
      (Cone.postcompose (structuredArrowFiniteComparisonIso S).inv).obj
        (measureRightExtension.coneAt S) :=
  Cone.ext (Iso.refl _) (by
    intro j
    change
      CMDG.CondensedCM4P2D.measureFunctor.map j.hom =
        𝟙 _ ≫
          (CMDG.CondensedCM4P2D.measureFunctor.map j.hom ≫
            CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom.app j.right) ≫
          CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.inv.app j.right
    simp)

/-- E2 pointwise form: at every profinite set the E1-counit right-extension cone is limiting. -/
noncomputable def measureRightExtensionIsPointwiseAt (S : Profinite.{u}) :
    measureRightExtension.IsPointwiseRightKanExtensionAt S := by
  have hpost :
      IsLimit
        ((Cone.postcompose (structuredArrowFiniteComparisonIso S).inv).obj
          (measureRightExtension.coneAt S)) :=
    (measureFunctorStructuredArrowIsLimit S).ofIsoLimit
      (structuredArrowMeasureConeIso S)
  exact
    (IsLimit.postcomposeInvEquiv
      (structuredArrowFiniteComparisonIso S)
      (measureRightExtension.coneAt S)) hpost

/-- E2 pointwise certificate. -/
noncomputable def measureRightExtensionIsPointwise :
    measureRightExtension.IsPointwiseRightKanExtension :=
  fun S => measureRightExtensionIsPointwiseAt S

/-- E2 ordinary form: the protected P2-D measure functor is a right Kan extension of the pinned
finite-free functor along `FintypeCat.toProfinite`, using the certified E1 comparison as counit. -/
theorem measureFunctorIsRightKanExtension :
    CMDG.CondensedCM4P2D.measureFunctor.IsRightKanExtension
      CMDG.CondensedCM4P2E.FiniteDualTransport.finiteComparisonNatIso.hom :=
  measureRightExtensionIsPointwise.isRightKanExtension

#check measurePresheafFunctorMapConeIsLimit
#check measureFunctorMapConeIsLimit
#check measureFunctorStructuredArrowIsLimit
#check measureRightExtension
#check structuredArrowFiniteComparisonIso
#check structuredArrowMeasureConeIso
#check measureRightExtensionIsPointwiseAt
#check measureRightExtensionIsPointwise
#check measureFunctorIsRightKanExtension

#print axioms measurePresheafFunctorMapConeIsLimit
#print axioms measureFunctorMapConeIsLimit
#print axioms measureFunctorStructuredArrowIsLimit
#print axioms measureRightExtension
#print axioms structuredArrowFiniteComparisonIso
#print axioms structuredArrowMeasureConeIso
#print axioms measureRightExtensionIsPointwiseAt
#print axioms measureRightExtensionIsPointwise
#print axioms measureFunctorIsRightKanExtension

end CMDG.CondensedCM4P2E.RightKanReconstruction