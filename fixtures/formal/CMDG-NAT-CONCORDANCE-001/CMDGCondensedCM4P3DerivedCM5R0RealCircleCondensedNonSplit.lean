import CMDGCondensedCM4P3DerivedCM5R0RealCircleSheafTransfer
import CMDGCondensedCM4P3DerivedCM5R0RealCircleUnderlyingNonSplit

/-!
# CMDG CM5: nonsplitting of the actual condensed real-circle extension

A Stonean point detects the nonzero order-two circle class. Every
additive section would send it into the torsion-free real product,
contradicting its image under the quotient. Transfer the obstruction
through the genuine Stonean sheaf equivalence into CondensedAb.
-/

noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
open CMDG.CM5R0.NonSplit

namespace CMDG.CondensedCM5R0.RealCircleNonSplit

variable (I : Type u) [Nonempty I]
local instance : IsTopologicalAddGroup (ULift.{u+1,u} (I → UnitAddCircle)) := ⟨⟩

private def testStonean : Stonean.{u} := Stonean.of (ULift.{u} PUnit)
private def testPoint : testStonean.{u} := ⟨PUnit.unit⟩

private def halfCircleSection : C(testStonean.{u}, ULift.{u+1,u} (I → UnitAddCircle)) :=
  ContinuousMap.const _ ⟨fun _ => ((1/2 : ℝ) : UnitAddCircle)⟩

omit [Nonempty I] in
private theorem halfCircleSection_two_zero :
    (2 : ℕ) • halfCircleSection I = 0 := by
  ext x i
  simpa [halfCircleSection, Pi.smul_apply] using circle_half_two_zero

private theorem halfCircleSection_ne_zero :
    halfCircleSection I ≠ 0 := by
  intro h
  let i : I := Classical.choice ‹Nonempty I›
  have hi := congrArg
    (fun f : C(testStonean.{u}, ULift.{u+1,u} (I → UnitAddCircle)) =>
      (f (testPoint.{u})).down i) h
  apply circle_half_ne_zero
  simpa [halfCircleSection] using hi

/-- The actual morphism of Stonean sheaves is not split epi. -/
theorem sheafRealCircle_noSection
    (s : stoneanModuleSheaf (ULift.{u+1,u} (I → UnitAddCircle)) ⟶
         stoneanModuleSheaf (ULift.{u+1,u} (I → ℝ)))
    (hs : s ≫ stoneanSheafMap (ULift.{u+1,u} (I → ℝ))
                 (realProductTopHom I) (realProductTopHom_continuous I) = 𝟙 _) : False := by
  letI : HasLimitsOfSize.{u,u+1} (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  let S : Stonean.{u} := testStonean.{u}
  let c : C(S, ULift.{u+1,u} (I → UnitAddCircle)) := halfCircleSection I
  let f : C(S, ULift.{u+1,u} (I → UnitAddCircle)) →ₗ[ULift.{u+1} ℤ]
    C(S, ULift.{u+1,u} (I → ℝ)) := (s.hom.app (Opposite.op S)).hom
  let r : C(S, ULift.{u+1,u} (I → ℝ)) := f c
  have hc : (2 : ℕ) • c = 0 := halfCircleSection_two_zero I
  have hr : (2 : ℕ) • r = 0 := by
    change (2 : ℕ) • f c = 0
    rw [← map_nsmul f, hc, map_zero]
  have hr0 : r = 0 := by
    ext x i
    have hi := congrArg (fun f : C(S, ULift.{u+1,u} (I → ℝ)) =>
        (f x).down i) hr
    have hz : (2 : ℕ) • ((r x).down i) = 0 := by
      simpa only [ContinuousMap.nsmul_apply, ULift.smul_down, Pi.smul_apply, ContinuousMap.zero_apply, ULift.zero_down, Pi.zero_apply] using hi
    exact add_self_eq_zero.mp (by simpa [two_nsmul] using hz)
  have hsS := congrArg
      (fun f : stoneanModuleSheaf (ULift.{u+1,u} (I → UnitAddCircle)) ⟶
          stoneanModuleSheaf (ULift.{u+1,u} (I → UnitAddCircle)) =>
        (f.hom.app (Opposite.op S)) c) hs
  have hc0 : c = 0 := by
    change (postcomposeAddHom (ULift.{u+1,u} (I → ℝ))
      (realProductTopHom I) (realProductTopHom_continuous I) S) r = c at hsS
    rw [hr0, map_zero] at hsS
    exact hsS.symm
  exact (halfCircleSection_ne_zero I) hc0


/-- The real-to-circle quotient is a genuinely nonsplit morphism in CondensedAb. -/
theorem condensedRealCircle_noSection
    (s : condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → UnitAddCircle)) ⟶
         condensedTopologicalGroupViaSheaf (ULift.{u+1,u} (I → ℝ)))
    (hs : s ≫ condensedRealToCircle I = 𝟙 _) : False := by
  letI : HasLimitsOfSize.{u,u+1} (ModuleCat.{u+1} (ULift.{u+1} ℤ)) :=
    hasLimitsOfSizeShrink.{u,u+1,u+1,u} _
  let E := Condensed.StoneanCompHaus.equivalence
    (ModuleCat.{u+1} (ULift.{u+1} ℤ))
  let t : stoneanModuleSheaf (ULift.{u+1,u} (I → UnitAddCircle)) ⟶
          stoneanModuleSheaf (ULift.{u+1,u} (I → ℝ)) := E.functor.preimage s
  have ht : t ≫ stoneanSheafMap (ULift.{u+1,u} (I → ℝ))
                 (realProductTopHom I) (realProductTopHom_continuous I) = 𝟙 _ := by
    apply E.functor.map_injective
    rw [CategoryTheory.Functor.map_comp]
    have hmap : E.functor.map t = s := E.functor.map_preimage s
    rw [hmap, E.functor.map_id]
    exact hs
  exact sheafRealCircle_noSection I t ht

/-- Non-split exact sequence on the actual condensed product objects. -/
theorem realCircleCondensedSequence_nonsplit :
    ¬ ∃ s : (realCircleCondensedSequence I).X₃ ⟶
              (realCircleCondensedSequence I).X₂,
          s ≫ (realCircleCondensedSequence I).g = 𝟙 _ := by
  rintro ⟨s, hs⟩
  exact condensedRealCircle_noSection I s hs

#print axioms realCircleCondensedSequence_nonsplit
#print axioms condensedRealCircle_noSection
#print axioms sheafRealCircle_noSection
end CMDG.CondensedCM5R0.RealCircleNonSplit
