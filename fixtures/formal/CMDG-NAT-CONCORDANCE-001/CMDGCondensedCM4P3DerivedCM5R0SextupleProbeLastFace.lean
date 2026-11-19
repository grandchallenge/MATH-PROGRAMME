import CMDGCondensedCM4P3DerivedCM5R0SextupleRepresentedProbe

/-!
# CM5 Ext5: last face of the actual represented sixth Cech probe

The sixth (last-vertex deletion) face agrees with the
universe-lifted split-set last face under genuine represented
categorical sixfold and fivefold Stonean equivalences.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

theorem stoneanCompHausProbeCechSextupleUlift_face5
    (T : Profinite.{u}) (U : Stonean.{u})
    (z : ULift.{u + 1}
      (U.compHaus ⟶ profiniteToCompHaus.obj
        (stoneanPresentationCechSextuples T))) :
    splitFreeCechSextFace5 (stoneanCompHausProbePresentationMap T U)
      (stoneanCompHausProbeCechSextupleUliftEquiv T U z) =
    stoneanCompHausProbeCechQuintupleUliftEquiv T U
      (ULift.up (z.down ≫ profiniteToCompHaus.map
        (pullback.fst
          (stoneanCechQuintupleVertexFirst T ≫ Profinite.presentation.π T)
          (Profinite.presentation.π T)))) := by
  rfl


/-- Sixth Čech boundary on the ACTUAL categorical sextuple
Profinite pullback, transported via the verified isomorphism. -/
noncomputable def stoneanCechCategoricalSixthBoundary (T : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechSextuples T)) ⟶
    ((Condensed.profiniteFree Coeff).obj
      (stoneanCechExplicitQuintupleProfinite T)) :=
  (Condensed.profiniteFree Coeff).map
    (stoneanCechCategoricalSextupleToExplicit T) ≫
      stoneanCechSixthBoundary T

theorem stoneanCechCategoricalSixthBoundary_comp_fifth_zero
    (T : Profinite.{u}) :
    stoneanCechCategoricalSixthBoundary T ≫
      stoneanCechFifthBoundary T = 0 := by
  unfold stoneanCechCategoricalSixthBoundary
  rw [Category.assoc, stoneanCechSixthBoundary_comp_fifthBoundary_zero,
    comp_zero]

/-- The categorical sixth boundary factors into the genuine fifth
Čech relation kernel, without asserting epimorphy. -/
noncomputable def stoneanCechCategoricalSixthToFifthRelation
    (T : Profinite.{u}) :
    ((Condensed.profiniteFree Coeff).obj
      (stoneanPresentationCechSextuples T)) ⟶
    stoneanCechFifthRelationKernel T :=
  (Condensed.profiniteFree Coeff).map
    (stoneanCechCategoricalSextupleToExplicit T) ≫
      stoneanCechSixthToFifthRelation T

theorem stoneanCechCategoricalSixthToFifthRelation_inclusion
    (T : Profinite.{u}) :
    stoneanCechCategoricalSixthToFifthRelation T ≫
      kernel.ι (stoneanCechFifthToFourthRelation T) =
        stoneanCechCategoricalSixthBoundary T := by
  unfold stoneanCechCategoricalSixthToFifthRelation
    stoneanCechCategoricalSixthBoundary
  rw [Category.assoc, stoneanCechSixthToFifthRelation_comp_inclusion]

#print axioms stoneanCechCategoricalSixthBoundary_comp_fifth_zero
#print axioms stoneanCechCategoricalSixthToFifthRelation_inclusion
#print axioms stoneanCompHausProbeCechSextupleUlift_face5
end CMDG.CondensedCM5R0
