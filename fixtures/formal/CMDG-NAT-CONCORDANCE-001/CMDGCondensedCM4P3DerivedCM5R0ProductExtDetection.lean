import CMDGCondensedCM4P3DerivedCM5R0FiniteTorusBoundary
import CMDGCondensedCM4P3DerivedCM5R0SolidAnalyticExtReduction

/-! Ext into arbitrary products is jointly detected by coordinate
projections. Use projective presentations rather than an unproved
exchange of products with derived Hom. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u v
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0
variable {J : Type v} (Y : J → Ambient.{u}) [HasProduct Y]

theorem product_ext_detect (q : ℕ) (X : Ambient.{u})
    (e : Abelian.Ext X (∏ᶜ Y) q)
    (h : ∀ j, e.comp (Abelian.Ext.mk₀ (Pi.π Y j)) (add_zero q) = 0) : e=0 := by
  induction q generalizing X with
  | zero =>
    apply Abelian.Ext.addEquiv₀.injective
    rw [map_zero]
    apply Pi.hom_ext
    intro j
    rw [zero_comp]
    have hj := h j
    rw [← Abelian.Ext.mk₀_addEquiv₀_apply e,Abelian.Ext.mk₀_comp_mk₀] at hj
    apply Abelian.Ext.addEquiv₀.symm.injective
    simpa only [Abelian.Ext.addEquiv₀_symm_apply,Abelian.Ext.mk₀_zero] using hj
  | succ q ih =>
    letI := ambientEnoughProjectives.{u}
    let P : ProjectivePresentation X := Classical.arbitrary _
    let S := presentationSequence P
    have hs := presentationSequence_shortExact P
    letI : Projective S.X₂ := P.projective
    have hz : (Abelian.Ext.mk₀ S.g).comp e (zero_add (q+1)) = 0 :=
      Abelian.Ext.eq_zero_of_projective _
    obtain ⟨x,hx⟩ := Abelian.Ext.contravariant_sequence_exact₃ hs (∏ᶜ Y) e hz
      (by omega : 1+q=q+1)
    have localLift (j : J) :
        ∃ y : Abelian.Ext S.X₂ (Y j) q,
          (Abelian.Ext.mk₀ S.f).comp y (zero_add q) =
            x.comp (Abelian.Ext.mk₀ (Pi.π Y j)) (add_zero q) := by
      have hzero : hs.extClass.comp (x.comp (Abelian.Ext.mk₀ (Pi.π Y j)) (add_zero q))
          (by omega : 1+q=q+1) = 0 := by
        rw [← Abelian.Ext.comp_assoc_of_third_deg_zero,hx]
        exact h j
      exact Abelian.Ext.contravariant_sequence_exact₁ hs (Y j) _ _ hzero
    cases q with
    | zero =>
      choose y hy using localLift
      let g : S.X₂ ⟶ ∏ᶜ Y := Pi.lift fun j => Abelian.Ext.addEquiv₀ (y j)
      have hg : (Abelian.Ext.mk₀ S.f).comp (Abelian.Ext.mk₀ g) (zero_add 0) = x := by
        apply Abelian.Ext.addEquiv₀.injective
        rw [Abelian.Ext.mk₀_comp_mk₀,← Abelian.Ext.addEquiv₀_symm_apply,AddEquiv.apply_symm_apply]
        change S.f ≫ g = Abelian.Ext.addEquiv₀ x
        apply Pi.hom_ext
        intro j
        have hj := hy j
        rw [← Abelian.Ext.mk₀_addEquiv₀_apply (y j),← Abelian.Ext.mk₀_addEquiv₀_apply x,
          Abelian.Ext.mk₀_comp_mk₀,Abelian.Ext.mk₀_comp_mk₀] at hj
        rw [Category.assoc]
        unfold g
        rw [Pi.lift_π]
        exact Abelian.Ext.addEquiv₀.symm.injective hj
      rw [← hx,← hg,← Abelian.Ext.comp_assoc,hs.extClass_comp,Abelian.Ext.zero_comp] <;> omega
    | succ q =>
      have hlocal (j : J) : x.comp (Abelian.Ext.mk₀ (Pi.π Y j)) (add_zero (q+1)) = 0 := by
        obtain ⟨y,hy⟩ := localLift j
        rw [Abelian.Ext.eq_zero_of_projective y,Abelian.Ext.comp_zero] at hy
        exact hy.symm
      have hx0 := ih S.X₁ x hlocal
      rw [← hx,hx0,Abelian.Ext.comp_zero]

theorem product_extPositive_zero (X : Ambient.{u}) (q : ℕ)
    (h : ∀ j (e : Abelian.Ext X (Y j) (q+1)), e=0)
    (e : Abelian.Ext X (∏ᶜ Y) (q+1)) : e=0 :=
  product_ext_detect Y (q+1) X e (fun j => h j _)

#print axioms product_ext_detect
#print axioms product_extPositive_zero
end CMDG.CondensedCM5R0
