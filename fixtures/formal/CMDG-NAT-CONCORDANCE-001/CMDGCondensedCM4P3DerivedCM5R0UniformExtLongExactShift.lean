import CMDGCondensedCM4P3DerivedCM5R0GSHigherExtShift
import CMDGCondensedCM4P3DerivedCM5R0UniformProbeAugmentationExact
import Mathlib.Algebra.Homology.DerivedCategory.Ext.ExactSequences

noncomputable section
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0

/-- An actual short exact sequence with Ext¹-zero middle term
has Ext¹-zero right term if every map from its left term extends
across the middle inclusion. No projectivity is inferred. -/
theorem shortExact_extOne_right_zero_of_hom_extensions
    (S : ShortComplex Ambient) (hS : S.ShortExact)
    (G : Ambient)
    (hExtMid : ∀ x : Abelian.Ext S.X₂ G 1, x = 0)
    (hHom : ∀ f : S.X₁ ⟶ G, ∃ g : S.X₂ ⟶ G,
      S.f ≫ g = f) :
    ∀ e : Abelian.Ext S.X₃ G 1, e = 0 := by
  intro e
  have hkill : (Abelian.Ext.mk₀ S.g).comp e (zero_add 1) = 0 :=
    hExtMid _
  obtain ⟨x,hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃ hS G e hkill
      (by omega : 1 + 0 = 1)
  obtain ⟨f,hf⟩ :=
    (Abelian.Ext.addEquiv₀ (X := S.X₁) (Y := G)).symm.surjective x
  have hxmk : Abelian.Ext.mk₀ f = x := by
    simpa only [Abelian.Ext.addEquiv₀_symm_apply] using hf
  obtain ⟨g,hg⟩ := hHom f
  have hzero :
      hS.extClass.comp (Abelian.Ext.mk₀ (S.f ≫ g)) (by omega : 1 + 0 = 1) = 0 := by
    have hz : hS.extClass.comp (Abelian.Ext.mk₀ S.f)
        (by omega : 1 + 0 = 1) = 0 := hS.extClass_comp
    calc
      hS.extClass.comp (Abelian.Ext.mk₀ (S.f ≫ g)) (by omega : 1 + 0 = 1) =
        hS.extClass.comp
          ((Abelian.Ext.mk₀ S.f).comp (Abelian.Ext.mk₀ g) (by omega : 0 + 0 = 0))
          (by omega : 1 + 0 = 1) := by rw [Abelian.Ext.mk₀_comp_mk₀]
      _ = (hS.extClass.comp (Abelian.Ext.mk₀ S.f)
            (by omega : 1 + 0 = 1)).comp
            (Abelian.Ext.mk₀ g) (by omega : 1 + 0 = 1) := by
          rw [Abelian.Ext.comp_assoc]
          omega
      _ = 0 := by simp only [hz, Abelian.Ext.zero_comp]
  calc
    e = hS.extClass.comp x (by omega : 1 + 0 = 1) := hx.symm
    _ = hS.extClass.comp (Abelian.Ext.mk₀ f) (by omega : 1 + 0 = 1) := by rw [hxmk]
    _ = hS.extClass.comp (Abelian.Ext.mk₀ (S.f ≫ g)) (by omega : 1 + 0 = 1) := by rw [hg]
    _ = 0 := hzero

/-- The long exact Ext sequence gives a uniform one-degree
descent from left and middle vanishing to right vanishing.
Here n=0 corresponds to Ext¹(left), Ext²(middle), Ext²(right). -/
theorem shortExact_extSucc_right_zero
    (S : ShortComplex Ambient) (hS : S.ShortExact)
    (G : Ambient) (n : ℕ)
    (hExtLeft : ∀ e : Abelian.Ext S.X₁ G (n + 1), e = 0)
    (hExtMid : ∀ e : Abelian.Ext S.X₂ G (n + 2), e = 0) :
    ∀ e : Abelian.Ext S.X₃ G (n + 2), e = 0 := by
  intro e
  have hkill :
      (Abelian.Ext.mk₀ S.g).comp e (zero_add (n + 2)) = 0 :=
    hExtMid _
  obtain ⟨x,hx⟩ :=
    Abelian.Ext.contravariant_sequence_exact₃
      hS G e hkill (by omega : 1 + (n + 1) = n + 2)
  rw [hExtLeft x] at hx
  have hzero :
      hS.extClass.comp (0 : Abelian.Ext S.X₁ G (n + 1))
        (by omega : 1 + (n + 1) = n + 2) = 0 := by
    exact Abelian.Ext.comp_zero _ _ _ _ _
  exact hx.symm.trans hzero

#print axioms shortExact_extSucc_right_zero

#print axioms shortExact_extOne_right_zero_of_hom_extensions
end CMDG.CondensedCM5R0
