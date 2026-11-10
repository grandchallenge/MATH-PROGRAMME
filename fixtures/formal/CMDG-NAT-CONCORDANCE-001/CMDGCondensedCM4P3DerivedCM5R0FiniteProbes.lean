import CMDGCondensedCM4P3DerivedCM5R0PositiveShifts
import Mathlib.CategoryTheory.Functor.KanExtension.Pointwise

/-!
# CMDG CM5-R0: derived comparison for finite profinite probes, every shift

The functor from finite sets to profinite spaces is fully faithful.
The pointwise right-Kan-extension counit of `profiniteSolid` is therefore
an isomorphism upon restriction to a finite profinite object.  As the
solidification map is a left inverse of this counit, it too is an
isomorphism.  Mapping into the derived category and shifting preserves
isomorphisms; consequently the derived comparison is bijective in all
integer degrees, including the first negative source shift n = -1.

This is a proof for finite *test objects*, not for arbitrary profinite tests.
It does not prove derived solidity, Ext vanishing for infinite profinite
tests, source equivalence, or global graph certification.
-/

noncomputable section

universe u

open CategoryTheory Pretriangulated

namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

/-- The right-Kan counit is invertible when restricted to a finite
profinite test object, by full faithfulness of the finite-set embedding. -/
private theorem finite_counit_isIso (X : FintypeCat.{u}) :
    IsIso ((Condensed.profiniteSolidCounit Coeff).app X) := by
  have h : IsIso (Condensed.profiniteSolidCounit Coeff) :=
    (Condensed.profiniteSolidIsPointwiseRightKanExtension Coeff).isIso_hom
  letI := h
  infer_instance

/-- The universal solidification arrow is invertible over finite profinite
test objects, independently of the target condensed module. -/
theorem solidification_isIso_finite (X : FintypeCat.{u}) :
    IsIso ((Condensed.profiniteSolidification Coeff).app
      (FintypeCat.toProfinite.obj X)) := by
  letI := finite_counit_isIso X
  have hfac :
      (Condensed.profiniteSolidification Coeff).app
        (FintypeCat.toProfinite.obj X) ≫
        (Condensed.profiniteSolidCounit Coeff).app X = 𝟙 _ := by
    simpa [Condensed.profiniteSolidification] using
      (Condensed.profiniteSolid Coeff).liftOfIsRightKanExtension_fac_app
        (Condensed.profiniteSolidCounit Coeff)
        (Condensed.profiniteFree Coeff)
        (𝟙 _) X
  exact isIso_of_comp_hom_eq_id
    ((Condensed.profiniteSolidCounit Coeff).app X) hfac

/-- Precomposition with an isomorphism is bijective on all Hom sets. -/
private theorem bijective_precomp_iso
    {C : Type*} [Category* C] {A B Z : C}
    (f : A ⟶ B) [IsIso f] :
    Function.Bijective (fun g : B ⟶ Z => f ≫ g) := by
  constructor
  · intro g h eq
    have he := congrArg (fun q => inv f ≫ q) eq
    simpa [Category.assoc] using he
  · intro q
    refine ⟨inv f ≫ q, ?_⟩
    simp [Category.assoc]

/-- Every shifted comparison is bijective on finite profinite test objects,
including the genuine Ext-sensitive n = -1 instance. -/
theorem comparisonAtShift_finite_bijective
    (S : Profinite.{u}) (X : FintypeCat.{u}) (n : ℤ) :
    Function.Bijective
      (comparisonAtShift S (FintypeCat.toProfinite.obj X) n) := by
  haveI : IsIso ((Condensed.profiniteSolidification Coeff).app
      (FintypeCat.toProfinite.obj X)) :=
    solidification_isIso_finite X
  haveI : IsIso (solidificationAtZero (FintypeCat.toProfinite.obj X)) := by
    dsimp [solidificationAtZero]
    infer_instance
  haveI : IsIso ((shiftFunctor (DerivedCategory Ambient) n).map
      (solidificationAtZero (FintypeCat.toProfinite.obj X))) := inferInstance
  change Function.Bijective
    (fun g => (shiftFunctor (DerivedCategory Ambient) n).map
      (solidificationAtZero (FintypeCat.toProfinite.obj X)) ≫ g)
  exact bijective_precomp_iso _

/-- The first negative shift for finite tests is a direct corollary. -/
theorem comparisonAtShift_neg_one_finite_bijective
    (S : Profinite.{u}) (X : FintypeCat.{u}) :
    Function.Bijective
      (comparisonAtShift S (FintypeCat.toProfinite.obj X) (-1)) :=
  comparisonAtShift_finite_bijective S X (-1)

#print axioms solidification_isIso_finite
#print axioms comparisonAtShift_finite_bijective
#print axioms comparisonAtShift_neg_one_finite_bijective

end CMDG.CondensedCM5R0
