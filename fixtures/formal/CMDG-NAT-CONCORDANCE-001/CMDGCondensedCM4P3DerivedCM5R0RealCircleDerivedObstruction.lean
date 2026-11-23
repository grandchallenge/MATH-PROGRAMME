import CMDGCondensedCM4P3DerivedCM5R0RealCircleCondensedNonSplit
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExtClass
import Mathlib.Algebra.Homology.DerivedCategory.FullyFaithful

/-!
# CMDG CM5: canonical nonzero derived connecting morphism

The actual short exact circle product extension is nonsplit; via full
faithfulness of the degree-zero embedding and the triangulated Yoneda exactness
of the actual distinguished triangle, its connecting map cannot vanish.
-/
noncomputable section
universe u
open CategoryTheory CategoryTheory.Limits DerivedCategory Pretriangulated Abelian
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
open CMDG.CondensedCM5R0.RealCircleSheafExact
open CMDG.CondensedCM5R0.RealCircleNonSplit
namespace CMDG.CondensedCM5R0.RealCircleDerivedObstruction

attribute [local instance] HasDerivedCategory.standard
variable (I : Type u) [Nonempty I]

private abbrev S := realCircleCondensedSequence I
private abbrev hs : (S I).ShortExact := realCircleCondensedSequence_shortExact I

/-- The authentic derived connecting morphism of the non-split short exact
real-circle sequence is nonzero. -/
theorem realCircle_singleDelta_ne_zero : (hs I).singleδ ≠ 0 := by
  intro hzero
  let F := singleFunctor CondensedAb.{u} (0 : ℤ)
  let T := (hs I).singleTriangle
  have hT : T ∈ distTriang (DerivedCategory CondensedAb.{u}) :=
    (hs I).singleTriangle_distinguished
  have hTzero : T.mor₃ = 0 := hzero
  have hc : (𝟙 T.obj₃) ≫ T.mor₃ = 0 := by simp [hTzero]
  obtain ⟨s, hsection⟩ := T.coyoneda_exact₃ hT (𝟙 T.obj₃) hc
  let s0 : (S I).X₃ ⟶ (S I).X₂ := F.preimage s
  have hs0 : s0 ≫ (S I).g = 𝟙 _ := by
    apply F.map_injective
    rw [F.map_comp, F.map_id]
    have hpre : F.map s0 = s := F.map_preimage s
    rw [hpre]
    exact hsection.symm
  exact realCircleCondensedSequence_nonsplit I ⟨s0, hs0⟩

#print axioms realCircle_singleDelta_ne_zero

local instance : HasExt.{u+2} CondensedAb.{u} := HasExt.standard _

/-- A concrete nonzero class in the actual Ext¹ group of condensed abelian groups. -/
theorem realCircle_extClass_ne_zero : (hs I).extClass ≠ 0 := by
  intro he
  have he' := congrArg (fun e : Ext.{u+2} (S I).X₃ (S I).X₁ 1 => e.hom) he
  apply realCircle_singleDelta_ne_zero I
  simpa only [ShortComplex.ShortExact.extClass_hom, Ext.zero_hom] using he'

#print axioms realCircle_extClass_ne_zero

end CMDG.CondensedCM5R0.RealCircleDerivedObstruction
