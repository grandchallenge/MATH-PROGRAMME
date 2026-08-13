import CMDGCondensedCM4P3GFiniteWindow

/-!
# CMDG CM4-P3-G Boolean finite-support extraction

This fixture packages the exact abstract slenderness step needed after the measure object has been
placed in basis coordinates: if an additive functional on an integer product has a locally constant
restriction to the Boolean cube, then its standard-coordinate coefficients vanish outside one
finite set.
-/

namespace CMDG.CondensedCM4P3G.FiniteSupport

open scoped Topology

/-- Embed a Boolean coordinate vector into the corresponding `0/1` integer vector. -/
def boolToInt {ι : Type*} (x : ι → Bool) : ι → ℤ :=
  fun i => if x i then 1 else 0

/-- The Boolean vector supported on one coordinate. -/
def boolIndicator {ι : Type*} [DecidableEq ι] (i : ι) : ι → Bool :=
  fun j => if j = i then true else false

/-- The integer standard-coordinate vector. -/
def intIndicator {ι : Type*} [DecidableEq ι] (i : ι) : ι → ℤ :=
  fun j => if j = i then 1 else 0

theorem boolToInt_boolIndicator {ι : Type*} [DecidableEq ι] (i : ι) :
    boolToInt (boolIndicator i) = intIndicator i := by
  funext j
  by_cases h : j = i <;> simp [boolToInt, boolIndicator, intIndicator, h]

theorem boolToInt_zero {ι : Type*} :
    boolToInt (fun _ : ι => false) = 0 := by
  funext i
  simp [boolToInt]

/-- Boolean local constancy forces finite standard-coordinate support for an additive functional
on the full integer product. -/
theorem finite_support_of_bool_locallyConstant
    {ι : Type*} [DecidableEq ι]
    (L : (ι → ℤ) →+ ℤ)
    (f : LocallyConstant (ι → Bool) ℤ)
    (hf : ∀ x : ι → Bool, f x = L (boolToInt x)) :
    ∃ I : Finset ι, ∀ i ∉ I, L (intIndicator i) = 0 := by
  obtain ⟨I, hI⟩ :=
    CMDG.CondensedCM4P3G.FiniteWindow.locallyConstant_boolPi_zero_finiteWindow f
  refine ⟨I, ?_⟩
  intro i hi
  have hzero : f (boolIndicator i) = f (fun _ => false) := by
    apply hI
    intro j hj
    have hji : j ≠ i := by
      intro h
      subst j
      exact hi hj
    simp [boolIndicator, hji]
  rw [hf, hf] at hzero
  rw [boolToInt_boolIndicator, boolToInt_zero, map_zero] at hzero
  exact hzero

#print finite_support_of_bool_locallyConstant
#print axioms finite_support_of_bool_locallyConstant

end CMDG.CondensedCM4P3G.FiniteSupport
