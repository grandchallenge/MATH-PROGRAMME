import CMDGCondensedCM4P3DerivedCM5R0UniformRealCircleExtTransfer

/-!
# Canonical connecting equivalence for the real/circle derived calculation

Given an actual short exact sequence in condensed modules, the long exact
sequence identifies Ext^1 of the quotient with Ext^0 of the kernel when
the middle term has Ext^0 = Ext^1 = 0. The isomorphism is the ACTUAL
Yoneda extension boundary, rather than an arbitrary bijection of groups.
This statement is conditional on middle vanishing, which is precisely
what the independent analytic real computation must establish.
-/

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- Actual long-exact connecting map from degree-zero Ext of the
left term to degree-one Ext of the quotient. -/
noncomputable def shortExact_realCircleConnecting
    (S : ShortComplex Ambient) (hS : S.ShortExact) (A : Ambient) :
    Abelian.Ext S.X₁ A 0 →+ Abelian.Ext S.X₃ A 1 :=
  hS.extClass.precomp A (by omega : 1 + 0 = 1)

/-- Under actual Ext^0 and Ext^1 acyclicity of the middle term,
the genuine connecting map is bijective. This gives the exact
canonical generator for the circle Ext^1 calculation. -/
theorem shortExact_realCircleConnecting_bijective
    (S : ShortComplex Ambient) (hS : S.ShortExact) (A : Ambient)
    (hMidZero : ∀ x : Abelian.Ext S.X₂ A 0, x = 0)
    (hMidOne : ∀ x : Abelian.Ext S.X₂ A 1, x = 0) :
    Function.Bijective (shortExact_realCircleConnecting S hS A) := by
  constructor
  · intro x y hxy
    have hker : shortExact_realCircleConnecting S hS A (x - y) = 0 := by
      rw [map_sub, hxy, sub_self]
    have hker' : hS.extClass.comp (x - y) (by omega : 1 + 0 = 1) = 0 := hker
    obtain ⟨z, hz⟩ :=
      Abelian.Ext.contravariant_sequence_exact₁ hS A (x - y)
        (by omega : 1 + 0 = 1) hker'
    have hxzero : x - y = 0 := by
      calc
        x - y = (Abelian.Ext.mk₀ S.f).comp z (zero_add 0) := hz.symm
        _ = (Abelian.Ext.mk₀ S.f).comp 0 (zero_add 0) := by rw [hMidZero z]
        _ = 0 := Abelian.Ext.comp_zero _ _ _ _ _
    exact sub_eq_zero.mp hxzero
  · intro e
    have hkill : (Abelian.Ext.mk₀ S.g).comp e (zero_add 1) = 0 :=
      hMidOne _
    obtain ⟨x, hx⟩ :=
      Abelian.Ext.contravariant_sequence_exact₃ hS A e hkill
        (by omega : 1 + 0 = 1)
    refine ⟨x, ?_⟩
    change hS.extClass.comp x (by omega : 1 + 0 = 1) = e
    exact hx

#print axioms shortExact_realCircleConnecting_bijective
end CMDG.CondensedCM5R0
