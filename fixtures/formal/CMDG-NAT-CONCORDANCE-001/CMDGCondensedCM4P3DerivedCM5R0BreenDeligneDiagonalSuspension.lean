import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneBarDiagonalComparison
import CMDGCondensedCM4P3DerivedCM5R0BreenDeligneStableInclusion

/-! Canonical stable comparison from suspended reduced chains
to reduced chains of the actual diagonal bar group. -/
noncomputable section
open CategoryTheory CategoryTheory.Limits Opposite AlgebraicTopology HomologicalComplex
open CMDG.CondensedCM5R0.BreenDeligneTensorSupport
open CMDG.CondensedCM5R0.BreenDeligneBottomAugmentation
open CMDG.CondensedCM5R0.EilenbergMacLaneModel
open CMDG.CondensedCM5R0.BreenDeligneBarTotal
open CMDG.CondensedCM5R0.BreenDeligneFirstColumnInclusion
open CMDG.CondensedCM5R0.BreenDeligneStableInclusion
open CMDG.CondensedCM5R0.BreenDeligneBarDiagonalComparison
namespace CMDG.CondensedCM5R0.BreenDeligneDiagonalSuspension

def diagonalSuspensionMap (A : AGrp) (n : ℕ) :
    suspendedReduced A n ⟶ diagonalReducedChains ((EilenbergMacLaneModel.em n).obj A) :=
  reducedSuspensionMap A n ≫ (diagonalComparison ((EilenbergMacLaneModel.em n).obj A)).inv

theorem diagonalSuspension_isIso (A : AGrp) (n j : ℕ) (hj : j<2*n+1) :
    IsIso (homologyMap (diagonalSuspensionMap A n) j) := by
  letI := reducedSuspension_isIso A n j hj
  let e := (diagonalComparison ((EilenbergMacLaneModel.em n).obj A)).symm
  have h : IsIso (homologyMap e.hom j) := by
    change IsIso (e.toHomologyIso j).hom
    infer_instance
  change IsIso (homologyMap (reducedSuspensionMap A n ≫ e.hom) j)
  rw [homologyMap_comp]
  infer_instance

def diagonalSuspensionIso (A : AGrp) (n j : ℕ) (hj : j<2*n+1) :
    (suspendedReduced A n).homology j ≅
      (diagonalReducedChains ((EilenbergMacLaneModel.em n).obj A)).homology j :=
  letI := diagonalSuspension_isIso A n j hj
  asIso (homologyMap (diagonalSuspensionMap A n) j)

#print axioms diagonalSuspension_isIso
end CMDG.CondensedCM5R0.BreenDeligneDiagonalSuspension
