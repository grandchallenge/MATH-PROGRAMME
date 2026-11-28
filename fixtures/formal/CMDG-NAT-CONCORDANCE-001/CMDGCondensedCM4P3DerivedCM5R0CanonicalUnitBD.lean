import CMDGCondensedCM4P3DerivedCM5R0ProductExtDetection
import CMDGCondensedCM4P3DerivedCM5R0UniformDerivedUnitExtCriterion

/-! The genuine canonical shifted comparison, relative only to
the universal finite-type Breen--Deligne resolution package. -/
noncomputable section
set_option backward.isDefEq.respectTransparency false
universe u
open CategoryTheory Limits
namespace CMDG.CondensedCM5R0
open BreenDeligneProbe FiniteTorusBoundary SolidIntegerProduct

theorem solid_scalar_extPositive_zero (B : UniversalBD.{u}) (T : Profinite.{u}) (q : ℕ)
    (e : Abelian.Ext (underivedObject T) discreteIntegerCoeff (q+1)) : e=0 := by
  let iso := solidIntegerIso T
  have hz := integer_extPositive_zero (Index T) B q
    ((Abelian.Ext.mk₀ iso.inv).comp e (zero_add (q+1)))
  have h := congrArg (fun x => (Abelian.Ext.mk₀ iso.hom).comp x (zero_add (q+1))) hz
  rw [Abelian.Ext.mk₀_comp_mk₀_assoc,Iso.hom_inv_id,Abelian.Ext.mk₀_id_comp,Abelian.Ext.comp_zero] at h
  exact h

theorem genuineSolidSource_extPositive_zero (B : UniversalBD.{u}) (T S : Profinite.{u}) (q : ℕ)
    (e : Abelian.Ext (underivedObject T) (underivedObject S) (q+1)) : e=0 := by
  let iso := gsFreeSolidToCoefficientProductIso S
  have hz := product_extPositive_zero (fun _ : LiftedSourceBasisIndex S => discreteIntegerCoeff.{u})
    (underivedObject T) q (fun _ a => solid_scalar_extPositive_zero B T q a)
    (e.comp (Abelian.Ext.mk₀ iso.hom) (add_zero (q+1)))
  have h := congrArg (fun x => x.comp (Abelian.Ext.mk₀ iso.inv) (add_zero (q+1))) hz
  rw [Abelian.Ext.comp_assoc_of_second_deg_zero,Abelian.Ext.mk₀_comp_mk₀,Iso.hom_inv_id,
    Abelian.Ext.comp_mk₀_id,Abelian.Ext.zero_comp] at h
  exact h

theorem canonicalUnit_allShifts_of_UniversalBD (B : UniversalBD.{u}) (S : Profinite.{u}) :
    ShiftedComparisonBijectiveCandidate S :=
  (shiftedComparisonCandidate_iff_genuineSolidSourceExtZero S).2
    (fun T q e => genuineSolidSource_extPositive_zero B T S q e)

#print axioms solid_scalar_extPositive_zero
#print axioms genuineSolidSource_extPositive_zero
#print axioms canonicalUnit_allShifts_of_UniversalBD
end CMDG.CondensedCM5R0
