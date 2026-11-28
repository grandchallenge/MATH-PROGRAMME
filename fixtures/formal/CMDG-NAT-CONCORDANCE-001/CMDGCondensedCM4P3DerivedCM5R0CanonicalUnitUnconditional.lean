import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneNormalizeResolution

/-! The actual Breen–Deligne resolution discharges the last
mathematical hypothesis of the genuine CM5-R0 shifted comparison.
This is the canonical map in the existing standard derived category,
not a replacement map and not a separate certification assertion. -/
noncomputable section
universe u
open CategoryTheory
namespace CMDG.CondensedCM5R0

def actualUniversalBD : BreenDeligneProbe.UniversalBD.{u} :=
  BreenDeligneNormalizeResolution.actualLatticeBD.toUniversalBD

theorem genuineSolidSource_extPositive_zero_unconditional
    (T S : Profinite.{u}) (q : ℕ)
    (e : Abelian.Ext (underivedObject T) (underivedObject S) (q+1)) : e = 0 :=
  genuineSolidSource_extPositive_zero actualUniversalBD T S q e

theorem canonicalUnit_allShifts (S : Profinite.{u}) :
    ShiftedComparisonBijectiveCandidate S :=
  canonicalUnit_allShifts_of_LatticeBD BreenDeligneNormalizeResolution.actualLatticeBD S

theorem canonicalUnit_atShift (S T : Profinite.{u}) (n : ℤ) :
    Function.Bijective (comparisonAtShift S T n) :=
  canonicalUnit_allShifts S T n

#print axioms actualUniversalBD
#print axioms genuineSolidSource_extPositive_zero_unconditional
#print axioms canonicalUnit_allShifts
#print axioms canonicalUnit_atShift
end CMDG.CondensedCM5R0
