import CMDGCondensedCM4P3DerivedCM5R0RealCircleCondensedNonSplit
import Mathlib.CategoryTheory.Preadditive.Projective.Basic

/-!
# CMDG CM5: the genuine condensed circle product is not projective

This is an actual categorical consequence of the nonsplit exact real/circle sequence.
It does not assert that the solidification of the circle is nonprojective, or compute Ext.
-/
noncomputable section
universe u
open CategoryTheory
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
open CMDG.CondensedCM5R0.RealCircleSheafExact
open CMDG.CondensedCM5R0.RealCircleNonSplit
namespace CMDG.CondensedCM5R0.RealCircleProjectivity

variable (I : Type u) [Nonempty I]

theorem circleProductCondensed_not_projective :
    ¬ Projective ((realCircleCondensedSequence I).X₃) := by
  intro hproj
  letI : Projective ((realCircleCondensedSequence I).X₃) := hproj
  letI : Epi ((realCircleCondensedSequence I).g) :=
    (realCircleCondensedSequence_shortExact I).epi_g
  let s := Projective.factorThru (𝟙 ((realCircleCondensedSequence I).X₃))
    ((realCircleCondensedSequence I).g)
  have hs : s ≫ (realCircleCondensedSequence I).g = 𝟙 _ :=
    Projective.factorThru_comp (𝟙 ((realCircleCondensedSequence I).X₃))
      ((realCircleCondensedSequence I).g)
  exact realCircleCondensedSequence_nonsplit I ⟨s, hs⟩

#print axioms circleProductCondensed_not_projective
end CMDG.CondensedCM5R0.RealCircleProjectivity
