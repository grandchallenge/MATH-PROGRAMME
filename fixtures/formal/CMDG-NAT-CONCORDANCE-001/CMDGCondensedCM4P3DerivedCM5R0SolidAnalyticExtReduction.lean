import CMDGCondensedCM4P3DerivedCM5R0SolidIntegerProduct
import CMDGCondensedCM4P3DerivedCM5R0RealCircleExtDimensionShift

/-! The exact analytic Ext obligation for the genuine solid source.
No analytic vanishing is assumed as an axiom. -/
noncomputable section
universe u
open CategoryTheory
open CMDG.CondensedCM5R0.RealCircleStoneanPresheaf
open CMDG.CondensedCM5R0.RealCircleExtDimensionShift
open CMDG.CondensedCM5R0.SolidIntegerProduct
namespace CMDG.CondensedCM5R0.SolidAnalyticExtReduction

private noncomputable instance : HasExt.{u+2} CondensedAb.{u} :=
  HasExt.standard _

theorem solidSourceExtZero_of_analytic (T S : Profinite.{u}) (q : ℕ)
    (hReal : ∀ n (e : Abelian.Ext (realCircleCondensedSequence (Index T)).X₂
      (underivedObject S) n), e = 0)
    (hCircle : ∀ e : Abelian.Ext (realCircleCondensedSequence (Index T)).X₃
      (underivedObject S) (q+2), e = 0) :
    ∀ e : Abelian.Ext (underivedObject T) (underivedObject S) (q+1), e = 0 := by
  intro e
  let i := solidIntegerIso T
  have hz := integerProduct_extPositive_zero_of_analytic_inputs (Index T)
    (underivedObject S) q hReal hCircle
      ((Abelian.Ext.mk₀ i.inv).comp e (zero_add (q+1)))
  have hh : (Abelian.Ext.mk₀ i.hom).comp
      ((Abelian.Ext.mk₀ i.inv).comp e (zero_add (q+1))) (zero_add (q+1)) = e := by
    rw [Abelian.Ext.mk₀_comp_mk₀_assoc, i.hom_inv_id, Abelian.Ext.mk₀_id_comp]
  rw [← hh, hz, Abelian.Ext.comp_zero]

#print axioms solidSourceExtZero_of_analytic
end CMDG.CondensedCM5R0.SolidAnalyticExtReduction
