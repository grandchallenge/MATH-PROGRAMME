import CMDGCondensedCM4P3DerivedCM5R0ShiftZero
import Mathlib.Algebra.Homology.DerivedCategory.TStructure

/-!
# CMDG CM5-R0: positive and nonnegative source shifts

For objects in the heart of the canonical derived t-structure, a positive
source shift has no maps into a degree-zero object.  Thus the CM5 shifted
solidification comparison is bijective for all positive source shifts,
independently of any higher Ext computation.  Together with the protected
zero-shift theorem, this covers all nonnegative source shifts.

IMPORTANT: under the cohomological convention used by the pinned mathlib
shift, negative source shifts correspond to the potentially nonzero higher
Ext groups.  Those comparisons remain unproved.

No axioms, sorry, generalized coefficients, source-semantic admission, or
claimed full derived solidity.
-/

noncomputable section

universe u

open CategoryTheory Pretriangulated

namespace CMDG.CondensedCM5R0

private noncomputable instance : HasDerivedCategory Ambient :=
  HasDerivedCategory.standard Ambient

/-- A positive source shift of a degree-zero derived object has no
morphisms into another degree-zero object, by the standard t-structure. -/
private theorem positiveShift_hom_eq_zero
    (A B : DerivedCategory Ambient)
    [DerivedCategory.TStructure.t.IsLE A 0]
    [DerivedCategory.TStructure.t.IsGE B 0]
    (n : ℤ) (hn : 0 < n)
    (f : (shiftFunctor (DerivedCategory Ambient) n).obj A ⟶ B) :
    f = 0 := by
  haveI : DerivedCategory.TStructure.t.IsLE
      ((shiftFunctor (DerivedCategory Ambient) n).obj A) (-n) :=
    DerivedCategory.TStructure.t.isLE_shift A 0 n (-n) (by omega)
  exact DerivedCategory.TStructure.t.zero f (-n) 0 (by omega)

/-- The actual previously defined comparison is bijective for every
strictly positive source shift; both Hom sets are singletons. -/
theorem comparisonAtShift_pos_bijective
    (S T : Profinite.{u}) (n : ℤ) (hn : 0 < n) :
    Function.Bijective (comparisonAtShift S T n) := by
  haveI : DerivedCategory.TStructure.t.IsLE (degreeZeroObject T) 0 := by
    dsimp [degreeZeroObject]
    infer_instance
  haveI : DerivedCategory.TStructure.t.IsLE (freeAtZero T) 0 := by
    dsimp [freeAtZero]
    infer_instance
  haveI : DerivedCategory.TStructure.t.IsGE (degreeZeroObject S) 0 := by
    dsimp [degreeZeroObject]
    infer_instance
  constructor
  · intro f g _
    exact (positiveShift_hom_eq_zero (degreeZeroObject T) (degreeZeroObject S)
      n hn f).trans
      (positiveShift_hom_eq_zero (degreeZeroObject T) (degreeZeroObject S) n hn g).symm
  · intro q
    refine ⟨0, ?_⟩
    exact (positiveShift_hom_eq_zero (freeAtZero T) (degreeZeroObject S)
      n hn (comparisonAtShift S T n 0)).trans
      (positiveShift_hom_eq_zero (freeAtZero T) (degreeZeroObject S) n hn q).symm

/-- Combination of the new positive-shift vanishing argument with the
protected zero-shift theorem, with negative shifts still open. -/
theorem comparisonAtShift_nonneg_bijective
    (S T : Profinite.{u}) (n : ℤ) (hn : 0 ≤ n) :
    Function.Bijective (comparisonAtShift S T n) := by
  rcases lt_or_eq_of_le hn with hpos | hzero
  · exact comparisonAtShift_pos_bijective S T n hpos
  · subst n
    exact comparisonAtShift_zero_bijective S T

#print axioms comparisonAtShift_pos_bijective
#print axioms comparisonAtShift_nonneg_bijective

end CMDG.CondensedCM5R0
