import CMDGCondensedCM4P3DerivedCM5R0UniformGenuineSolidExtAcyclic
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-!
# CMDG CM5 E3: long-exact Ext bridge for the real/circle triangle

This is the real categorical transfer required by Scholze's computation
of RHom(product Z, Z) from the real and circle derived-Hom calculations.
It is valid for any exact short complex in the genuine condensed-module
category and does not assume that an unconstructed real/circle short
complex already exists or is exact.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Contravariant long-exact Ext transfer in the exact degree needed for
`0 → ∏ Z → ∏ R → ∏ (R/Z) → 0`: when the middle term has vanishing
Ext^(q+1) and the quotient has vanishing Ext^(q+2), so does the
leftmost term at Ext^(q+1). The connecting map is the ACTUAL extension
class of the supplied short exact sequence. -/
theorem shortExact_extPositive_left_zero_of_middle_and_quotient
    (S : ShortComplex Ambient) (hS : S.ShortExact)
    (A : Ambient) (q : ℕ)
    (hMiddle : ∀ x : Abelian.Ext S.X₂ A (q + 1), x = 0)
    (hQuotient : ∀ x : Abelian.Ext S.X₃ A (q + 2), x = 0) :
    ∀ e : Abelian.Ext S.X₁ A (q + 1), e = 0 := by
  intro e
  have hkill : hS.extClass.comp e (by omega : 1 + (q + 1) = q + 2) = 0 :=
    hQuotient _
  obtain ⟨x, hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₁ hS A e
      (by omega : 1 + (q + 1) = q + 2) hkill
  calc
    e = (Abelian.Ext.mk₀ S.f).comp x (zero_add (q + 1)) := hx.symm
    _ = (Abelian.Ext.mk₀ S.f).comp 0 (zero_add (q + 1)) := by rw [hMiddle x]
    _ = 0 := Abelian.Ext.comp_zero _ _ _ _ _

/-- Uniform version of the canonical real/circle triangle transfer:
the middle degree and shifted quotient vanishing imply all positive
source Ext vanishing. Does not assume either vanishing itself. -/
theorem shortExact_extAllPositive_left_zero_of_middle_and_quotient
    (S : ShortComplex Ambient) (hS : S.ShortExact) (A : Ambient)
    (hMiddle : ∀ (q : ℕ) (e : Abelian.Ext S.X₂ A (q + 1)), e = 0)
    (hQuotient : ∀ (q : ℕ) (e : Abelian.Ext S.X₃ A (q + 2)), e = 0) :
    ∀ (q : ℕ) (e : Abelian.Ext S.X₁ A (q + 1)), e = 0 := by
  intro q e
  exact shortExact_extPositive_left_zero_of_middle_and_quotient
    S hS A q (hMiddle q) (hQuotient q) e

#print axioms shortExact_extPositive_left_zero_of_middle_and_quotient
#print axioms shortExact_extAllPositive_left_zero_of_middle_and_quotient

end CMDG.CondensedCM5R0
