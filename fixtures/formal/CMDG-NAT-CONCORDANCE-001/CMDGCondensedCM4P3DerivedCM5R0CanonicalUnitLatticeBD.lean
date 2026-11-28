import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneAllModuleExtension
import CMDGCondensedCM4P3DerivedCM5R0CanonicalUnitBD

/-! Reduction of the canonical comparison to finite-lattice exactness. -/
noncomputable section
universe u
namespace CMDG.CondensedCM5R0
open BreenDeligneProbe.UniversalExtension
theorem canonicalUnit_allShifts_of_LatticeBD (B : LatticeBD.{u}) (S : Profinite.{u}) :
    ShiftedComparisonBijectiveCandidate S :=
  canonicalUnit_allShifts_of_UniversalBD B.toUniversalBD S
#print axioms canonicalUnit_allShifts_of_LatticeBD
end CMDG.CondensedCM5R0
