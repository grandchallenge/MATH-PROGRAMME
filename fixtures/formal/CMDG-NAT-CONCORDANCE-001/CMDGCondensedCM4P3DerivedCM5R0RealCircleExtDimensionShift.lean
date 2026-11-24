import CMDGCondensedCM4P3DerivedCM5R0RealCircleFiniteCoordinateNaturality
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

/-! Genuine connecting-map dimension shift for the protected real/circle
short exact sequence, with no assumed comparison map. This transports
the analytic Ext inputs when established; it does not assert them. -/
noncomputable section
universe u
open CategoryTheory
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
open CMDG.CondensedCM5R0.RealCircleSheafExact
namespace CMDG.CondensedCM5R0.RealCircleExtDimensionShift

private noncomputable instance : HasExt.{u+2} CondensedAb.{u} :=
  HasExt.standard _

/-- Connecting map in the genuine contravariant Ext long exact sequence. -/
def connecting (I : Type u) (Y : CondensedAb.{u}) (n : ℕ) :
    Abelian.Ext (realCircleCondensedSequence I).X₁ Y n →+
    Abelian.Ext (realCircleCondensedSequence I).X₃ Y (n+1) :=
  (realCircleCondensedSequence_shortExact I).extClass.precomp Y (by omega)

theorem connecting_bijective_of_real_vanishes
    (I : Type u) (Y : CondensedAb.{u}) (n : ℕ)
    (h₀ : ∀ e : Abelian.Ext (realCircleCondensedSequence I).X₂ Y n, e = 0)
    (h₁ : ∀ e : Abelian.Ext (realCircleCondensedSequence I).X₂ Y (n+1), e = 0) :
    Function.Bijective (connecting I Y n) := by
  constructor
  · intro a b hab
    have hx : connecting I Y n (a-b) = 0 := by
      rw [map_sub, hab, sub_self]
    have hx' : (realCircleCondensedSequence_shortExact I).extClass.comp (a-b)
        (by omega : 1+n=n+1) = 0 := hx
    obtain ⟨z,hz⟩ := Abelian.Ext.contravariant_sequence_exact₁
      (realCircleCondensedSequence_shortExact I) Y (a-b)
      (by omega : 1+n=n+1) hx'
    rw [h₀ z, Abelian.Ext.comp_zero] at hz
    exact sub_eq_zero.mp hz.symm
  · intro e
    obtain ⟨x,hx⟩ := Abelian.Ext.contravariant_sequence_exact₃
      (realCircleCondensedSequence_shortExact I) Y e (h₁ _)
      (by omega : 1+n=n+1)
    exact ⟨x,hx⟩

/-- The actual boundary transports higher circle vanishing to higher
integer-product vanishing; degree zero of the circle is not assumed. -/
theorem integerProduct_extPositive_zero_of_analytic_inputs
    (I : Type u) (Y : CondensedAb.{u}) (q : ℕ)
    (hReal : ∀ n (e : Abelian.Ext (realCircleCondensedSequence I).X₂ Y n), e = 0)
    (hCircle : ∀ e : Abelian.Ext (realCircleCondensedSequence I).X₃ Y (q+2), e = 0) :
    ∀ e : Abelian.Ext (realCircleCondensedSequence I).X₁ Y (q+1), e = 0 := by
  intro e
  apply (connecting_bijective_of_real_vanishes I Y (q+1)
    (hReal _) (hReal _)).1
  rw [map_zero]
  exact hCircle _

#print axioms connecting_bijective_of_real_vanishes
#print axioms integerProduct_extPositive_zero_of_analytic_inputs
end CMDG.CondensedCM5R0.RealCircleExtDimensionShift
